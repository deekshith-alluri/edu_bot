from services.pdf_ops import PDFSearchEngine
from services.query_classifier import classify_query
from services.pipeline import handle_query_pipeline

# ---------------- CORE PIPELINE ----------------
def main_pipe(query, pdf_path=None, age=None, clazz=None, top_n_sentences=5, relevance_threshold=0.1, country="India", BOE="TG SCERT or TG BIE"):
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
    print(f"Result: {result}")  
    return result

if __name__ == "__main__":
    while True:
        q=str(input("enter query or 'e' to exit:\t"))
        if q == 'e':
            break
        pdf_path="C:/Users/Nandini/Desktop/edu_bot/data/cms.pdf"
        age = "20"
        clazz="UG 1st Year"
        BOE = "Osmania University"
        main_pipe(query=q, pdf_path=pdf_path, age=age, clazz=clazz, BOE=BOE)