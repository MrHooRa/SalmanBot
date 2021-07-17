# Defualt pacakges
import os

# Mysql db
import mysql.connector
from mysql.connector import Error

# Discord packages
import discord
from discord.ext import commands
from discord.ext import tasks


class FivePD():

    def __init__(self):
        print("\n*******************************"
              + "\n - FivePD with Discord -"
              + f"\n -> Created new FivePD obj!"
              + "\n*******************************")
        print("Created new FivePD obj!")

    # Set database details and connections | Boolean
    def db(self, host, user, password, database, tableName):
        # Make a connection to data base
        try:
            # Connecte to MySql database
            self.connection = mysql.connector.connect(host=host,
                                                      database=database,
                                                      user=user,
                                                      password=password)
            self.table = tableName
            if self.connection.is_connected():
                return True
            return False

        # Catch the error
        except Error as e:
            print("Error while connecting to MySQL ->", e)
            return False

    # Close db connection | Boolean
    def db_close(self):
        try:
            if self.connection.is_connected():
                self.connection.close()
                # print("MySQL connection is closed")
                return True
        except Error as e:
            print("Error while close db connection ->", e)
            return False

    def get(self):
        resutls = []

        try:
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute(
                    f"SELECT `gameName`, `isAdmin`, `activated` FROM {self.table}")
                resutls = cursor.fetchall()

        except Error as e:
            print("Error while trying to get data ->", e)

        return resutls
