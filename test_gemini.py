import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('GEMINI_API_KEY')
print('Key loaded:', bool(key))
if not key:
    raise SystemExit('No API key')
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content('Hello Gemini!')
print('Response:', response.text)
