import google.generativeai as genai
from PIL import Image
import json

class GeminiScanner:
    def __init__(self):
        # Configure the API key from environment variable
        genai.configure()
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def scan_product_image(self, image_path):
        """Extract product information from an image"""
        img = Image.open(image_path)
        
        prompt = """Extract from this product image. Return ONLY valid JSON, no other text:
        {
            "product_name": "full product name",
            "brand": "brand name",
            "ingredients": "complete ingredients list",
            "allergens": "allergen warnings if any",
            "serving_size": "serving size (e.g., 15g)",
            "servings_per_pack": "number of servings",
            "energy_per_serving": 0,
            "nutritional_table": []
        }"""
        
        response = self.model.generate_content([prompt, img])
        # Extract JSON from response
        text = response.text
        # Find JSON part (between { and })
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end != 0:
            json_str = text[start:end]
            return json.loads(json_str)
        return None
    
    def analyze_health(self, ingredients_text):
        """Analyze health score based on ingredients"""
        harmful = {'sugar': 10, 'palm oil': 12, 'refined flour': 10}
        beneficial = {'protein': 8, 'fiber': 10, 'vitamin': 8}
        
        ingredients_lower = ingredients_text.lower()
        harmful_found = [i for i in harmful if i in ingredients_lower]
        beneficial_found = [i for i in beneficial if i in ingredients_lower]
        
        score = 70 - sum(harmful.get(i,0) for i in harmful_found) + sum(beneficial.get(i,0) for i in beneficial_found)
        score = max(0, min(100, score))
        
        if score >= 80:
            category = "Excellent"
        elif score >= 60:
            category = "Good"
        elif score >= 40:
            category = "Average"
        elif score >= 20:
            category = "Poor"
        else:
            category = "Avoid"
        
        return {
            'health_score': score,
            'health_category': category,
            'harmful_ingredients': harmful_found,
            'beneficial_ingredients': beneficial_found
        }
