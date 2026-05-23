import google.generativeai as genai
from PIL import Image
import json
import re
import os

class GeminiScanner:
    def __init__(self):
        # Configure Gemini
        genai.configure()
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def scan_product_image(self, image_path):
        """Extract product information from image"""
        try:
            img = Image.open(image_path)
            
            prompt = """Analyze this food product packaging image carefully. Extract the following information and return ONLY valid JSON (no other text, no markdown):

{
    "product_name": "Exact product name as shown on front",
    "brand": "Brand name",
    "ingredients": "Complete ingredients list exactly as written",
    "allergens": "Allergen information (contains: ...)",
    "serving_size": "Serving size (e.g., 100g, 1 biscuit)",
    "servings_per_pack": "Number of servings per pack",
    "energy_per_serving": "Calories per serving (just the number)",
    "nutritional_table": [
        {"nutrient_name": "Protein", "per_100g": "7.9g", "per_serving": "2g"},
        {"nutrient_name": "Carbohydrates", "per_100g": "69.8g", "per_serving": "17.5g"},
        {"nutrient_name": "Fat", "per_100g": "18.2g", "per_serving": "4.6g"}
    ]
}

If any information is missing, use null. Extract actual values from the image."""
            
            response = self.model.generate_content([prompt, img])
            
            # Extract JSON from response
            response_text = response.text
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            
            if json_match:
                data = json.loads(json_match.group())
                return data
            return None
            
        except Exception as e:
            print(f"Scan error: {e}")
            return None
    
    def analyze_health(self, ingredients_text):
        """Analyze health score based on ingredients"""
        harmful = {
            'refined sugar': 15, 'sugar': 10, 'high fructose corn syrup': 15,
            'palm oil': 12, 'refined flour': 10, 'maida': 10, 'preservative': 8,
            'artificial color': 8, 'artificial flavour': 5, 'msg': 10,
            'trans fat': 20, 'hydrogenated oil': 15
        }
        
        beneficial = {
            'whole grain': 10, 'protein': 8, 'fiber': 10, 'vitamin': 8,
            'mineral': 8, 'calcium': 5, 'iron': 5, 'probiotic': 12,
            'no added sugar': 15, 'low fat': 8, 'natural': 5, 'organic': 10
        }
        
        ingredients_lower = ingredients_text.lower() if ingredients_text else ""
        
        harmful_found = [i for i in harmful if i in ingredients_lower]
        beneficial_found = [i for i in beneficial if i in ingredients_lower]
        
        total_penalty = sum(harmful.get(i, 0) for i in harmful_found)
        total_bonus = sum(beneficial.get(i, 0) for i in beneficial_found)
        
        score = 70 - total_penalty + total_bonus
        score = max(0, min(100, score))
        
        if score >= 80:
            category = "Excellent"
            emoji = "🌟"
        elif score >= 60:
            category = "Good"
            emoji = "👍"
        elif score >= 40:
            category = "Average"
            emoji = "😐"
        elif score >= 20:
            category = "Poor"
            emoji = "⚠️"
        else:
            category = "Avoid"
            emoji = "❌"
        
        return {
            'health_score': score,
            'health_category': f"{emoji} {category}",
            'harmful_ingredients': harmful_found,
            'beneficial_ingredients': beneficial_found
        }
