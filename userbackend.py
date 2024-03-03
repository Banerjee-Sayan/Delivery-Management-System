import mysql.connector
from tkinter import messagebox

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="delivery"
    )
class UserBackend:
    def __init__(self, connection):
        self.connection = connection

    def authenticate_user(self, user_id, password):
        query = "SELECT * FROM user_registration WHERE user_id_entry = %s AND password_entry = %s"
        cursor = self.connection.cursor()
        cursor.execute(query, (user_id, password))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            return True  
        else:
            return False
    
    def register_user(self, name, email, phone_number, user_id, password):
        insert_user_data(self.connection, name, email, phone_number, user_id, password)
            


def create_user_registration_table(connection):
    create_user_registration_query = """
    CREATE TABLE IF NOT EXISTS user_registration (
        name_entry VARCHAR(20),
        email_entry VARCHAR(100),
        phone_number_entry  BIGINT,
        user_id_entry VARCHAR(20) NOT NULL PRIMARY KEY,
        password_entry VARCHAR(20)
    )
    """
    with connection.cursor() as cursor:
        cursor.execute(create_user_registration_query)
        connection.commit()

def create_delivery_form(connection):
        create_delivery_form_query = """
        CREATE TABLE IF NOT EXISTS delivery_registration (
            destination_id VARCHAR(20),
            name VARCHAR(100),
            street VARCHAR(20),
            city VARCHAR(20),
            state VARCHAR(255)
        )
        """
        with connection.cursor() as cursor:
            cursor.execute(create_delivery_form_query)
            connection.commit()

def create_address_book(connection):
    create_address="""
    CREATE TABLE IF NOT EXISTs address_book(
        latitude VARCHAR(20),
        longitude VARCHAR(20),
        street VARCHAR(50),
        city VARCHAR(50),
        state VARCHAR(50),
        phn BIGINT
    )
    """
    with connection.cursor() as cursor:
        cursor.execute(create_address)
        connection.commit()


def insert_user_data(connection, name, email, phone_number, user_id, password):
    insert_query = "INSERT INTO user_registration (name_entry, email_entry, phone_number_entry, user_id_entry, password_entry) VALUES (%s, %s, %s, %s, %s)"
    values = (name, email, phone_number, user_id, password)
    with connection.cursor() as cursor:
        cursor.execute(insert_query, values)
        connection.commit()

def update_user_data(connection,current_password,new_password,confirm_password):
    update_query = "UPDATE user_registration SET password_entry = %s WHERE user_id_entry = %s"
    values = (new_password,current_password)  
    with connection.cursor() as cursor:
        cursor.execute(update_query, values)
        connection.commit()


def insert_delivery_data(connection, destination_id, name, street, city, state):
    insert_query = """
    INSERT INTO delivery_registration(destination_id, name, street, city, state)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (destination_id, name, street, city, state)
    with connection.cursor() as cursor:
        cursor.execute(insert_query, values)
        connection.commit()

def add_address(connection,latitude,longitude,street,city,state,phn):
    insert_query = """
    INSERT INTO address_book(latitude,longitude,street,city,state,phn)
    Values(%s,%s,%s, %s, %s, %s)
    """
    values = (latitude,longitude,street,city,state,phn)
    with connection.cursor() as cursor:
        cursor.execute(insert_query,values)
        connection.commit()



def close_connection(connection):
    connection.close()
