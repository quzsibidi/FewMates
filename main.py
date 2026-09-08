import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY bulunamadı! .env dosyasını kontrol edin.")

genai.configure(api_key=API_KEY)

def load_custom_school_data(filepath: str = "okul_data.json") -> str:
    """Herhangi bir okulun JSON verisini yükler."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return json.dumps(data, ensure_ascii=False, indent=2)
    except FileNotFoundError:
        return "{'bilgi': 'Özel okul verisi yüklenmedi, genel moddasın.'}"

def create_experimental_bot(data_path: str = "okul_data.json", mode_instruction: str = None):
    """
    Deneysel Okul Botu Fabrikası.
    Hem okul verisini hem de test edilecek modu dinamik alır.
    """
    school_info = load_custom_school_data(data_path)
    
    base_instruction = f"""
    Sen deneysel bir Okul Asistanı botusun.
    Görevin: Sana sağlanan okul veritabanına göre soruları yanıtlamak.
    Veritabanında olmayan bilgiler için uydurma yapma, 'Bu bilgi veritabanımda yok' de.
    
    [YÜKLENEN OKUL VERİTABANI]:
    {school_info}
    """
    
    if mode_instruction:
        base_instruction += f"\n\n[DENEYSEL MOD/KİŞİLİK TALİMATI]: {mode_instruction}"

    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=base_instruction
    )

def start_chat_session(model):
    return model.start_chat(history=[])

def send_message(chat_session, message: str) -> str:
    try:
        response = chat_session.send_message(message)
        return response.text
    except Exception as e:
        return f"[API Hatası]: {str(e)}"

if __name__ == "__main__":
    # Örnek Deney: "Disiplinli Nöbetçi Öğretmen Modu"
    TEST_MODE = "Sen sert ama adil bir nöbetçi öğretmensin. Soruları kısa ve ciddi yanıtla."
    
    bot = create_experimental_bot(mode_instruction=TEST_MODE)
    session = start_chat_session(bot)
    
    print("--- Deneysel Bot Testi ---")
    print("Soru: Derste telefon kullanabilir miyim?")
    print("Cevap:", send_message(session, "Derste telefon kullanabilir miyim?"))