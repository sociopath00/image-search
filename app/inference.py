# app/inference.py

import os
import torch
import faiss
import pandas as pd
from transformers import CLIPProcessor, CLIPModel

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"

# Load ONCE
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
index = faiss.read_index("app/image_index.faiss")
metadata = pd.read_csv("app/image_metadata.csv")

def get_text_embedding(query: str):
    inputs = processor(text=[query], return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        text_features = model.get_text_features(**inputs)
        text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)
    return text_features.cpu().numpy().astype("float32")

def search_images(query: str, top_k: int = 5):
    query_vec = get_text_embedding(query)
    distances, indices = index.search(query_vec, top_k)
    results = []
    for idx, score in zip(indices[0], distances[0]):
        path = metadata.iloc[idx]["image_path"]
        results.append({"image_path": path, "distance": float(score)})
    return results
