import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="ubuntu",
  passwd="mysql",
  database="messages"
)

mycursor = mydb.cursor()

mycursor.execute("SET time_zone='+08:00'")
'''
sql = "INSERT INTO message(msg_id, msg_content, usr_id) VALUES(%s, %s, %s)"
val = (1, 'hello', 1)
mycursor.execute(sql, val)

sql = "INSERT INTO user(usr_id, username) VALUES(%s, %s)"
val = (1, 'edwin')
mycursor.execute(sql, val)

mydb.commit() #this is required to update the changes
'''

sql = "SELECT user.username AS user, message.msg_content AS content FROM user INNER JOIN message ON message.usr_id = user.usr_id"
mycursor.execute(sql)

res = mycursor.fetchall()

for x in res:
    print(x)

mycursor.execute("SHOW TABLES")

for x in mycursor:
    print (x)

print(mydb)