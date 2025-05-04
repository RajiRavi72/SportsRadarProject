import mysql.connector

def db_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Raji",   
        database="sportsradar_db"
    )

# import pymysql
# from sqlalchemy import create_engine
# def db_conn():
#     conn = create_engine("mysql+pymysql://root:Raji@localhost/sportsradar_db")  
#     return conn