from flask import Flask, jsonify, request, g
app = Flask(__name__)
from passlib.hash import bcrypt
from session_store import SessionStore

session_store = SessionStore()

def load_session_data():
    auth_header  = request.headers.get("Authorization")
    #dont forget space after Bearer
    if auth_header and auth_header.startswith('Bearer '):
        session_id = auth_header.removeprefix('Bearer ')
    else:
        session_id = None

    if session_id:
        #load the data
        session_data = session_store.get_session_data(session_id)
        print('the session data:', session_data)

    #if the session id is either missing or session data is invalid
    if session_id == None or session_data == None:
        #create a new session
        session_id = session_store.create_session()
        #load the session with the new session ID
        session_data = session_store.get_session_data(session_id)

    #this will save both into the global scope
    g.session_id = session_id
    g.session_data = session_data
    print("session ID:", g.session_id)
    print("session data:", g.session_data)
    

@app.before_request
def before_request_func():
    print(f"Processing {request.method} request for {request.url}")
    if request.method == "OPTIONS":
        #app is an instance of flask
        response = app.response_class("", status=204)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
    load_session_data()

@app.after_request
def after_request_func(response):
    # print("session ID:", g.session_id)
    # print("session data:", g.session_data)
    #set a cookie
    # response.set_cookie("session_id", g.session_id, samesite="None", secure=True)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

@app.route("/sessions/settings", methods=["PUT"])
def setFavoriteColor():
    print("The reqeust data is ", request.form)
    color = request.form["color"]
    g.session_data["fav_color"] = color
    return "Color Saved", 200, {"Access-Control-Allow-Origin" : "*"}

@app.route("/sessions", methods=["GET"])
def retrieve_session():
    print("Made it to retreive session()")
    return {
        "id" : g.session_id,
        "data" : g.session_data
    }

@app.route("/sessions", methods=["DELETE"])
def logout_user():
    print("Session Data at logout:", g.session_data)
    if "fav_color" not in g.session_data:
        return "Unauthenticated", 401

    del g.session_data["fav_color"]
    return "Deleted", 200, {"Access-Control-Allow-Origin" : "*"}

def run():
    app.run(port=8080, host='0.0.0.0')

if __name__ == '__main__':
    run()
