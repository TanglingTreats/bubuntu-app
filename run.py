from flask import Flask, render_template, request, redirect
import os, psycopg2

from pgdb import PGDB

DATABASE_URL = os.environ['DATABASE_URL']

#print(conn.get_dsn_parameters(),"\n")

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
mycursor = conn.cursor()
 
app = Flask(__name__)

app.secret_key = os.getenv("SECRET", "secretkey123")

messages = []
users = []

isUserIn = False

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/messages")
def message():
    messages.clear()
    users.clear()
    db = PGDB()
    
    sql = """SELECT users.username AS user, 
    message.msg_content AS content 
    FROM users 
    INNER JOIN message ON message.usr_id = users.usr_id"""
    
    res = db.get_data(sql)
    for x in res:
        post = {
            "username": x[0],
            "message":x[1]
        }
        messages.append(post)
        
    sql = "SELECT DISTINCT usr_id, username FROM users"
    
    res = db.get_data(sql)
    for x in res:
        print(x)
        user = {
            "user_id": x[0],
            "username": x[1]
        }
        users.append(user)
    
    return render_template("chat.html", messages=messages)
    
@app.route("/messages", methods=["POST"])
def get_message():
    global isUserIn
    db = PGDB()
    
    username = request.form.get("username")
    msg = request.form.get("message")
    
    if username != '' and msg != '':
        for i in users:
            if i['username'] == username:
                isUserIn = True
                break
            else:
                isUserIn = False
                
        if(isUserIn):
            #If user is in record, use user_id to store message with id
            user_id = i['user_id']
            db.create_msg(user_id, msg)
            #execute_query(user_id, msg)
            
        else:
            #else create a new record for user and store user_id in both tables
            #query for highest user_id, then add 1 to store as new user_id
            query="SELECT MAX(usr_id) FROM users"
            mycursor.execute(query)
            res = mycursor.fetchall()
                
            if(res[0][0] is None):
                new_user_id = 1
            else:
                new_user_id = res[0][0]+1
                
            val = (new_user_id, username)
            query = "INSERT INTO users(usr_id, username) VALUES(%s, %s)"
            db.create_user(query, val)
            
            db.create_msg(new_user_id, msg)
        
    return redirect("/messages")

    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "0.0.0.0"),
            port=int(os.environ.get("PORT", "5000")),
            debug=False)