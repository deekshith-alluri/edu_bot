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

    # Logged in - fetch robust DB data
    user_data = db_services.get_user(user) or {}
    response = make_response(render_template("dashboard.html", user=user, user_data=user_data))

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
    
    # Extra data points
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    gender = data.get("gender")
    class_study = data.get("class_study")
    dob = data.get("dob")
    country = data.get("country")
    state = data.get("state")
    school = data.get("school")
    board = data.get("board")
    phone = data.get("phone")

    # --- Validation ---
    if not username or not email or not password:
        return jsonify({"error": "All primary fields are required"}), 400
        
    if not dob or not country or not board or not gender:
        return jsonify({"error": "DOB, Gender, Country, and Board of Education are strictly required."}), 400

    success, message = db_services.create_user(
        username, email, password,
        firstName=firstName, lastName=lastName, gender=gender, class_study=class_study,
        dob=dob, country=country, state=state, school=school, board=board, phone=phone
    )

    if not success:
        if message == "username_exists":
            return jsonify({"error": "Username already taken"}), 409
        if message == "email_exists":
            return jsonify({"error": "Email already registered"}), 409

    return jsonify({"message": "User registered successfully"}), 201

@app.route("/profile")
def profile():
    user, _ = get_current_user()
    if not user:
        return redirect("/authenticate")
    user_data = db_services.get_user(user) or {}
    return render_template('profile.html', user=user, user_data=user_data)

@app.route("/api/user/update", methods=["POST"])
def update_user_profile():
    user, response, error = api_auth_required()
    if error:
        return error
    
    data = request.json
    # Only update what was provided
    db_services.update_user(user, **data)
    
    if not response:
        response = make_response(jsonify({"message": "Profile updated"}))
    else:
        response.data = jsonify({"message": "Profile updated"}).data
        response.content_type = 'application/json'
        
    return response

@app.route("/api/user/delete", methods=["POST"])
def delete_user_account():
    user, response, error = api_auth_required()
    if error:
        return error
        
    db_services.delete_user(user)
    
    res = make_response(jsonify({"message": "Account deleted"}))
    res.set_cookie("access_token", "", expires=0)
    res.set_cookie("refresh_token", "", expires=0)
    return res

@app.route("/logout", methods=["POST"])
def logout():
    response = make_response(redirect("/"))
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)