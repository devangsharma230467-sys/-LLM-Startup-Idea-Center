import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
key = os.getenv('GEMINI_API_KEY')
print('Key loaded:', bool(key))
if not key:
    raise SystemExit('No API key')

genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Hello Gemini!')
print('Response:', response.text)
