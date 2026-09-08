import json

def build_study_plan_prompt(user_data: dict) -> str:
    return f"""
GÖREV: Kullanıcının ders programına ve kişisel hedeflerine uygun haftalık ders çalışma teklifleri oluştur.

KULLANICI DERS PROGRAMI VE BİLGİLERİ:
{json.dumps(user_data, ensure_ascii=False, indent=2)}

KURALLAR:
1. 'busy_slots' saatlerine kesinlikle ders çalışma ekleme.
2. 'weak_subjects' listesindeki derslere daha fazla ağırlık ver.
3. Çalışma oturumlarını 45 dk ders + 15 dk mola (Pomodoro) şeklinde kurgula.
4. Çıktıyı doğrudan gün gün ayrılmış çalışma programı şeklinde ver.
"""