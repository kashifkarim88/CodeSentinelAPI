import requests
from src.config import HF_TOKEN

MODEL_ID = "mrm8488/codebert-base-finetuned-detect-insecure-code"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def analyze_code(code: str):
    # This sends the code to Hugging Face's servers instead of running it locally
    response = requests.post(API_URL, headers=headers, json={"inputs": code})
    
    if response.status_code != 200:
        # Fallback if the API is busy/loading
        return {"label": "LABEL_0", "confidence": 0.0}
        
    results = response.json()
    # The API returns a list of list: [[{'label': '...', 'score': ...}]]
    top_prediction = results[0][0] 
    
    return {
        "label": top_prediction["label"],
        "confidence": round(top_prediction["score"], 4)
    }