from flask import Flask
from flask import json
from flask import request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Hello world</p>", {"Access-Control-Allow-Origin": "*"}

@app.route("/index")
def myindex():
    return "<p>index</p>"

guitars = [
    {"name": "Fender Stratocaster", "price": 107.39, "rating": 7},
    {"name": "Gibson Les Paul", "price": 2499.99, "rating": 9},
    {"name": "Ibanez RG550", "price": 999.99, "rating": 8},
    {"name": "PRS Custom 24", "price": 3499.00, "rating": 9},
    {"name": "Yamaha Pacifica 112V", "price": 329.99, "rating": 8},
    {"name": "Epiphone SG Standard", "price": 499.99, "rating": 7},
    {"name": "Gretsch G2622 Streamliner", "price": 649.99, "rating": 8},
    {"name": "Jackson JS32 Dinky", "price": 379.99, "rating": 7},
    {"name": "Taylor 214ce", "price": 1199.00, "rating": 9},
    {"name": "Martin D-28", "price": 3199.00, "rating": 10}
]

@app.route("/guitars")
def get_guitars():
    json_data = json.dumps(guitars, indent=2)
    return json_data, {"Access-Control-Allow-Origin": "*"}

@app.route("/guitars", methods=["POST"])
def create_a_new_guitar():
    print("The request data is ", request)
    
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
    
    guitars.append({"name": name, "rating": int(rating_num), "price": float(price)})

    return "created", 201, {"Access-Control-Allow-Origin": "*"}



def run():
    app.run(port=5000, host='0.0.0.0')

if __name__ == "__main__":
    run()