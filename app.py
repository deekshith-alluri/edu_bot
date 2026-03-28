from flask import Flask, request, jsonify, redirect, render_template
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from config import _SECRET_KEY_FLASK
from services.pdf_ops import PDFSearchEngine
from services.query_classifier import classify_query
from services.pipeline import handle_query_pipeline

app = Flask(__name__)

# JWT Config
app.config["JWT_SECRET_KEY"] =  _SECRET_KEY_FLASK # change later
jwt = JWTManager(app)

# ---------------- CORE PIPELINE ----------------
def main(
    query,
    pdf_path=None,
    age=None,
    clazz=None,
    top_n_sentences=5,
    relevance_threshold=0.1,
    country="India",
    BOE="TG SCERT or TG BIE"
):
    context_text = None
    top_sentences = []
    max_score = 0.0

    if pdf_path:
        search_engine = PDFSearchEngine(pdf_path)
        top_results = search_engine.query(query, top_n=top_n_sentences)

        if top_results and isinstance(top_results[0], tuple):
            top_sentences = [t[0] for t in top_results]
            top_scores = [t[1] for t in top_results]
        else:
            top_sentences = top_results or []
            top_scores = [0.0] * len(top_sentences)

        max_score = max(top_scores) if top_scores else 0.0

        print(f"Max similarity score: {max_score}")

        if not top_sentences or max_score < relevance_threshold:
            return {
                "query": query,
                "classification": None,
                "confidence_score": round(max_score, 3),
                "message": "Cannot answer this query from the provided PDF.",
                "source_context": [],
                "simple_explanation": None,
                "deep_explanation": None,
                "important_points": None,
                "quiz": None,
                "youtube_recommendations": None
            }

        context_text = " ".join(top_sentences)

    classification_result = classify_query(
        query,
        age=age,
        clazz=clazz,
        country=country,
        BOE=BOE
    )

    result = handle_query_pipeline(
        query_text=query,
        classification_result=classification_result,
        age=age,
        clazz=clazz,
        context_text=context_text
    )

    result["classification"] = classification_result
    result["confidence_score"] = round(max_score, 3) if pdf_path else None
    result["source_context"] = top_sentences if pdf_path else None

    return result



# ---------------- HELPERS ----------------

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "message": "Token is missing",
        "redirect": "/login"
    }), 401


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "message": "Token has expired",
        "redirect": "/login"
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "message": "Invalid token",
        "redirect": "/login"
    }), 401

# ---------------- AUTH ROUTES ----------------

@app.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    # Dummy auth
    if username == "admin" and password == "admin":
        access_token = create_access_token(identity=username)
        return jsonify({
            "message": "Login successful",
            "access_token": access_token
        })

    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/welcome")
def welcome():
    return jsonify({"message": "Welcome to the EduBot API!"})


# ---------------- PROTECTED ROUTES ----------------

@app.route("/profile")
@jwt_required()
def profile():
    current_user = get_jwt_identity()

    return jsonify({
        "username": current_user,
        "role": "student",
        "preferences": {
            "class": "10th grade",
            "country": "India"
        }
    })


@app.route("/dashboard", methods=["POST"])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()

    data = request.json

    query = data.get("query")
    pdf_path = data.get("pdf_path")
    age = data.get("age")
    clazz = data.get("class")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    result = main(
        query=query,
        pdf_path=pdf_path,
        age=age,
        clazz=clazz
    )

    result["user"] = current_user  # optional tagging

    return jsonify(result)


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)