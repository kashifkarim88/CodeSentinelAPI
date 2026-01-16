from fastapi import APIRouter, HTTPException
import json
from src.schemas import CodeRequest
from src.services.detector import analyze_code
from src.services.llm import generate_secure_fix
from src.services.diff import generate_diff

router = APIRouter()

# Mapping CWEs to OWASP for better reporting
CWE_TO_OWASP = {
    "CWE-89": "A03:2021-Injection",
    "CWE-79": "A07:2021-Identification and Authentication Failures",
    "CWE-22": "A01:2021-Broken Access Control"
}

@router.post("/analyze")
def analyze(request: CodeRequest):
    # 1. Run the local AI Detector
    detection = analyze_code(request.code)
    
    # In your current logic, you noted LABEL_1 is SECURE and LABEL_0 is INSECURE
    is_vulnerable = (detection["label"] == "LABEL_1")

    try:
        # 2. Call the LLM
        raw_llm = generate_secure_fix(request.code, detection["confidence"], is_vulnerable)
        
        # Ensure we are dealing with a string before cleaning
        if isinstance(raw_llm, dict):
            # If llm.py accidentally returned a dict, convert it or handle it
            parsed = raw_llm
        else:
            clean_json = str(raw_llm).replace("```json", "").replace("```", "").strip()
            parsed = json.loads(clean_json, strict=False)
        
        # 3. Enhance the response data
        if is_vulnerable:
            cwe_id = parsed.get("cwe_id", "Unknown")
            parsed["status"] = "vulnerable"
            parsed["owasp_category"] = CWE_TO_OWASP.get(cwe_id, "Unknown/General Injection")
        else:
            parsed["status"] = "safe"
            parsed["owasp_category"] = "None"

        # Common fields
        parsed["confidence"] = detection["confidence"]
        
        # SAFETY CHECK for Diff: Ensure secure_code is a string
        secure_code_proposal = parsed.get("secure_code", "")
        if isinstance(secure_code_proposal, str):
            parsed["diff"] = generate_diff(request.code, secure_code_proposal)
        else:
            parsed["diff"] = "Could not generate diff: secure_code is not a string"
        
        return parsed
        
    except Exception as e:
        return {
            "status": "vulnerable" if is_vulnerable else "safe",
            "confidence": detection["confidence"],
            "error": f"LLM Analysis failed: {str(e)}",
            "secure_code": request.code # Return original code as fallback
        }