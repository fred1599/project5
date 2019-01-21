import requests

from random import choice, sample
from lxml.html import fromstring


def get_category():
    http = "https://fr.openfoodfacts.org/categories&json=1"
    r = requests.get(http)
    return [key['name'] for key in r.json().get('tags')]
    

def get_meal(category, page, pays):
    payload = {
                'action': 'process',
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                'tag_0': category,
                'sort_by': 'unique_scans_n',
                'page_size': str(page),
                'countries': pays,
                'json': 1,
                'page': 1,
            }

    ingredients = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params=payload)
    r = ingredients.json()
    result = r.get('products')
    return result

def get_products(infos):
    return [(info.get('product_name_fr'), info.get('url')) \
             for info in infos]


def get_choice(category, n=5, product=False):
    categories = sample(category, n)
    urls = []

    for ind, cat in enumerate(categories):
        try:
            if product:
                cat, url = cat
                urls.append(url)
            print('{}: {}'.format(ind+1, cat))
        except UnicodeEncodeError:
            continue

    while True:
        try:
            choice = int(input('Entrer votre choix: '))
            break
        except ValueError:
            continue
    if urls:
        return categories[choice-1][0], urls[choice-1]
    return categories[choice-1]

def parse_ingredients(url):
    content = requests.get(url).text
    page = fromstring(content)
    result = page.xpath('//div[@id="ingredients_list"]/text()')[0]
    return [ing for ing in result.split(',') if ing]

if __name__ == "__main__":
    categories = get_category()
    category = get_choice(categories, 5)
    infos = get_meal(category, 1, 'France')
    products = get_products(infos)
    product, url = get_choice(products, len(products), product=True)
    print(url)
    print(parse_ingredients(url))