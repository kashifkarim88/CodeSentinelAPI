import requests
import json
from src.config import OPENROUTER_API_KEY, OPENROUTER_MODEL

def generate_secure_fix(code: str, confidence: float) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # OpenRouter strictly requires these headers to avoid the 401 cookie error
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000", # Required for OpenRouter identity
        "X-Title": "Code Sentinel API"
    }

    prompt = f"""
    You are a senior security engineer. Fix this INSECURE code.
    Respond ONLY with a valid JSON object.
    
    JSON format:
    {{
      "vulnerability_type": "",
      "cwe_id": "",
      "explanation": "",
      "attack_example": "",
      "secure_code": ""
    }}

    Code to fix:
    {code}
    """

    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are a secure coding expert. Output JSON only."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
        
        # This will catch 401, 403, 500 errors immediately
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
        
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err.response.text}")
        raise Exception(f"OpenRouter Auth Error: {err.response.status_code}")
    except Exception as e:
        print(f"LLM Error: {e}")
        raise e