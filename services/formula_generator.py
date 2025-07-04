import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_excel_formula(prompt: str) -> dict:
    system_msg = """
    You are an AI assistant for generating structured Excel modification instructions.

    Respond ONLY in JSON like the following:
    - For a sort: {"operation": "sort", "column": "Status", "order": "asc"}
    - For a filter: {"operation": "filter", "column": "Profit", "condition": {"operator": ">", "value": 300}}
    - For an update: {"operation": "update", "column": "Status", "value": "Complete"}

    Do NOT add explanations. Do NOT include markdown.
    Only return valid JSON.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content.strip()
        print("[LLM Raw Output]", content)
        return json.loads(content)
    except Exception as e:
        print("[LLM ERROR]", str(e))
        return {"error": "Could not parse LLM response"}