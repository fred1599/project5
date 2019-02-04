import requests
import sys

from random import sample, choice
from lxml.html import fromstring
from my_menu import Menu
from base import Base


class Categorie:

    def __init__(self, name):
        self.nom = name
        self.pays = 'France'
        self.url = ''
        self.nb_produits = 0

    def __str__(self):
        return self.nom

class Categories(list):

    URL = "https://fr.openfoodfacts.org/categories&json=1"

    def __init__(self):
        super().__init__()
        self.load()

    def load(self):
        r = requests.get(Categories.URL)
        for key in r.json().get('tags'):
            categorie = Categorie(key['name'])
            self.append(categorie)

    def get_categories(self, n):
        if n < 1 or n > len(self):
            n = 5

        return sorted(sample(self, n), key=lambda cat: cat.nom)

    def get_names(self, n):
        return [cat.nom for cat in self.get_categories(n)]

class Products(list):

    URL = 'https://fr.openfoodfacts.org/cgi/search.pl'
    PAYLOAD = {
        'action': 'process',
        'tagtype_0': 'categories',
        'tag_contains_0': 'contains',
        'tag_0': None,
        'sort_by': 'unique_scans_n',
        'page_size': 1,
        'countries': 'France',
        'json': 1,
        'page': 1,
    }

    def __init__(self, categorie):
        super().__init__()
        Products.PAYLOAD['tag_0'] = categorie
        self.load()

    def load(self):
        r = requests.get(Products.URL, params=Products.PAYLOAD)
        for product in r.json().get('products'):
            self.append(product)

    def get_info(self, info):
        infos = []
        for product in self:
            if info in product:
                infos.append(product[info])
        return infos     


class Ingredients(str):

    PATH = '//div[@id="ingredients_list"]/text()'

    def __init__(self, url):
        super().__init__()
        self.url = url

    def load(self):
        content = requests.get(self.url).text
        page = fromstring(content)
        result = page.xpath(Ingredients.PATH)
        products = ''
        if result:
            products = ''.join(result)
        return products

    def __str__(self):
        return self.load()


def display_info(products, names, product):
    index = names.index(product)
    url_produit = products.get_info('url')[index]
    magasin_produit = products.get_info('brands')[index]
    ingredients_produit = Ingredients(url_produit)
    print('\n'.join([
        'nom du produit: {}'.format(product),
        'magasin du produit: {}'.format(magasin_produit),
        'URL du produit: {}'.format(url_produit),
        'ingrédients du produit: \n\n{}'.format(ingredients_produit),
    ]))



MENU = Menu()
categories = Categories().get_names(5) # chargement de la liste des catégories existantes
menu_cat = MENU.add(categories)

try:
    base_name = sys.argv[1]
except IndexError:
    base_name = 'my_base'

base = Base(base_name)

while True:
    MENU.display()
    index = MENU.get_choice()

    if index == None:
        continue

    cat = categories[index]

    if not base.in_categories(cat):
        print('La catégorie {} est inconnu dans la base de données'.
            format(cat)
        )
        choice = input("Voulez-vous enregistrer dans la base de données (y/n): ")
        if choice == 'y':
            base.add_to_category((cat,))

    products = Products(cat)
    names = products.get_info('product_name_fr')
    menu_product = MENU.add(names)
    MENU.display()
    index = MENU.get_choice()

    if index == None:
        continue

    product = names[index]

    if not base.search_to_products(product):
        print('Le produit {} est inconnu dans la base de données'.
            format(product)
        )
        choice = input("Voulez-vous enregistrer dans la base de données (y/n): ")
        if choice == 'y':
            url_produit = products.get_info('url')[index]
            magasin_produit = products.get_info('brands')[index]
            ingredients_produit = Ingredients(url_produit)
            values = (
                product,
                url_produit,
                str(ingredients_produit),
                magasin_produit
            )
            base.add_to_products(tuple(values))

    break

print('\n\n')
display_info(products, names, product)