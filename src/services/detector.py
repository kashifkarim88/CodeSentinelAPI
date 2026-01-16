import requests
from src.config import HF_TOKEN

API_URL = "https://api-inference.huggingface.co/models/mrm8488/codebert-base-finetuned-detect-insecure-code"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def analyze_code(code: str):
    # 1. Define the payload FIRST
    payload = {
        "inputs": code, 
        "options": {"wait_for_model": True}
    }
    
    try:
        # 2. Now you can use 'payload' because it was defined above
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        
        results = response.json()
        
        # Debug print to help us fix the "Confidence: 0" issue later
        print(f"DEBUG - Detector Response: {results}")

        if isinstance(results, list) and len(results) > 0:
            # CodeBERT mapping
            data = results[0]
            if isinstance(data, list): data = data[0]
            
            return {
                "label": data.get("label"),
                "confidence": round(data.get("score", 0) * 100, 2)
            }

    except Exception as e:
        print(f"Detector Error: {e}")
    
    return {"label": "LABEL_0", "confidence": 0.0}