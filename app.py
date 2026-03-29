from flask import Flask, request, jsonify, redirect, render_template, make_response
from flask_jwt_extended import JWTManager
from datetime import timedelta
from config import _SECRET_KEY_FLASK, _DB_ADDR
from flask_pymongo import PyMongo
from utils.utility_funcs import set_auth_cookies, get_current_user, api_auth_required

# ---------------- APP INIT ----------------
app = Flask(__name__)

# JWT CONFIG
app.config["JWT_SECRET_KEY"] = _SECRET_KEY_FLASK
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token"

app.config["JWT_COOKIE_SECURE"] = False  # ⚠️ True in production (HTTPS)
app.config["JWT_COOKIE_SAMESITE"] = "Lax"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)

# MongoDB (future use)
app.config["MONGO_URI"] = _DB_ADDR
# mongo = PyMongo(app) # uncomment it after fixing setting-up the DB



# ---------------- UI ROUTES ----------------

@app.route("/")
def home():
    user, needs_refresh = get_current_user()

    if not user:
        return render_template("welcome.html")

    # Logged in
    response = make_response(render_template("dashboard.html", user=user))

    # Silent refresh
    if needs_refresh:
        response = set_auth_cookies(response, user)

    return response


# ---------------- AUTH ROUTES ----------------

@app.route("/authenticate", methods=["POST", "GET"])
def authenticate():

    if request.method == "GET":
        return render_template("authenticate.html")
    
    if request.method =='POST':
        data = request.json
        username = data.get("username")
        password = data.get("password")

        # Dummy auth (replace with MongoDB later)
        if username == "admin" and password == "admin":
            response = jsonify({"message": "Login successful"})
            response = set_auth_cookies(response, username)
            return response

    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/logout")
def logout():
    response = redirect("/")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


# ---------------- API ROUTES ----------------

@app.route("/api/query", methods=["POST"])
def api_query():

    user, refresh_response, error = api_auth_required()

    if error:
        return error

    data = request.json
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query required"}), 400

    # Plug your AI pipeline here
    result = {
        "query": query,
        "response": f"Processed for {user}"
    }

    # Attach refreshed cookies if needed
    if refresh_response:
        refresh_response.set_data(jsonify(result).get_data())
        return refresh_response

    return jsonify(result)


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)