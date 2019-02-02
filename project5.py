import requests
import json
import sys

from random import sample
from my_menu import Menus, Menu
from lxml.html import fromstring
from base import Base

class Categories:

	"""
	:rtype: Categories
	"""

	URL = "https://fr.openfoodfacts.org/categories&json=1"

	def __init__(self):
		self.r = self.connect()
		self.list = self.get(self.r)

	def connect(self):
		r = requests.get(Categories.URL)
		return r

	def get(self, r, limit=5):
		"""
		:type r: Request
		:type limit: int
		:rtype: list
		"""
		categories = [key['name'] for key in r.json().get('tags')]
		return sample(categories, limit)

class Meals:

	"""
	get all products of category
	:type cat: str
	:type page: int
	:type pays: str
	:rtype: Meals
	"""

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
		"""
		return all ingredients of product
		:type url: str
		:rtype: str
		"""
		content = requests.get(url).text
		page = fromstring(content)
		result = page.xpath('//div[@id="ingredients_list"]/text()')
		if result:
			products = ''.join(result)
		else:
			products = None
		return products

def get_res(objects, menus):
	"""
	if z key, return value for the new choice
	:type objects: list
	:type menus: Menu
	:rtype: str or tuple
	"""
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
		return value, meals.pr
	return value

def display_result(pr, url, ingredients, brand):
	"""
	display results for research products
	:type pr: str
	:type url: str
	:type brand: str
	:type ingredients: str
	:rtype: None
	"""
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
values = get_res(meals.pr, MENUS)

if isinstance(values, tuple):
	value, meals.pr = values
else:
	value = values

product = my_base.search_to_products(value)
if product:
	display_result(*product)
	sys.exit() # on quitte le programme
print("Non trouvé dans la base de données")
choice = input("Voulez-vous l'enregistrer dans la base (y/n): ")
if choice.lower()[0] == 'y':
	print("Enregistrement dans la base de données")
	try:
		url = meals.urls[meals.pr.index(value)]
		brands = meals.brands[meals.pr.index(value)]
	except IndexError:
		print("url: {}".format(url))
		print("brand: {}".format(brands))
		sys.exit("Erreur d'index")
products = Products.parse_ingredients(url)
if not products:
	products = ''
results = (value, url, products, brands,)
my_base.add_to_products(results)
display_result(*results)

print('Voici la liste des produits enregistrés:')
print()
my_base.get_all_products('product')
print()
print('Voici la liste des catégories enregistrés:')
print()
my_base.get_all_products('category')