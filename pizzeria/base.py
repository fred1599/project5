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
        self.create_tables('category', 'product', 'favorites')
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

    def add(self, table, *values):
        if table not in ('category', 'product', 'favorites'):
            raise TypeError('Erreur sur le nom de la table: {}'.format(table))

        if table == 'category':
            sql = """INSERT INTO category (name) VALUES (%s)"""

            index_max = len(values)-1
            if index_max == 0:
                values = values[0]
                self.cursor.execute(sql, (values,))
            else:
                raise ValueError("Erreur, trop d'infos à insérer")
        
        elif table == 'favorites':
            sql = """INSERT INTO favorites (id_cat, name, url, ingredients, magasin)\
            VALUES {}""".format(values)
            
            self.cursor.execute(sql)
        
        else:
            sql = """INSERT INTO product (id_cat, name, url, ingredients, magasin)\
            VALUES {}""".format(values)
            
            self.cursor.execute(sql)

        
        self.cnx.commit()

    def contains(self, table, value):
        if table in ('category', 'product', 'favorites'):
            sql = """SELECT name FROM {} where name=%s""".format(table)
            self.cursor.execute(sql, (value,))
            result = self.cursor.fetchall()
            if result:
                return True
        else:
            print("table {} non présente dans la base".format(table))
        return False

    def get_id(self, table, object):

        sql = """SELECT id_category FROM {} WHERE name=%s""".format(table)

        self.cursor.execute(sql, (object,))
        result = self.cursor.fetchone()
        if result:
            my_id = result[0]
        else:
            my_id = None
        return my_id

    def get_infos(self, table, product):
        if table not in ('category', 'product', 'favorites'):
            raise TypeError("table vaut category ou product")

        if table == 'category':
            raise NotImplementedError('research in table category not implemented')

        sql = """SELECT name, url, ingredients, magasin FROM product WHERE name=%s"""
        self.cursor.execute(sql, (product,))
        result = self.cursor.fetchone()
        return result
