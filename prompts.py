import json

def build_system_instruction(school_info: str, user_data: dict, mode_instruction: str = None) -> str:
    user_info_str = json.dumps(user_data, ensure_ascii=False, indent=2)
    
    base_instruction = f"""
Sen gelişmiş bir Okul ve Ders Danışmanı botusun.
Görevin:
1. Okul genel sorularını [OKUL VERİTABANI] içinden yanıtlamak.
2. Çalışma önerilerini [KULLANICI DERS PROGRAMI VE BİLGİLERİ] verisine göre kişiye özel sunmak.

Veritabanında veya kullanıcı programında olmayan genel bilgiler için uydurma yapma, dürüstçe bilmediğini söyle.

[OKUL VERİTABANI]:
{school_info}

[KULLANICI DERS PROGRAMI VE BİLGİLERİ]:
{user_info_str}
"""
    if mode_instruction:
        base_instruction += f"\n\n[DENEYSEL MOD / ÖZEL TALİMAT]: {mode_instruction}"
        
    return base_instruction