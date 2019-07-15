from flask import Flask, render_template, request, redirect
import os, psycopg2
'''
mydb = mysql.connector.connect(
  host="localhost",
  user="ubuntu",
  passwd="mysql",
  database="messages"
)
'''
'''
mydb = psycopg2.connect(user="postgres",
                        password="postgres",
                        host="localhost",
                        database="messages")
'''
DATABASE_URL = os.environ['DATABASE_URL']
mydb = psycopg2.connect(DATABASE_URL, sslmode="require")
mycursor = mydb.cursor()

#print(mydb.get_dsn_parameters(),"\n")
 
app = Flask(__name__)

app.secret_key = os.getenv("SECRET", "secretkey123")

messages = []
users = []

isUserIn = False
    
@app.route("/")
def index():
    messages.clear()
    users.clear()
    sql = """SELECT users.username AS user, 
    message.msg_content AS content 
    FROM users 
    INNER JOIN message ON message.usr_id = users.usr_id"""
    
    mycursor.execute(sql)

    res = mycursor.fetchall()
    for x in res:
        post = {
            "username": x[0],
            "message":x[1]
        }
        messages.append(post)
        
    sql = "SELECT DISTINCT usr_id, username FROM users"
    mycursor.execute(sql)
    
    res = mycursor.fetchall()
    for x in res:
        user = {
            "user_id": x[0],
            "username": x[1]
        }
        users.append(user)
    
    print(users)
    return render_template("index.html", messages=messages)
    
@app.route("/", methods=["POST"])
def get_message():
    global isUserIn
    if request.form.get("Submit"):
        print("Run")
        username = request.form.get("username")
        msg = request.form.get("message")
        
        if username != '' and msg != '':
            print("If ran")
            for i in users:
                if i['username'] == username:
                    print("true")
                    
                    isUserIn = True
                    break
                else:
                    print("false")
                    isUserIn = False
                    
            if(isUserIn):
                #If user is in record, use user_id to store message with id
                user_id = i['user_id']
                execute_query(user_id, msg)
                
            else:
                #else create a new record for user and store user_id in both tables
                #query for highest user_id, then add 1 to store as new user_id
                print("This ain't the user id")
                query="SELECT MAX(usr_id) FROM users"
                mycursor.execute(query)
                res = mycursor.fetchall()
                    
                if(res[0][0] is None):
                    new_user_id = 1
                else:
                    new_user_id = res[0][0]+1
                    
                val = (new_user_id, username)
                print(val)
                query = "INSERT INTO users(usr_id, username) VALUES(%s, %s)"
                mycursor.execute(query, val)
                
                execute_query(new_user_id, msg)
                
                
            
    if request.form.get("Clear"):
        messages.clear()
        print(messages)
        
    return redirect("/")
    
def execute_query(user_id, msg):
    query="SELECT MAX(msg_id) FROM message"
    mycursor.execute(query)
    res = mycursor.fetchall()
    if(res[0][0] is None):
        msg_id = 1
    else:
        msg_id = res[0][0]+1
    val = (msg_id, msg, user_id)
    
    
    query = """INSERT INTO message(msg_id, msg_content, usr_id) 
                VALUES(%s, %s, %s)"""
    mycursor.execute(query, val)
    mydb.commit()
    
    

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)