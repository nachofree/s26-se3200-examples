from flask import Flask
from flask import json
from flask import request
from db import *

app = Flask(__name__)


@app.route("/guitars/<int:id>", methods = ["OPTIONS"])
def do_preflight(id):
    print ("This is the preflight")
    #need to respond with correct headers
    #Access-Control-Allow-Origin: https://foo.bar.org
    #Access-Control-Allow-Methods: POST, GET, OPTIONS, DELETE
    #Access-Control-Allow-Headers: X-Requested-With

    return '', 204, {"Access-Control-Allow-Origin": "*",
                     "Access-Control-Allow-Methods": "PUT, DELETE",
                     "Access-Control-Allow-Headers": "Content-Type"}

@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Hello world</p>", {"Access-Control-Allow-Origin": "*"}

@app.route("/index")
def myindex():
    return "<p>index</p>"


@app.route("/guitars/<int:id>", methods=["DELETE"])
def delete_guitar(id):
    db = DB('guitars.db')
    db.deleteRecord(id)
    return "Deleted", 200, {"Access-Control-Allow-Origin": "*"}


@app.route("/guitars")
def get_guitars():
    db = DB('guitars.db')
    
    guitars = db.readAllRecords()
    return guitars, {"Access-Control-Allow-Origin": "*"}


@app.route("/guitars", methods=["POST"])
def create_a_new_guitar():
    print("The request data is ", request)
    db = DB('guitars.db')
    
    # Validate that required fields are present
    if 'name' not in request.form:
        return "Error: 'name' field is required", 400, {"Access-Control-Allow-Origin": "*"}
    if 'rating' not in request.form:
        return "Error: 'rating' field is required", 400, {"Access-Control-Allow-Origin": "*"}
    
    name = request.form['name'].strip()
    rating = request.form['rating'].strip()
    price = request.form['price'].strip()
    
    
    # Validate rating is a valid number
    try:
        rating_num = float(rating)
    except (ValueError, TypeError):
        return "Error: 'rating' must be a valid number", 400, {"Access-Control-Allow-Origin": "*"}
    
    # Validate rating is in reasonable range (0-10)
    if rating_num < 0 or rating_num > 10:
        return "Error: 'rating' must be between 0 and 10", 400, {"Access-Control-Allow-Origin": "*"}
    
    guitar = {"name": name, "rating": int(rating_num), "price": float(price)}
    db.saveRecord(guitar)
    return "created", 201, {"Access-Control-Allow-Origin": "*"}



def run():
    app.run(port=5000, host='0.0.0.0')

if __name__ == "__main__":
    run()