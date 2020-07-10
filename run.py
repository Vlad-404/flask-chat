import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = "randomstring123"
messages = []

def add_messages(username, message):
    """Add messages to the messages list"""
    now = datetime.now().strftime("%H:%M:%S")
    messages.append("({}) {}: {}".format(now, username, message))


def get_all_messages():
    """Get all messages and separate them with 'br'"""
    return "<br>".join(messages)


@app.route("/", methods=["GET", "POST"])
def index():
    """ Main page with instructions"""
    if request.method == "POST":
        session["username"] = request.form["username"]

    if "username" in session:
        return redirect(session["username"])

    return render_template("index.html")
 

@app.route('/<username>')
def user(username):
    """Dispaly chat messages"""
    return "<h1>Welcome, {0}</h1>{1}".format(username, get_all_messages())


@app.route('/<username>/<message>')
def send_message(username, message):
    """Create a new message and redirect back to chat app"""
    add_messages(username, message)
    return redirect("/" + username)


if __name__ == "__main__":
    app.run(host = os.getenv("IP"),
        port = int(os.getenv("PORT")),
        debug = True)