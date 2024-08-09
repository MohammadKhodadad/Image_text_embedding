import os
import requests
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import matplotlib.pyplot as plt
import torch

def describe_images_blip(image_files):
    processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
    model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", device_map="auto")
    
    descriptions = []
    
    for image_file in image_files:
        raw_image = Image.open(image_file).convert('RGB')
        question = "Describe all the notable and interesting features of this house."
        inputs = processor(raw_image, question, return_tensors="pt").to("cuda", torch.float16)


        out = model.generate(**inputs)
        description = processor.decode(out[0], skip_special_tokens=True)
        descriptions.append((image_file, description))
    
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
