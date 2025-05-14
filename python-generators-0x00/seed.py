#!/usr/bin/python3
import csv
import mysql.connector
import uuid


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
    mycursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")

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
    "inserts data from a csv file in the database if it does not exist"
    cursor = connection.cursor()
    with open(data, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT IGNORE INTO user_data (id, name, age, email)
                VALUES (%s, %s, %s, %s)
            """, (str(uuid.uuid4()), row['name'], row['age'], row['email']))
    connection.commit()
    cursor.close()

