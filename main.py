import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY bulunamadı! .env dosyasını kontrol edin.")

genai.configure(api_key=API_KEY)

def load_school_data(filepath: str = "okul_data.json") -> str:
    """Okulun statik genel verisini yükler."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.dumps(json.load(f), ensure_ascii=False, indent=2)
    except FileNotFoundError:
        return "{'bilgi': 'Genel okul verisi yüklenmedi.'}"

# Okul verisi sabit olduğu için bir kere belleğe alıyoruz
SCHOOL_INFO = load_school_data()

def create_user_bot(user_schedule: dict, mode_instruction: str = None):
    """
    Her istek atan kullanıcı için dinamik olarak model nesnesi üretir.
    user_schedule: Frontend veya DB'den gelen kullanıcıya özel veri.
    """
    user_info_str = json.dumps(user_schedule, ensure_ascii=False, indent=2) if user_schedule else "Kullanıcı ders programı girmedi."
    
    base_instruction = f"""
    Sen gelişmiş bir Okul ve Ders Danışmanı botusun.
    Görevin:
    1. Okul genel sorularını [OKUL VERİTABANI] içinden yanıtlamak.
    2. Çalışma önerilerini [KULLANICI DERS PROGRAMI] verisine göre Kişiye Özel sunmak.

    [OKUL VERİTABANI]:
    {SCHOOL_INFO}

    [AKTİF KULLANICININ DERS PROGRAMI VE BİLGİLERİ]:
    {user_info_str}
    """
    
    if mode_instruction:
        base_instruction += f"\n\n[ÖZEL TALİMAT]: {mode_instruction}"

    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=base_instruction
    )

# --- CANLI KULLANIM SİMÜLASYONU ---
if __name__ == "__main__":
    # Örnek Kullanıcı 1 (Frontend'den/DB'den gelen veri)
    user_1_data = {
        "user_id": "usr_101",
        "zayif_dersler": ["Fizik"],
        "dolu_saatler": {"Pazartesi": ["08:30-15:30", "18:00-19:30"]},
        "gunluk_hedef_saat": 2
    }

    # Örnek Kullanıcı 2
    user_2_data = {
        "user_id": "usr_102",
        "zayif_dersler": ["Matematik", "Kimya"],
        "dolu_saatler": {"Pazartesi": ["08:30-16:00"]},
        "gunluk_hedef_saat": 4
    }

    # Kullanıcı 1 İstek Atıyor
    bot_user_1 = create_user_bot(user_schedule=user_1_data)
    session_1 = bot_user_1.start_chat(history=[])
    res_1 = session_1.send_message("Bugün boş vaktimde ne çalışayım?")
    print(f"--- User 1 Yanıtı ---\n{res_1.text}\n")

    # Kullanıcı 2 İstek Atıyor
    bot_user_2 = create_user_bot(user_schedule=user_2_data)
    session_2 = bot_user_2.start_chat(history=[])
    res_2 = session_2.send_message("Bugün boş vaktimde ne çalışayım?")
    print(f"--- User 2 Yanıtı ---\n{res_2.text}")