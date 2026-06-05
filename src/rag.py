import requests

from src.config import (
    NVIDIA_API_KEY,
    BASE_URL,
    MODEL
)

def generate_answer(context, question):

    prompt = f"""
Context:
{context}

Question:
{question}

Answer:
"""

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {

        "model": MODEL,

        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],

        "temperature": 0.3,
        "max_tokens": 512
    }

    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=payload
    )

    try:
        res_json = response.json()
    except Exception as e:
        raise Exception(f"Failed to parse NVIDIA API JSON response: {e}. Raw response: {response.text}")

    if "choices" not in res_json:
        # Extract details or error message if present, otherwise fall back to stringified JSON
        error_details = res_json.get("detail") or res_json.get("error", {}).get("message") or str(res_json)
        raise Exception(f"NVIDIA API Error: {error_details}")

    return res_json["choices"][0]["message"]["content"]