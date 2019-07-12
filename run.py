from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

app.secret_key = os.getenv("SECRET", "secretkey123")

messages = []

@app.route("/")
def index():
    return render_template("index.html", messages=messages)
    
@app.route("/", methods=["POST"])
def get_message():
    if request.form.get("Submit"):
        print("Run")
        username = request.form.get("username")
        msg = request.form.get("message")
        
        if username != '' and msg != '':
            post = {
                "username": username,
                "message": msg
                }
            messages.append(post)
            print(messages)
            
    if request.form.get("Clear"):
        messages.clear()
        print(messages)
        
    return redirect("/")
    
    

if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "0.0.0.0"),
            port=int(os.environ.get("PORT", "5000")),
            debug=True)