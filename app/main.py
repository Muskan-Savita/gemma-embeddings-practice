from fastapi import FastAPI
from pydantic import BaseModel
from app.detection import detect, sanitize

app = FastAPI(title="PII Sanitizer API")

class TextIn(BaseModel):
    text: str

class SanitizeOut(BaseModel):
    sanitized: str
    findings: list[str]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/sanitize", response_model=SanitizeOut)
def sanitize_endpoint(body: TextIn):
    findings = [label for label, _, _ in detect(body.text)]
    return SanitizeOut(sanitized=sanitize(body.text), findings=findings)
