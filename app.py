from flask import Flask, request, jsonify, redirect, render_template, make_response
from flask_jwt_extended import JWTManager
from datetime import timedelta
from config import _SECRET_KEY_FLASK, _DB_ADDR
from utils.utility_funcs import set_auth_cookies, get_current_user, api_auth_required
from core import db_services
from apis.query import query_bp

# ---------------- APP INIT ----------------
app = Flask(__name__)
app.register_blueprint(query_bp)

# JWT CONFIG
app.config["JWT_SECRET_KEY"] = _SECRET_KEY_FLASK
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token"

app.config["JWT_COOKIE_SECURE"] = False  # True in production (HTTPS)
app.config["JWT_COOKIE_SAMESITE"] = "Lax"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)

# database: MongoDB
app.config['MONGO_URI'] = _DB_ADDR
db_services.init_db(app)


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

    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    success, result = db_services.authenticate_user(username, password)

    if not success:
        # IMPORTANT: don't reveal whether username or password is wrong
        return jsonify({"error": "Login failed"}), 401

    response = jsonify({"message": "Login successful"})
    response = set_auth_cookies(response, username)

    return response

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # --- Validation ---
    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    success, message = db_services.create_user(username, email, password)

    if not success:
        if message == "username_exists":
            return jsonify({"error": "Username already taken"}), 409
        if message == "email_exists":
            return jsonify({"error": "Email already registered"}), 409

    return jsonify({"message": "User registered successfully"}), 201

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/logout", methods=["POST"])
def logout():
    response = make_response(redirect("/"))
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
    app.run(debug=True, port=5000)