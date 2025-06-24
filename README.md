# Visual Image Search

The App will allow you to search similar images based on the text query

## Prerequisites

1. Python
2. UV package Manager
3. Docker (for containerization)

## Running on local

1. Clone the repo <br>
    `git clone https://github.com/sociopath00/image-search.git`

2. Create virtual env <br>
    `uv venv`

3. Activate virtual env <br>
    `source .venv/bin/activate`

4. Install the dependencies <br>
    `uv pip install -r pyprojec.toml`

5. Download the images <br>
    `python -m app.download_images`

6. Create .env file and add OPENAI_APIKEY

7. Run the backend <br>
    `uvicorn app.app:app --reload`

8. Run the Frontend <br>
    `streamlit run ui_app.py`

## Running on Docker

1. Build a docker 
    `docker build -t img-search-app .`

2. Run the app
    `docker run -p 8000:8000 -p 8501:8501 img-search-app`