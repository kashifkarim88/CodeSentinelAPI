from fastapi import APIRouter, HTTPException
import json
from src.schemas import CodeRequest
from src.services.detector import analyze_code
from src.services.llm import generate_secure_fix
from src.services.diff import generate_diff

router = APIRouter()

CWE_TO_OWASP = {"CWE-89": "A03: Injection", "CWE-79": "A07: XSS"}

@router.post("/analyze")
def analyze(request: CodeRequest):
    detection = analyze_code(request.code)

    # CHECK THE LABEL CAREFULLY:
    # If the model says LABEL_1, it means the code is SECURE/SAFE.
    if detection["label"] == "LABEL_1": 
        return {
            "status": "safe",
            "confidence": detection["confidence"],
            "vulnerability_type": "None",
            "secure_code": request.code
        }

    # If we reach here, it means it is LABEL_0 (INSECURE)
    # Now we call the LLM to get the fix
    try:
        raw_llm = generate_secure_fix(request.code, detection["confidence"])
        
        # OpenRouter sometimes wraps JSON in markdown blocks like ```json ... ```
        # We need to clean that so json.loads doesn't fail
        clean_json = raw_llm.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(clean_json)
        
        cwe_id = parsed.get("cwe_id", "Unknown")
        parsed["status"] = "vulnerable"
        parsed["confidence"] = detection["confidence"]
        parsed["owasp_category"] = CWE_TO_OWASP.get(cwe_id, "Unknown")
        parsed["diff"] = generate_diff(request.code, parsed.get("secure_code", ""))
        
        return parsed
        
    except Exception as e:
        # If LLM fails, at least return the detection info
        return {
            "status": "vulnerable",
            "confidence": detection["confidence"],
            "error": f"LLM Fix failed: {str(e)}"
        }