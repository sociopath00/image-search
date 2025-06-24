import openai
import base64
from app import config

openai.api_key = config.OPENAI_APIKEY


def generate_explanation(image_path: str, query: str) -> str:
    # Read image and convert to base64
    with open(image_path, "rb") as img_file:
        image_b64 = base64.b64encode(img_file.read()).decode("utf-8")

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert image analyst who explains how visual content matches text queries."},
            {"role": "user", "content": [
                {"type": "text", "text": f"Explain why the following image is relevant to the query: '{query}'"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_b64}"
                    }
                }
            ]}
        ],
        max_tokens=300
    )

    return response.choices[0].message.content.strip()



if __name__ == "__main__":
    # image_path = "app/images/10640.jpg"
    image_path = "app/images/3762.jpg"
    query = "A couple hanging on a beach"

    result = generate_explanation(image_path, query)
    print(result)
