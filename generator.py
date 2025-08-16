import google.generativeai as genai
import os
import json

# API Key from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_quiz(job_role, num_tech=5, num_hr=3):
    prompt = f"""
    Generate {num_tech} technical and {num_hr} HR interview questions for the role {job_role}.
    Return output strictly in JSON format like this:

    {{
      "questions": [
        {{
          "question": "What is Python?",
          "options": ["Language", "OS", "Database", "Compiler"],
          "answer": "Language"
        }}
      ]
    }}
    """

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    try:
        data = json.loads(response.text)
    except Exception:
        data = {"questions": []}

    return data
