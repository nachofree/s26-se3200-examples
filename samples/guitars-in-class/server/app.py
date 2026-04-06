from flask import Flask
from flask import json
from flask import request, g
from realdb import *
from session_store import SessionStore

app = Flask(__name__)

session_store = SessionStore()

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
    if "email" not in g.session_data:
        return
    
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



@app.route("/login", methods=["POST"])
def process_login():
    print("Got here")
    if 'email' not in request.form:
        return "Error: 'email' field is required", 400, {"Access-Control-Allow-Origin": "*"}
    if 'password' not in request.form:
        return "Error: 'passwrod' is required", 400, {"Access-Control-Allow-Origin": "*"}
    db = RealDB('database.db')
    email = request.form['email'].strip()
    password = request.form['password'].strip()
    is_valid = db.validate_password(email, password)
    if is_valid:
        g.session_data["email"] = email
        return "Valid {email}", 200, {"Access-Control-Allow-Origin": "*"}
    else:
        return "Invalid {email}", 401, {"Access-Control-Allow-Origin": "*"}

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


@app.route("/users", methods=["POST"])
def create_a_new_user():
    db = RealDB('database.db')

    email = request.form['email']
    password = request.form['password']

    if 'email' not in request.form:
        return "Error: 'email' field is required", 400, {"Access-Control-Allow-Origin": "*"}
    
    if len(password) < 5:
        return "Error: 'password' must be more than 5 chars", 400, {"Access-Control-Allow-Origin": "*"}

    if not db.checkUserExists(email):
        db.saveUser(email, password)
        return "created", 201, {"Access-Control-Allow-Origin": "*"}
    else:
        return "User already exists", 400

@app.after_request
def after_request_function(response):
    print("AFter request")
    response.headers["Access-Control-Allow-Origin"] = "*" 
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS" 
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization" 
    return response 

@app.before_request
def before_request_function():
    print("BEFORE REQUEST:", request.method)
    if request.method == "OPTIONS":
        return "", 204
    load_session_data()

@app.route("/sessions/settings", methods=["PUT"])
def setFavoriteColor():
    color = request.form["color"]
    g.session_data["fav_color"] = color
    return "Color saved", 200

@app.route("/sessions", methods=["GET"])
def retrieve_session():
    return {
        "id": g.session_id,
        "data": g.session_data
    }

@app.route("/sessions", methods=["DELETE"])
def delete_session():
    if "fav_color" not in g.session_data:
        return "Unauthenticated", 401
    del g.session_data['fav_color']
    return "Deleted", 200

def load_session_data():
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith('Bearer '):
        session_id = auth_header.removeprefix('Bearer ')
    else:
        session_id = None

    if session_id:
        session_data = session_store.get_session_data(session_id)
        print("The session data is ", session_data)

    if session_id == None or session_data == None:
        session_id = session_store.create_session()
        session_data = session_store.get_session_data(session_id)

    g.session_id = session_id
    g.session_data = session_data

    




def run():
    app.run(port=5000, host='0.0.0.0')

if __name__ == "__main__":
    run()