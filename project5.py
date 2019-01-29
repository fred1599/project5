import requests
import re
import unidecode
import json

from random import sample
from my_menu import Menus, Menu
from lxml.html import fromstring
from base import Base

class Categories:

	URL = "https://fr.openfoodfacts.org/categories&json=1"

	def __init__(self):
		self.r = self.connect()
		self.list = self.get(self.r)

	def connect(self):
		r = requests.get(Categories.URL)
		return r

	def get(self, r, limit=5):
		categories = [key['name'] for key in r.json().get('tags')]
		return sample(categories, limit)

class Meals:

	URL = 'https://fr.openfoodfacts.org/cgi/search.pl'
	PAYLOAD = {
		'action': 'process',
        'tagtype_0': 'categories',
        'tag_contains_0': 'contains',
        'tag_0': None,
        'sort_by': 'unique_scans_n',
        'page_size': None,
        'countries': None,
        'json': 1,
        'page': 1,
	}

	def __init__(self, cat, page=1, pays='France'):
		Meals.PAYLOAD['tag_0'] = cat
		Meals.PAYLOAD['page_size'] = page
		Meals.PAYLOAD['countries'] = pays
		self.meals = self.connect()
		self.pr, self.urls, self.brands = self.get_meal()

	def connect(self):
		r = requests.get(Meals.URL, params=Meals.PAYLOAD)
		self.r_json = r.json()

		return self.r_json

	def get_meal(self):
		result = self.meals.get('products')
		infos = ('product_name_fr', 'url', 'brands')
		meals = []
		for info in infos:
			meals.append([key[info] for key in result if info in key])
		return meals

class Products:

	def parse_ingredients(url):
		content = requests.get(url).text
		page = fromstring(content)
		result = page.xpath('//div[@id="ingredients_list"]/text()')
		if result:
			products = ''.join(result)
		else:
			products = None
		return products

def get_res(objects, menus):
	menu = Menu(objects)
	menus = menus + menu
	menu.display()
	value = menu.get_value(menus)
	print()
	if isinstance(value, Menu):
		new_menu = value
		new_menu.display()
		meals = Meals(new_menu.get_value(menus))
		value = get_res(meals.pr, menus)
	return value

def display_result(pr, url, brand, ingredients):
	print('produit: {}'.format(pr))
	print()
	print('url: {}'.format(url))
	print()
	print('brand: {}'.format(brand))
	print()
	print('ingredients:')
	print()
	print(ingredients)



my_base = Base("my_base")
MENUS = Menus()
categories = Categories()
value = get_res(categories.list, MENUS)
meals = Meals(value)
my_base.add_to_category((value,))
value = get_res(meals.pr, MENUS)
url = meals.urls[meals.pr.index(value)]
brands = meals.brands[meals.pr.index(value)]
products = Products.parse_ingredients(url)
display_result(value, url, brands, products)
my_base.add_to_products((value, url, products, brands,))
my_base.cnx.close()