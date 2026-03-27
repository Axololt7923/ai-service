import google.generativeai as genai
import dotenv
import os

#this program checks which Gemini models are available for the provided API token

dotenv.load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)

print("Danh sách các model hỗ trợ generateContent:")
print("-" * 40)

# Lấy danh sách các model
for m in genai.list_models():
    # Lọc ra những model hỗ trợ tạo text (generateContent)
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
