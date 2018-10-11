
from django.http import HttpResponse,HttpResponseNotModified
from django.shortcuts import render
from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.template import Context, loader
from . import templates

from airtable import Airtable


def index(request):

	main_menu = set()
	sub_menu = set()
	menu = getMenuData()

	return render(request, "menu.html", {'main_menu': menu,'sub_menu':sub_menu})

def getMenuData():

	AT = Airtable(settings.AIRTABLE_DATABASE_ID,
		  'Config',
		  api_key=settings.AIRTABLE_API_KEY)

	all_data = AT.get_all(formula="{Live}=TRUE()")
	main = AT.get_iter(fields = ['Main Menu'])
	menu = {}
	no_name_num = 1

	for page in main:
		for record in page:
			menu[record['fields']['Main Menu']] = {}

	for item in all_data:
		aux = menu[item['fields']['Main Menu']]

		if 'Name' in item['fields'].keys():
			link_name = item['fields']['Name']
			link = item['fields']['URL']
		else:
			print(item,no_name_num)
			link_name = 'No Name URL #' + str(no_name_num)
			link = item['fields']['URL']
			no_name_num += 1

		try:
			s_menu = item['fields']['Sub-menu']
			if s_menu not in aux.keys():
				aux[s_menu] = {link_name:link}
			else:
				aux[s_menu][link_name] = link

		except:

			if 'No Name Sub-Menu' not in aux.keys():
				aux["No Name Sub-Menu"] = {link_name:link}
			else:
				aux["No Name Sub-Menu"][link_name] = link
	return menu
