from flask import Flask, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import setup

# Load environment variables from the .env file (if present)
load_dotenv()

settings=dict()
settings["PGUSER"] = os.getenv("PGUSER")
settings["PGPASSWORD"] = os.getenv("PGPASSWORD")
settings["PGHOST"] = os.getenv("PGHOST")
settings["PGPORT"] = os.getenv("PGPORT")
settings["PGDB"] = os.getenv("PGDB")

app = Flask(__name__, template_folder="templates")

app.config[
    "SQLALCHEMY_DATABASE_URI"] = f"postgresql://{settings['PGUSER']}:{settings['PGPASSWORD']}@{settings['PGHOST']}:{settings['PGPORT']}/{settings['PGDB']}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

class DB:
    def getInstance(self):
        self.db = SQLAlchemy(app)
        return self.db


db = DB().getInstance()

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """print(request.form["email"])
            print(request.form)"""
    # request.form creates a special dictionary through which we can access the value of corresponding key
    if request.method == "POST":
        username = request.form["account_name"]
        email = request.form["email"]
        password = request.form["password"]
        cnfrm_password = request.form["cnfrm_password"]

        if password == cnfrm_password:
            # Create a new User instance and add it to the database
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/signup/success")
        return "Passwords do not match"
    return render_template("signup.html")


@app.route("/signup/success")
def success():
    # Fetch and display user data from the database (this is just an example)
    users = User.query.all()
    for u in users:
        print(u)
    return "success "
    # return render_template("success.html", users=users)


if __name__ == "__main__":
    try:
        with app.app_context():
            #setup.create_users(db)
            db.create_all()
            app.run(debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")

        