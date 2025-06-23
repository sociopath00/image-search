# app/main.py

from fastapi import FastAPI, Query
from pydantic import BaseModel
from app.inference import search_images
from app.explain import generate_explanation

app = FastAPI()

class SearchRequest(BaseModel):
    query: str

class ExplanationRequest(BaseModel):
    image_path: str
    query: str

@app.post("/search")
def search_api(request: SearchRequest):
    results = search_images(request.query)
    return results

@app.post("/explain")
def explain_api(request: ExplanationRequest):
    # explanation = generate_explanation(request.image_path, request.query)
    explanation = "Not Found"
    return {"explanation": explanation}
