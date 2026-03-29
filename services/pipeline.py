from services.builder import (
    generate_simple_explanation,
    generate_deep_explanation,
    generate_quiz,
    generate_important_points
)
from services.yt_recommendations import recommend_videos

def handle_query_pipeline(query_text, classification_result, age=None, clazz=None, context_text=None):
    """
    Orchestrates the full pipeline based on the classification result.
    context_text: text retrieved from PDFSearchEngine
    Returns a JSON-ready dict.
    """
    response = {
        "query": query_text,
        "classification": classification_result,
        "simple_explanation": None,
        "deep_explanation": None,
        "important_points": None,
        "quiz": None,
        "youtube_recommendations": None
    }

    classified_into = classification_result.get("classified_into", "").lower()

    if classified_into in ["simple", "fact-check"]:
        response["simple_explanation"] = generate_simple_explanation(query=query_text, age=age, clazz=clazz, context_text=context_text)

    elif classified_into == "medium":
        response["deep_explanation"] = generate_deep_explanation(query=query_text, age=age, clazz=clazz, context_text=context_text)

    elif classified_into == "hard":
        response["deep_explanation"] = generate_deep_explanation(query=query_text, age=age, clazz=clazz, context_text=context_text) 
        # context_text required for quiz and key points
        if context_text:
            response["quiz"] = generate_quiz(context_text)
            response["important_points"] = generate_important_points(context_text)
        response["youtube_recommendations"] = recommend_videos(query_text, age, clazz)

    else:
        response["simple_explanation"] = generate_simple_explanation(query_text, age, clazz)

    return response