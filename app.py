from flask import Flask, render_template, request, redirect, flash
from dotenv import load_dotenv
from models import db, TicketRequest  
import os
from arsenal_bot import run_bot

app = Flask(__name__)
app.secret_key = "arsenal_secret_key"
load_dotenv()


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tickets.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
       
        email = request.form["email"]
        password = request.form["password"]
        fixture_url = request.form["fixture_url"]
        blocks = request.form["blocks"]
        prices = request.form["prices"]
        quantity = request.form["quantity"]
        headless = "headless" in request.form

       
        os.environ["ARS_EMAIL"] = email
        os.environ["ARS_PASS"] = password
        os.environ["ARS_FIXTURE_URL"] = fixture_url
        os.environ["ARS_BLOCKS"] = blocks
        os.environ["ARS_PRICES"] = prices
        os.environ["ARS_QTY"] = quantity
        os.environ["ARS_HEADLESS"] = "true" if headless else "false"

    
        new_request = TicketRequest(
            email=email,
            fixture_url=fixture_url,
            blocks=blocks,
            prices=prices,
            quantity=int(quantity),
            headless=headless
        )
        db.session.add(new_request)
        db.session.commit()

        try:
            flash("Running bot… please wait!", "info")
            run_bot()
            flash("Ticket booking attempt completed.", "success")
        except Exception as e:
            flash(f" Error: {str(e)}", "danger")

        return redirect("/")

    return render_template("index.html")


@app.route("/history")
def history():
    requests = TicketRequest.query.order_by(TicketRequest.timestamp.desc()).all()
    return render_template("history.html", requests=requests)

if __name__ == "__main__":
    app.run(debug=True)
