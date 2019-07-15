import os, psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
mycursor = conn.cursor()

#print(conn.get_dsn_parameters(),"\n")

query = """CREATE TABLE message(msg_id INT PRIMARY KEY, msg_content VARCHAR, usr_id INT)"""
mycursor.execute(query);

'''
query = """CREATE TABLE users(usr_id INT PRIMARY KEY, username VARCHAR)"""
mycursor.execute(query);
'''

conn.commit()