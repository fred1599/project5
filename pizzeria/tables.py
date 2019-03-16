TABLES = {}

TABLES['category'] = """CREATE TABLE IF NOT EXISTS category(
id_category INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
name TEXT,
url TEXT,
products INT UNSIGNED
)"""

TABLES['product'] = """CREATE TABLE IF NOT EXISTS product(
id_product INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
id_cat INT UNSIGNED,
name TEXT,
url TEXT,
ingredients TEXT,
brands TEXT,
grades TEXT,
CONSTRAINT fk_product FOREIGN KEY (id_cat) REFERENCES category(id_category)
)"""

TABLES['favorites'] = """CREATE TABLE IF NOT EXISTS favorites(
id_product INT UNSIGNED,
id_cat INT UNSIGNED,
name TEXT,
url TEXT,
ingredients TEXT,
brands TEXT,
grades TEXT
)"""