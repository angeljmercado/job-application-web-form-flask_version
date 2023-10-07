from datetime import datetime
from decouple import config
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)

# contants for the app instances from the Flask Class
app.config["SECRET_KEY"] = "mysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = config("email")
app.config["MAIL_PASSWORD"] = config("password")

# Instance for the sqlite database
db = SQLAlchemy(app)

# Instance for the mail function
mail = Mail(app)

class Form(db.Model):
    """ creates a database with the columns defined below """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Stores data that the user inputs in the webpage
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        # Add data stored in the variables to the "data.db" database
        form = Form(first_name=first_name, last_name=last_name,
        email=email, date=date, occupation=occupation)
        db.session.add(form)
        db.session.commit()

        # Variables in preparation to send email message
        message_body = f"""Hello! {first_name},
        Thank you for submitting a job application with us.
        We will get back to you shortly.
                           
        Best Regards,
        Recruiting Team"""
        message = Message(subject=f"{first_name}'s Job Application.",
        sender=app.config["MAIL_USERNAME"],
        recipients=[email],
        body=message_body)

        mail.send(message)

        #Message after user presses submit
        flash("Your form was submitted sucessfully!", "success")
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
