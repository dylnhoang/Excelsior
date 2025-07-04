import os
import pandas as pd
from dotenv import load_dotenv
import openai

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

UPLOAD_DIR = "uploads"

def generate_excel_action(file_id: str, prompt: str):
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File with ID {file_id} not found.")
    
    df = pd.read_excel(file_path)
    headers = df.columns.tolist()
    sample_rows = df.head(3).to_dict(orient="records")

    system_prompt = (
        "You're an intelligent Excel assistant. Given a table and user instruction, "
        "return a clean JSON object that describes what Excel operation to perform.\n"
        "Supported actions: filter, sort, highlight, rename_column, add_column.\n"
        "Example outputs:\n"
        "{'operation': 'filter', 'column': 'Region', 'condition': '==', 'value': 'West'}\n"
        "{'operation': 'sort', 'column': 'Profit', 'order': 'descending'}\n"
        "Respond ONLY with JSON."
    )

    user_prompt = f"""Instruction: {prompt}
    Headers: {headers}
    Sample rows: {sample_rows}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            { "role": "system", "content": system_prompt },
            { "role": "user", "content": user_prompt }
        ]
    )

    action_json = response.choices[0].message.content.strip()

    try:
        return eval(action_json)
    except Exception as e:
        raise ValueError(f"Failed to parse LLM response: {action_json}")