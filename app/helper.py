import os
import torch
import faiss
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm
from transformers import CLIPProcessor, CLIPModel

# required for MacOs
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Prevent OpenMP crashes on macOS

IMAGE_FOLDER = "images/"
INDEX_OUTPUT = "image_index.faiss"
METADATA_OUTPUT = "image_metadata.csv"

# MODEL SETUP 
device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# EMBEDDING FUNCTION 
def get_image_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
        image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
    return image_features.cpu().numpy().squeeze()


def build_faiss_index():
    image_files = [
        f for f in os.listdir(IMAGE_FOLDER)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    image_embeddings = []
    image_paths = []

    for img_file in tqdm(image_files, desc="Embedding Images"):
        img_path = os.path.join(IMAGE_FOLDER, img_file)
        try:
            embedding = get_image_embedding(img_path)
            image_embeddings.append(embedding)
            image_paths.append(img_path)
        except Exception as e:
            print(f"Failed to process {img_file}: {e}")

    # Convert to NumPy matrix
    embedding_matrix = np.vstack(image_embeddings).astype("float32")

    # Build FAISS index
    dim = embedding_matrix.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embedding_matrix)

    # Save outputs
    faiss.write_index(index, INDEX_OUTPUT)
    pd.DataFrame({"image_path": image_paths}).to_csv(METADATA_OUTPUT, index=False)
    print(f"Saved index to {INDEX_OUTPUT} and metadata to {METADATA_OUTPUT}")

if __name__ == "__main__":
    build_faiss_index()
