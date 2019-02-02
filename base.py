import getpass
import mysql.connector
import sys

from mysql.connector import errorcode
from tables import TABLES

class Base:
    def __init__(self, path):
        self.path = path
        self.user = input('Enter Username: ')
        self.password = getpass.getpass(prompt='Enter password: ')
        self.connect()
        self.create_tables('category', 'product')
        self.id_cat = None
            

    def connect(self):
        try:
            self.cnx = mysql.connector.connect(user=self.user, database=self.path, 
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

    def add_to_category(self, value):
        sql = """INSERT INTO category (name) VALUES (%s)"""
        self.cursor.execute(sql, value)
        self.cnx.commit()
        self.id_cat = self.cursor.lastrowid

    def add_to_products(self, values):
        sql = """INSERT INTO product (id_cat, name, url, ingredients, magasin) 
                VALUES ({}, %s, %s, %s, %s)""".\
                format(self.id_cat)
        self.cursor.execute(sql, values)
        self.cnx.commit()

    def search_to_products(self, value):
        sql = """SELECT name, url, ingredients, magasin FROM product"""
        self.cursor.execute(sql)
        for values in self.cursor.fetchall():
            if value in values:
                return values

    def get_all_products(self, table):
        sql = """SELECT name FROM {}""".format(table)
        self.cursor.execute(sql)
        products_list = sorted(self.cursor.fetchall())
        for ind, product in enumerate(products_list, start=1):
            print("{}:\t{}".format(ind, product[0]))