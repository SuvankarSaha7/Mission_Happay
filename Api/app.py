
# import flask
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://neondb_owner:npg_HAlpP4EC6YZT@ep-dark-sky-ahi1mneg-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

db = SQLAlchemy(app)

# making division table
class Division(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))

class Unit(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    unit_name=db.Column(db.String(100))
    division_id = db.Column(db.Integer, db.ForeignKey('division.id'))


with app.app_context():
    db.create_all()

@app.route("/checkup_db")
def checkup_db():
    try:
        db.session.execute(text("SELECT 1")) # this line means that if the backend is connect to DB successfully or not 
        return {"Status":"Success","message":"Database connected successfull"}
    except Exception as e:
        return {"Status":"Error", "message":str(e)}
    
@app.route("/divisions",methods=["GET"]) 
def divsions():
    try:
        division = Division.query.all() # here "query" is inbuild method when we define model then this type of properties or method already inherits from the model 
        #Division.query → query builder
        #Division.query.all() → get all rows
        #Division.query.get(id) → get by primary key

        # Division.query.filter_by(name="HR") → filtering

        # Division.query.first() → first row

        # Division.query.count() → total row
        #
        res = [{"id":d.id,"name":d.name} for d in division]
        return jsonify(res)
    except Exception as e:
        return {"Status":"Error","message":str(e)}
    



@app.route("/divisions/<div_name>" , methods=["POST"])
def divisions(div_name):
    try:
        div = Division(name = div_name)
        db.session.add(div)
        db.session.commit()
        return {"Status":"ok","message":f"division {div_name} create in DB"}
    except Exception as e:
        return {"Status":"error","message":str(e)}


@app.route('/')
def home():
    return "✅ Flask is working excellent!"

if __name__ == '__main__':
    app.run(debug=True)


