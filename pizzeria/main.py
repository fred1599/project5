import requests

from base import Base
from tables import TABLES
from random import choice, sample

URL_CATEGORIES = 'https://fr.openfoodfacts.org/categories&json=1'
URL_PRODUCTS = 'https://fr.openfoodfacts.org/cgi/search.pl'
PARAMS = {
        'action': 'process',
        'tagtype_0': "categories",
        'tag_contains_0': 'contains',
        'tag_0': None,
        'sort_by': 'unique_scans_n',
        'page_size': 1,
        'countries': 'France',
        'json': 1,
        'page': 1,
}

MENU = [
    "Quel aliment souhaitez-vous remplacer ?",
    "Retrouver mes aliments substitués."
]

class Category:
    def __init__(self, name, url, products):
        self.name = name
        self.url = url
        self.products = products # number of products in category

class Product:
    def __init__(self, name, url, brands, 
                 categories, ingredients,
                 nutrition_grades):
        self.name = name
        self.url = url
        self.brands = '|'.join(brands.split(',')) if brands else None
        self.categories = categories.split(',') if categories else None
        self.ingredients = '|'.join([info['text'] for info in ingredients])
        self.nutrition_grades = nutrition_grades
        

def load_categories(url):
    r = requests.get(url)
    for infos in r.json().get('tags'):
        yield Category(infos['name'], infos['url'], infos['products'])


def load_products(url, category):
    PARAMS['tag_0'] = category
    r = requests.get(url, params=PARAMS)
    for p in r.json().get('products'):
        try:
            yield Product(p['product_name'], p['url'], p['brands'],
                      p['categories'], p['ingredients'], 
                      p.get('nutrition_grades', None))
        except:
            print('Error with {}'.format(p['product_name']))

def get_choice(iterable):
    for i, obj in enumerate(iterable, start=1):
        print('{} - {}'.format(i, obj))
    try:
        c = int(input('Enter your choice: '))
        if c not in range(1, len(iterable)+1):
            c = len(iterable)
        return c
    except ValueError:
        return get_choice(iterable)

bdd = Base()
bdd.connect()
bdd.create_tables(*[t for t in TABLES])
results = {}
flag = True
categories = bdd.get_categories(400)
for cat in categories:
    products = bdd.get_products(cat)
    if products:
        results[cat] = list(set(products))

length = len(results)
categories = sample([c for c in results], 10 if length>10 else length)

c = get_choice(MENU)
if c == 1:
    c = get_choice(categories)
    cat_name = categories[c-1]
    c = get_choice(results[cat_name])
    product = results[cat_name][c-1]
    substitute = bdd.get_substitute(cat_name, product)
    if substitute:
        name, url, ingredients, brands, grade = choice(substitute)[2:]
        c = input('substitute by {} with grade {}? (yes/no): '.format(name, grade))
        if c == 'yes':
            print('Name of product: {}\nURL: {}\nIngredients: {}\nBrands: {}\nGrade: {}'\
                  .format(name, url, ingredients, brands, grade))
        else:
            name, url, ingredients, brands, grade = bdd.get_info_product(product)[2:]
            print('Name of product: {}\nURL: {}\nIngredients: {}\nBrands: {}\nGrade: {}'\
                  .format(name, url, ingredients, brands, grade))
        
    else:
        print('pas de substitut possible !')
        name, url, ingredients, brands, grade = bdd.get_info_product(product)[2:]
        print('Name of product: {}\nURL: {}\nIngredients: {}\nBrands: {}\nGrade: {}'\
                  .format(name, url, ingredients, brands, grade))
        c = input('Save product ? (yes/no): ')
        if c == 'yes':
            bdd.add_favorites(product, cat_name)
            print('{} saved !!!'.format(product))
elif c == 2:
    fav = list(set(bdd.get_all_favorites()))
    names = [favorite[2] for favorite in fav]
    c = get_choice(names)
    name, url, ingredients, brands, grade = fav[c-1][2:]
    print('Name of product: {}\nURL: {}\nIngredients: {}\nBrands: {}\nGrade: {}'\
                  .format(name, url, ingredients, brands, grade))