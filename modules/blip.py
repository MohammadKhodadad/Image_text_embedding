import os
import requests
from PIL import Image
from transformers import AutoProcessor, Blip2ForConditionalGeneration
import matplotlib.pyplot as plt
import torch

def describe_images_blip(image_files, query="What’s in this image? split features with '\n'"):
    processor = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
    model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    
    descriptions = []
    
    for i,image_file in enumerate(image_files):
        raw_image = Image.open(image_file).convert('RGB')
        if isinstance(query,list):
            question = f"Question: {query[i]} (yes or no) Answer: "
        else:
            question = f"Question: {query} Answer: "
        # inputs = processor(image, return_tensors="pt").to(device, torch.float16)

        # generated_ids = model.generate(**inputs, max_new_tokens=20)
        # generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        # print(generated_text)
        inputs = processor(raw_image, text=question, return_tensors="pt").to("cuda", torch.float16)


        generated_ids = model.generate(**inputs,max_length=100)
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        descriptions.append((image_file, generated_text))
        print(generated_ids,generated_text)
    
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
