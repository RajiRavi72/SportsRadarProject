import mysql.connector

def db_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Raji",  # give your password here 
        database="sportsradar_db"  # give your db name here
    )

