import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_cors import CORS
from dotenv import load_dotenv

# Load .env only for local development
load_dotenv()

app = Flask(__name__)
CORS(app)

# Read DB URL from env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is missing! Add it in Render Environment Variables.")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Database Models
class Division(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(100))
    division_id = db.Column(db.Integer, db.ForeignKey('division.id'))


# Create tables
with app.app_context():
    db.create_all()


# Routes
@app.route("/checkup_db")
def checkup_db():
    try:
        db.session.execute(text("SELECT 1"))
        return {"Status": "Success", "message": "Database connected successfully"}
    except Exception as e:
        return {"Status": "Error", "message": str(e)}


@app.route("/divisions", methods=["GET"])
def divisions():
    try:
        division_list = Division.query.all()
        res = [{"id": d.id, "name": d.name} for d in division_list]
        return jsonify(res)
    except Exception as e:
        return {"Status": "Error", "message": str(e)}


@app.route("/divisions/<div_name>", methods=["POST"])
def create_division(div_name):
    try:
        div = Division(name=div_name)
        db.session.add(div)
        db.session.commit()
        return {"Status": "ok", "message": f"Division {div_name} created"}
    except Exception as e:
        return {"Status": "Error", "message": str(e)}


@app.route("/")
def home():
    return "✅ Flask is working excellent!"


if __name__ == '__main__':
    app.run(debug=True)
