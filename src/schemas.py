from pydantic import BaseModel

class CodeRequest(BaseModel):
    code: str

class AnalysisResponse(BaseModel):
    vulnerability_type: str
    cwe_id: str
    explanation: str
    attack_example: str
    secure_code: str
    confidence: float
    owasp_category: str
    diff: str