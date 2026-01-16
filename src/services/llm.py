import requests
import json
from src.config import OPENROUTER_API_KEY, OPENROUTER_MODEL

def generate_secure_fix(code: str, confidence: float, is_vulnerable: bool) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://codesentinel.render.com",
        "X-Title": "Code Sentinel API"
    }

    # IMPORTANT: We use a block string format for the code inside the prompt
    if is_vulnerable:
        system_role = "You are a Cyber Security Expert. You MUST respond ONLY with a valid JSON object."
        prompt = f"""Analyze this VULNERABLE code. 
Return a JSON object with: 
"vulnerability_type", "cwe_id", "explanation", "attack_example", and "secure_code".
Ensure "secure_code" is a valid string with properly escaped newlines and quotes.

CODE TO ANALYZE:
{code}
"""
    else:
        system_role = "You are a Senior Python Developer. You MUST respond ONLY with a valid JSON object."
        prompt = f"""Analyze this SECURE code for PEP8 and performance optimizations.
Return a JSON object with:
"vulnerability_type": "None (Secure)", "cwe_id": "None", "explanation", "attack_example": "N/A", "secure_code".

CODE TO OPTIMIZE:
{code}
"""

    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1 # Keep it low to prevent the AI from "talking" too much
    }

    try:
        # We use json.dumps(data) to ensure the entire request is valid JSON
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        raise Exception(f"LLM Connection Error: {str(e)}")