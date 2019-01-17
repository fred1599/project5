import getpass
import mysql.connector

from mysql.connector import errorcode
from tables import TABLES

class Base:
    def __init__(self, path):
        self.path = path
        self.user = input('Enter Username: ')
        self.password = getpass.getpass(prompt='Enter password: ')
        self.connect()
        self.create_tables('category', 'meal')
            

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
        
    def create_tables(self, *tablenames):
        for table in tablenames:
            self.cursor.execute(TABLES[table])

base = Base('my_base')