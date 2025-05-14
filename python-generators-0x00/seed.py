#!/usr/bin/python3
import mysql.connector


def connect_db():
    "connects to the mysql database server"
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
    )

def create_database(connection):
    "creates the database ALX_prodev if it does not exist"
    mycursor = connection.cursor()
    mycursor.execute("CREATE DATABASE ALX_prodev")

def connect_to_prodev():
    "connects the the ALX_prodev database in MYSQL"
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="ALX_prodev"
    )

def create_table(connection):
    "creates a table user_data if it does not exists with the required fields"
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            email VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

def insert_data(connection, data):
    "inserts data in the database if it does not exist"