import mysql.connector
from mysql.connector import Error
from logs import *


class DB():
    def __init__(self, username, password, database, host):
        self.username = username
        self.password = password
        self.database = database
        self.host = host

        self.logs = Logs(name='db.py', tabs=2)

    def connect(self):
        """Connect to database"""
        try:
            self.connection = mysql.connector.connect(host=self.host,
                                                      user=self.username,
                                                      password=self.password,
                                                      database=self.database)
            return True
        except Error as e:
            self.logs.log(f"Can not connect to database!. -> Exception: {e}", True, type="Error")
            return False
    
    def close(self):
        try:
            if self.connection.is_connected():
                self.connection.close()
                return True
        except Error as e:
            self.logs.log(f"Can not close db connection. -> Exception: {e}", True, type="Error")
            return False

    def is_connected(self):
        return self.connection.is_connected()