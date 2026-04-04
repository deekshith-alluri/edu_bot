from flask import Blueprint, request, jsonify
from services.pipeline import handle_query_pipeline #look before execution
from services.pdf_ops import PDFSearchEngine # look for engine.query()

query_bp = Blueprint("query_bp", __name__, url_prefix="/api")


# ---------- QUERY ROUTE ----------
@query_bp.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    user_query = data.get("query")

    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    result=f'Received Data: {user_query}'
    print(result)
    # result = run_pipeline(user_query)

    return jsonify(result)


# ---------- PDF UPLOAD ----------
@query_bp.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF allowed"}), 400

    # Process PDF
    # response = handle_pdf_upload(file)

    response = f"{file.filename} is uploaded successfully!"

    return jsonify({
        "message": f"{file.filename} uploaded successfully",
        "data": response
    })