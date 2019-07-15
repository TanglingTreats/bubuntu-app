import os, psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
mycursor = conn.cursor()

print(conn.get_dsn_parameters(),"\n")