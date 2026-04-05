import re
import json
from google import genai
from google.genai import types
from config import _MODEL_API_KEY

# Initialize client (make sure your GOOGLE_API_KEY is set)
client = genai.Client(api_key=_MODEL_API_KEY)


# Main funtion
def classify_query(query: str, age: int, clazz: str, country: str, BOE: str) -> dict:
    """
        Sends the query to Gemini Flash 2.5 to classify difficulty.
        Returns: {'classified_into': 'simple' OR 'hard'}
    """
    instruction = f"""
        You are a query classifier.
        Given a user query, classify whether the query is 'greeting', 'simple', 
        or 'medium' or 'hard' or 'fact-check' for a {age}-year-old student in {clazz} class studying in {BOE} in {country}. 

        Respond ONLY with a JSON object in this exact format:
        {{"classified_into":"greeting" OR "classified_into":"simple" OR "classified_into":"medium" OR "classified_into":"hard" OR "classified_into":"fact-check"}}

        Use ```json ...``` markdown formatting.

        Query: "{query}"
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=instruction,
        config=types.GenerateContentConfig(
            temperature=0.0,
            candidate_count=1
        )
    )

    raw_text = response.text.strip()

    # --- Extract JSON inside ```json ... ``` ---
    match = re.search(r"```json\s*(\{.*?\})\s*```", raw_text, re.DOTALL)

    if match:
        json_text = match.group(1)
        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            return {"classified_into": "unknown"}
    else:
        # fallback if not in code block
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            return {"classified_into": "unknown"}

    


# Example usage
if __name__ == "__main__":
    while True:
        q = str(input("Ask anything or 'e'=>exit :\t"))
        if q == 'e':
            break
        result = classify_query(q, age=20, clazz="UG 1st Yr", country="India", BOE="Osmania University")
        print(result)
