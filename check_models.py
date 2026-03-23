import google.generativeai as genai
from os import getenv

api_key = getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("--- Modelos disponibles para tu API KEY ---")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"ID: {m.name}  |  Display: {m.display_name}")