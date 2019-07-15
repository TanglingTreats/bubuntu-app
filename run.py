from flask import Flask, render_template, request, redirect
import os, mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="ubuntu",
  passwd="mysql",
  database="messages"
)

mycursor = mydb.cursor()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET", "secretkey123")

messages = []
users = []

isUserIn = False



@app.route("/")
def index():
    messages.clear()
    users.clear()
    sql = "SELECT user.username AS user, message.msg_content AS content FROM user INNER JOIN message ON message.usr_id = user.usr_id"
    mycursor.execute(sql)

    res = mycursor.fetchall()
    for x in res:
        post = {
            "username": x[0],
            "message":x[1]
        }
        messages.append(post)
        
    sql = "SELECT DISTINCT (usr_id) FROM user"
    mycursor.execute(sql)
    
    res = mycursor.fetchall()
    for x in res:
        user = {
            "user_id": x[0]
        }
        users.append(user)
    
    print(users)
    return render_template("index.html", messages=messages)
    
@app.route("/", methods=["POST"])
def get_message():
    
    if request.form.get("Submit"):
        print("Run")
        username = request.form.get("username")
        msg = request.form.get("message")
        
        if username != '' and msg != '':
            print("If ran")
            for i in users:
                if i['username'] == username:
                    isUserIn = True
                    break
                else:
                    isUserIn = False
                    
                    
            if(isUserIn):
                #If user is in record, use user_id to store message with id
                user_id = i['user_id']
                
                execute_query(user_id, msg)
                
            else:
                #else create a new record for user and store user_id in both tables
                #query for highest user_id, then add 1 to store as new user_id
                print("This ain't the user id")
                query="SELECT MAX(usr_id) FROM user"
                mycursor.execute(query)
                res = mycursor.fetchall()
                new_user_id = res[0][0]+1
                val = (new_user_id, username)
                print(val)
                query = "INSERT INTO user(usr_id, username) VALUES(%s, %s)"
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
    msg_id = res[0][0]+1
    val = (msg_id, msg, user_id)
    
    
    query = "INSERT INTO message(msg_id, msg_content, usr_id) VALUES(%s, %s, %s)"
    mycursor.execute(query, val)
    mydb.commit()
    
    

if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "0.0.0.0"),
            port=int(os.environ.get("PORT", "5000")),
            debug=True)