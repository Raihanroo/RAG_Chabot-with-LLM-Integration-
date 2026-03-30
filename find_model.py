import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("🔍 Available embedding models:\n")
found = False
for model in genai.list_models():
    if "embedContent" in model.supported_generation_methods:
        print(f"✅ {model.name}")
        found = True

if not found:
    print("❌ No embedding models found!")
    print("Your API key might be invalid or expired.")
