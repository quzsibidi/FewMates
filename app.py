import os
import json
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Environment Ayarları
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY bulunamadı! Lütfen .env dosyasını kontrol edin.")
    st.stop()

genai.configure(api_key=API_KEY)

# Sayfa Yapılandırması
st.set_page_config(page_title="Deneysel Okul Asistanı", page_icon="🏫", layout="wide")
st.title("🏫 Deneysel Okul Asistanı")

# --- SOL PANEL (Ayarlar & Veri Yükleme) ---
with st.sidebar:
    st.header("⚙️ Bot Konfigürasyonu")
    
    # 1. Mod/Kişilik Seçimi (2. Kişi Görevi)
    st.subheader("1. Bot Kişiliği (Prompt)")
    try:
        with open("prompts.json", "r", encoding="utf-8") as f:
            prompts = json.load(f)
        selected_mode = st.selectbox("Bir kişilik seçin:", list(prompts.keys()))
        system_instruction = prompts[selected_mode]
    except Exception:
        system_instruction = "Sen yardımcı bir okul asistanısın."
        st.warning("prompts.json bulunamadı, varsayılan mod kullanılıyor.")

    # 2. Okul Verisi Yükleme (3. Kişi Görevi)
    st.subheader("2. Okul Veritabanı (JSON)")
    uploaded_file = st.file_uploader("Okul JSON dosyasını yükleyin", type=["json"])
    
    if uploaded_file is not None:
        school_data = json.load(uploaded_file)
        st.success("Özel Okul Verisi Yüklendi!")
    else:
        # Varsayılan Veri
        try:
            with open("okul_data.json", "r", encoding="utf-8") as f:
                school_data = json.load(f)
            st.info("Varsayılan okul_data.json kullanılıyor.")
        except Exception:
            school_data = {"bilgi": "Veri yok"}

    if st.button("Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.session_state.chat = None
        st.rerun()

# --- BACKEND MODEL KURULUMU ---
full_instruction = f"""
Sen deneysel bir Okul Asistanı botusun.
Aşağıdaki okul verilerini referans alarak soruları yanıtla.
Bilgilerde olmayan konular için uydurma yapma, 'Bu bilgi okul veritabanında yer almıyor' de.

[YÜKLENEN OKUL VERİTABANI]:
{json.dumps(school_data, ensure_ascii=False, indent=2)}

[KİŞİLİK VE ÜSLUP TALİMATI]:
{system_instruction}
"""

if "chat" not in st.session_state or st.session_state.chat is None:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=full_instruction
    )
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SOHBET EKRANI ---
# Geçmiş Mesajları Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı Mesaj Girişi
if user_input := st.chat_input("Okul hakkında bir şey sorun..."):
    # Kullanıcı Mesajını Ekrana Yaz
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Bot Yanıtını Üret ve Ekrana Yaz
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(user_input)
            bot_reply = response.text
        except Exception as e:
            bot_reply = f"[Hata]: {str(e)}"
        
        st.markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})