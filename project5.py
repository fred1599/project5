import requests

from random import choice, sample



def get_category():
    http = "https://fr.openfoodfacts.org/categories&json=1"
    r = requests.get(http)
    return [key['name'] for key in r.json().get('tags')]
    

def get_ingredients(category, page, pays):
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


def get_choice(category, n=5):
    categories = sample(category, n)
    for ind, cat in enumerate(categories):
        try:
            print('{}: {}'.format(ind+1, cat))
        except UnicodeEncodeError:
            continue

    while True:
        try:
            choice = int(input('Entrer votre choix: '))
            break
        except ValueError:
            continue
    return categories[choice-1]

category = get_choice(get_category())
products = get_ingredients(category, 1, 'France')
display_infos(products)