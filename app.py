# python -m pip install flask flask_session
# python -m flask run
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from datetime import datetime
from helpers import login_required
import sqlite3

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@login_required
@app.route("/", methods=["GET","POST"])
def home():
    messages = []
    with sqlite3.connect("message.db") as conn:
      c = conn.cursor()
      if request.method == "POST":
        c.execute("INSERT INTO messages VALUES (?,?,?)",(request.form.get("user"), request.form.get("message"), datetime.now()))
      c = conn.cursor()
      messages = c.execute("SELECT * FROM messages")
      conn.commit()
    return render_template("index.html", messages=messages)
  
@app.route("/group/<groupID>", methods=["GET","POST"])
def group(groupID):

  messages = []

  with sqlite3.connect("message.db") as conn:
    c = conn.cursor()
    if request.method == "POST":
      image = request.form.get("image")
      c.execute("INSERT INTO messages VALUES (?,?,?,?,?)",(session.get("user_id"), (image is None), image, request.form.get("message"), datetime.now()))
    c = conn.cursor()
    messages = c.execute("SELECT * FROM messages WHERE groupID == ?", groupID)
    conn.commit()
  
  return render_template("index.html", messages=messages, group=group)

@app.route("/login", methods=["GET","POST"])

def login():
  session.clear()

  if request.method == "POST":

    with sqlite3.connect("message.db") as conn:
      c = conn.cursor()
      user_id = c.execute("SELECT ID FROM users WHERE username == (?)", request.forms.get("username"))[0]
      session["user_id"] = user_id

    return redirect("/")
  
  else:
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
  session.clear()
  if request.method == "POST":
    pass
  else:
    return render_template("register.html")

'''
CREATE TABLE users (
  ID int NOT NULL,
  username varchar(30) NOT NULL,
  password NOT NULL,
  email varchar(100) NOT NULL,
  profilePicture image,
  PRIMARY KEY (ID)
);
CREATE TABLE groups (
  ID int NOT NULL AUTO_INCREMENT,
  groupname varchar(30),
  groupImage image,
  isDm bit,
  usersInGroup char NOT NULL,
  PRIMARY KEY (ID)
);
CREATE TABLE messages (
  ID int NOT NULL AUTO_INCREMENT,
  userID int,
  groupID int,
  hasImage bit,
  image image
  message text,
  date datetime,
  PRIMARY KEY (ID),
  FOREIGN KEY (groupID) REFERENCES groups(ID),
  FOREIGN KEY (userID) REFERENCES users(ID)
);
CREATE TABLE ID (
  userID int,
  groupID int,
  messageID int
);
'''

# @app.route("/<point1>", methods=["GET","POST"])
# def drew(point1):
#     if request.method == "POST":
#         point = request.form.get("draw")
#         return redirect(f"/{point}")
#     else:
#         return render_template("drew.html", point=point1)
