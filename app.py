
from flask import Flask, render_template, request, session, redirect, url_for
import requests 
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

API_KEY = os.getenv("API_KEY")
SECRET_PASSWORD = os.getenv("SECRET_PASSWORD")

def get_exchange_rate(base, target):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{base}/{target}"
    response = requests.get(url)
    data = response.json()
    if data["result"] == "success":
        return data["conversion_rate"]
    return None

@app.route("/", methods=["GET"])
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None 
    if request.method == "POST":
        if request.form["password"] == SECRET_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("index"))
        else: 
            error = "Wrong password du Stinker, try again"
    return render_template("login.html", error=error)

@app.route("/convert", methods=["POST"])
def convert():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    base = request.form["base"].upper()
    target = request.form["target"].upper()
    amount = float(request.form["amount"])
    rate = get_exchange_rate(base, target)
    result = round(amount * rate, 2) if rate else None
    return render_template("index.html", result=result, base=base, target=target, amount=amount)

if __name__ == "__main__":
    app.run(debug=True)


