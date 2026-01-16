import requests
import json
from src.config import OPENROUTER_API_KEY, OPENROUTER_MODEL

def generate_secure_fix(code: str, confidence: float, is_vulnerable: bool) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://codesentinel.render.com", # Updated for production
        "X-Title": "Code Sentinel API"
    }

    # --- DYNAMIC PROMPT LOGIC ---
    if is_vulnerable:
        # SECURITY MODE
        system_role = "You are a secure coding expert. Output JSON only."
# Inside generate_secure_fix when is_vulnerable is False:
        prompt = f"""
        You are a Senior Python Developer. This code has been verified as SECURITY SAFE.
        Do NOT invent vulnerabilities. Instead, focus on:
        1. PEP 8 formatting.
        2. Type hinting.
        3. Logical efficiency.

        Return JSON:
        {{
        "vulnerability_type": "None (Verified Safe)",
        "cwe_id": "None",
        "explanation": "Code is secure. Refactored for standard Python 3 idioms.",
        "attack_example": "N/A",
        "secure_code": "..."
        }}
        CODE: {code}
        """
    else:
        # ASSISTANT MODE
        system_role = "You are a senior Python developer and code reviewer. Output JSON only."
        prompt = f"""
        You are a senior developer. This code is SECURITY SAFE (Confidence: {confidence}%).
        Perform a code review: check for syntax errors, PEP 8 compliance, and refactor for performance.
        
        Respond ONLY with a valid JSON object.
        JSON format:
        {{
          "vulnerability_type": "None (Secure)",
          "cwe_id": "None",
          "explanation": "Summary of refactoring and optimizations made",
          "attack_example": "N/A",
          "secure_code": "The optimized/clean version of the code"
        }}

        Code to refactor:
        {code}
        """

    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
        
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err.response.text}")
        raise Exception(f"OpenRouter Auth Error: {err.response.status_code}")
    except Exception as e:
        print(f"LLM Error: {e}")
        raise e