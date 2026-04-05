from flask import Blueprint, request, jsonify
from services.pipeline import handle_query_pipeline #look before execution
from services.pdf_ops import PDFSearchEngine # look for engine.query()
import os
from core.main_pipeline import main_pipe

query_bp = Blueprint("query_bp", __name__, url_prefix="/api")


# ---------- QUERY ROUTE ----------
@query_bp.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    user_query = data.get("query", "")
    age = data.get("age", "Unknown")
    clazz = data.get("class", "Unknown")
    country = data.get("country", "Unknown")
    board = data.get("board_of_edu", "Unknown")
    pdf_path = data.get("pdf_path", "")

    if not user_query:
        return jsonify({"error": "Query is required"}), 400

 
    abs_pdf_path = None
    if pdf_path and len(pdf_path) > 0:
        abs_pdf_path = os.path.abspath(pdf_path)

    try:        
        result = main_pipe(
            query=user_query,
            pdf_path=abs_pdf_path,
            age=age,
            clazz=clazz,
            top_n_sentences=5,
            relevance_threshold=0.1,
            country=country,
            BOE=board
        )
        
        # main_pipe returns a dict compatible with frontend parser, return as JSON
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ---------- PDF UPLOAD ----------
@query_bp.route("/upload", methods=["POST"])
def upload():
    import os
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF allowed"}), 400

    # Process PDF
    upload_dir = "pdf_content"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    file.save(file_path)

    try:
        from services.pdf_ops import PDFSearchEngine
        # Initializing the engine automatically builds and saves the cache
        engine = PDFSearchEngine(file_path)
    except Exception as e:
        print("Caching error:", e)

    response = f"{file.filename} is uploaded successfully! Initiated cache."

    return jsonify({
        "message": f"{file.filename} uploaded successfully",
        "data": response,
        "filename": file.filename
    })