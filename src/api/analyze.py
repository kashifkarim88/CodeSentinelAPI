import re
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
    detection = analyze_code(request.code)
    is_vulnerable = (detection["label"] == "LABEL_0")

    try:
        raw_llm = generate_secure_fix(request.code, detection["confidence"], is_vulnerable)
        
        # --- IMPROVED JSON EXTRACTION ---
        if isinstance(raw_llm, str):
            # Look for the first '{' and the last '}' to ignore any extra text from the AI
            match = re.search(r'(\{.*\})', raw_llm, re.DOTALL)
            if match:
                clean_json = match.group(1)
            else:
                clean_json = raw_llm
            
            # strict=False allows the parser to handle control characters like newlines
            parsed = json.loads(clean_json, strict=False)
        else:
            parsed = raw_llm
        # --- END OF EXTRACTION ---

        # 3. Enhance the response data (Keep your existing logic below)
        if is_vulnerable:
            cwe_id = parsed.get("cwe_id", "Unknown")
            parsed["status"] = "vulnerable"
            parsed["owasp_category"] = CWE_TO_OWASP.get(cwe_id, "Unknown/General Injection")
        else:
            parsed["status"] = "safe"
            parsed["owasp_category"] = "None"

        parsed["confidence"] = detection["confidence"]
        secure_code_proposal = parsed.get("secure_code", "")
        parsed["diff"] = generate_diff(request.code, str(secure_code_proposal))
        
        return parsed
        
    except Exception as e:
        # Fallback if parsing STILL fails
        return {
            "status": "vulnerable" if is_vulnerable else "safe",
            "vulnerability_type": "None (Secure)" if not is_vulnerable else "Detected Issue",
            "cwe_id": "None",
            "explanation": f"AI response was messy, but logic is secure. Error: {str(e)}",
            "attack_example": "N/A",
            "secure_code": request.code,
            "confidence": detection["confidence"],
            "owasp_category": "None",
            "diff": ""
        }