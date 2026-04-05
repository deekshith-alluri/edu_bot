from services.builder import (
    generate_simple_explanation,
    generate_deep_explanation,
    generate_quiz,
    generate_important_points
)
from services.yt_recommendations import recommend_videos

def handle_query_pipeline(query_text, classification_result, age=None, clazz=None, context_text=None, country=None):
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

    if classified_into == "greeting":
        response["simple_explanation"] = {"answer": "Hey there! 👋 What would you like to learn today?"}

    elif classified_into in ["simple", "fact-check"]:
        response["simple_explanation"] = generate_simple_explanation(query=query_text, age=age, clazz=clazz, context_text=context_text)

    elif classified_into == "medium":
        response["deep_explanation"] = generate_deep_explanation(query=query_text, age=age, clazz=clazz, context_text=context_text)

    elif classified_into == "hard":
        response["deep_explanation"] = generate_deep_explanation(query=query_text, age=age, clazz=clazz, context_text=context_text) 
        
        # Always generate quiz and key points for 'hard' queries
        if context_text:
            response["quiz"] = generate_quiz(context=context_text)
            response["important_points"] = generate_important_points(topic_or_context=context_text)
        else:
            response["quiz"] = generate_quiz(query=query_text, age=age, country=country, clazz=clazz)
            response["important_points"] = generate_important_points(query=query_text, age=age, country=country, clazz=clazz)
            
        response["youtube_recommendations"] = recommend_videos(query_text, age, clazz)

    else:
        response["simple_explanation"] = generate_simple_explanation(query_text, age, clazz)

    return response