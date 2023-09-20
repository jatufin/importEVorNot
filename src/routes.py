from app import app

from flask import redirect, render_template

@app.route("/")
def main():
    return redirect("/index")

@app.route("/index")
def index():
     return render_template("index.html", foo="Bar")
