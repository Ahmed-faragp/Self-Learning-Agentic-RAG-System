
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key)


def classify_intent(query):
    prompt = f"""Classify the following user question into one of two categories: "explanation" or "coding".
    Question: {query}
    - If the user is asking for a code implementation, return only one word  "coding"
    - If the user is asking for an explanation of a concept or code, return only one word  "explanation"
    """ 
    response = client.chat.completions.create(
        model="meta-llama/llama-3-8b-instruct", 
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    intent = response.choices[0].message.content.strip().lower()
    if intent not in ["explanation", "coding"]:
        intent = "explanation"  # default to explanation if unclear
    return intent

    
       
# classification = classify_intent("How do I reverse a linked list in Python?")
# print("Classified intent:", classification)