import os
import openai
import base64
from dotenv import load_dotenv
import requests
import matplotlib.pyplot as plt
from PIL import Image

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to get image descriptions using OpenAI API
def describe_images_openai(image_files,query="What’s in this image? split features with '\n'"):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    descriptions = []

    for i,image_file in enumerate(image_files):
        base64_image = encode_image(image_file)
        if isinstance(query,list):
            question = f"Question: {query[i]} (yes or no) Answer: "
        else:
            question = f"Question: {query} Answer: "
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            description = response.json()['choices'][0]['message']['content']
            descriptions.append((image_file, description))
        else:
            descriptions.append((image_file, "Description request failed."))
    
    return descriptions

# Function to plot images with descriptions
def plot_images_with_descriptions(descriptions):
    for image_file, description in descriptions:
        image = Image.open(image_file)
        plt.figure(figsize=(10, 6))
        plt.imshow(image)
        plt.title(description, fontsize=12)
        plt.axis('off')
        plt.show()