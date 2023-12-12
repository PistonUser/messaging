# python -m pip install flask
# python -m flask run
from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    messages = []
    with sqlite3.connect("message.db") as conn:
      c = conn.cursor
      if request.method == "POST":
        c.execute("INSERT INTO messages VALUES (?,?)",(request.form.get("user"), request.form.get("message")))
        conn.commit()
      messages = c.execute("SELECT * FROM messages")
    return render_template("index.html", messages=messages)

# @app.route("/<point1>", methods=["GET","POST"])
# def drew(point1):
#     if request.method == "POST":
#         point = request.form.get("draw")
#         return redirect(f"/{point}")
#     else:
#         return render_template("drew.html", point=point1)
