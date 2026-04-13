import os
import re
import json
from google import genai
from google.genai import types
from config import _MODEL_API_KEY

# Initialize the client
client = genai.Client(api_key=_MODEL_API_KEY)


# Gemini Call Function --------
def call_gemini(prompt: str, temperature: float = 0.0) -> str:
    """
    Generic function to call Gemini 2.5 Flash with any prompt.
    Returns the model's raw text.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            candidate_count=1
        )
    )

    return response.text.strip()


# extract content from markdown i.e., response from the LLM
def extract_json_from_md(raw_text: str) -> dict | list:
    """
    Extract JSON inside ```json ... ``` or fallback to raw text.
    Supports JSON object or JSON array.
    Returns Python dict or list.
    """
    match = re.search(r"```json\s*(\{.*?\}|\[.*?\])\s*```", raw_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return {"error": "json_decode_failed"}
    else:
        # fallback if no code block, try parsing raw text
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            return {"error": "json_not_found"}


# SIMPLE Explanation  --------
def generate_simple_explanation(query: str, age: int = None, clazz: str = None, context_text=None) -> str:
    """
    Generates a short 2-3 line explanation for the query.
    """
    prompt = f"""
    You are an educational assistant for "Study Spark".
    Explain the following query in 2-3 simple sentences.
    Query: "{query}"
    Try Using HTML not MARKDOWN.
    Respond ONLY with a JSON object in this exact format:
    {{"answer":"YOUR_ANSWER_HERE"}}
    """
    if context_text:
        prompt+=f"from context : {context_text}"

    if age and clazz:
        prompt += f"\nThis explanation is for a {age}-year-old student in {clazz} class in appropriate tone so that they can understand."

    return extract_json_from_md(call_gemini(prompt))


# DEEP Explanation  ----------
def generate_deep_explanation(query: str, age: int = None, clazz: str = None, context_text=None) -> str:
    """
    Generates a detailed explanation for the query.
    """
    prompt = f"""
    You are an educational assistant for Study Spark.
    Provide a deep and thorough explanation of the following query.
    Query: "{query}"
    Try Using HTML not MARKDOWN.
    Respond ONLY with a JSON object in this exact format:
    {{"answer":"YOUR_ANSWER_HERE"}}
    """
    if context_text:
        prompt+=f"from context : {context_text}"

    if age and clazz:
        prompt += f"\nThis explanation is for a {age}-year-old student in {clazz} class in appropriate tone so that they can understand."

    return extract_json_from_md(call_gemini(prompt))


# QUIZ Builders --------------
def generate_quiz(context: str = None, query: str = None, age: int = None, country: str = None, clazz: str = None, num_questions: int = 4) -> list:
    """
    Generates a quiz from the given context, or falls back to using query, age, class, and country if context is absent.
    Returns a list of dictionaries in the form:
    {"question": "...", "options": [...], "correct_option": "x"}
    """
    prompt = f"""
        You are an educational assistant for Study Spark.
        Generate {num_questions} multiple-choice questions.
        Each question must have 4 options.
        Respond ONLY with a JSON array in this exact format:
        TRY USING HTML NOT MARKDOWN.
        [
        {{"question":"...", "options":["...","...","...","..."], "correct_option":"x"}},
        ...
        ]
    """

    if context:
        prompt += f"\nBased ONLY on the following context:\n{context}\n"
    else:
        prompt += f"\nBased on the topic of the query: '{query}'\n"
        if age and clazz:
            prompt += f"Tailor the difficulty for a {age}-year-old student in {clazz} class."
        if country:
            prompt += f" Consider the educational standards and common phrasing in {country}."

    raw_text = call_gemini(prompt)

    # Extract JSON inside ```json ... ``` if present
    quiz_json = extract_json_from_md(raw_text)

    # If extraction fails, return empty list
    if isinstance(quiz_json, list):
        return quiz_json
    else:
        return []


# Important points to remember
def generate_important_points(topic_or_context: str = None, query: str = None, age: int = None, country: str = None, clazz: str = None) -> list:
    """
    Generates important points, formulas, or exam-focused notes for a topic.
    Returns a list of strings in JSON array format.
    """
    prompt = f"""
    You are an educational assistant.
    List the important points a student should remember for exams regarding this topic.
    Include key formulas, concepts, or rules in bullet-point style.
    
    TRY TO USE HTML NOT MARKDOWN like lists <li> OR <ul>. 
    Respond ONLY with a JSON array of strings, like:
    ["Point-1", "Point-2", "Point-3", ...]
    """

    if topic_or_context:
        prompt += f"\nBased ONLY on the following Context:\n{topic_or_context}\n"
    else:
        prompt += f"\nBased on the topic of the query: '{query}'\n"
        if age and clazz:
            prompt += f"Tailor the important points for a {age}-year-old student in {clazz} class."
        if country:
            prompt += f" Consider the educational curriculum typically taught in {country}."

    raw_text = call_gemini(prompt)
    points_json = extract_json_from_md(raw_text)

    # Ensure we always return a list
    if isinstance(points_json, list):
        return points_json
    else:
        return []

# -------- Example Usage --------
if __name__ == "__main__":
    # query_text = "Explain the process of Phothosynthesis"

    # simple_ans = generate_simple_explanation(query_text, age=15, clazz="10th grade")
    # print("\n--- Simple Explanation ---\n", simple_ans)

    # deep_ans = generate_deep_explanation(query_text, age=15, clazz="10th grade")
    # print("\n--- Deep Explanation ---\n", deep_ans)
    

    # context = str(input("Enter Context :\t"))
    # quiz_json = generate_quiz(context=context)
    # print(quiz_json)

    topic = str(input("Enter your choice of toppic to build IMP Points :\t"))
    result=generate_important_points(topic_or_context=topic)
    print(result)