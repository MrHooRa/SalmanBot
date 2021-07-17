# Default packages
import os

# Mysql db
import mysql.connector
from mysql.connector import Error

# Get database login details
host = os.getenv('DB_HOSTNAME')
user = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')


def getMessage(connection):
    try:
        if connection.is_connected():
            cursor = connection.cursor()

        # YOUR CODE HERE

        cursor.execute("SELECT * FROM `discordSendMsg` WHERE `isSent` != true")
        getAllMessages = cursor.fetchall()

        for message in getAllMessages:
            if(message[3] == "false"):
                break
        print(message)
        cursor.execute(f"UPDATE `discordSendMsg` SET `isSent` = 'true' WHERE `discordSendMsg`.`id` = {message[0]}")
        cursor.execute("DELETE FROM `discordSendMsg` WHERE `isSent` = 'true'")
        connection.commit()
        cursor.close()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
    
    return message