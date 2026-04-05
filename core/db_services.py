from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

mongo = PyMongo()
# ---------------- INIT ----------------

def init_db(app):
    mongo.init_app(app)


# ---------------- COLLECTIONS ----------------

def get_users_collection():
    return mongo.cx["admin"]["users"]


def get_appdata_collection():
    return mongo.cx["locals"]["appdata"]


# ---------------- USER FUNCTIONS ----------------

def create_user(username, email, password, **kwargs):
    users = get_users_collection()

    if users.find_one({"username": username}):
        return False, "username_exists"

    if users.find_one({"email": email}):
        return False, "email_exists"

    hashed_password = generate_password_hash(password)

    user_doc = {
        "username": username,
        "email": email,
        "password": hashed_password
    }
    # Update with extra demographic variables
    user_doc.update(kwargs)

    users.insert_one(user_doc)

    return True, "User created"

def authenticate_user(username, password):
    users = get_users_collection()

    user = users.find_one({"username": username})

    if not user:
        return False, "User not found"

    if not check_password_hash(user["password"], password):
        return False, "Invalid password"

    return True, user

def get_user(username):
    users = get_users_collection()
    user = users.find_one({"username": username}, {"_id": 0, "password": 0})
    return user

def update_user(username, **kwargs):
    users = get_users_collection()
    users.update_one({"username": username}, {"$set": kwargs})
    return True

def delete_user(username):
    users = get_users_collection()
    users.delete_one({"username": username})
    return True


# ---------------- APP DATA FUNCTIONS ----------------

def save_user_query(username, query, response):
    appdata = get_appdata_collection()

    appdata.insert_one({
        "username": username,
        "query": query,
        "response": response
    })


def get_user_history(username, limit=10):
    appdata = get_appdata_collection()

    history = list(
        appdata.find({"username": username})
        .sort("_id", -1)
        .limit(limit)
    )

    return history