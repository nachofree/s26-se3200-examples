from flask import Flask
from flask import json

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

from flask import request
@app.route("/guitars", methods=["POST"])
def create_a_guitar():
    print("The request data is ", request.form)
    # guitars.append(request.form)
    name = request.form['name']
    print("The name is ", name)
    guitars.append({"name": name})
    return "Created", 201, {"Access-Control-Allow-Origin":"*"}



def run():
    app.run(port=5000, host='0.0.0.0')

if __name__ == "__main__":
    run()