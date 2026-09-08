import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY ortam değişkeni bulunamadı! .env dosyasını kontrol edin.")
    
    genai.configure(api_key=api_key)
    # Varsayılan hızlı model
    return genai.GenerativeModel("gemini-1.5-flash")

def get_response(model, prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"API Hatası: {str(e)}"

if __name__ == "__main__":
    bot = init_gemini()
    print("Bot hazır! Test yanıtı alınıyor...")
    print(get_response(bot, "Merhaba, çalışıyor musun?"))