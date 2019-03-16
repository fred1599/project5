import mysql.connector

from mysql.connector import errorcode
from random import sample
from tables import TABLES

class Base:
    def __init__(self, name='my_base'):
        self.name = name
        self.user = 'fred1599'
        self.password = 'pablouche87'
    
    def connect(self):
        try:
            self.cnx = mysql.connector.connect(user=self.user, database=self.name, 
                    password=self.password, auth_plugin='mysql_native_password')
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            sys.exit(-1)
    
    def create_tables(self, *tablenames):
        for table in tablenames:
            self.cursor.execute(TABLES[table])
    
    def get_id_category(self, cat_name):
        sql = 'SELECT id_category FROM category WHERE name=%s'
        self.cursor.execute(sql, (cat_name,))
        result = self.cursor.fetchall()
        if result:
            return result[0][0]
    
    def add_category(self, cat):
        values = (cat.name, cat.url, cat.products)
        sql = 'INSERT INTO category (name, url, products) VALUES (%s,%s,%s)'
        self.cursor.execute(sql, values)
        self.cnx.commit()
    
    def add_product(self, product):
        categories = product.categories
        sql = 'INSERT INTO product (id_cat, name, url,\
                                    ingredients, brands,\
                                    grades) VALUES \
                                    (%s,%s,%s,%s,%s,%s)'
        for cat in categories:
            id_cat = self.get_id_category(cat)
            if id_cat:
                values = (id_cat, product.name, product.url,
                      product.ingredients, product.brands,
                      product.nutrition_grades)
                self.cursor.execute(sql, values)
        self.cnx.commit()
    
    def get_all_categories(self):
        sql = 'SELECT name FROM category'
        self.cursor.execute(sql)
        records = self.cursor.fetchall()
        return records
    
    def get_categories(self, n):
        sql = 'SELECT name FROM category'
        self.cursor.execute(sql)
        records = self.cursor.fetchall()
        return [t[0] for t in sample(records, n)]
    
    def get_grade(self, product_name):
        sql = 'SELECT grades FROM product WHERE name=%s'
        self.cursor.execute(sql, (product_name,))
        return self.cursor.fetchall()
    
    def get_products(self, cat_name):
        id_cat = self.get_id_category(cat_name)
        sql = 'SELECT name FROM product WHERE id_cat=%s'
        self.cursor.execute(sql, (int(id_cat),))
        return [t[0] for t in self.cursor.fetchall()]
    
    def get_substitute(self, cat_name, product_name):
        id_cat = self.get_id_category(cat_name)
        try:
            grade = self.get_grade(product_name)[0][0].lower()
            sql = 'SELECT * FROM product WHERE id_cat=%s AND ORD(grades)<ORD(%s)'
            values = (id_cat, grade)
            self.cursor.execute(sql, values)
            return self.cursor.fetchall()
        except (IndexError, AttributeError):
            return []
    
    def add_favorites(self, product_name, cat_name):
        id_cat = self.get_id_category(cat_name)
        sql = 'SELECT * FROM product WHERE name=%s AND id_cat=%s'
        sql_insert = 'INSERT INTO favorites (id_product,id_cat,\
                name,url,ingredients,brands,\
                grades) VALUES (%s,%s,%s,%s,%s,%s,%s)'
        self.cursor.execute(sql, (product_name, id_cat,))
        records = self.cursor.fetchall()
        if records:
            values = records[0]
            self.cursor.execute(sql_insert, values)
        self.cnx.commit()
    
    def get_favorites(self, product_name):
        sql = 'SELECT * FROM favorites WHERE name=%s'
        values = (product_name,)
        self.cursor.execute(sql, values)
        try:
            res = self.cursor.fetchall()[0]
        except IndexError:
            res = tuple()
        return res
    
    def get_info_product(self, product_name):
        sql = 'SELECT * FROM product WHERE name=%s'
        self.cursor.execute(sql, (product_name,))
        records = self.cursor.fetchall()
        return records[0]
    
    def get_all_favorites(self):
        sql = 'SELECT * FROM favorites'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res