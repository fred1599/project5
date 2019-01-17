TABLES = {}

TABLES['category'] = """CREATE TABLE IF NOT EXISTS category(
id INT PRIMARY KEY,
name TEXT,
meal TEXT)
"""

TABLES['meal'] = """CREATE TABLE IF NOT EXISTS meal(
id INT PRIMARY KEY,
product TEXT,
grade TEXT,
ingredients TEXT,
magasin TEXT,
url TEXT)
"""