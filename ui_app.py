import streamlit as st
import requests
from PIL import Image
import os

FASTAPI_URL = "http://localhost:8000"  # FastAPI backend

st.set_page_config(page_title="Visual Search", layout="wide")
st.title("Visual Search for Image Database")

query = st.text_input("Enter your search query:", placeholder="e.g. a dog on a beach")

if st.button("Search") and query:
    with st.spinner("Calling backend..."):
        res = requests.post(f"{FASTAPI_URL}/search", json={"query": query})
        if res.status_code != 200:
            st.error("Failed to fetch search results.")
            st.stop()
        results = res.json()

    for i, result in enumerate(results):
        col1, col2 = st.columns([1, 2])

        with col1:
            image = Image.open(os.path.join("app", result["image_path"])).convert("RGB")
            st.image(image, caption=f"Rank {i+1}", width=250)

        with col2:
            st.markdown(f"**Image Path:** `{result['image_path']}`")
            st.markdown(f"**Distance:** `{result['distance']:.4f}`")

            with st.spinner("Explaining..."):
                ex_res = requests.post(
                    f"{FASTAPI_URL}/explain",
                    json={"image_path": os.path.join("app",result["image_path"]), "query": query}
                )
                if ex_res.status_code != 200:
                    explanation = "Error in explanation"
                else:
                    explanation = ex_res.json()["explanation"]

            st.markdown(f"**🤖 Explanation:** {explanation}")
