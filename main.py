from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)
messages = []

@app.route("/")
def index():
    return render_template("index.html", messages=messages)
    
@app.route("/", methods=["POST"])
def get_message():
    username = request.form.get("username")
    msg = request.form.get("message")
    
    post = {
        "username": username,
        "message": msg
        }
    messages.append(post)
    print(messages)
    return redirect("/")

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)