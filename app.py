# python -m pip install flask
# python -m flask run
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
messages = []

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
      messages += [{"name":request.form.get("user"),"message":request.form.get("message")}]
    return render_template("index.html", messages=messages)

@app.route("/<point1>", methods=["GET","POST"])
def drew(point1):
    if request.method == "POST":
        point = request.form.get("draw")
        return redirect(f"/{point}")
    else:
        list = grid()
        return render_template("drew.html", grid=list.grid, point=point1)
