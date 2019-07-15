import psycopg2

mydb = psycopg2.connect(user="postgres",
                            password="postgres",
                            host="127.0.0.1",
                            database="messages")
                            
mycursor = mydb.cursor()

#print (mydb.get_dsn_parameters(),"\n")
'''
sql = "INSERT INTO message(msg_id, msg_content, usr_id) VALUES(%s, %s, %s)"
val = (1, 'hello', 1)
mycursor.execute(sql, val)

sql = "INSERT INTO users(usr_id, username) VALUES(%s, %s)"
val = (1, 'edwin')
mycursor.execute(sql, val)

mydb.commit() #this is required to update the changes
'''
sql = "SELECT users.username AS user, message.msg_content AS content FROM users INNER JOIN message ON message.usr_id = users.usr_id"
mycursor.execute(sql)

res = mycursor.fetchall()

for x in res:
    print(x)