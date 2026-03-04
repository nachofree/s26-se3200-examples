from flask import Flask
from flask import json
from flask import request
from realdb import *

app = Flask(__name__)

# db = DummyDB('database.json')

@app.route("/guitars/<int:id>", methods=["OPTIONS"])
def do_preflight(id):
    return '', 204, {"Access-Control-Allow-Origin": "*",
                     "Access-Control-Allow-Methods": "PUT, DELETE",
                     "Access-Control-Allow-Headers": "Content-Type"}

@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Hello world</p>", {"Access-Control-Allow-Origin": "*"}

@app.route("/index")
def myindex():
    return "<p>index</p>"



@app.route("/guitars")
def get_guitars():
    db = RealDB('database.db')

    # json_data = json.dumps(guitars, indent=2)
    json_data = db.readAllRecords()
    return json_data, {"Access-Control-Allow-Origin": "*"}

@app.route("/guitars/<int:id>", methods=["DELETE"])
def delete_guitar(id):
    db = RealDB('database.db')
    db.deleteGuitar(id)
    return "Deleted", 200,  {"Access-Control-Allow-Origin": "*"}

@app.route("/guitars/<int:id>", methods=["PUT"])
def update_guitar(id):
    db = RealDB('database.db')
    
    # Validate that required fields are present
    if 'name' not in request.form:
        return "Error: 'name' field is required", 400, {"Access-Control-Allow-Origin": "*"}
    if 'rating' not in request.form:
        return "Error: 'rating' field is required", 400, {"Access-Control-Allow-Origin": "*"}
    if 'price' not in request.form:
        return "Error: 'price' field is required", 400, {"Access-Control-Allow-Origin": "*"}
    
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
    
    # Validate price is a valid number
    try:
        price_num = float(price)
    except (ValueError, TypeError):
        return "Error: 'price' must be a valid number", 400, {"Access-Control-Allow-Origin": "*"}
    
    # Validate price is positive
    if price_num < 0:
        return "Error: 'price' must be positive", 400, {"Access-Control-Allow-Origin": "*"}
    
    guitar = {"name": name, "rating": int(rating_num), "price": price_num}
    db.updateGuitar(id, guitar)

    return "updated", 200, {"Access-Control-Allow-Origin": "*"}







@app.route("/guitars", methods=["POST"])
def create_a_new_guitar():
    # print("The request data is ", request)
    db = RealDB('database.db')

    
    # Validate that required fields are present
    if 'name' not in request.form:
        return "Error: 'name' field is required", 400, {"Access-Control-Allow-Origin": "*"}
    if 'rating' not in request.form:
        return "Error: 'rating' field is required", 400, {"Access-Control-Allow-Origin": "*"}
    if 'price' not in request.form:
        return "Error: 'price' field is required", 400, {"Access-Control-Allow-Origin": "*"}
    
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
    
    # Validate price is a valid number
    try:
        price_num = float(price)
    except (ValueError, TypeError):
        return "Error: 'price' must be a valid number", 400, {"Access-Control-Allow-Origin": "*"}
    
    # Validate price is positive
    if price_num < 0:
        return "Error: 'price' must be positive", 400, {"Access-Control-Allow-Origin": "*"}
    
    # guitars.append({"name": name, "rating": int(rating_num), "price": price_num})
    guitar = {"name": name, "rating": int(rating_num), "price": price_num}
    db.saveRecord(guitar)

    return "created", 201, {"Access-Control-Allow-Origin": "*"}



def run():
    app.run(port=5000, host='0.0.0.0')

if __name__ == "__main__":
    run()