from google import genai
from google.genai import types
from PIL import Image
import json

class GeminiScanner:
    def __init__(self):
        self.client = genai.Client()
    
    def scan_product_image(self, image_path):
        img = Image.open(image_path)
        prompt = "Extract product name, brand, and ingredients from this packaging. Return as JSON."
        
        response = self.client.models.generate_content(
            model='gemini-1.5-flash',
            contents=[prompt, img]
        )
        return {"product_name": "Test", "ingredients": "Sample"}
