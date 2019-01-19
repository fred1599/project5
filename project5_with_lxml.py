import requests
import lxml.html
import unidecode

from lxml import html
from random import choice, sample
from urllib.parse import urljoin

URL_BASE = "https://fr.openfoodfacts.org/"
URL = "https://fr.openfoodfacts.org/categories"
URL_PRODUCT = 'https://fr.openfoodfacts.org/categorie/'

def get_category():
    page = requests.get(URL).content
    tree = html.fromstring(page)
    categories = tree.xpath('//tbody/tr/td/a[@class="tag well_known"]/text()')
    return categories
    

def get_products(category, page, pays):
    # minuscule et supp accents
    url = '-'.join(unidecode.unidecode(category.lower()).split())
    cat = urljoin('categorie/', url)
    URL_MEAL = urljoin(URL, cat)
    page = requests.get(URL_MEAL).content
    tree = html.fromstring(page)
    products = tree.xpath('//ul[@class="products"]/li/a/span/text()')
    urls_cat = tree.xpath('//ul[@class="products"]/li/a')
    href = [url.attrib['href'] for url in urls_cat]
    return (products, href)

def get_properties(product, url):
    new_url = urljoin(URL_BASE, url)
    page = requests.get(new_url).content
    tree = html.fromstring(page)
    description = tree.xpath('//div[@property="food:ingredientListAsText"]/text()')
    if description:
        return '\n'.join(description)
    else:
        return ''


def display_infos(products):
    properties = [
            'product_name_fr',
            'nutrition_grade_fr',
            'ingredients_text_fr',
            'stores',
            'id',
            'url',
        ]

    for property in products:
        for name in properties:
            if name in property:
                print(property.get(name))
        print('-' * 100)


def get_choice(category, n=150):
    counter = 0
    categories = []
    while counter < n:
        try:
            cat = choice(category)
            print('{}: {}'.format(counter+1, cat))
            counter += 1
            categories.append(cat)
        except UnicodeEncodeError:
            continue

    while True:
        try:
            my_choice = int(input('Entrer votre choix: '))
            break
        except ValueError:
            continue
    return categories[my_choice-1]

category = get_choice(get_category())
products, url = get_products(category, 1, 'France')
product = get_choice(products, n=len(products))
url_product = url[products.index(product)]
properties = get_properties(product, url_product)
print(properties)
