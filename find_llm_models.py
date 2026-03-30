import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("🔍 Available LLM models for generateContent:\n")

# Try to list available models
try:
    # List all models
    models = client.models.list()

    for model in models:
        if "generateContent" in str(
            model.supported_actions
        ) or "generateContent" in dir(model):
            print(f"✅ {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")
    print("\nTrying alternative method...")

# Alternative: Try common model names
common_models = [
    "gemini-1.5-flash",
    "models/gemini-1.5-flash",
    "gemini-1.5-pro",
    "models/gemini-1.5-pro",
    "gemini-2.0-flash-exp",
    "models/gemini-2.0-flash-exp",
    "gemini-pro",
    "models/gemini-pro",
]

print("\n📝 Testing common model names:\n")
for model_name in common_models:
    try:
        response = client.models.generate_content(
            model=model_name, contents="Say hello"
        )
        print(f"✅ WORKING: {model_name}")
        print(f"   Response: {response.text[:50]}...")
        break
    except Exception as e:
        print(f"❌ {model_name}: Not working")
