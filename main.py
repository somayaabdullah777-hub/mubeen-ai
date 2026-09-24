"""
Mubeen AI (مُبين AI) — Smart platform for the Prophetic Seerah in world languages.
Full 25-question bilingual quiz + Timeline + AI Chat + mobile-optimized chat input.
"""

import base64
import json
import os
import random
from typing import Optional

import requests
import streamlit as st

# ---------------------------------------------------------------------------
# 1. PAGE CONFIG
# ---------------------------------------------------------------------------
def _load_favicon():
    for path in ["assets/logo_favicon.png", "assets/logo.png"]:
        try:
            with open(path, "rb") as f:
                return f.read()
        except Exception:
            continue
    return "🕌"


st.set_page_config(
    page_title="Mubeen AI | مُبين AI",
    page_icon=_load_favicon(),
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# 2. LOGO LOADER
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_logo_base64(path: str = "assets/logo.png") -> str:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# 3. QUIZ BANK — 25 questions × 10 languages
# ---------------------------------------------------------------------------
QUIZ_BANK = {
    "ar": [
        {"q": "في أي عام ميلادي وُلد النبي ﷺ؟",
         "options": ["570م", "571م", "572م", "573م"], "answer": 1,
         "explanation": "وُلد النبي ﷺ عام الفيل (571م) كما ورد في «الرحيق المختوم»."},
        {"q": "ما اسم والدة النبي ﷺ؟",
         "options": ["حليمة السعدية", "آمنة بنت وهب", "خديجة بنت خويلد", "فاطمة بنت أسد"], "answer": 1,
         "explanation": "والدة النبي ﷺ هي آمنة بنت وهب بن عبد مناف."},
        {"q": "في أي غار نزل الوحي على النبي ﷺ أول مرة؟",
         "options": ["غار ثور", "غار حراء", "غار الكهف", "غار الرقيم"], "answer": 1,
         "explanation": "نزل الوحي في غار حراء بجبل النور قرب مكة."},
        {"q": "ما أول سورة نزلت من القرآن الكريم؟",
         "options": ["الفاتحة", "العلق", "المدثر", "البقرة"], "answer": 1,
         "explanation": "أول ما نزل قوله تعالى: ﴿اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ﴾ من سورة العلق."},
        {"q": "كم كان عمر النبي ﷺ عند نزول الوحي؟",
         "options": ["30 سنة", "35 سنة", "40 سنة", "45 سنة"], "answer": 2,
         "explanation": "كان عمره ﷺ أربعين سنة عند بعثته."},
        {"q": "من هي أول من آمن بالنبي ﷺ من النساء؟",
         "options": ["عائشة", "خديجة", "فاطمة", "حفصة"], "answer": 1,
         "explanation": "أول من آمن به ﷺ زوجته خديجة بنت خويلد رضي الله عنها."},
        {"q": "من أول من أسلم من الرجال الأحرار؟",
         "options": ["أبو بكر الصديق", "عمر بن الخطاب", "عثمان بن عفان", "علي بن أبي طالب"], "answer": 0,
         "explanation": "أبو بكر الصديق رضي الله عنه أول من أسلم من الرجال الأحرار."},
        {"q": "من الصحابي الذي رافق النبي ﷺ في هجرته؟",
         "options": ["علي", "أبو بكر", "عمر", "عثمان"], "answer": 1,
         "explanation": "رافقه أبو بكر الصديق رضي الله عنه."},
        {"q": "ما أول مسجد أسسه النبي ﷺ عند وصوله إلى المدينة؟",
         "options": ["المسجد النبوي", "مسجد قباء", "المسجد الأقصى", "مسجد القبلتين"], "answer": 1,
         "explanation": "أسس مسجد قباء أول مسجد في الإسلام."},
        {"q": "في أي سنة هجرية وقعت غزوة بدر؟",
         "options": ["الأولى", "الثانية", "الثالثة", "الرابعة"], "answer": 1,
         "explanation": "وقعت في السنة الثانية للهجرة، وتسمى يوم الفرقان."},
        {"q": "كم كان عدد المسلمين في غزوة بدر؟",
         "options": ["300", "313", "350", "400"], "answer": 1,
         "explanation": "كان عددهم 313 رجلاً."},
        {"q": "في أي سنة هجرية وقعت غزوة أحد؟",
         "options": ["الثانية", "الثالثة", "الرابعة", "الخامسة"], "answer": 1,
         "explanation": "وقعت غزوة أحد في السنة الثالثة للهجرة."},
        {"q": "من هو سيد الشهداء في غزوة أحد؟",
         "options": ["حمزة بن عبد المطلب", "مصعب بن عمير", "أنس بن النضر", "سعد بن الربيع"], "answer": 0,
         "explanation": "حمزة بن عبد المطلب عم النبي ﷺ، لقّبه النبي ﷺ بسيد الشهداء."},
        {"q": "في أي سنة هجرية وقعت غزوة الخندق؟",
         "options": ["الثالثة", "الرابعة", "الخامسة", "السادسة"], "answer": 2,
         "explanation": "وقعت في السنة الخامسة للهجرة."},
        {"q": "من الذي اقترح حفر الخندق؟",
         "options": ["أبو بكر", "عمر", "سلمان الفارسي", "علي"], "answer": 2,
         "explanation": "سلمان الفارسي رضي الله عنه اقترح حفر الخندق."},
        {"q": "في أي سنة هجرية وقع صلح الحديبية؟",
         "options": ["الرابعة", "الخامسة", "السادسة", "السابعة"], "answer": 2,
         "explanation": "وقع في السنة السادسة للهجرة."},
        {"q": "بماذا وصف الله صلح الحديبية في القرآن؟",
         "options": ["فتحاً عظيماً", "فتحاً مبيناً", "نصراً مؤزراً", "رحمة واسعة"], "answer": 1,
         "explanation": "قال تعالى: ﴿إِنَّا فَتَحْنَا لَكَ فَتْحًا مُبِينًا﴾."},
        {"q": "من الذي أعطاه النبي ﷺ الراية في خيبر؟",
         "options": ["أبو بكر", "عمر", "علي بن أبي طالب", "عثمان"], "answer": 2,
         "explanation": "أعطى النبي ﷺ الراية لعلي بن أبي طالب."},
        {"q": "كم عدد القادة الثلاثة الذين استُشهدوا في مؤتة؟",
         "options": ["قائدان", "ثلاثة قادة", "أربعة قادة", "خمسة قادة"], "answer": 1,
         "explanation": "زيد بن حارثة، جعفر بن أبي طالب، وعبد الله بن رواحة."},
        {"q": "في أي سنة هجرية كانت حجة الوداع؟",
         "options": ["الثامنة", "التاسعة", "العاشرة", "الحادية عشرة"], "answer": 2,
         "explanation": "حجّ النبي ﷺ حجة الوداع في السنة العاشرة للهجرة."},
        {"q": "في أي سنة هجرية توفي النبي ﷺ؟",
         "options": ["التاسعة", "العاشرة", "الحادية عشرة", "الثانية عشرة"], "answer": 2,
         "explanation": "توفي النبي ﷺ في السنة الحادية عشرة للهجرة."},
        {"q": "كم كان عمر النبي ﷺ عند وفاته؟",
         "options": ["60 سنة", "62 سنة", "63 سنة", "65 سنة"], "answer": 2,
         "explanation": "توفي ﷺ وعمره ثلاث وستون سنة."},
        {"q": "من هي أصغر بنات النبي ﷺ؟",
         "options": ["زينب", "رقية", "أم كلثوم", "فاطمة"], "answer": 3,
         "explanation": "فاطمة الزهراء رضي الله عنها أصغر بنات النبي ﷺ."},
        {"q": "ما لقب أبي بكر الصديق؟",
         "options": ["الفاروق", "الصديق", "ذو النورين", "سيف الله"], "answer": 1,
         "explanation": "لقّبه النبي ﷺ بالصديق لتصديقه بالإسراء."},
        {"q": "ما لقب عمر بن الخطاب؟",
         "options": ["الصديق", "الفاروق", "ذو النورين", "أمين الأمة"], "answer": 1,
         "explanation": "لقّبه النبي ﷺ بالفاروق لأنه فرّق بين الحق والباطل."},
    ],
    "en": [
        {"q": "In which Gregorian year was the Prophet ﷺ born?",
         "options": ["570 AD", "571 AD", "572 AD", "573 AD"], "answer": 1,
         "explanation": "The Prophet ﷺ was born in the Year of the Elephant (571 AD) as mentioned in 'The Sealed Nectar'."},
        {"q": "What is the name of the Prophet's ﷺ mother?",
         "options": ["Halimah al-Sa'diyah", "Aminah bint Wahb", "Khadijah bint Khuwaylid", "Fatimah bint Asad"], "answer": 1,
         "explanation": "The Prophet's ﷺ mother is Aminah bint Wahb ibn Abd Manaf."},
        {"q": "In which cave did the first revelation descend upon the Prophet ﷺ?",
         "options": ["Cave of Thawr", "Cave of Hira", "Cave of Kahf", "Cave of Raqim"], "answer": 1,
         "explanation": "The revelation descended in the Cave of Hira on Jabal al-Nur near Makkah."},
        {"q": "What is the first Surah revealed of the Quran?",
         "options": ["Al-Fatihah", "Al-Alaq", "Al-Muddathir", "Al-Baqarah"], "answer": 1,
         "explanation": "The first verses revealed were 'Read in the name of your Lord who created' from Surah Al-Alaq."},
        {"q": "How old was the Prophet ﷺ when the revelation first came?",
         "options": ["30 years", "35 years", "40 years", "45 years"], "answer": 2,
         "explanation": "He ﷺ was forty years old at the start of his prophethood."},
        {"q": "Who was the first woman to believe in the Prophet ﷺ?",
         "options": ["Aisha", "Khadijah", "Fatimah", "Hafsah"], "answer": 1,
         "explanation": "The first to believe in him ﷺ was his wife Khadijah bint Khuwaylid (may Allah be pleased with her)."},
        {"q": "Who was the first free man to embrace Islam?",
         "options": ["Abu Bakr al-Siddiq", "Umar ibn al-Khattab", "Uthman ibn Affan", "Ali ibn Abi Talib"], "answer": 0,
         "explanation": "Abu Bakr al-Siddiq (may Allah be pleased with him) was the first free man to embrace Islam."},
        {"q": "Which Companion accompanied the Prophet ﷺ during the Hijrah?",
         "options": ["Ali", "Abu Bakr", "Umar", "Uthman"], "answer": 1,
         "explanation": "Abu Bakr al-Siddiq (may Allah be pleased with him) accompanied him."},
        {"q": "What was the first mosque the Prophet ﷺ established upon arriving in Madinah?",
         "options": ["The Prophet's Mosque", "Quba Mosque", "Al-Aqsa Mosque", "Qiblatayn Mosque"], "answer": 1,
         "explanation": "He established Quba Mosque, the first mosque in Islam."},
        {"q": "In which Hijri year did the Battle of Badr take place?",
         "options": ["First", "Second", "Third", "Fourth"], "answer": 1,
         "explanation": "It took place in the 2nd year after Hijrah, known as the Day of Distinction."},
        {"q": "How many Muslims were at the Battle of Badr?",
         "options": ["300", "313", "350", "400"], "answer": 1,
         "explanation": "There were 313 men."},
        {"q": "In which Hijri year did the Battle of Uhud take place?",
         "options": ["Second", "Third", "Fourth", "Fifth"], "answer": 1,
         "explanation": "The Battle of Uhud took place in the 3rd year after Hijrah."},
        {"q": "Who is the Master of Martyrs in the Battle of Uhud?",
         "options": ["Hamza ibn Abd al-Muttalib", "Mus'ab ibn Umayr", "Anas ibn al-Nadr", "Sa'd ibn al-Rabi"], "answer": 0,
         "explanation": "Hamza ibn Abd al-Muttalib, the Prophet's ﷺ uncle, whom the Prophet ﷺ titled Master of Martyrs."},
        {"q": "In which Hijri year did the Battle of the Trench take place?",
         "options": ["Third", "Fourth", "Fifth", "Sixth"], "answer": 2,
         "explanation": "It took place in the 5th year after Hijrah."},
        {"q": "Who suggested digging the trench?",
         "options": ["Abu Bakr", "Umar", "Salman al-Farisi", "Ali"], "answer": 2,
         "explanation": "Salman al-Farisi (may Allah be pleased with him) suggested digging the trench."},
        {"q": "In which Hijri year was the Treaty of Hudaybiyyah concluded?",
         "options": ["Fourth", "Fifth", "Sixth", "Seventh"], "answer": 2,
         "explanation": "It was concluded in the 6th year after Hijrah."},
        {"q": "How did Allah describe the Treaty of Hudaybiyyah in the Quran?",
         "options": ["A great victory", "A clear victory", "A mighty triumph", "Vast mercy"], "answer": 1,
         "explanation": "Allah said: 'Indeed We have granted you a clear victory.'"},
        {"q": "Whom did the Prophet ﷺ give the banner to at Khaybar?",
         "options": ["Abu Bakr", "Umar", "Ali ibn Abi Talib", "Uthman"], "answer": 2,
         "explanation": "The Prophet ﷺ gave the banner to Ali ibn Abi Talib."},
        {"q": "How many commanders were martyred at Mu'tah?",
         "options": ["Two", "Three", "Four", "Five"], "answer": 1,
         "explanation": "Zayd ibn Harithah, Ja'far ibn Abi Talib, and Abdullah ibn Rawahah."},
        {"q": "In which Hijri year was the Farewell Pilgrimage?",
         "options": ["Eighth", "Ninth", "Tenth", "Eleventh"], "answer": 2,
         "explanation": "The Prophet ﷺ performed the Farewell Pilgrimage in the 10th year after Hijrah."},
        {"q": "In which Hijri year did the Prophet ﷺ pass away?",
         "options": ["Ninth", "Tenth", "Eleventh", "Twelfth"], "answer": 2,
         "explanation": "The Prophet ﷺ passed away in the 11th year after Hijrah."},
        {"q": "How old was the Prophet ﷺ when he passed away?",
         "options": ["60 years", "62 years", "63 years", "65 years"], "answer": 2,
         "explanation": "He ﷺ passed away at the age of sixty-three."},
        {"q": "Who was the youngest daughter of the Prophet ﷺ?",
         "options": ["Zaynab", "Ruqayyah", "Umm Kulthum", "Fatimah"], "answer": 3,
         "explanation": "Fatimah al-Zahra (may Allah be pleased with her) was the youngest daughter of the Prophet ﷺ."},
        {"q": "What is the title of Abu Bakr al-Siddiq?",
         "options": ["Al-Farooq", "Al-Siddiq", "Dhul-Nurayn", "Sword of Allah"], "answer": 1,
         "explanation": "The Prophet ﷺ titled him Al-Siddiq for confirming the Israa."},
        {"q": "What is the title of Umar ibn al-Khattab?",
         "options": ["Al-Siddiq", "Al-Farooq", "Dhul-Nurayn", "Trustee of the Ummah"], "answer": 1,
         "explanation": "The Prophet ﷺ titled him Al-Farooq for distinguishing truth from falsehood."},
    ],
    "ur": [
        {"q": "نبی ﷺ کی ولادت کس عیسوی سال میں ہوئی؟",
         "options": ["570ء", "571ء", "572ء", "573ء"], "answer": 1,
         "explanation": "نبی ﷺ کی ولادت عام الفیل (571ء) میں ہوئی۔"},
        {"q": "نبی ﷺ کی والدہ کا نام کیا ہے؟",
         "options": ["حلیمہ سعدیہ", "آمنہ بنت وہب", "خدیجہ بنت خویلد", "فاطمہ بنت اسد"], "answer": 1,
         "explanation": "نبی ﷺ کی والدہ آمنہ بنت وہب ہیں۔"},
        {"q": "پہلی وحی نبی ﷺ پر کس غار میں نازل ہوئی؟",
         "options": ["غار ثور", "غار حرا", "غار کہف", "غار رقیم"], "answer": 1,
         "explanation": "وحی جبل النور کے غار حرا میں نازل ہوئی۔"},
        {"q": "قرآن کریم کی پہلی نازل ہونے والی سورت کون سی ہے؟",
         "options": ["الفاتحہ", "العلق", "المدثر", "البقرہ"], "answer": 1,
         "explanation": "پہلی آیات سورۃ العلق سے نازل ہوئیں۔"},
        {"q": "وحی کے نزول کے وقت نبی ﷺ کی عمر کتنی تھی؟",
         "options": ["30 سال", "35 سال", "40 سال", "45 سال"], "answer": 2,
         "explanation": "بعثت کے وقت آپ ﷺ کی عمر چالیس سال تھی۔"},
        {"q": "عورتوں میں سب سے پہلے نبی ﷺ پر ایمان کس نے لایا؟",
         "options": ["عائشہ", "خدیجہ", "فاطمہ", "حفصہ"], "answer": 1,
         "explanation": "سب سے پہلے خدیجہ بنت خویلد رضی اللہ عنہا نے ایمان لایا۔"},
        {"q": "آزاد مردوں میں سب سے پہلے اسلام کس نے قبول کیا؟",
         "options": ["ابو بکر صدیق", "عمر بن خطاب", "عثمان بن عفان", "علی بن ابی طالب"], "answer": 0,
         "explanation": "ابو بکر صدیق رضی اللہ عنہ۔"},
        {"q": "ہجرت کے سفر میں نبی ﷺ کے ساتھ کون تھا؟",
         "options": ["علی", "ابو بکر", "عمر", "عثمان"], "answer": 1,
         "explanation": "ابو بکر صدیق رضی اللہ عنہ۔"},
        {"q": "مدینہ پہنچنے پر نبی ﷺ نے پہلی مسجد کون سی تعمیر کی؟",
         "options": ["مسجد نبوی", "مسجد قباء", "مسجد اقصیٰ", "مسجد قبلتین"], "answer": 1,
         "explanation": "مسجد قباء، اسلام کی پہلی مسجد۔"},
        {"q": "غزوۂ بدر کس ہجری سال میں پیش آیا؟",
         "options": ["پہلا", "دوسرا", "تیسرا", "چوتھا"], "answer": 1,
         "explanation": "دوسرے ہجری میں، اسے یوم الفرقان کہا جاتا ہے۔"},
        {"q": "غزوۂ بدر میں مسلمانوں کی تعداد کتنی تھی؟",
         "options": ["300", "313", "350", "400"], "answer": 1,
         "explanation": "ان کی تعداد 313 تھی۔"},
        {"q": "غزوۂ اُحد کس ہجری سال میں پیش آیا؟",
         "options": ["دوسرا", "تیسرا", "چوتھا", "پانچواں"], "answer": 1,
         "explanation": "تیسرے ہجری میں۔"},
        {"q": "غزوۂ اُحد میں سید الشہداء کون ہیں؟",
         "options": ["حمزہ بن عبد المطلب", "مصعب بن عمیر", "انس بن النضر", "سعد بن ربیع"], "answer": 0,
         "explanation": "حمزہ بن عبد المطلب، نبی ﷺ کے چچا۔"},
        {"q": "غزوۂ خندق کس ہجری سال میں پیش آیا؟",
         "options": ["تیسرا", "چوتھا", "پانچواں", "چھٹا"], "answer": 2,
         "explanation": "پانچویں ہجری میں۔"},
        {"q": "خندق کھودنے کی تجویز کس نے دی؟",
         "options": ["ابو بکر", "عمر", "سلمان فارسی", "علی"], "answer": 2,
         "explanation": "سلمان فارسی رضی اللہ عنہ۔"},
        {"q": "صلح حدیبیہ کس ہجری سال میں ہوا؟",
         "options": ["چوتھا", "پاچواں", "چھٹا", "ساتواں"], "answer": 2,
         "explanation": "چھٹے ہجری میں۔"},
        {"q": "اللہ نے قرآن میں صلح حدیبیہ کو کیا کہا؟",
         "options": ["عظیم فتح", "فتح مبین", "بڑی نصرت", "وسیع رحمت"], "answer": 1,
         "explanation": "﴿اِنَّا فَتَحْنَا لَكَ فَتْحًا مُّبِيْنًا﴾۔"},
        {"q": "خیبر میں نبی ﷺ نے پرچم کس کو دیا؟",
         "options": ["ابو بکر", "عمر", "علی بن ابی طالب", "عثمان"], "answer": 2,
         "explanation": "علی بن ابی طالب رضی اللہ عنہ۔"},
        {"q": "غزوۂ موتہ میں کتنے قائدین شہید ہوئے؟",
         "options": ["دو", "تین", "چار", "پانچ"], "answer": 1,
         "explanation": "زید، جعفر، اور ابن رواحہ۔"},
        {"q": "حجۃ الوداع کس ہجری سال میں ادا کیا گیا؟",
         "options": ["آٹھواں", "نواں", "دسواں", "گیارہواں"], "answer": 2,
         "explanation": "دسویں ہجری میں۔"},
        {"q": "نبی ﷺ کی وفات کس ہجری سال میں ہوئی؟",
         "options": ["نواں", "دسواں", "گیارہواں", "بارہواں"], "answer": 2,
         "explanation": "گیارہویں ہجری میں۔"},
        {"q": "وفات کے وقت نبی ﷺ کی عمر کتنی تھی؟",
         "options": ["60 سال", "62 سال", "63 سال", "65 سال"], "answer": 2,
         "explanation": "ترسٹھ سال۔"},
        {"q": "نبی ﷺ کی سب سے چھوٹی بیٹی کون ہیں؟",
         "options": ["ذینب", "رقیہ", "ام کلثوم", "فاطمہ"], "answer": 3,
         "explanation": "فاطمہ زہراء رضی اللہ عنہا۔"},
        {"q": "ابو بکر صدیق کا لقب کیا ہے؟",
         "options": ["فاروق", "صدیق", "ذو النورین", "سیف اللہ"], "answer": 1,
         "explanation": "نبی ﷺ نے انہیں صدیق کا لقب دیا۔"},
        {"q": "عمر بن خطاب کا لقب کیا ہے؟",
         "options": ["صدیق", "فاروق", "ذو النورین", "امین امت"], "answer": 1,
         "explanation": "نبی ﷺ نے انہیں فاروق کا لقب دیا۔"},
    ],
    "id": [
        {"q": "Pada tahun Masehi berapa Nabi ﷺ dilahirkan?",
         "options": ["570 M", "571 M", "572 M", "573 M"], "answer": 1,
         "explanation": "Nabi ﷺ dilahirkan pada Tahun Gajah (571 M)."},
        {"q": "Siapa nama ibu Nabi ﷺ?",
         "options": ["Halimah as-Sa'diyah", "Aminah binti Wahb", "Khadijah binti Khuwailid", "Fatimah binti Asad"], "answer": 1,
         "explanation": "Ibu Nabi ﷺ adalah Aminah binti Wahb."},
        {"q": "Di gua mana wahyu pertama turun kepada Nabi ﷺ?",
         "options": ["Gua Tsur", "Gua Hira", "Gua Kahfi", "Gua Raqim"], "answer": 1,
         "explanation": "Wahyu turun di Gua Hira."},
        {"q": "Surah pertama yang diturunkan dari Al-Quran?",
         "options": ["Al-Fatihah", "Al-Alaq", "Al-Muddatstsir", "Al-Baqarah"], "answer": 1,
         "explanation": "Ayat pertama dari Surah Al-Alaq."},
        {"q": "Berapa usia Nabi ﷺ saat wahyu pertama turun?",
         "options": ["30 tahun", "35 tahun", "40 tahun", "45 tahun"], "answer": 2,
         "explanation": "Usia beliau ﷺ empat puluh tahun."},
        {"q": "Siapa wanita pertama yang beriman kepada Nabi ﷺ?",
         "options": ["Aisyah", "Khadijah", "Fatimah", "Hafshah"], "answer": 1,
         "explanation": "Khadijah binti Khuwailid ra."},
        {"q": "Siapa orang merdeka pertama yang masuk Islam?",
         "options": ["Abu Bakar ash-Shiddiq", "Umar bin al-Khaththab", "Utsman bin Affan", "Ali bin Abi Thalib"], "answer": 0,
         "explanation": "Abu Bakar ash-Shiddiq ra."},
        {"q": "Sahabat yang menemani Nabi ﷺ dalam hijrah?",
         "options": ["Ali", "Abu Bakar", "Umar", "Utsman"], "answer": 1,
         "explanation": "Abu Bakar ash-Shiddiq ra."},
        {"q": "Masjid pertama yang dibangun Nabi ﷺ saat tiba di Madinah?",
         "options": ["Masjid Nabawi", "Masjid Quba", "Masjid Aqsha", "Masjid Qiblatain"], "answer": 1,
         "explanation": "Masjid Quba."},
        {"q": "Pada tahun Hijriah keberapa Perang Badar terjadi?",
         "options": ["Pertama", "Kedua", "Ketiga", "Keempat"], "answer": 1,
         "explanation": "Tahun ke-2 Hijriah, Yaumul Furqan."},
        {"q": "Berapa jumlah kaum Muslimin dalam Perang Badar?",
         "options": ["300", "313", "350", "400"], "answer": 1,
         "explanation": "313 orang."},
        {"q": "Pada tahun Hijriah keberapa Perang Uhud terjadi?",
         "options": ["Kedua", "Ketiga", "Keempat", "Kelima"], "answer": 1,
         "explanation": "Tahun ke-3 Hijriah."},
        {"q": "Siapa Sayyid Syuhada dalam Perang Uhud?",
         "options": ["Hamzah bin Abdul Muththalib", "Mush'ab bin Umair", "Anas bin an-Nadhr", "Sa'd bin ar-Rabi'"], "answer": 0,
         "explanation": "Hamzah bin Abdul Muththalib."},
        {"q": "Pada tahun Hijriah keberapa Perang Khandaq terjadi?",
         "options": ["Ketiga", "Keempat", "Kelima", "Keenam"], "answer": 2,
         "explanation": "Tahun ke-5 Hijriah."},
        {"q": "Siapa yang mengusulkan penggalian parit?",
         "options": ["Abu Bakar", "Umar", "Salman al-Farisi", "Ali"], "answer": 2,
         "explanation": "Salman al-Farisi ra."},
        {"q": "Pada tahun Hijriah keberapa Perjanjian Hudaibiyah terjadi?",
         "options": ["Keempat", "Kelima", "Keenam", "Ketujuh"], "answer": 2,
         "explanation": "Tahun ke-6 Hijriah."},
        {"q": "Bagaimana Allah menyebut Perjanjian Hudaibiyah dalam Al-Quran?",
         "options": ["Kemenangan besar", "Kemenangan nyata", "Kemenangan perkasa", "Rahmat luas"], "answer": 1,
         "explanation": "Kemenangan yang nyata."},
        {"q": "Kepada siapa Nabi ﷺ memberikan panji di Khaibar?",
         "options": ["Abu Bakar", "Umar", "Ali bin Abi Thalib", "Utsman"], "answer": 2,
         "explanation": "Ali bin Abi Thalib."},
        {"q": "Berapa komandan yang syahid di Mu'tah?",
         "options": ["Dua", "Tiga", "Empat", "Lima"], "answer": 1,
         "explanation": "Zaid, Ja'far, dan Abdullah bin Rawahah."},
        {"q": "Pada tahun Hijriah keberapa Haji Wada' dilaksanakan?",
         "options": ["Kedelapan", "Kesembilan", "Kesepuluh", "Kesebelas"], "answer": 2,
         "explanation": "Tahun ke-10 Hijriah."},
        {"q": "Pada tahun Hijriah keberapa Nabi ﷺ wafat?",
         "options": ["Kesembilan", "Kesepuluh", "Kesebelas", "Kedua belas"], "answer": 2,
         "explanation": "Tahun ke-11 Hijriah."},
        {"q": "Berapa usia Nabi ﷺ saat wafat?",
         "options": ["60 tahun", "62 tahun", "63 tahun", "65 tahun"], "answer": 2,
         "explanation": "Enam puluh tiga tahun."},
        {"q": "Siapa putri termuda Nabi ﷺ?",
         "options": ["Zainab", "Ruqayyah", "Ummu Kultsum", "Fatimah"], "answer": 3,
         "explanation": "Fatimah az-Zahra ra."},
        {"q": "Apa gelar Abu Bakar ash-Shiddiq?",
         "options": ["Al-Faruq", "Ash-Shiddiq", "Dzun Nurain", "Pedang Allah"], "answer": 1,
         "explanation": "Ash-Shiddiq."},
        {"q": "Apa gelar Umar bin al-Khaththab?",
         "options": ["Ash-Shiddiq", "Al-Faruq", "Dzun Nurain", "Aminul Ummah"], "answer": 1,
         "explanation": "Al-Faruq."},
    ],
    "tr": [
        {"q": "Hz. Peygamber ﷺ hangi miladi yılda doğdu?",
         "options": ["570", "571", "572", "573"], "answer": 1,
         "explanation": "Fil Yılı'nda (571)."},
        {"q": "Hz. Peygamber'in ﷺ annesinin adı nedir?",
         "options": ["Halime es-Sa'diyye", "Âmine bint Vehb", "Hatice bint Huveylid", "Fatıma bint Esed"], "answer": 1,
         "explanation": "Âmine bint Vehb."},
        {"q": "İlk vahiy hangi mağarada nazil oldu?",
         "options": ["Sevr Mağarası", "Hira Mağarası", "Kehf Mağarası", "Rakîm Mağarası"], "answer": 1,
         "explanation": "Hira Mağarası."},
        {"q": "Kur'an-ı Kerim'in ilk inen suresi hangisidir?",
         "options": ["Fatiha", "Alak", "Müddessir", "Bakara"], "answer": 1,
         "explanation": "Alak suresi."},
        {"q": "Vahyin ilk geldiğinde Hz. Peygamber kaç yaşındaydı?",
         "options": ["30", "35", "40", "45"], "answer": 2,
         "explanation": "Kırk yaşında."},
        {"q": "Hz. Peygamber'e ﷺ ilk iman eden kadın kimdir?",
         "options": ["Aişe", "Hatice", "Fatıma", "Hafsa"], "answer": 1,
         "explanation": "Hatice bint Huveylid."},
        {"q": "Özgür erkeklerden İslam'ı ilk kabul eden kimdir?",
         "options": ["Ebû Bekir es-Sıddîk", "Ömer b. Hattâb", "Osman b. Affân", "Ali b. Ebû Tâlib"], "answer": 0,
         "explanation": "Ebû Bekir es-Sıddîk."},
        {"q": "Hicret sırasında Hz. Peygamber'e ﷺ kim eşlik etti?",
         "options": ["Ali", "Ebû Bekir", "Ömer", "Osman"], "answer": 1,
         "explanation": "Ebû Bekir es-Sıddîk."},
        {"q": "Hz. Peygamber ﷺ Medine'ye vardığında ilk hangi mescidi inşa etti?",
         "options": ["Mescid-i Nebevî", "Kuba Mescidi", "Mescid-i Aksâ", "Kıbleteyn Mescidi"], "answer": 1,
         "explanation": "Kuba Mescidi."},
        {"q": "Bedir Savaşı hangi hicri yılda oldu?",
         "options": ["Birinci", "İkinci", "Üçüncü", "Dördüncü"], "answer": 1,
         "explanation": "Hicretin 2. yılı."},
        {"q": "Bedir Savaşı'nda kaç Müslüman vardı?",
         "options": ["300", "313", "350", "400"], "answer": 1,
         "explanation": "313 kişi."},
        {"q": "Uhud Savaşı hangi hicri yılda oldu?",
         "options": ["İkinci", "Üçüncü", "Dördüncü", "Beşinci"], "answer": 1,
         "explanation": "Hicretin 3. yılı."},
        {"q": "Uhud'da şehitlerin efendisi kimdir?",
         "options": ["Hamza b. Abdülmuttalib", "Mus'ab b. Umeyr", "Enes b. Nadr", "Sa'd b. Rebî"], "answer": 0,
         "explanation": "Hamza b. Abdülmuttalib."},
        {"q": "Hendek Savaşı hangi hicri yılda oldu?",
         "options": ["Üçüncü", "Dördüncü", "Beşinci", "Altıncı"], "answer": 2,
         "explanation": "Hicretin 5. yılı."},
        {"q": "Hendek kazma fikrini kim ortaya attı?",
         "options": ["Ebû Bekir", "Ömer", "Selman-ı Fârisî", "Ali"], "answer": 2,
         "explanation": "Selman-ı Fârisî."},
        {"q": "Hudeybiye Antlaşması hangi hicri yılda yapıldı?",
         "options": ["Dördüncü", "Beşinci", "Altıncı", "Yedinci"], "answer": 2,
         "explanation": "Hicretin 6. yılı."},
        {"q": "Allah, Kur'an'da Hudeybiye Antlaşması'nı nasıl nitelendirdi?",
         "options": ["Büyük bir fetih", "Apaçık bir fetih", "Muhteşem bir zafer", "Geniş bir rahmet"], "answer": 1,
         "explanation": "Apaçık bir fetih."},
        {"q": "Hayber'de Hz. Peygamber ﷺ sancağı kime verdi?",
         "options": ["Ebû Bekir", "Ömer", "Ali b. Ebû Tâlib", "Osman"], "answer": 2,
         "explanation": "Ali b. Ebû Tâlib."},
        {"q": "Mute'de kaç komutan şehit oldu?",
         "options": ["İki", "Üç", "Dört", "Beş"], "answer": 1,
         "explanation": "Zeyd, Ca'fer, Abdullah b. Revâha."},
        {"q": "Veda Haccı hangi hicri yılda yapıldı?",
         "options": ["Sekizinci", "Dokuzuncu", "Onuncu", "On birinci"], "answer": 2,
         "explanation": "Hicretin 10. yılı."},
        {"q": "Hz. Peygamber ﷺ hangi hicri yılda vefat etti?",
         "options": ["Dokuzuncu", "Onuncu", "On birinci", "On ikinci"], "answer": 2,
         "explanation": "Hicretin 11. yılı."},
        {"q": "Vefat ettiğinde Hz. Peygamber kaç yaşındaydı?",
         "options": ["60", "62", "63", "65"], "answer": 2,
         "explanation": "Altmış üç."},
        {"q": "Hz. Peygamber'in ﷺ en küçük kızı kimdir?",
         "options": ["Zeyneb", "Rukiyye", "Ümmü Gülsüm", "Fâtıma"], "answer": 3,
         "explanation": "Fâtıma ez-Zehrâ."},
        {"q": "Ebû Bekir es-Sıddîk'ın lakabı nedir?",
         "options": ["el-Fârûk", "es-Sıddîk", "Zinnûreyn", "Allah'ın Kılıcı"], "answer": 1,
         "explanation": "es-Sıddîk."},
        {"q": "Ömer b. Hattâb'ın lakabı nedir?",
         "options": ["es-Sıddîk", "el-Fârûk", "Zinnûreyn", "Ümmetin Emini"], "answer": 1,
         "explanation": "el-Fârûk."},
    ],
    "fr": [
        {"q": "En quelle année grégorienne le Prophète ﷺ est-il né ?",
         "options": ["570 ap. J.-C.", "571 ap. J.-C.", "572 ap. J.-C.", "573 ap. J.-C."], "answer": 1,
         "explanation": "L'Année de l'Éléphant (571)."},
        {"q": "Quel est le nom de la mère du Prophète ﷺ ?",
         "options": ["Halimah al-Sa'diyah", "Aminah bint Wahb", "Khadijah bint Khuwaylid", "Fatimah bint Asad"], "answer": 1,
         "explanation": "Aminah bint Wahb."},
        {"q": "Dans quelle grotte la première révélation est-elle descendue ?",
         "options": ["Grotte de Thawr", "Grotte de Hira", "Grotte de Kahf", "Grotte de Raqim"], "answer": 1,
         "explanation": "La grotte de Hira."},
        {"q": "Quelle est la première sourate révélée du Coran ?",
         "options": ["Al-Fatihah", "Al-Alaq", "Al-Muddathir", "Al-Baqarah"], "answer": 1,
         "explanation": "Al-Alaq."},
        {"q": "Quel âge avait le Prophète ﷺ lors de la première révélation ?",
         "options": ["30 ans", "35 ans", "40 ans", "45 ans"], "answer": 2,
         "explanation": "Quarante ans."},
        {"q": "Qui fut la première femme à croire au Prophète ﷺ ?",
         "options": ["Aïcha", "Khadijah", "Fatimah", "Hafsah"], "answer": 1,
         "explanation": "Khadijah bint Khuwaylid."},
        {"q": "Qui fut le premier homme libre à embrasser l'islam ?",
         "options": ["Abu Bakr al-Siddiq", "Umar ibn al-Khattab", "Uthman ibn Affan", "Ali ibn Abi Talib"], "answer": 0,
         "explanation": "Abu Bakr al-Siddiq."},
        {"q": "Quel Compagnon a accompagné le Prophète ﷺ lors de l'Hégire ?",
         "options": ["Ali", "Abu Bakr", "Umar", "Uthman"], "answer": 1,
         "explanation": "Abu Bakr al-Siddiq."},
        {"q": "Quelle fut la première mosquée établie par le Prophète ﷺ à son arrivée à Médine ?",
         "options": ["La mosquée du Prophète", "La mosquée de Quba", "La mosquée al-Aqsa", "La mosquée des Deux Qiblas"], "answer": 1,
         "explanation": "La mosquée de Quba."},
        {"q": "En quelle année hégirienne eut lieu la bataille de Badr ?",
         "options": ["Première", "Deuxième", "Troisième", "Quatrième"], "answer": 1,
         "explanation": "2e année."},
        {"q": "Combien de musulmans y avait-il à la bataille de Badr ?",
         "options": ["300", "313", "350", "400"], "answer": 1,
         "explanation": "313 hommes."},
        {"q": "En quelle année hégirienne eut lieu la bataille d'Uhud ?",
         "options": ["Deuxième", "Troisième", "Quatrième", "Cinquième"], "answer": 1,
         "explanation": "3e année."},
        {"q": "Qui est le Maître des Martyrs à la bataille d'Uhud ?",
         "options": ["Hamza ibn Abd al-Muttalib", "Mus'ab ibn Umayr", "Anas ibn al-Nadr", "Sa'd ibn al-Rabi"], "answer": 0,
         "explanation": "Hamza ibn Abd al-Muttalib."},
        {"q": "En quelle année hégirienne eut lieu la bataille de la Tranchée ?",
         "options": ["Troisième", "Quatrième", "Cinquième", "Sixième"], "answer": 2,
         "explanation": "5e année."},
        {"q": "Qui a suggéré de creuser la tranchée ?",
         "options": ["Abu Bakr", "Umar", "Salman al-Farisi", "Ali"], "answer": 2,
         "explanation": "Salman al-Farisi."},
        {"q": "En quelle année hégirienne le traité de Hudaybiyya fut-il conclu ?",
         "options": ["Quatrième", "Cinquième", "Sixième", "Septième"], "answer": 2,
         "explanation": "6e année."},
        {"q": "Comment Allah a-t-Il décrit le traité de Hudaybiyya dans le Coran ?",
         "options": ["Une grande victoire", "Une victoire éclatante", "Un triomphe puissant", "Une vaste miséricorde"], "answer": 1,
         "explanation": "Une victoire éclatante."},
        {"q": "À qui le Prophète ﷺ a-t-il remis l'étendard à Khaybar ?",
         "options": ["Abu Bakr", "Umar", "Ali ibn Abi Talib", "Uthman"], "answer": 2,
         "explanation": "Ali ibn Abi Talib."},
        {"q": "Combien de commandants furent martyrisés à Mu'ta ?",
         "options": ["Deux", "Trois", "Quatre", "Cinq"], "answer": 1,
         "explanation": "Zayd, Ja'far, Abdullah ibn Rawahah."},
        {"q": "En quelle année hégirienne eut lieu le Pèlerinage d'adieu ?",
         "options": ["Huitième", "Neuvième", "Dixième", "Onzième"], "answer": 2,
         "explanation": "10e année."},
        {"q": "En quelle année hégirienne le Prophète ﷺ est-il décédé ?",
         "options": ["Neuvième", "Dixième", "Onzième", "Douzième"], "answer": 2,
         "explanation": "11e année."},
        {"q": "Quel âge avait le Prophète ﷺ lors de son décès ?",
         "options": ["60 ans", "62 ans", "63 ans", "65 ans"], "answer": 2,
         "explanation": "Soixante-trois ans."},
        {"q": "Qui était la plus jeune fille du Prophète ﷺ ?",
         "options": ["Zaynab", "Ruqayyah", "Umm Kulthum", "Fatimah"], "answer": 3,
         "explanation": "Fatimah al-Zahra."},
        {"q": "Quel est le titre d'Abu Bakr al-Siddiq ?",
         "options": ["Al-Farooq", "Al-Siddiq", "Dhul-Nurayn", "L'Épée d'Allah"], "answer": 1,
         "explanation": "Al-Siddiq."},
        {"q": "Quel est le titre d'Umar ibn al-Khattab ?",
         "options": ["Al-Siddiq", "Al-Farooq", "Dhul-Nurayn", "Le Confident de la Umma"], "answer": 1,
         "explanation": "Al-Farooq."},
    ],
    "es": [
        {"q": "¿En qué año gregoriano nació el Profeta ﷺ?",
         "options": ["570 d.C.", "571 d.C.", "572 d.C.", "573 d.C."], "answer": 1,
         "explanation": "El Año del Elefante (571)."},
        {"q": "¿Cuál es el nombre de la madre del Profeta ﷺ?",
         "options": ["Halimah al-Sa'diyah", "Aminah bint Wahb", "Khadijah bint Khuwaylid", "Fatimah bint Asad"], "answer": 1,
         "explanation": "Aminah bint Wahb."},
        {"q": "¿En qué cueva descendió la primera revelación?",
         "options": ["Cueva de Thawr", "Cueva de Hira", "Cueva de Kahf", "Cueva de Raqim"], "answer": 1,
         "explanation": "La Cueva de Hira."},
        {"q": "¿Cuál es la primera sura revelada del Corán?",
         "options": ["Al-Fatihah", "Al-Alaq", "Al-Muddathir", "Al-Baqarah"], "answer": 1,
         "explanation": "Al-Alaq."},
        {"q": "¿Cuántos años tenía el Profeta ﷺ cuando llegó la primera revelación?",
         "options": ["30 años", "35 años", "40 años", "45 años"], "answer": 2,
         "explanation": "Cuarenta años."},
        {"q": "¿Quién fue la primera mujer en creer en el Profeta ﷺ?",
         "options": ["Aisha", "Khadijah", "Fatimah", "Hafsah"], "answer": 1,
         "explanation": "Khadijah bint Khuwaylid."},
        {"q": "¿Quién fue el primer hombre libre en abrazar el Islam?",
         "options": ["Abu Bakr al-Siddiq", "Umar ibn al-Khattab", "Uthman ibn Affan", "Ali ibn Abi Talib"], "answer": 0,
         "explanation": "Abu Bakr al-Siddiq."},
        {"q": "¿Qué Compañero acompañó al Profeta ﷺ durante la Hégira?",
         "options": ["Ali", "Abu Bakr", "Umar", "Uthman"], "answer": 1,
         "explanation": "Abu Bakr al-Siddiq."},
        {"q": "¿Cuál fue la primera mezquita que estableció el Profeta ﷺ al llegar a Medina?",
         "options": ["La Mezquita del Profeta", "La Mezquita de Quba", "La Mezquita al-Aqsa", "La Mezquita de las Dos Qiblas"], "answer": 1,
         "explanation": "La Mezquita de Quba."},
        {"q": "¿En qué año hégira tuvo lugar la batalla de Badr?",
         "options": ["Primero", "Segundo", "Tercero", "Cuarto"], "answer": 1,
         "explanation": "2º año."},
        {"q": "¿Cuántos musulmanes había en la batalla de Badr?",
         "options": ["300", "313", "350", "400"], "answer": 1,
         "explanation": "313 hombres."},
        {"q": "¿En qué año hégira tuvo lugar la batalla de Uhud?",
         "options": ["Segundo", "Tercero", "Cuarto", "Quinto"], "answer": 1,
         "explanation": "3er año."},
        {"q": "¿Quién es el Señor de los Mártires en la batalla de Uhud?",
         "options": ["Hamza ibn Abd al-Muttalib", "Mus'ab ibn Umayr", "Anas ibn al-Nadr", "Sa'd ibn al-Rabi"], "answer": 0,
         "explanation": "Hamza ibn Abd al-Muttalib."},
        {"q": "¿En qué año hégira tuvo lugar la batalla de la Trinchera?",
         "options": ["Tercero", "Cuarto", "Quinto", "Sexto"], "answer": 2,
         "explanation": "5º año."},
        {"q": "¿Quién sugirió cavar la trinchera?",
         "options": ["Abu Bakr", "Umar", "Salman al-Farisi", "Ali"], "answer": 2,
         "explanation": "Salman al-Farisi."},
        {"q": "¿En qué año hégira se concluyó el tratado de Hudaybiyyah?",
         "options": ["Cuarto", "Quinto", "Sexto", "Séptimo"], "answer": 2,
         "explanation": "6º año."},
        {"q": "¿Cómo describió Allah el tratado de Hudaybiyyah en el Corán?",
         "options": ["Una gran victoria", "Una victoria manifiesta", "Un triunfo poderoso", "Una vasta misericordia"], "answer": 1,
         "explanation": "Una victoria manifiesta."},
        {"q": "¿A quién entregó el Profeta ﷺ el estandarte en Jaybar?",
         "options": ["Abu Bakr", "Umar", "Ali ibn Abi Talib", "Uthman"], "answer": 2,
         "explanation": "Ali ibn Abi Talib."},
        {"q": "¿Cuántos comandantes fueron martirizados en Mu'ta?",
         "options": ["Dos", "Tres", "Cuatro", "Cinco"], "answer": 1,
         "explanation": "Zayd, Ya'far, Abdullah ibn Rawaha."},
        {"q": "¿En qué año hégira tuvo lugar la Peregrinación de Despedida?",
         "options": ["Octavo", "Noveno", "Décimo", "Undécimo"], "answer": 2,
         "explanation": "10º año."},
        {"q": "¿En qué año hégira falleció el Profeta ﷺ?",
         "options": ["Noveno", "Décimo", "Undécimo", "Duodécimo"], "answer": 2,
         "explanation": "11º año."},
        {"q": "¿Cuántos años tenía el Profeta ﷺ al fallecer?",
         "options": ["60 años", "62 años", "63 años", "65 años"], "answer": 2,
         "explanation": "Sesenta y tres."},
        {"q": "¿Quién fue la hija más joven del Profeta ﷺ?",
         "options": ["Zaynab", "Ruqayyah", "Umm Kulthum", "Fatimah"], "answer": 3,
         "explanation": "Fatimah al-Zahra."},
        {"q": "¿Cuál es el título de Abu Bakr al-Siddiq?",
         "options": ["Al-Farooq", "Al-Siddiq", "Dhul-Nurayn", "La Espada de Allah"], "answer": 1,
         "explanation": "Al-Siddiq."},
        {"q": "¿Cuál es el título de Umar ibn al-Khattab?",
         "options": ["Al-Siddiq", "Al-Farooq", "Dhul-Nurayn", "El Confiable de la Umma"], "answer": 1,
         "explanation": "Al-Farooq."},
    ],
    "ru": [
        {"q": "В каком году по григорианскому календарю родился Пророк ﷺ?",
         "options": ["570 г.", "571 г.", "572 г.", "573 г."], "answer": 1,
         "explanation": "Год Слона (571)."},
        {"q": "Как зовут мать Пророка ﷺ?",
         "options": ["Халима ас-Саадия", "Амина бинт Вахб", "Хадиджа бинт Хувайлид", "Фатима бинт Асад"], "answer": 1,
         "explanation": "Амина бинт Вахб."},
        {"q": "В какой пещере снизошло первое откровение?",
         "options": ["Пещера Саур", "Пещера Хира", "Пещера Кахф", "Пещера Раким"], "answer": 1,
         "explanation": "Пещера Хира."},
        {"q": "Какая сура Корана была ниспослана первой?",
         "options": ["Аль-Фатиха", "Аль-Алак", "Аль-Муддассир", "Аль-Бакара"], "answer": 1,
         "explanation": "Аль-Алак."},
        {"q": "Сколько лет было Пророку ﷺ при первом откровении?",
         "options": ["30 лет", "35 лет", "40 лет", "45 лет"], "answer": 2,
         "explanation": "Сорок лет."},
        {"q": "Кто была первой женщиной, уверовавшей в Пророка ﷺ?",
         "options": ["Аиша", "Хадиджа", "Фатима", "Хафса"], "answer": 1,
         "explanation": "Хадиджа бинт Хувайлид."},
        {"q": "Кто был первым свободным мужчиной, принявшим ислам?",
         "options": ["Абу Бакр ас-Сиддик", "Умар ибн аль-Хаттаб", "Усман ибн Аффан", "Али ибн Абу Талиб"], "answer": 0,
         "explanation": "Абу Бакр ас-Сиддик."},
        {"q": "Какой сподвижник сопровождал Пророка ﷺ во время хиджры?",
         "options": ["Али", "Абу Бакр", "Умар", "Усман"], "answer": 1,
         "explanation": "Абу Бакр ас-Сиддик."},
        {"q": "Какую первую мечеть основал Пророк ﷺ по прибытии в Медину?",
         "options": ["Мечеть Пророка", "Мечеть Куба", "Мечеть аль-Акса", "Мечеть двух кибл"], "answer": 1,
         "explanation": "Мечеть Куба."},
        {"q": "В каком году хиджры произошла битва при Бадре?",
         "options": ["Первом", "Втором", "Третьем", "Четвёртом"], "answer": 1,
         "explanation": "2-й год."},
        {"q": "Сколько мусульман было в битве при Бадре?",
         "options": ["300", "313", "350", "400"], "answer": 1,
         "explanation": "313 человек."},
        {"q": "В каком году хиджры произошла битва при Ухуде?",
         "options": ["Втором", "Третьем", "Четвёртом", "Пятом"], "answer": 1,
         "explanation": "3-й год."},
        {"q": "Кто является Господином шахидов в битве при Ухуде?",
         "options": ["Хамза ибн Абд аль-Мутталиб", "Мусъаб ибн Умайр", "Анас ибн ан-Надр", "Саад ибн ар-Раби"], "answer": 0,
         "explanation": "Хамза ибн Абд аль-Мутталиб."},
        {"q": "В каком году хиджры произошла битва у Рва?",
         "options": ["Третьем", "Четвёртом", "Пятом", "Шестом"], "answer": 2,
         "explanation": "5-й год."},
        {"q": "Кто предложил вырыть ров?",
         "options": ["Абу Бакр", "Умар", "Салман аль-Фариси", "Али"], "answer": 2,
         "explanation": "Салман аль-Фариси."},
        {"q": "В каком году хиджры был заключён Худайбийский договор?",
         "options": ["Четвёртом", "Пятом", "Шестом", "Седьмом"], "answer": 2,
         "explanation": "6-й год."},
        {"q": "Как Аллах описал Худайбийский договор в Коране?",
         "options": ["Великая победа", "Явная победа", "Мощный триумф", "Обширная милость"], "answer": 1,
         "explanation": "Явная победа."},
        {"q": "Кому Пророк ﷺ вручил знамя в Хайбаре?",
         "options": ["Абу Бакру", "Умару", "Али ибн Абу Талибу", "Усману"], "answer": 2,
         "explanation": "Али ибн Абу Талибу."},
        {"q": "Сколько полководцев пали шахидами при Муте?",
         "options": ["Два", "Три", "Четыре", "Пять"], "answer": 1,
         "explanation": "Зейд, Джафар, Абдуллах ибн Раваха."},
        {"q": "В каком году хиджры состоялось Прощальное паломничество?",
         "options": ["Восьмом", "Девятом", "Десятом", "Одиннадцатом"], "answer": 2,
         "explanation": "10-й год."},
        {"q": "В каком году хиджры Пророк ﷺ скончался?",
         "options": ["Девятом", "Десятом", "Одиннадцатом", "Двенадцатом"], "answer": 2,
         "explanation": "11-й год."},
        {"q": "Сколько лет было Пророку ﷺ при кончине?",
         "options": ["60 лет", "62 года", "63 года", "65 лет"], "answer": 2,
         "explanation": "Шестьдесят три."},
        {"q": "Кто была младшей дочерью Пророка ﷺ?",
         "options": ["Зайнаб", "Рукайя", "Умм Кульсум", "Фатима"], "answer": 3,
         "explanation": "Фатима аз-Захра."},
        {"q": "Каков титул Абу Бакра ас-Сиддика?",
         "options": ["Аль-Фарук", "Ас-Сиддик", "Зун-Нурайн", "Меч Аллаха"], "answer": 1,
         "explanation": "Ас-Сиддик."},
        {"q": "Каков титул Умара ибн аль-Хаттаба?",
         "options": ["Ас-Сиддик", "Аль-Фарук", "Зун-Нурайн", "Доверенный уммы"], "answer": 1,
         "explanation": "Аль-Фарук."},
    ],
    "zh": [
        {"q": "先知 ﷺ 出生于公历哪一年？",
         "options": ["公元570年", "公元571年", "公元572年", "公元573年"], "answer": 1,
         "explanation": "象年（571年）。"},
        {"q": "先知 ﷺ 的母亲叫什么名字？",
         "options": ["哈莉玛·萨迪娅", "阿米娜·宾特·瓦赫卜", "赫蒂彻·宾特·胡韦利德", "法蒂玛·宾特·阿萨德"], "answer": 1,
         "explanation": "阿米娜·宾特·瓦赫卜。"},
        {"q": "第一次启示降示在哪个山洞？",
         "options": ["骚尔洞", "希拉洞", "凯赫夫洞", "拉基姆洞"], "answer": 1,
         "explanation": "希拉洞。"},
        {"q": "《古兰经》中最早降示的章节是哪一章？",
         "options": ["开端章", "血块章", "盖被的人章", "黄牛章"], "answer": 1,
         "explanation": "血块章。"},
        {"q": "第一次启示降临时，先知 ﷺ 多大年龄？",
         "options": ["30岁", "35岁", "40岁", "45岁"], "answer": 2,
         "explanation": "四十岁。"},
        {"q": "第一位信仰先知 ﷺ 的女性是谁？",
         "options": ["阿伊莎", "赫蒂彻", "法蒂玛", "哈芙赛"], "answer": 1,
         "explanation": "赫蒂彻·宾特·胡韦利德。"},
        {"q": "第一位接受伊斯兰的自由男性是谁？",
         "options": ["艾布·伯克尔·松迪格", "欧麦尔·本·哈塔卜", "奥斯曼·本·阿凡", "阿里·本·阿比·塔利卜"], "answer": 0,
         "explanation": "艾布·伯克尔·松迪格。"},
        {"q": "迁徙期间哪一位圣门弟子陪伴先知 ﷺ？",
         "options": ["阿里", "艾布·伯克尔", "欧麦尔", "奥斯曼"], "answer": 1,
         "explanation": "艾布·伯克尔。"},
        {"q": "先知 ﷺ 抵达麦地那后建立的第一座清真寺是哪座？",
         "options": ["先知清真寺", "库巴清真寺", "阿克萨清真寺", "双向清真寺"], "answer": 1,
         "explanation": "库巴清真寺。"},
        {"q": "白德尔战役发生在伊历哪一年？",
         "options": ["第一年", "第二年", "第三年", "第四年"], "answer": 1,
         "explanation": "第二年。"},
        {"q": "白德尔战役中有多少穆斯林？",
         "options": ["300人", "313人", "350人", "400人"], "answer": 1,
         "explanation": "313人。"},
        {"q": "伍侯德战役发生在伊历哪一年？",
         "options": ["第二年", "第三年", "第四年", "第五年"], "answer": 1,
         "explanation": "第三年。"},
        {"q": "伍侯德战役中谁是烈士之主？",
         "options": ["哈姆扎·本·阿卜杜勒·穆塔里卜", "穆斯阿卜·本·乌麦尔", "阿纳斯·本·纳德尔", "萨阿德·本·拉比"], "answer": 0,
         "explanation": "哈姆扎·本·阿卜杜勒·穆塔里卜。"},
        {"q": "壕沟战役发生在伊历哪一年？",
         "options": ["第三年", "第四年", "第五年", "第六年"], "answer": 2,
         "explanation": "第五年。"},
        {"q": "谁建议挖掘壕沟？",
         "options": ["艾布·伯克尔", "欧麦尔", "萨勒曼·法里西", "阿里"], "answer": 2,
         "explanation": "萨勒曼·法里西。"},
        {"q": "侯代比亚和约缔结于伊历哪一年？",
         "options": ["第四年", "第五年", "第六年", "第七年"], "answer": 2,
         "explanation": "第六年。"},
        {"q": "真主在《古兰经》中如何描述侯代比亚和约？",
         "options": ["伟大的胜利", "明显的胜利", "强大的凯旋", "广阔的慈悯"], "answer": 1,
         "explanation": "明显的胜利。"},
        {"q": "在海巴尔，先知 ﷺ 将旗帜交给了谁？",
         "options": ["艾布·伯克尔", "欧麦尔", "阿里·本·阿比·塔利卜", "奥斯曼"], "answer": 2,
         "explanation": "阿里。"},
        {"q": "在穆塔战役中有几位将领殉道？",
         "options": ["两位", "三位", "四位", "五位"], "answer": 1,
         "explanation": "宰德、贾法尔、阿卜杜拉·本·拉瓦哈。"},
        {"q": "辞别朝觐发生在伊历哪一年？",
         "options": ["第八年", "第九年", "第十年", "第十一年"], "answer": 2,
         "explanation": "第十年。"},
        {"q": "先知 ﷺ 在伊历哪一年归真？",
         "options": ["第九年", "第十年", "第十一年", "第十二年"], "answer": 2,
         "explanation": "第十一年。"},
        {"q": "先知 ﷺ 归真时多大年龄？",
         "options": ["60岁", "62岁", "63岁", "65岁"], "answer": 2,
         "explanation": "六十三岁。"},
        {"q": "谁是先知 ﷺ 最小的女儿？",
         "options": ["宰娜卜", "鲁卡娅", "乌姆·库勒苏姆", "法蒂玛"], "answer": 3,
         "explanation": "法蒂玛·扎赫拉。"},
        {"q": "艾布·伯克尔·松迪格的称号是什么？",
         "options": ["法鲁克", "松迪格", "双光者", "真主之剑"], "answer": 1,
         "explanation": "松迪格。"},
        {"q": "欧麦尔·本·哈塔卜的称号是什么？",
         "options": ["松迪格", "法鲁克", "双光者", "乌玛的忠信者"], "answer": 1,
         "explanation": "法鲁克。"},
    ],
    "hi": [
        {"q": "पैग़ंबर ﷺ का जन्म ग्रेगोरियन वर्ष में कब हुआ?",
         "options": ["570 ई.", "571 ई.", "572 ई.", "573 ई."], "answer": 1,
         "explanation": "हाथी के वर्ष (571 ई.)।"},
        {"q": "पैग़ंबर ﷺ की माता का नाम क्या है?",
         "options": ["हलीमा सादिया", "आमिना बिन्त वहब", "ख़दीजा बिन्त ख़ुवैलिद", "फ़ातिमा बिन्त असद"], "answer": 1,
         "explanation": "आमिना बिन्त वहब।"},
        {"q": "पहली वह्य किस गुफा में नाज़िल हुई?",
         "options": ["ग़ार-ए-सौर", "ग़ार-ए-हिरा", "ग़ार-ए-कहफ़", "ग़ार-ए-रक़ीम"], "answer": 1,
         "explanation": "ग़ार-ए-हिरा।"},
        {"q": "क़ुरआन की पहली नाज़िल होने वाली सूरह कौन है?",
         "options": ["अल-फ़ातिहा", "अल-अलक़", "अल-मुद्दस्सिर", "अल-बक़रा"], "answer": 1,
         "explanation": "अल-अलक़।"},
        {"q": "पहली वह्य के समय पैग़ंबर ﷺ की उम्र कितनी थी?",
         "options": ["30 साल", "35 साल", "40 साल", "45 साल"], "answer": 2,
         "explanation": "चालीस वर्ष।"},
        {"q": "पैग़ंबर ﷺ पर सबसे पहले किस औरत ने ईमान लाया?",
         "options": ["आइशा", "ख़दीजा", "फ़ातिमा", "हफ़्सा"], "answer": 1,
         "explanation": "ख़दीजा बिन्त ख़ुवैलिद।"},
        {"q": "आज़ाद मर्दों में सबसे पहले किसने इस्लाम क़बूल किया?",
         "options": ["अबू बक्र सिद्दीक़", "उमर बिन ख़त्ताब", "उस्मान बिन अफ़्फ़ान", "अली बिन अबी तालिब"], "answer": 0,
         "explanation": "अबू बक्र सिद्दीक़।"},
        {"q": "हिजरत में पैग़ंबर ﷺ के साथ कौन थे?",
         "options": ["अली", "अबू बक्र", "उमर", "उस्मान"], "answer": 1,
         "explanation": "अबू बक्र सिद्दीक़।"},
        {"q": "मदीना पहुँचने पर पैग़ंबर ﷺ ने पहली कौन-सी मस्जिद बनाई?",
         "options": ["मस्जिद-ए-नबवी", "मस्जिद-ए-क़ुबा", "मस्जिद-ए-अक़्सा", "मस्जिद-ए-क़िब्लतैन"], "answer": 1,
         "explanation": "मस्जिद-ए-क़ुबा।"},
        {"q": "ग़ज़्वा-ए-बद्र किस हिजरी साल में हुआ?",
         "options": ["पहला", "दूसरा", "तीसरा", "चौथा"], "answer": 1,
         "explanation": "दूसरा।"},
        {"q": "ग़ज़्वा-ए-बद्र में मुसलमानों की तादाद कितनी थी?",
         "options": ["300", "313", "350", "400"], "answer": 1,
         "explanation": "313।"},
        {"q": "ग़ज़्वा-ए-उहुद किस हिजरी साल में हुआ?",
         "options": ["दूसरा", "तीसरा", "चौथा", "पाँचवाँ"], "answer": 1,
         "explanation": "तीसरा।"},
        {"q": "ग़ज़्वा-ए-उहुद में सैयदुश-शुहदा कौन हैं?",
         "options": ["हमज़ा बिन अब्दुल मुत्तलिब", "मुसअब बिन उमैर", "अनस बिन नदर", "सअद बिन रबी"], "answer": 0,
         "explanation": "हमज़ा बिन अब्दुल मुत्तलिब।"},
        {"q": "ग़ज़्वा-ए-ख़ंदक़ किस हिजरी साल में हुआ?",
         "options": ["तीसरा", "चौथा", "पाँचवाँ", "छठा"], "answer": 2,
         "explanation": "पाँचवाँ।"},
        {"q": "ख़ंदक़ खोदने की तजवीज़ किसने दी?",
         "options": ["अबू बक्र", "उमर", "सलमान फ़ारसी", "अली"], "answer": 2,
         "explanation": "सलमान फ़ारसी।"},
        {"q": "सुलह-ए-हुदैबिय्या किस हिजरी साल में हुई?",
         "options": ["चौथा", "पाँचवाँ", "छठा", "सातवाँ"], "answer": 2,
         "explanation": "छठा।"},
        {"q": "अल्लाह ने क़ुरआन में सुलह-ए-हुदैबिय्या को क्या कहा?",
         "options": ["अज़ीम फ़तह", "फ़तह-ए-मुबीन", "बड़ी नुसरत", "वसी रहमत"], "answer": 1,
         "explanation": "फ़तह-ए-मुबीन।"},
        {"q": "ख़ैबर में पैग़ंबर ﷺ ने झंडा किसको दिया?",
         "options": ["अबू बक्र", "उमर", "अली बिन अबी तालिब", "उस्मान"], "answer": 2,
         "explanation": "अली बिन अबी तालिब।"},
        {"q": "ग़ज़्वा-ए-मूता में कितने सरदार शहीद हुए?",
         "options": ["दो", "तीन", "चार", "पाँच"], "answer": 1,
         "explanation": "ज़ैद, जाफ़र, अब्दुल्लाह बिन रवाहा।"},
        {"q": "हज्जतुल विदा किस हिजरी साल में अदा किया गया?",
         "options": ["आठवाँ", "नौवाँ", "दसवाँ", "ग्यारहवाँ"], "answer": 2,
         "explanation": "दसवाँ।"},
        {"q": "पैग़ंबर ﷺ की वफ़ात किस हिजरी साल में हुई?",
         "options": ["नौवाँ", "दसवाँ", "ग्यारहवाँ", "बारहवाँ"], "answer": 2,
         "explanation": "ग्यारहवाँ।"},
        {"q": "वफ़ात के वक़्त पैग़ंबर ﷺ की उम्र कितनी थी?",
         "options": ["60 साल", "62 साल", "63 साल", "65 साल"], "answer": 2,
         "explanation": "तिरसठ।"},
        {"q": "पैग़ंबर ﷺ की सबसे छोटी बेटी कौन हैं?",
         "options": ["ज़ैनब", "रुक़य्या", "उम्मे कुलसूम", "फ़ातिमा"], "answer": 3,
         "explanation": "फ़ातिमा ज़हरा।"},
        {"q": "अबू बक्र सिद्दीक़ का लक़ब क्या है?",
         "options": ["फ़ारूक़", "सिद्दीक़", "ज़ुन-नूरैन", "सैफ़ुल्लाह"], "answer": 1,
         "explanation": "सिद्दीक़।"},
        {"q": "उमर बिन ख़त्ताब का लक़ब क्या है?",
         "options": ["सिद्दीक़", "फ़ारूक़", "ज़ुन-नूरैन", "अमीनुल उम्मत"], "answer": 1,
         "explanation": "फ़ारूक़।"},
    ],
}

# ---------------------------------------------------------------------------
# 4. LOCATIONS
# ---------------------------------------------------------------------------
LOCATIONS = [
    {"key": "makkah", "name": {"ar": "مكة المكرمة", "en": "Makkah", "ur": "مکہ مکرمہ",
                                "id": "Makkah", "tr": "Mekke", "fr": "La Mecque",
                                "es": "La Meca", "ru": "Мекка", "zh": "麦加", "hi": "मक्का"},
     "subtitle": {"ar": "مولد النبي ﷺ وبعثته", "en": "Birthplace & Prophethood",
                  "ur": "نبی ﷺ کی ولادت اور بعثت", "id": "Tempat lahir & kenabian",
                  "tr": "Doğum ve peygamberlik", "fr": "Naissance & prophétie",
                  "es": "Nacimiento y profecía", "ru": "Рождение и пророчество",
                  "zh": "出生地与使命", "hi": "जन्म और नुबुव्वत"},
     "context": {
         "ar": "في مكة وُلد النبي ﷺ ونشأ، وفيها نزل الوحي عليه أول مرة، ومنها انطلقت دعوة التوحيد.",
         "en": "In Makkah the Prophet ﷺ was born and raised, the first revelation descended upon him.",
         "ur": "مکہ مکرمہ میں نبی ﷺ کی ولادت ہوئی اور پرورش پائی۔",
         "id": "Di Makkah Nabi ﷺ dilahirkan dan dibesarkan.",
         "tr": "Mekke'de Peygamber ﷺ doğdu ve büyüdü.",
         "fr": "À La Mecque, le Prophète ﷺ est né et a grandi.",
         "es": "En La Meca nació y creció el Profeta ﷺ.",
         "ru": "В Мекке Пророк ﷺ родился и вырос.",
         "zh": "先知 ﷺ 在麦加出生并成长。",
         "hi": "मक्का में पैग़ंबर ﷺ का जन्म और पालन-पोषण हुआ।",
     }},
    {"key": "hira", "name": {"ar": "غار حراء", "en": "Cave of Hira", "ur": "غارِ حرا",
                              "id": "Gua Hira", "tr": "Hira Mağarası", "fr": "Grotte de Hira",
                              "es": "Cueva de Hira", "ru": "Пещера Хира", "zh": "希拉山洞",
                              "hi": "ग़ार-ए-हिरा"},
     "subtitle": {"ar": "مكان نزول الوحي أول مرة", "en": "First revelation site",
                  "ur": "پہلی وحی کا مقام", "id": "Tempat wahyu pertama",
                  "tr": "İlk vahiy yeri", "fr": "Lieu de la première révélation",
                  "es": "Lugar de la primera revelación", "ru": "Место первого откровения",
                  "zh": "首次启示之地", "hi": "पहली वह्य की जगह"},
     "context": {
         "ar": "في غار حراء تحنّث النبي ﷺ وتعبّد، وفيه نزل جبريل عليه السلام بأول آيات سورة العلق.",
         "en": "In the Cave of Hira the Prophet ﷺ used to retreat and worship.",
         "ur": "غارِ حرا میں نبی ﷺ عبادت کیا کرتے تھے۔",
         "id": "Di Gua Hira Nabi ﷺ berkhalwat.",
         "tr": "Hira Mağarası'nda Peygamber ﷺ inzivaya çekilirdi.",
         "fr": "Dans la grotte de Hira, le Prophète ﷺ s'isolait.",
         "es": "En la Cueva de Hira el Profeta ﷺ se retiraba.",
         "ru": "В пещере Хира Пророк ﷺ уединялся.",
         "zh": "先知 ﷺ 曾在希拉山洞静修。",
         "hi": "ग़ार-ए-हिरा में पैग़ंबर ﷺ इबादत करते थे।",
     }},
    {"key": "taif", "name": {"ar": "الطائف", "en": "Taif", "ur": "طائف", "id": "Taif",
                              "tr": "Taif", "fr": "Taïf", "es": "Taif", "ru": "Таиф",
                              "zh": "塔伊夫", "hi": "ताइफ़"},
     "subtitle": {"ar": "رحلة الدعوة إلى الطائف", "en": "Dawah journey to Taif",
                  "ur": "طائف کی دعوت کا سفر", "id": "Perjalanan dakwah ke Taif",
                  "tr": "Taif'e davet yolculuğu", "fr": "Voyage de la da'wa à Taïf",
                  "es": "Viaje de la dawa a Taif", "ru": "Путь призыва в Таиф",
                  "zh": "塔伊夫宣教之旅", "hi": "ताइफ़ की दावत"},
     "context": {
         "ar": "خرج النبي ﷺ إلى الطائف بعد اشتداد أذى قريش، يدعو ثقيفًا إلى الإسلام.",
         "en": "After Quraysh's persecution intensified, the Prophet ﷺ went to Taif.",
         "ur": "قریش کے ظلم کے بڑھنے پر نبی ﷺ طائف تشریف لے گئے۔",
         "id": "Setelah penindasan Quraisy memuncak, Nabi ﷺ pergi ke Taif.",
         "tr": "Kureyş baskısı artınca Peygamber ﷺ Taif'e gitti.",
         "fr": "Après les persécutions, le Prophète ﷺ se rendit à Taïf.",
         "es": "Tras la persecución, el Profeta ﷺ fue a Taif.",
         "ru": "После гонений Пророк ﷺ отправился в Таиф.",
         "zh": "迫害加剧后，先知 ﷺ 前往塔伊夫。",
         "hi": "क़ुरैश के ज़ुल्म बढ़ने पर पैग़ंबर ﷺ ताइफ़ गए।",
     }},
    {"key": "quba", "name": {"ar": "مسجد قباء", "en": "Quba Mosque", "ur": "مسجدِ قباء",
                              "id": "Masjid Quba", "tr": "Kuba Mescidi", "fr": "Mosquée de Quba",
                              "es": "Mezquita de Quba", "ru": "Мечеть Куба", "zh": "库巴清真寺",
                              "hi": "मस्जिद-ए-क़ुबा"},
     "subtitle": {"ar": "أول مسجد أُسِّس في الإسلام", "en": "First mosque in Islam",
                  "ur": "اسلام کا پہلا مسجد", "id": "Masjid pertama dalam Islam",
                  "tr": "İslam'da ilk mescit", "fr": "Première mosquée de l'islam",
                  "es": "Primera mezquita del Islam", "ru": "Первая мечеть в исламе",
                  "zh": "伊斯兰首座清真寺", "hi": "इस्लाम की पहली मस्जिद"},
     "context": {
         "ar": "عند قدومه ﷺ مهاجرًا نزل بقباء، وأسّس مسجد قباء أول مسجد في الإسلام.",
         "en": "Upon arriving as a migrant, the Prophet ﷺ stayed at Quba.",
         "ur": "ہجرت کے موقع پر نبی ﷺ قباء میں ٹھہرے۔",
         "id": "Saat hijrah, Nabi ﷺ singgah di Quba.",
         "tr": "Hicret sırasında Peygamber ﷺ Kuba'ya uğradı.",
         "fr": "Lors de l'hégire, le Prophète ﷺ séjourna à Quba.",
         "es": "Al emigrar, el Profeta ﷺ se alojó en Quba.",
         "ru": "Во время хиджры Пророк ﷺ остановился в Кубе.",
         "zh": "迁徙途中，先知 ﷺ 在库巴停留。",
         "hi": "हिजरत के मौक़े पर पैग़ंबर ﷺ क़ुबा में ठहरे।",
     }},
    {"key": "madinah", "name": {"ar": "المدينة المنورة", "en": "Madinah", "ur": "مدینہ منورہ",
                                 "id": "Madinah", "tr": "Medine", "fr": "Médine",
                                 "es": "Medina", "ru": "Медина", "zh": "麦地那", "hi": "मदीना"},
     "subtitle": {"ar": "دار الهجرة وموطن الأنصار", "en": "City of Hijrah & Ansar",
                  "ur": "دارُالہجرت اور انصار کا گھر", "id": "Kota Hijrah & Ansar",
                  "tr": "Hicret ve Ensar şehri", "fr": "Cité de l'Hégire",
                  "es": "Ciudad de la Hégira", "ru": "Город хиджры",
                  "zh": "迁徙之城", "hi": "हिजरत का शहर"},
     "context": {
         "ar": "هاجر النبي ﷺ إلى المدينة فبنى المسجد النبوي، وآخى بين المهاجرين والأنصار.",
         "en": "The Prophet ﷺ migrated to Madinah and built the Prophet's Mosque.",
         "ur": "نبی ﷺ مدینہ ہجرت کی اور مسجدِ نبوی تعمیر فرمائی۔",
         "id": "Nabi ﷺ berhijrah ke Madinah dan membangun Masjid Nabawi.",
         "tr": "Peygamber ﷺ Medine'ye hicret etti.",
         "fr": "Le Prophète ﷺ émigra à Médine.",
         "es": "El Profeta ﷺ emigró a Medina.",
         "ru": "Пророк ﷺ совершил хиджру в Медину.",
         "zh": "先知 ﷺ 迁徙至麦地那。",
         "hi": "पैग़ंबर ﷺ ने मदीना की हिजरत की।",
     }},
    {"key": "badr", "name": {"ar": "بدر", "en": "Badr", "ur": "بدر", "id": "Badr",
                              "tr": "Bedir", "fr": "Badr", "es": "Badr", "ru": "Бадр",
                              "zh": "白德尔", "hi": "बद्र"},
     "subtitle": {"ar": "موقع غزوة بدر الكبرى", "en": "Great Battle of Badr",
                  "ur": "غزوۂ بدر کبریٰ", "id": "Perang Badar Besar",
                  "tr": "Büyük Bedir Savaşı", "fr": "Grande bataille de Badr",
                  "es": "Gran batalla de Badr", "ru": "Великая битва при Бадре",
                  "zh": "白德尔大战", "hi": "ग़ज़्वा-ए-बद्र"},
     "context": {
         "ar": "في السنة الثانية للهجرة وقعت غزوة بدر، فأيّد الله المسلمين رغم قلتهم.",
         "en": "In the 2nd year after Hijrah, the Battle of Badr took place.",
         "ur": "دوسری ہجری میں غزوۂ بدر پیش آیا۔",
         "id": "Pada tahun ke-2 Hijrah terjadi Perang Badar.",
         "tr": "Hicretin 2. yılında Bedir Savaşı oldu.",
         "fr": "La 2e année de l'Hégire eut lieu la bataille de Badr.",
         "es": "En el año 2 de la Hégira tuvo lugar la batalla de Badr.",
         "ru": "Во 2-м году хиджры произошла битва при Бадре.",
         "zh": "迁徙第二年发生白德尔战役。",
         "hi": "हिजरी के दूसरे साल ग़ज़्वा-ए-बद्र हुआ।",
     }},
    {"key": "uhud", "name": {"ar": "جبل أحد", "en": "Mount Uhud", "ur": "جبلِ اُحد",
                              "id": "Gunung Uhud", "tr": "Uhud Dağı", "fr": "Mont Uhud",
                              "es": "Monte Uhud", "ru": "Гора Ухуд", "zh": "伍侯德山",
                              "hi": "जबल-ए-उहुद"},
     "subtitle": {"ar": "موقع غزوة أحد", "en": "Battle of Uhud",
                  "ur": "غزوۂ اُحد", "id": "Perang Uhud", "tr": "Uhud Savaşı",
                  "fr": "Bataille d'Uhud", "es": "Batalla de Uhud",
                  "ru": "Битва при Ухуде", "zh": "伍侯德战役", "hi": "ग़ज़्वा-ए-उहुद"},
     "context": {
         "ar": "في السنة الثالثة للهجرة وقعت غزوة أحد، واستُشهد فيها سبعون من الصحابة.",
         "en": "In the 3rd year after Hijrah the Battle of Uhud occurred.",
         "ur": "تیسری ہجری میں غزوۂ اُحد پیش آیا۔",
         "id": "Pada tahun ke-3 Hijrah terjadi Perang Uhud.",
         "tr": "Hicretin 3. yılında Uhud Savaşı oldu.",
         "fr": "La 3e année de l'Hégire eut lieu la bataille d'Uhud.",
         "es": "En el año 3 de la Hégira ocurrió la batalla de Uhud.",
         "ru": "В 3-м году хиджры произошла битва при Ухуде.",
         "zh": "迁徙第三年发生伍侯德战役。",
         "hi": "हिजरी के तीसरे साल ग़ज़्वा-ए-उहुद हुआ।",
     }},
    {"key": "khandaq", "name": {"ar": "موقع الخندق", "en": "Trench (Khandaq)", "ur": "خندق",
                                 "id": "Perang Khandaq", "tr": "Hendek",
                                 "fr": "Tranchée (Khandaq)", "es": "Trinchera (Jandaq)",
                                 "ru": "Ров (Хандак)", "zh": "壕沟战役", "hi": "ख़ंदक़"},
     "subtitle": {"ar": "موقع غزوة الخندق (الأحزاب)", "en": "Battle of the Trench",
                  "ur": "غزوۂ خندق", "id": "Perang Khandaq", "tr": "Hendek Savaşı",
                  "fr": "Bataille de la Tranchée", "es": "Batalla de la Trinchera",
                  "ru": "Битва у рва", "zh": "壕沟战役", "hi": "ग़ज़्वा-ए-ख़ंदक़"},
     "context": {
         "ar": "في السنة الخامسة للهجرة تحزّبت القبائل على المدينة، فحفر المسلمون الخندق.",
         "en": "In the 5th year after Hijrah, the tribes allied against Madinah.",
         "ur": "پانچویں ہجری میں قبائل مدینہ کے خلاف جمع ہوئے۔",
         "id": "Pada tahun ke-5 Hijrah, kabilah bersekutu melawan Madinah.",
         "tr": "Hicretin 5. yılında kabileler Medine'ye karşı birleşti.",
         "fr": "La 5e année de l'Hégire, les tribus s'allièrent contre Médine.",
         "es": "En el año 5 de la Hégira, las tribus se aliaron contra Medina.",
         "ru": "В 5-м году хиджры племена объединились против Медины.",
         "zh": "迁徙第五年，各部落结盟围攻麦地那。",
         "hi": "हिजरी के पाँचवें साल क़बीले मदीना के ख़िलाफ़ जमा हुए।",
     }},
    {"key": "hudaybiyyah", "name": {"ar": "الحديبية", "en": "Hudaybiyyah", "ur": "حدیبیہ",
                                     "id": "Hudaibiyah", "tr": "Hudeybiye",
                                     "fr": "Hudaybiyya", "es": "Hudaybiyyah",
                                     "ru": "Худайбия", "zh": "侯代比亚", "hi": "हुदैबिय्या"},
     "subtitle": {"ar": "موقع صلح الحديبية", "en": "Treaty of Hudaybiyyah",
                  "ur": "صلحِ حدیبیہ", "id": "Perjanjian Hudaibiyah",
                  "tr": "Hudeybiye Antlaşması", "fr": "Traité de Hudaybiyya",
                  "es": "Tratado de Hudaybiyyah", "ru": "Худайбийский договор",
                  "zh": "侯代比亚和约", "hi": "सुलह-ए-हुदैबिय्या"},
     "context": {
         "ar": "في السنة السادسة للهجرة وقع صلح الحديبية، وقد سمّاه الله فتحًا مبينًا.",
         "en": "In the 6th year after Hijrah, the Treaty of Hudaybiyyah was concluded.",
         "ur": "چھٹی ہجری میں صلحِ حدیبیہ ہوا۔",
         "id": "Pada tahun ke-6 Hijrah terjadi Perjanjian Hudaibiyah.",
         "tr": "Hicretin 6. yılında Hudeybiye Antlaşması yapıldı.",
         "fr": "La 6e année de l'Hégire, le traité de Hudaybiyya fut conclu.",
         "es": "En el año 6 de la Hégira se concluyó el tratado.",
         "ru": "В 6-м году хиджры был заключён договор.",
         "zh": "迁徙第六年缔结侯代比亚和约。",
         "hi": "हिजरी के छठे साल सुलह-ए-हुदैबिय्या हुई।",
     }},
    {"key": "khaybar", "name": {"ar": "خيبر", "en": "Khaybar", "ur": "خیبر", "id": "Khaybar",
                                 "tr": "Hayber", "fr": "Khaybar", "es": "Jaybar",
                                 "ru": "Хайбар", "zh": "海巴尔", "hi": "ख़ैबर"},
     "subtitle": {"ar": "موقع غزوة خيبر", "en": "Battle of Khaybar",
                  "ur": "غزوۂ خیبر", "id": "Perang Khaybar", "tr": "Hayber Savaşı",
                  "fr": "Bataille de Khaybar", "es": "Batalla de Jaybar",
                  "ru": "Битва при Хайбаре", "zh": "海巴尔战役", "hi": "ग़ज़्वा-ए-ख़ैबर"},
     "context": {
         "ar": "في السنة السابعة للهجرة فتح المسلمون حصون خيبر، وأعطى النبي ﷺ الراية لعلي.",
         "en": "In the 7th year after Hijrah the Muslims conquered Khaybar.",
         "ur": "ساتویں ہجری میں مسلمانوں نے خیبر فتح کیا۔",
         "id": "Pada tahun ke-7 Hijrah kaum Muslimin menaklukkan Khaybar.",
         "tr": "Hicretin 7. yılında Hayber fethedildi.",
         "fr": "La 7e année de l'Hégire, les musulmans conquirent Khaybar.",
         "es": "En el año 7 de la Hégira los musulmanes conquistaron Jaybar.",
         "ru": "В 7-м году хиджры мусульмане завоевали Хайбар.",
         "zh": "迁徙第七年，穆斯林攻克海巴尔。",
         "hi": "हिजरी के सातवें साल मुसलमानों ने ख़ैबर फ़तह किया।",
     }},
    {"key": "mutah", "name": {"ar": "مؤتة", "en": "Mu'tah", "ur": "موتہ", "id": "Mu'tah",
                               "tr": "Mute", "fr": "Mu'ta", "es": "Mu'ta", "ru": "Мута",
                               "zh": "穆塔", "hi": "मूता"},
     "subtitle": {"ar": "موقع غزوة مؤتة", "en": "Battle of Mu'tah",
                  "ur": "غزوۂ موتہ", "id": "Perang Mu'tah", "tr": "Mute Savaşı",
                  "fr": "Bataille de Mu'ta", "es": "Batalla de Mu'ta",
                  "ru": "Битва при Муте", "zh": "穆塔战役", "hi": "ग़ज़्वा-ए-मूता"},
     "context": {
         "ar": "في السنة الثامنة للهجرة وقعت غزوة مؤتة، واستُشهد فيها القادة الثلاثة.",
         "en": "In the 8th year after Hijrah the Battle of Mu'tah took place.",
         "ur": "آٹھویں ہجری میں غزوۂ موتہ پیش آیا۔",
         "id": "Pada tahun ke-8 Hijrah terjadi Perang Mu'tah.",
         "tr": "Hicretin 8. yılında Mute Savaşı oldu.",
         "fr": "La 8e année de l'Hégire eut lieu la bataille de Mu'ta.",
         "es": "En el año 8 de la Hégira ocurrió la batalla de Mu'ta.",
         "ru": "В 8-м году хиджры произошла битва при Муте.",
         "zh": "迁徙第八年发生穆塔战役。",
         "hi": "हिजरी के आठवें साल ग़ज़्वा-ए-मूता हुआ।",
     }},
    {"key": "tabuk", "name": {"ar": "تبوك", "en": "Tabuk", "ur": "تبوک", "id": "Tabuk",
                               "tr": "Tebük", "fr": "Tabouk", "es": "Tabuk", "ru": "Табук",
                               "zh": "塔布克", "hi": "तबूक"},
     "subtitle": {"ar": "موقع غزوة تبوك", "en": "Expedition of Tabuk",
                  "ur": "غزوۂ تبوک", "id": "Ekspedisi Tabuk", "tr": "Tebük Seferi",
                  "fr": "Expédition de Tabouk", "es": "Expedición de Tabuk",
                  "ru": "Поход на Табук", "zh": "塔布克远征", "hi": "ग़ज़्वा-ए-तबूक"},
     "context": {
         "ar": "في السنة التاسعة للهجرة خرج النبي ﷺ في غزوة تبوك في حرّ شديد.",
         "en": "In the 9th year after Hijrah the Prophet ﷺ set out for Tabuk.",
         "ur": "نویں ہجری میں نبی ﷺ غزوۂ تبوک کے لیے نکلے۔",
         "id": "Pada tahun ke-9 Hijrah Nabi ﷺ berangkat ke Tabuk.",
         "tr": "Hicretin 9. yılında Peygamber ﷺ Tebük'e çıktı.",
         "fr": "La 9e année de l'Hégire, le Prophète ﷺ partit pour Tabouk.",
         "es": "En el año 9 de la Hégira el Profeta ﷺ partió hacia Tabuk.",
         "ru": "В 9-м году хиджры Пророк ﷺ выступил в Табук.",
         "zh": "迁徙第九年，先知 ﷺ 出征塔布克。",
         "hi": "हिजरी के नौवें साल पैग़ंबर ﷺ ग़ज़्वा-ए-तबूक के लिए निकले।",
     }},
    {"key": "arafat", "name": {"ar": "جبل عرفات", "en": "Mount Arafat", "ur": "جبلِ عرفات",
                                "id": "Gunung Arafat", "tr": "Arafat Dağı",
                                "fr": "Mont Arafat", "es": "Monte Arafat",
                                "ru": "Гора Арафат", "zh": "阿拉法特山", "hi": "जबल-ए-अरफ़ात"},
     "subtitle": {"ar": "موقع حجة الوداع", "en": "Farewell Pilgrimage",
                  "ur": "حجۃ الوداع", "id": "Haji Wada'", "tr": "Veda Haccı",
                  "fr": "Pèlerinage d'adieu", "es": "Peregrinación de despedida",
                  "ru": "Прощальное паломничество", "zh": "辞别朝觐", "hi": "हज्जतुल विदा"},
     "context": {
         "ar": "في السنة العاشرة للهجرة حجّ النبي ﷺ حجة الوداع، وخطب في عرفة خطبةً جامعة.",
         "en": "In the 10th year after Hijrah the Prophet ﷺ performed the Farewell Pilgrimage.",
         "ur": "دسویں ہجری میں نبی ﷺ نے حجۃ الوداع ادا کیا۔",
         "id": "Pada tahun ke-10 Hijrah Nabi ﷺ menunaikan Haji Wada'.",
         "tr": "Hicretin 10. yılında Peygamber ﷺ Veda Haccı'nı yaptı.",
         "fr": "La 10e année de l'Hégire, le Prophète ﷺ accomplit le Pèlerinage d'adieu.",
         "es": "En el año 10 de la Hégira el Profeta ﷺ realizó la Peregrinación de despedida.",
         "ru": "В 10-м году хиджры Пророк ﷺ совершил прощальное паломничество.",
         "zh": "迁徙第十年，先知 ﷺ 完成辞别朝觐。",
         "hi": "हिजरी के दसवें साल पैग़ंबर ﷺ ने हज्जतुल विदा अदा किया।",
     }},
]

# ---------------------------------------------------------------------------
# 5. UI TRANSLATIONS
# ---------------------------------------------------------------------------
UI_TEXT = {
    "ar": {"app_name": "مُبين AI", "tagline": "منصة ذكية تخدم السيرة النبوية بلغات العالم",
           "select_lang": "اختر اللغة", "events_title": "أحداث السيرة والغزوات والمعارك",
           "select_event": "اختر الحدث", "chat_title": "اسأل مُبين AI",
           "chat_placeholder": "اكتب سؤالك حول السيرة النبوية...", "chat_button": "إرسال",
           "spinner": "جارٍ البحث في كتاب «الرحيق المختوم»...", "about_title": "عن الموقع",
           "about_text": "موقع يعتمد على كتاب «الرحيق المختوم» للشيخ صفي الرحمن المباركفوري.",
           "events_hint": "اختر حدثاً لقراءة نبذة عنه، أو اسأل مُبين AI مباشرة.",
           "suggestions": "💡 اقتراحات سريعة", "menu": "☰ القائمة",
           "rtl": True, "dir": "rtl"},
    "en": {"app_name": "Mubeen AI", "tagline": "A smart platform serving the Prophetic Seerah",
           "select_lang": "Select Language", "events_title": "Seerah Events, Battles & Expeditions",
           "select_event": "Select an event", "chat_title": "Ask Mubeen AI",
           "chat_placeholder": "Type your question about the Seerah...", "chat_button": "Send",
           "spinner": "Searching 'The Sealed Nectar'...", "about_title": "About",
           "about_text": "A site grounded in 'The Sealed Nectar' by Safiur Rahman Mubarakpuri.",
           "events_hint": "Select an event or ask Mubeen AI directly.",
           "suggestions": "💡 Quick prompts", "menu": "☰ Menu",
           "rtl": False, "dir": "ltr"},
    "ur": {"app_name": "مبین AI", "tagline": "عالمی زبانوں میں سیرت نبوی کی خدمت کرنے والا ذہین پلیٹ فارم",
           "select_lang": "زبان منتخب کریں", "events_title": "سیرت کے واقعات، غزوات اور معرکے",
           "select_event": "واقعہ منتخب کریں", "chat_title": "مبین AI سے پوچھیں",
           "chat_placeholder": "سیرت نبوی کے بارے میں اپنا سوال لکھیں...", "chat_button": "بھیجیں",
           "spinner": "«الرحيق المختوم» میں تلاش ہو رہی ہے...", "about_title": "سائٹ کے بارے میں",
           "about_text": "یہ سائٹ شیخ صفی الرحمن مبارکپوری کی کتاب پر مبنی ہے۔",
           "events_hint": "کوئی واقعہ منتخب کریں یا مبین AI سے پوچھیں۔",
           "suggestions": "💡 فوری تجاویز", "menu": "☰ مینو",
           "rtl": True, "dir": "rtl"},
    "id": {"app_name": "Mubeen AI", "tagline": "Platform cerdas yang melayani Sirah Nabawiyah",
           "select_lang": "Pilih Bahasa", "events_title": "Peristiwa, Perang & Ekspedisi Sirah",
           "select_event": "Pilih peristiwa", "chat_title": "Tanya Mubeen AI",
           "chat_placeholder": "Tulis pertanyaan Anda...", "chat_button": "Kirim",
           "spinner": "Menelusuri 'The Sealed Nectar'...", "about_title": "Tentang",
           "about_text": "Situs yang bersumber dari 'The Sealed Nectar'.",
           "events_hint": "Pilih peristiwa atau tanya Mubeen AI langsung.",
           "suggestions": "💡 Saran cepat", "menu": "☰ Menu",
           "rtl": False, "dir": "ltr"},
    "tr": {"app_name": "Mubeen AI", "tagline": "Siyer-i Nebi'ye dünya dillerinde hizmet eden platform",
           "select_lang": "Dil Seçin", "events_title": "Siyer Olayları, Savaşlar ve Seferler",
           "select_event": "Bir olay seçin", "chat_title": "Mubeen AI'ya Sor",
           "chat_placeholder": "Siyer hakkında sorunuzu yazın...", "chat_button": "Gönder",
           "spinner": "'The Sealed Nectar' taranıyor...", "about_title": "Hakkında",
           "about_text": "Safiur Rahman Mubarakpuri'nin eserine dayanır.",
           "events_hint": "Bir olay seçin veya Mubeen AI'ya sorun.",
           "suggestions": "💡 Hızlı öneriler", "menu": "☰ Menü",
           "rtl": False, "dir": "ltr"},
    "fr": {"app_name": "Mubeen AI", "tagline": "Plateforme intelligente au service de la Sîra",
           "select_lang": "Choisir la langue", "events_title": "Événements, Batailles & Expéditions",
           "select_event": "Sélectionner un événement", "chat_title": "Demander à Mubeen AI",
           "chat_placeholder": "Écrivez votre question...", "chat_button": "Envoyer",
           "spinner": "Recherche dans 'The Sealed Nectar'...", "about_title": "À propos",
           "about_text": "Un site basé sur 'The Sealed Nectar'.",
           "events_hint": "Sélectionnez un événement ou demandez à Mubeen AI.",
           "suggestions": "💡 Suggestions rapides", "menu": "☰ Menu",
           "rtl": False, "dir": "ltr"},
    "es": {"app_name": "Mubeen AI", "tagline": "Plataforma inteligente al servicio de la Sira",
           "select_lang": "Seleccionar idioma", "events_title": "Eventos, Batallas y Expediciones",
           "select_event": "Selecciona un evento", "chat_title": "Pregunta a Mubeen AI",
           "chat_placeholder": "Escribe tu pregunta...", "chat_button": "Enviar",
           "spinner": "Buscando en 'The Sealed Nectar'...", "about_title": "Acerca de",
           "about_text": "Un sitio basado en 'The Sealed Nectar'.",
           "events_hint": "Selecciona un evento o pregunta a Mubeen AI.",
           "suggestions": "💡 Sugerencias rápidas", "menu": "☰ Menú",
           "rtl": False, "dir": "ltr"},
    "ru": {"app_name": "Mubeen AI", "tagline": "Умная платформа, служащая Сире",
           "select_lang": "Выберите язык", "events_title": "События, битвы и походы Сиры",
           "select_event": "Выберите событие", "chat_title": "Спросить Mubeen AI",
           "chat_placeholder": "Напишите вопрос...", "chat_button": "Отправить",
           "spinner": "Поиск в 'The Sealed Nectar'...", "about_title": "О сайте",
           "about_text": "Сайт основан на книге 'The Sealed Nectar'.",
           "events_hint": "Выберите событие или спросите Mubeen AI.",
           "suggestions": "💡 Быстрые подсказки", "menu": "☰ Меню",
           "rtl": False, "dir": "ltr"},
    "zh": {"app_name": "Mubeen AI", "tagline": "以世界多种语言服务先知传记的智能平台",
           "select_lang": "选择语言", "events_title": "先知传记事件、战役与远征",
           "select_event": "选择事件", "chat_title": "询问 Mubeen AI",
           "chat_placeholder": "请输入您的问题...", "chat_button": "发送",
           "spinner": "正在检索《The Sealed Nectar》...", "about_title": "关于",
           "about_text": "本站基于《The Sealed Nectar》。",
           "events_hint": "选择事件或直接询问 Mubeen AI。",
           "suggestions": "💡 快速提示", "menu": "☰ 菜单",
           "rtl": False, "dir": "ltr"},
    "hi": {"app_name": "Mubeen AI", "tagline": "विश्व की भाषाओं में सीरत की सेवा करने वाला प्लेटफ़ॉर्म",
           "select_lang": "भाषा चुनें", "events_title": "सीरत की घटनाएँ, लड़ाइयाँ और अभियान",
           "select_event": "घटना चुनें", "chat_title": "Mubeen AI से पूछें",
           "chat_placeholder": "सीरत के बारे में अपना प्रश्न लिखें...", "chat_button": "भेजें",
           "spinner": "'The Sealed Nectar' में खोज रहे हैं...", "about_title": "परिचय",
           "about_text": "यह साइट 'The Sealed Nectar' पर आधारित है।",
           "events_hint": "कोई घटना चुनें या Mubeen AI से पूछें।",
           "suggestions": "💡 त्वरित सुझाव", "menu": "☰ मेनू",
           "rtl": False, "dir": "ltr"},
}

LANG_LABELS = {
    "ar": "🇸🇦 العربية", "en": "🇬🇧 English", "ur": "🇵🇰 اُردو",
    "id": "🇮🇩 Bahasa Indonesia", "tr": "🇹🇷 Türkçe", "fr": "🇫🇷 Français",
    "es": "🇪🇸 Español", "ru": "🇷🇺 Русский", "zh": "🇨🇳 中文", "hi": "🇮🇳 हिन्दी",
}

LANG_NAMES_FOR_PROMPT = {
    "ar": "Arabic (العربية)", "en": "English", "ur": "Urdu (اُردو)",
    "id": "Indonesian (Bahasa Indonesia)", "tr": "Turkish (Türkçe)",
    "fr": "French (Français)", "es": "Spanish (Español)", "ru": "Russian (Русский)",
    "zh": "Chinese (中文)", "hi": "Hindi (हिन्दी)",
}

SUGGESTIONS = {
    "ar": ["ما هي فوائد غزوة بدر؟", "ما الدروس المستفادة من صلح الحديبية؟",
‎           "ما العبر من غزوة أحد؟", "كيف كانت أخلاق النبي ﷺ مع أهل مكة؟"],
    "en": ["What are the lessons from the Battle of Badr?",
           "What wisdom is found in the Treaty of Hudaybiyyah?",
           "What lessons came from the Battle of Uhud?",
           "How was the Prophet's ﷺ character with the people of Makkah?"],
    "ur": ["غزوۂ بدر کے فوائد کیا ہیں؟", "صلح حدیبیہ سے کیا سبق ملتا ہے؟",
‎           "غزوۂ اُحد سے کیا عبرت ہے؟", "نبی ﷺ کا اخلاق اہلِ مکہ کے ساتھ کیسا تھا؟"],
    "id": ["Apa pelajaran dari Perang Badar?", "Apa hikmah dari Perjanjian Hudaibiyah?",
           "Apa pelajaran dari Perang Uhud?", "Bagaimana akhlak Nabi ﷺ terhadap penduduk Makkah?"],
    "tr": ["Bedir Savaşı'ndan çıkarılacak dersler nelerdir?",
           "Hudeybiye Antlaşması'ndaki hikmet nedir?",
           "Uhud Savaşı'ndan hangi dersler çıkarıldı?",
           "Peygamber ﷺ'in Mekke halkına karşı ahlakı nasıldı?"],
    "fr": ["Quelles leçons tirer de la bataille de Badr ?",
           "Quelle sagesse dans le traité de Hudaybiyya ?",
           "Quelles leçons de la bataille d'Uhud ?",
           "Quel était le caractère du Prophète ﷺ avec les gens de La Mecque ?"],
    "es": ["¿Qué lecciones hay en la batalla de Badr?",
           "¿Qué sabiduría hay en el tratado de Hudaybiyyah?",
           "¿Qué lecciones dejó la batalla de Uhud?",
           "¿Cómo era el carácter del Profeta ﷺ con la gente de La Meca?"],
    "ru": ["Какие уроки из битвы при Бадре?",
           "В чём мудрость Худайбийского договора?",
           "Какие уроки из битвы при Ухуде?",
           "Каким был нрав Пророка ﷺ с жителями Мекки?"],
    "zh": ["白德尔战役的教训是什么？", "侯代比亚和约中的智慧是什么？",
           "伍侯德战役的教训是什么？", "先知 ﷺ 对麦加人的品格如何？"],
    "hi": ["बद्र की लड़ाई से क्या सबक़ मिलते हैं?", "सुलह-ए-हुदैबिय्या में क्या हिकमत है?",
           "उहुद की लड़ाई से क्या सबक़ मिले?", "पैग़ंबर ﷺ का अख़लाक़ मक्का वालों के साथ कैसा था?"],
}

# ---------------------------------------------------------------------------
# 6. QUIZ UI LABELS
# ---------------------------------------------------------------------------
QUIZ_LABELS = {
    "ar": {"quiz_title": "📝 اختبار السيرة النبوية",
           "quiz_intro": "اختبر معرفتك بالسيرة النبوية عبر 10 أسئلة عشوائية من بنك يحتوي على 25 سؤالاً.",
           "question_of": "السؤال {current} من {total}",
           "next_button": "السؤال التالي →", "finish_button": "إظهار النتيجة",
           "check_button": "تحقق من الإجابة", "start_button": "▶️ ابدأ الاختبار",
           "exit_button": "🚪 الخروج من الاختبار",
           "explanation_label": "📖 التوضيح:", "your_score": "نتيجتك النهائية",
           "excellent": "🏆 ممتاز! أنت خبير في السيرة النبوية",
           "very_good": "🌟 جيد جدًا! معرفتك بالسيرة قوية",
           "good": "👍 جيد! تحتاج إلى مراجعة بعض الأحداث",
           "try_again": "📚 حاول مرة أخرى!",
           "restart_button": "🔄 إعادة الاختبار",
           "please_select": "⚠️ اختر إجابة أولاً",
           "page_home": "🏠 الرئيسية", "page_quiz": "📝 اختبار السيرة",
           "questions": "أسئلة"},
    "en": {"quiz_title": "📝 Seerah Quiz",
           "quiz_intro": "Test your knowledge with 10 random questions from a bank of 25.",
           "question_of": "Question {current} of {total}",
           "next_button": "Next Question →", "finish_button": "Show Result",
           "check_button": "Check Answer", "start_button": "▶️ Start Quiz",
           "exit_button": "🚪 Exit Quiz",
           "explanation_label": "📖 Explanation:", "your_score": "Your Final Score",
           "excellent": "🏆 Excellent! You are a Seerah expert",
           "very_good": "🌟 Very good! Your knowledge is strong",
           "good": "👍 Good! You need to review some events",
           "try_again": "📚 Try again!",
           "restart_button": "🔄 Restart Quiz",
           "please_select": "⚠️ Please select an answer",
           "page_home": "🏠 Home", "page_quiz": "📝 Seerah Quiz",
           "questions": "Questions"},
    "ur": {"quiz_title": "📝 سیرت نبوی کا امتحان",
           "quiz_intro": "25 سوالوں کے ذخیرے سے 10 بے ترتیب سوالات۔",
           "question_of": "سوال {current} از {total}",
           "next_button": "اگلا سوال →", "finish_button": "نتیجہ دکھائیں",
           "check_button": "جواب چیک کریں", "start_button": "▶️ امتحان شروع کریں",
           "exit_button": "🚪 امتحان سے باہر نکلیں",
           "explanation_label": "📖 وضاحت:", "your_score": "آپ کا حتمی نتیجہ",
           "excellent": "🏆 بہترین!", "very_good": "🌟 بہت اچھا!",
           "good": "👍 اچھا!", "try_again": "📚 دوبارہ کوشش کریں!",
           "restart_button": "🔄 دوبارہ امتحان",
           "please_select": "⚠️ پہلے جواب منتخب کریں",
           "page_home": "🏠 مرکزی صفحہ", "page_quiz": "📝 سیرت کا امتحان",
           "questions": "سوالات"},
    "id": {"quiz_title": "📝 Kuis Sirah",
           "quiz_intro": "Uji pengetahuan Anda dengan 10 pertanyaan acak dari 25.",
           "question_of": "Pertanyaan {current} dari {total}",
           "next_button": "Pertanyaan Berikutnya →", "finish_button": "Tampilkan Hasil",
           "check_button": "Periksa Jawaban", "start_button": "▶️ Mulai Kuis",
           "exit_button": "🚪 Keluar dari Kuis",
           "explanation_label": "📖 Penjelasan:", "your_score": "Skor Akhir Anda",
           "excellent": "🏆 Luar biasa!", "very_good": "🌟 Sangat baik!",
           "good": "👍 Bagus!", "try_again": "📚 Coba lagi!",
           "restart_button": "🔄 Mulai Ulang",
           "please_select": "⚠️ Pilih jawaban dulu",
           "page_home": "🏠 Beranda", "page_quiz": "📝 Kuis Sirah",
           "questions": "Pertanyaan"},
    "tr": {"quiz_title": "📝 Siyer Sınavı",
           "quiz_intro": "25 sorudan 10 rastgele soruyla bilginizi test edin.",
           "question_of": "Soru {current} / {total}",
           "next_button": "Sonraki Soru →", "finish_button": "Sonucu Göster",
           "check_button": "Cevabı Kontrol Et", "start_button": "▶️ Sınava Başla",
           "exit_button": "🚪 Sınavdan Çık",
           "explanation_label": "📖 Açıklama:", "your_score": "Final Puanınız",
           "excellent": "🏆 Mükemmel!", "very_good": "🌟 Çok iyi!",
           "good": "👍 İyi!", "try_again": "📚 Tekrar deneyin!",
           "restart_button": "🔄 Yeniden Başlat",
           "please_select": "⚠️ Önce bir cevap seçin",
           "page_home": "🏠 Ana Sayfa", "page_quiz": "📝 Siyer Sınavı",
           "questions": "Soru"},
    "fr": {"quiz_title": "📝 Quiz Sîra",
           "quiz_intro": "Testez vos connaissances avec 10 questions aléatoires sur 25.",
           "question_of": "Question {current} sur {total}",
           "next_button": "Question Suivante →", "finish_button": "Afficher le Résultat",
           "check_button": "Vérifier", "start_button": "▶️ Commencer",
           "exit_button": "🚪 Quitter le Quiz",
           "explanation_label": "📖 Explication :", "your_score": "Votre Score Final",
           "excellent": "🏆 Excellent !", "very_good": "🌟 Très bien !",
           "good": "👍 Bien !", "try_again": "📚 Réessayez !",
           "restart_button": "🔄 Recommencer",
           "please_select": "⚠️ Sélectionnez une réponse",
           "page_home": "🏠 Accueil", "page_quiz": "📝 Quiz Sîra",
           "questions": "Questions"},
    "es": {"quiz_title": "📝 Cuestionario de Sira",
           "quiz_intro": "Pon a prueba tu conocimiento con 10 preguntas aleatorias de 25.",
           "question_of": "Pregunta {current} de {total}",
           "next_button": "Siguiente →", "finish_button": "Mostrar Resultado",
           "check_button": "Verificar", "start_button": "▶️ Iniciar",
           "exit_button": "🚪 Salir del Cuestionario",
           "explanation_label": "📖 Explicación:", "your_score": "Tu Puntuación Final",
           "excellent": "🏆 ¡Excelente!", "very_good": "🌟 ¡Muy bien!",
           "good": "👍 ¡Bien!", "try_again": "📚 ¡Inténtalo de nuevo!",
           "restart_button": "🔄 Reiniciar",
           "please_select": "⚠️ Selecciona una respuesta",
           "page_home": "🏠 Inicio", "page_quiz": "📝 Cuestionario",
           "questions": "Preguntas"},
    "ru": {"quiz_title": "📝 Викторина по Сире",
           "quiz_intro": "Проверьте знания через 10 случайных вопросов из 25.",
           "question_of": "Вопрос {current} из {total}",
           "next_button": "Следующий →", "finish_button": "Показать Результат",
           "check_button": "Проверить", "start_button": "▶️ Начать",
           "exit_button": "🚪 Выйти из Викторины",
           "explanation_label": "📖 Объяснение:", "your_score": "Ваш Счёт",
           "excellent": "🏆 Отлично!", "very_good": "🌟 Очень хорошо!",
           "good": "👍 Хорошо!", "try_again": "📚 Попробуйте снова!",
           "restart_button": "🔄 Начать Заново",
           "please_select": "⚠️ Выберите ответ",
           "page_home": "🏠 Главная", "page_quiz": "📝 Викторина",
           "questions": "Вопросов"},
    "zh": {"quiz_title": "📝 先知传记测验",
           "quiz_intro": "通过25题中随机抽取的10道题测试您的知识。",
           "question_of": "第 {current} 题，共 {total} 题",
           "next_button": "下一题 →", "finish_button": "显示结果",
           "check_button": "检查答案", "start_button": "▶️ 开始测验",
           "exit_button": "🚪 退出测验",
           "explanation_label": "📖 解释：", "your_score": "您的最终得分",
           "excellent": "🏆 优秀！", "very_good": "🌟 很好！",
           "good": "👍 不错！", "try_again": "📚 再试一次！",
           "restart_button": "🔄 重新开始",
           "please_select": "⚠️ 请先选择答案",
           "page_home": "🏠 首页", "page_quiz": "📝 测验",
           "questions": "题"},
    "hi": {"quiz_title": "📝 सीरत प्रश्नोत्तरी",
           "quiz_intro": "25 प्रश्नों से 10 यादृच्छिक प्रश्नों के साथ अपना ज्ञान परखें।",
           "question_of": "प्रश्न {current} / {total}",
           "next_button": "अगला प्रश्न →", "finish_button": "परिणाम दिखाएँ",
           "check_button": "उत्तर जाँचें", "start_button": "▶️ प्रश्नोत्तरी शुरू करें",
           "exit_button": "🚪 प्रश्नोत्तरी से बाहर",
           "explanation_label": "📖 व्याख्या:", "your_score": "आपका अंतिम स्कोर",
           "excellent": "🏆 उत्कृष्ट!", "very_good": "🌟 बहुत अच्छा!",
           "good": "👍 अच्छा!", "try_again": "📚 फिर कोशिश करें!",
           "restart_button": "🔄 पुनः आरंभ करें",
           "please_select": "⚠️ पहले उत्तर चुनें",
           "page_home": "🏠 होम", "page_quiz": "📝 प्रश्नोत्तरी",
           "questions": "प्रश्न"},
}

# ---------------------------------------------------------------------------
# 7. SESSION STATE
# ---------------------------------------------------------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_key" not in st.session_state:
    st.session_state.selected_key = LOCATIONS[0]["key"]
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "quiz_current" not in st.session_state:
    st.session_state.quiz_current = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_answered" not in st.session_state:
    st.session_state.quiz_answered = False
if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False
if "quiz_selected" not in st.session_state:
    st.session_state.quiz_selected = None
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []
if "close_menu" not in st.session_state:
    st.session_state.close_menu = False

# ---------------------------------------------------------------------------
# 8. HELPERS
# ---------------------------------------------------------------------------
def location_name(loc, lang):
    return loc["name"].get(lang, loc["name"]["en"])

def location_subtitle(loc, lang):
    return loc["subtitle"].get(lang, loc["subtitle"]["en"])

def location_context(loc, lang):
    return loc["context"].get(lang, loc["context"]["en"])

def _get_secret(name):
    key = os.environ.get(name)
    if key:
        return key.strip()
    try:
        key = st.secrets.get(name)
    except Exception:
        key = None
    if key:
        return str(key).strip()
    return None

# ---------------------------------------------------------------------------
# 9. AI
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_gemini_client():
    api_key = _get_secret("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        from google import genai
        return genai.Client(api_key=api_key)
    except Exception:
        return None


def call_gemini(prompt, system_instruction):
    client = get_gemini_client()
    if client is None:
        return ""
    try:
        from google.genai import types
    except Exception:
        return ""
    for model_name in ["gemini-2.5-flash", "gemini-2.0-flash"]:
        try:
            response = client.models.generate_content(
                model=model_name, contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction, temperature=0.3),
            )
            text = getattr(response, "text", None)
            if text and text.strip():
                return text.strip()
        except Exception:
            continue
    return ""


def call_groq(prompt, system_instruction):
    groq_key = _get_secret("GROQ_API_KEY")
    if not groq_key:
        return ""
    for model_name in ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]:
        try:
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {groq_key}",
                         "Content-Type": "application/json"},
                json={"model": model_name,
                      "messages": [{"role": "system", "content": system_instruction},
                                   {"role": "user", "content": prompt}],
                      "temperature": 0.3, "max_tokens": 2048},
                timeout=45,
            )
            if resp.status_code == 200:
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                if content and content.strip():
                    return content.strip()
        except Exception:
            continue
    return ""


def call_ai(prompt, system_instruction):
    answer = call_gemini(prompt, system_instruction)
    if answer and len(answer) > 20:
        return answer
    answer = call_groq(prompt, system_instruction)
    if answer and len(answer) > 20:
        return answer
    return "⚠️ تعذّر الحصول على إجابة حالياً. يرجى المحاولة بعد لحظات."


def build_system_instruction(lang_code):
    target_lang = LANG_NAMES_FOR_PROMPT.get(lang_code, "Arabic (العربية)")
    return f"""أنت "مُبين AI" — مساعد متخصص في السيرة النبوية، ومصدرك الأساسي هو كتاب «الرحيق المختوم» للشيخ صفي الرحمن المباركفوري.

‎📖 قواعد الدقة:
‎1. اعتمد على المعلومات الموثقة من «الرحيق المختوم» وكتب السيرة المعتمدة.
‎2. إذا لم تكن المعلومة موجودة، قل بوضوح: "هذه المعلومة ليست في المصدر الذي أعتمد عليه".
‎3. لا تخترع أحداثاً أو تواريخ أو أسماء.

‎📝 قواعد التنسيق:
‎- ابدأ بجواب مباشر في سطر واحد.
‎- استخدم عناوين فرعية بصيغة `**العنوان**`.
‎- اترك سطراً فارغاً بين كل فقرة.

‎🌍 اللغة: أجب بالكامل بلغة **{target_lang}**.
‎🚫 ممنوعات: لا تخترع أحاديث أو أسانيد."""


def build_user_prompt(lang_code, question):
    target_lang = LANG_NAMES_FOR_PROMPT.get(lang_code, "Arabic (العربية)")
    return f"""أجب على السؤال التالي باللغة {target_lang} بدقة عالية:

‎السؤال: {question}

‎تذكير:
‎- ابدأ بجواب مباشر.
‎- استخدم عناوين ونقاط منظمة.
‎- إذا لم تجد المعلومة، اعترف بذلك بوضوح."""

# ---------------------------------------------------------------------------
# 10. CSS — Awwwards-level redesign (colors/fonts locked)
# ---------------------------------------------------------------------------
def inject_css(lang_dir, rtl):
    align = "right" if rtl else "left"
    side_border = "right" if rtl else "left"
    opp_side = "left" if rtl else "right"
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800&family=Amiri:wght@400;700&display=swap');

        :root {{
            --deep-green: #0F4C3A;
            --deep-green-dark: #0A3527;
            --green-mid: #1E6E52;
            --matte-gold: #C9A227;
            --gold-light: #EFDFA6;
            --gold-dark: #8A6914;
            --gold-soft-bg: #FBF3DC;
            --cream: #FAF7F0;
            --cream-deep: #F1EAD8;
            --marble: #FFFFFF;
            --text-dark: #20281F;
            --text-mid: #45514A;
        }}

        html, body, [class*="css"], .stApp {{
            background-color: var(--cream) !important;
            font-family: 'Cairo', 'Amiri', sans-serif !important;
        }}
        .stApp {{
            background-image:
                radial-gradient(circle at 8% 8%, rgba(201,162,39,0.07) 0%, transparent 38%),
                radial-gradient(circle at 92% 92%, rgba(15,76,58,0.06) 0%, transparent 38%);
        }}
        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 6rem !important;
            max-width: 1400px !important;
        }}
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Amiri', 'Cairo', serif !important;
            color: var(--deep-green) !important;
        }}
        p, span, div, label, li, a, button, input, textarea, select {{
            font-family: 'Cairo', 'Amiri', sans-serif !important;
        }}
        p, li {{
            color: var(--text-dark) !important;
        }}

        section[data-testid="stSidebar"] {{ display: none !important; }}
        header[data-testid="stHeader"] {{
            display: none !important; visibility: hidden !important; height: 0 !important;
        }}
        header[data-testid="stHeader"] * {{ display: none !important; visibility: hidden !important; }}
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapseButton"] {{ display: none !important; }}
        #MainMenu, footer {{ visibility: hidden; }}
        [data-testid="stDecoration"], [data-testid="stStatusWidget"] {{ display: none !important; }}

        @keyframes fadeInLogo {{
            from {{ opacity: 0; transform: translateY(-10px) scale(0.97); }}
            to   {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes glowPulse {{
            0%, 100% {{ opacity: 0.55; }}
            50% {{ opacity: 1; }}
        }}
        @keyframes starPulse {{
            0%, 100% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.15); opacity: 0.85; }}
        }}

        /* ===================== Mosaic divider strip (used on cards/hero) ===================== */
        .mubeen-mosaic-strip {{
            height: 6px;
            width: 100%;
            background: repeating-linear-gradient(
                45deg,
                var(--matte-gold) 0px, var(--matte-gold) 8px,
                var(--deep-green) 8px, var(--deep-green) 16px
            );
        }}

        /* ===================== Expander / Menu ===================== */
        div[data-testid="stExpander"] {{
            border: 2px solid var(--matte-gold) !important;
            border-radius: 16px !important;
            background-color: var(--marble) !important;
            margin-bottom: 18px !important;
            box-shadow: 0 8px 30px rgba(15, 76, 58, 0.18) !important;
            overflow: hidden !important;
            animation: fadeInUp 0.4s ease-out;
        }}
        div[data-testid="stExpander"] summary {{
            background: linear-gradient(135deg, var(--deep-green-dark) 0%, var(--deep-green) 55%, var(--green-mid) 100%) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            padding: 16px 22px !important;
            cursor: pointer !important;
            border-bottom: 3px solid var(--matte-gold) !important;
            transition: filter 0.2s ease !important;
        }}
        div[data-testid="stExpander"] summary:hover {{ filter: brightness(1.1); }}
        div[data-testid="stExpander"] summary p {{
            color: #FFFFFF !important; font-weight: 700 !important; margin: 0 !important; font-size: 1.1rem !important;
        }}
        div[data-testid="stExpander"] svg {{ fill: var(--gold-light) !important; color: var(--gold-light) !important; }}
        div[data-testid="stExpander"] > div {{ padding: 20px !important; background: var(--marble) !important; }}

        div[data-testid="stExpander"] summary span[data-testid*="stIcon"] {{
            font-size: 0 !important; color: transparent !important;
        }}
        div[data-testid="stExpander"] summary span[data-testid*="stIcon"]::after {{
            content: "▼" !important;
            font-size: 13px !important;
            color: var(--gold-light) !important;
            font-weight: 700 !important;
            display: inline-block !important;
            margin-{('left' if not rtl else 'right')}: 8px !important;
            vertical-align: middle !important;
        }}

        /* ===================== Hero — evokes the Green Dome at dusk ===================== */
        .mubeen-header {{
            position: relative;
            background: linear-gradient(180deg, var(--deep-green-dark) 0%, var(--deep-green) 55%, var(--green-mid) 100%);
            border: 2px solid var(--matte-gold);
            border-radius: 20px;
            padding: 40px 28px 54px 28px;
            margin-bottom: 24px;
            box-shadow:
                0 18px 44px rgba(10, 53, 39, 0.4),
                inset 0 0 0 1px rgba(239, 223, 166, 0.18);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 260px;
            overflow: hidden;
            text-align: center;
        }}
        /* faint geometric star lattice overlay */
        .mubeen-header::before {{
            content: "";
            position: absolute;
            inset: 0;
            opacity: 0.10;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 120 120'%3E%3Cg fill='none' stroke='%23EFDFA6' stroke-width='1.4'%3E%3Cpath d='M60 8 L98 34 L84 80 L36 80 L22 34 Z'/%3E%3Ccircle cx='60' cy='60' r='48'/%3E%3Cpath d='M60 8 L60 112 M8 60 L112 60'/%3E%3C/g%3E%3C/svg%3E");
            background-size: 130px 130px;
            pointer-events: none;
        }}
        /* dome + minaret silhouette, gold line-art, glowing softly */
        .mubeen-header::after {{
            content: "";
            position: absolute;
            bottom: -6px;
            left: 50%;
            transform: translateX(-50%);
            width: 260px;
            height: 96px;
            opacity: 0.9;
            animation: glowPulse 4.5s ease-in-out infinite;
            background-repeat: no-repeat;
            background-position: bottom center;
            background-size: contain;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='150' viewBox='0 0 400 150'%3E%3Cg fill='none' stroke='%23C9A227' stroke-width='2.2' stroke-linecap='round'%3E%3Cline x1='40' y1='150' x2='40' y2='55'/%3E%3Crect x='30' y='40' width='20' height='16' rx='2'/%3E%3Ccircle cx='40' cy='34' r='5'/%3E%3Cline x1='360' y1='150' x2='360' y2='55'/%3E%3Crect x='350' y='40' width='20' height='16' rx='2'/%3E%3Ccircle cx='360' cy='34' r='5'/%3E%3Cpath d='M140 150 L140 90 Q140 55 200 55 Q260 55 260 90 L260 150 Z'/%3E%3Cpath d='M170 55 Q200 15 230 55'/%3E%3Ccircle cx='200' cy='18' r='6'/%3E%3Cline x1='200' y1='18' x2='200' y2='4'/%3E%3Cpath d='M60 150 L60 120 L80 120 L80 100 L110 100 L110 150'/%3E%3Cpath d='M290 150 L290 120 L310 120 L310 100 L340 100 L340 150'/%3E%3C/g%3E%3C/svg%3E");
        }}
        .mubeen-header .mubeen-logo-banner {{
            position: relative;
            z-index: 1;
            height: 150px;
            width: auto;
            max-width: 100%;
            filter: drop-shadow(0 0 22px rgba(201, 162, 39, 0.5));
            animation: fadeInLogo 0.8s ease-out;
            margin-bottom: 6px;
        }}
        .mubeen-header .mubeen-app-title {{
            position: relative;
            z-index: 1;
            font-family: 'Amiri', serif;
            font-size: 2.15rem;
            font-weight: 700;
            color: #FFFFFF;
            text-shadow: 0 2px 10px rgba(0,0,0,0.35);
            margin: 4px 0 2px 0;
        }}
        .mubeen-header .mubeen-app-rule {{
            position: relative;
            z-index: 1;
            width: 130px;
            height: 3px;
            margin: 8px auto 4px auto;
            background: linear-gradient(90deg, transparent, var(--matte-gold), transparent);
            border-radius: 2px;
        }}
        .mubeen-header .mubeen-app-tagline {{
            position: relative;
            z-index: 1;
            color: var(--gold-light);
            font-size: 0.98rem;
            font-weight: 600;
            letter-spacing: 0.2px;
        }}

        /* ===================== Hint bar ===================== */
        .mubeen-hint {{
            background: var(--marble);
            border: 1px solid var(--matte-gold);
            border-radius: 12px;
            padding: 10px 16px;
            margin-bottom: 16px;
            color: var(--text-mid) !important;
            font-size: 0.92rem;
            font-weight: 600;
        }}
        .mubeen-hint * {{ color: var(--text-mid) !important; }}

        /* ===================== Event / Milestone Cards — mihrab-arch style ===================== */
        .mubeen-card {{
            position: relative;
            background: var(--marble);
            border: 2px solid var(--matte-gold);
            border-radius: 48px 48px 14px 14px;
            padding: 0 0 18px 0;
            margin-bottom: 16px;
            box-shadow: 0 8px 24px rgba(201, 160, 39, 0.16);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            animation: fadeInUp 0.4s ease-out;
            overflow: hidden;
        }}
        .mubeen-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 16px 36px rgba(15, 76, 58, 0.22);
        }}
        .mubeen-card .milestone-body {{
            padding: 16px 24px 0 24px;
        }}
        .mubeen-card .milestone-title {{
            color: var(--deep-green) !important;
            font-family: 'Amiri', serif;
            font-size: 1.38rem;
            font-weight: 700;
        }}
        .mubeen-card .milestone-subtitle {{
            color: var(--gold-dark) !important;
            font-size: 0.97rem;
            margin-top: 5px;
            font-weight: 700;
        }}
        .mubeen-card .milestone-desc {{
            color: var(--text-dark) !important;
            font-size: 1.02rem;
            margin-top: 12px;
            line-height: 2;
        }}

        /* ===================== Chat messages ===================== */
        .mubeen-user-msg {{
            position: relative;
            background: var(--cream-deep);
            border: 1px solid var(--matte-gold);
            border-{side_border}: 6px solid var(--matte-gold);
            border-radius: 14px;
            padding: 12px 18px;
            margin: 10px 0;
            color: var(--deep-green) !important;
            font-weight: 700;
            font-size: 1rem;
            animation: fadeInUp 0.35s ease-out;
        }}
        .mubeen-user-msg * {{ color: var(--deep-green) !important; }}
        .mubeen-ai-answer {{
            position: relative;
            background: var(--marble);
            border: 2px solid var(--matte-gold);
            border-{side_border}: 6px solid var(--deep-green);
            border-radius: 14px;
            padding: 18px 22px;
            margin: 10px 0 20px 0;
            box-shadow: 0 8px 24px rgba(201, 160, 39, 0.16);
            animation: fadeInUp 0.4s ease-out;
        }}
        .mubeen-ai-answer .ai-label {{
            color: var(--deep-green) !important;
            font-weight: 800;
            font-size: 1rem;
            display: inline-block;
            margin-bottom: 12px;
            padding-bottom: 6px;
            border-bottom: 2px solid var(--matte-gold);
        }}
        .mubeen-ai-answer .ai-label::before {{ content: "🕌 "; }}
        .mubeen-ai-answer .ai-body {{
            color: var(--text-dark) !important;
            font-size: 1.03rem;
            line-height: 2.15;
        }}
        .mubeen-ai-answer .ai-body strong {{
            color: var(--deep-green) !important;
            font-weight: 800;
            font-size: 1.05rem;
        }}

        /* ===================== Buttons ===================== */
        .stFormSubmitButton > button,
        div[data-testid="stButton"] button {{
            background: linear-gradient(135deg, var(--deep-green-dark) 0%, var(--deep-green) 60%, var(--green-mid) 100%) !important;
            color: #FFFFFF !important;
            border: 1.5px solid var(--matte-gold) !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            padding: 0.65rem 1rem !important;
            width: 100%;
            box-shadow: 0 4px 12px rgba(15, 76, 58, 0.22) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease !important;
        }}
        .stFormSubmitButton > button:hover,
        div[data-testid="stButton"] button:hover {{
            filter: brightness(1.12);
            transform: translateY(-2px);
            box-shadow: 0 8px 22px rgba(201, 162, 39, 0.38) !important;
        }}
        .stFormSubmitButton > button:active,
        div[data-testid="stButton"] button:active {{ transform: scale(0.98); }}

        /* Secondary (quiz options) */
        div[data-testid="stButton"] button[kind="secondary"] {{
            background-color: var(--marble) !important;
            color: var(--deep-green) !important;
            border: 2px solid var(--gold-light) !important;
            border-{side_border}: 5px solid var(--matte-gold) !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            padding: 14px 18px !important;
            font-size: 1rem !important;
            text-align: {align} !important;
            margin-bottom: 8px !important;
            box-shadow: none !important;
            transition: background 0.2s ease, border-color 0.2s ease, transform 0.2s ease !important;
        }}
        div[data-testid="stButton"] button[kind="secondary"]:hover {{
            background-color: var(--gold-soft-bg) !important;
            border-color: var(--matte-gold) !important;
            transform: translateX({'3px' if rtl else '-3px'});
        }}

        /* ===================== Chat Input ===================== */
        div[data-testid="stChatInput"] {{
            position: fixed !important;
            bottom: 0 !important; left: 0 !important; right: 0 !important;
            z-index: 999999 !important;
            background: linear-gradient(180deg, rgba(250, 247, 240, 0.5) 0%, rgba(250,247,240,0.97) 45%) !important;
            padding: 12px 16px 16px 16px !important;
            border-top: 2px solid var(--matte-gold) !important;
            box-shadow: 0 -6px 24px rgba(201, 162, 39, 0.2) !important;
            backdrop-filter: blur(15px) !important;
        }}
        div[data-testid="stChatInput"] textarea {{
            background-color: var(--marble) !important;
            border: 2px solid var(--matte-gold) !important;
            border-radius: 12px !important;
            color: var(--text-dark) !important;
            font-size: 16px !important;
            padding: 14px 16px !important;
            min-height: 52px !important;
            line-height: 1.5 !important;
            text-indent: 0 !important;
            transition: box-shadow 0.2s ease, border-color 0.2s ease !important;
        }}
        div[data-testid="stChatInput"] textarea:focus {{
            border-color: var(--deep-green) !important;
            box-shadow: 0 0 0 3px rgba(201, 162, 39, 0.22), 0 4px 20px rgba(201, 162, 39, 0.16) !important;
            outline: none !important;
        }}
        div[data-testid="stChatInput"] textarea::placeholder {{ color: #7a7a7a !important; opacity: 1 !important; }}
        div[data-testid="stChatInput"] button {{
            background: linear-gradient(135deg, var(--deep-green) 0%, var(--green-mid) 100%) !important;
            color: #FFFFFF !important;
            border: 1px solid var(--matte-gold) !important;
            border-radius: 10px !important;
            transition: filter 0.2s ease !important;
        }}
        div[data-testid="stChatInput"] button:hover {{ filter: brightness(1.12); }}
        div[data-testid="stChatInput"] button svg {{ fill: #FFFFFF !important; color: #FFFFFF !important; }}

        /* ===================== Inputs ===================== */
        .stTextInput input, .stTextArea textarea,
        .stSelectbox div[data-baseweb="select"] > div {{
            border: 1px solid var(--matte-gold) !important;
            border-radius: 10px !important;
            background-color: var(--marble) !important;
            color: var(--text-dark) !important;
            font-size: 16px !important;
            font-weight: 600 !important;
        }}
        .stSelectbox label, .stSelectbox p {{ color: var(--deep-green) !important; font-weight: 700 !important; }}

        /* ===================== Quiz progress bar ===================== */
        .mubeen-progress-track {{
            background: var(--cream-deep);
            border-radius: 10px;
            height: 14px;
            overflow: hidden;
            border: 1px solid var(--matte-gold);
        }}
        .mubeen-progress-fill {{
            background: linear-gradient(90deg, var(--deep-green) 0%, var(--matte-gold) 100%);
            height: 100%;
            transition: width 0.4s ease;
        }}

        /* ===================== Score card ===================== */
        .mubeen-score-star {{
            display: inline-block;
            animation: starPulse 1.6s ease-in-out infinite;
        }}

        @media (max-width: 900px) {{
            .block-container {{
                padding-left: 0.7rem !important;
                padding-right: 0.7rem !important;
                padding-bottom: 7rem !important;
            }}
            .mubeen-header {{ padding: 26px 16px 46px 16px; min-height: 200px; }}
            .mubeen-header .mubeen-logo-banner {{ height: 110px; }}
            .mubeen-header .mubeen-app-title {{ font-size: 1.6rem; }}
            .mubeen-header::after {{ width: 190px; height: 70px; }}
            h2 {{ font-size: 1.3rem !important; }}
            .mubeen-ai-answer .ai-body {{ font-size: 0.97rem; }}
            div[data-testid="stChatInput"] {{ padding: 10px 12px 14px 12px !important; }}
            div[data-testid="stChatInput"] textarea {{
                font-size: 16px !important; min-height: 50px !important; padding: 12px 14px !important;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# 11. Markdown Formatter
# ---------------------------------------------------------------------------
def format_answer_markdown(text):
    import html as html_lib
    import re
    safe = html_lib.escape(text)
    safe = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe)
    safe = re.sub(r"^### (.+)$", r"<h3>\1</h3>", safe, flags=re.MULTILINE)
    safe = re.sub(r"^## (.+)$", r"<h3>\1</h3>", safe, flags=re.MULTILINE)
    safe = re.sub(r"^# (.+)$", r"<h3>\1</h3>", safe, flags=re.MULTILINE)
    parts = safe.split("\n\n")
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if p.startswith("<h3"):
            out.append(p)
        else:
            out.append(f"<p>{p.replace(chr(10), '<br>')}</p>")
    return "".join(out)

# ---------------------------------------------------------------------------
# 12. Quiz Renderer
# ---------------------------------------------------------------------------
def render_quiz(t, rtl, lang_dir, lang):
    ql = QUIZ_LABELS.get(lang, QUIZ_LABELS.get("en", QUIZ_LABELS["ar"]))
    total = 10

    col_exit, col_spacer, col_info = st.columns([1, 2, 1])
    with col_exit:
        if st.button(ql["exit_button"], key="exit_quiz_btn", use_container_width=True):
            st.session_state.quiz_started = False
            st.session_state.quiz_finished = False
            st.session_state.quiz_current = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_selected = None
            st.session_state.quiz_answered = False
            st.session_state.current_page = "home"
            st.session_state.close_menu = True
            st.rerun()

    if not st.session_state.quiz_started and not st.session_state.quiz_finished:
        st.markdown(
            f"""
            <div class="mubeen-card" dir="{lang_dir}" style="border-color:#0F4C3A; text-align:center; padding:34px 30px;">
                <div style="font-size:3rem; margin-bottom:14px;">📝</div>
                <h2 style="color:#0F4C3A; font-family:'Amiri', serif; margin:8px 0;">{ql['quiz_title']}</h2>
                <p style="color:#20281F; font-weight:600; font-size:1.02rem; line-height:1.9; margin-top:14px;">{ql['quiz_intro']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col_a, col_b, col_c = st.columns([1, 1, 1])
        with col_b:
            if st.button(ql["start_button"], key="start_quiz_btn", use_container_width=True):
                bank = QUIZ_BANK.get(lang, QUIZ_BANK.get("ar", []))
                st.session_state.quiz_questions = random.sample(bank, 10) if len(bank) >= 10 else bank
                st.session_state.quiz_started = True
                st.session_state.quiz_current = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_answered = False
                st.session_state.quiz_finished = False
                st.session_state.quiz_selected = None
                st.rerun()
        return

    if st.session_state.quiz_finished:
        score = st.session_state.quiz_score
        total_q = len(st.session_state.quiz_questions)
        percentage = int((score / total_q) * 100) if total_q > 0 else 0

        if percentage >= 90:
            feedback = ql["excellent"]; color = "#1B4D3E"; emoji = "🏆"
        elif percentage >= 70:
            feedback = ql["very_good"]; color = "#2c6a58"; emoji = "🌟"
        elif percentage >= 50:
            feedback = ql["good"]; color = "#8A6914"; emoji = "👍"
        else:
            feedback = ql["try_again"]; color = "#7A3B12"; emoji = "📚"

        st.markdown(
            f"""
            <div class="mubeen-card" dir="{lang_dir}" style="border-color:{color};
                        text-align:center; padding:34px 30px; margin-top:20px;">
                <div class="mubeen-score-star" style="font-size:4rem; margin-bottom:10px;">{emoji}</div>
                <h2 style="color:{color}; font-family:'Amiri', serif;
                           margin:8px 0; font-size:1.8rem;">{ql['your_score']}</h2>
                <div style="font-size:3rem; font-weight:800; color:{color};
                            font-family:'Amiri', serif; margin:14px 0;">
                    {score} / {total_q}
                </div>
                <div style="font-size:1.3rem; color:#20281F; font-weight:600; margin:8px 0;">({percentage}%)</div>
                <p style="color:#20281F; font-size:1.05rem; line-height:1.9;
                          margin-top:20px; font-weight:700;">{feedback}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col_x, col_y, col_z = st.columns([1, 1, 1])
        with col_y:
            if st.button(ql["restart_button"], key="restart_quiz_btn", use_container_width=True):
                bank = QUIZ_BANK.get(lang, QUIZ_BANK.get("ar", []))
                st.session_state.quiz_questions = random.sample(bank, 10) if len(bank) >= 10 else bank
                st.session_state.quiz_started = True
                st.session_state.quiz_finished = False
                st.session_state.quiz_current = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_selected = None
                st.session_state.quiz_answered = False
                st.rerun()
        return

    idx = st.session_state.quiz_current
    total_q = len(st.session_state.quiz_questions)
    if idx >= total_q:
        st.session_state.quiz_finished = True
        st.rerun()

    q = st.session_state.quiz_questions[idx]
    progress_pct = int(((idx) / total_q) * 100)

    st.markdown(
        f"""
        <div dir="{lang_dir}" style="margin-bottom:14px;">
            <div style="color:#1B4D3E; font-weight:700; font-size:1rem; margin-bottom:8px;">
                {ql['question_of'].format(current=idx + 1, total=total_q)}
            </div>
            <div class="mubeen-progress-track">
                <div class="mubeen-progress-fill" style="width:{progress_pct}%;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="mubeen-card" dir="{lang_dir}" style="border-color:#0F4C3A;
                    padding:28px 24px 22px 24px; margin-bottom:14px;">
            <div style="color:#0F4C3A; font-family:'Amiri', serif;
                        font-size:1.28rem; font-weight:700; line-height:1.75;">
                {q['q']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    letters = ["A", "B", "C", "D"]
    for i, opt in enumerate(q["options"]):
        if st.session_state.quiz_answered:
            badge = "✅" if i == q["answer"] else ("❌" if i == st.session_state.quiz_selected else "⚪")
        else:
            badge = "🟡" if i == st.session_state.quiz_selected else "⚪"

        if not st.session_state.quiz_answered:
            if st.button(f"{badge}  {letters[i]}. {opt}", key=f"opt_{idx}_{i}", use_container_width=True):
                st.session_state.quiz_selected = i
                st.rerun()
        else:
            bg_color = "#E4F4EA" if i == q["answer"] else ("#FBE4E4" if i == st.session_state.quiz_selected else "#FAF7F0")
            border_color = "#0F4C3A" if i == q["answer"] else ("#B23A3A" if i == st.session_state.quiz_selected else "#EFDFA6")
            st.markdown(
                f"""
                <div dir="{lang_dir}" style="
                    background:{bg_color};
                    border:2px solid {border_color};
                    border-radius:10px;
                    padding:14px 18px;
                    margin-bottom:8px;
                    font-weight:700;
                    color:#20281F;
                    font-size:1.02rem;
                    text-align:{'right' if rtl else 'left'};">
                    {badge}  {letters[i]}. {opt}
                </div>
                """,
                unsafe_allow_html=True,
            )

    if not st.session_state.quiz_answered:
        col_a, col_b, col_c = st.columns([1, 1, 1])
        with col_b:
            if st.button(ql["check_button"], key=f"check_{idx}", use_container_width=True):
                if st.session_state.quiz_selected is not None:
                    st.session_state.quiz_answered = True
                    if st.session_state.quiz_selected == q["answer"]:
                        st.session_state.quiz_score += 1
                    st.rerun()
                else:
                    st.warning(ql["please_select"])
    else:
        st.markdown(
            f"""
            <div class="mubeen-card" dir="{lang_dir}"
                 style="border-color:#C9A227; background:#FBF3DC; margin-top:14px; padding:26px 24px 22px 24px;">
                <div style="color:#8A6914; font-weight:800; font-size:1.02rem;
                            margin-bottom:8px;">{ql['explanation_label']}</div>
                <div style="color:#20281F; font-weight:500; font-size:1.02rem; line-height:2;">
                    {q['explanation']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col_a, col_b, col_c = st.columns([1, 1, 1])
        with col_b:
            button_label = ql["finish_button"] if (idx + 1) >= total_q else ql["next_button"]
            if st.button(button_label, key=f"next_{idx}", use_container_width=True):
                st.session_state.quiz_current += 1
                st.session_state.quiz_answered = False
                st.session_state.quiz_selected = None
                if st.session_state.quiz_current >= total_q:
                    st.session_state.quiz_finished = True
                st.rerun()

# ---------------------------------------------------------------------------
# 13. Close Menu JS
# ---------------------------------------------------------------------------
def close_menu_js():
    st.markdown(
        """
        <script>
        (function() {
            const closeAll = () => {
                const doc = window.parent.document;
                doc.querySelectorAll('[data-testid="stExpander"] details[open]').forEach(d => {
                    d.removeAttribute('open');
                });
            };
            setTimeout(closeAll, 200);
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# 14. MAIN
# ---------------------------------------------------------------------------
def main():
    t = UI_TEXT[st.session_state.lang]
    rtl = t["rtl"]
    lang_dir = t["dir"]

    inject_css(lang_dir, rtl)

    if st.session_state.close_menu:
        close_menu_js()
        st.session_state.close_menu = False

    with st.expander(t["menu"], expanded=False):
        st.markdown(
            f"""
            <div style="background:#F5F2EB; border:2px solid #1B4D3E;
                        border-radius:10px; padding:22px 18px; text-align:center;
                        margin-bottom:14px;">
                <h1 style="color:#1B4D3E; font-family:'Amiri', serif;
                           margin:0; font-size:1.7rem; font-weight:700;">{t['app_name']}</h1>
                <p style="color:#C5A059; font-size:0.9rem; margin-top:8px;">{t['tagline']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        ql = QUIZ_LABELS.get(st.session_state.lang, QUIZ_LABELS["ar"])
        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            if st.button(ql["page_home"], key="nav_home", use_container_width=True):
                st.session_state.current_page = "home"
                st.session_state.close_menu = True
                st.rerun()
        with nav_col2:
            if st.button(ql["page_quiz"], key="nav_quiz", use_container_width=True):
                st.session_state.current_page = "quiz"
                st.session_state.close_menu = True
                st.rerun()

        st.markdown("<hr style='border: 1px solid #C5A059; opacity:0.4; margin: 14px 0;'>",
                    unsafe_allow_html=True)

        st.markdown(
            f"<label style='color:#1B4D3E; font-weight:700; font-size:1rem;'>{t['select_lang']}</label>",
            unsafe_allow_html=True,
        )
        current_index = list(LANG_LABELS.keys()).index(st.session_state.lang)
        chosen = st.selectbox(
            label=t["select_lang"],
            options=list(LANG_LABELS.keys()),
            format_func=lambda code: LANG_LABELS[code],
            index=current_index,
            label_visibility="collapsed",
            key="lang_selector",
        )
        if chosen != st.session_state.lang:
            st.session_state.lang = chosen
            st.session_state.chat_history = []
            st.rerun()

        st.markdown("<hr style='border: 1px solid #C5A059; opacity:0.4; margin: 14px 0;'>",
                    unsafe_allow_html=True)

        st.markdown(
            f"<h4 style='color:#1B4D3E; font-family:Amiri, serif; font-size:1.05rem; margin-bottom:6px;'>{t['about_title']}</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='font-size:0.92rem; color:#45514A; font-weight:600; line-height:1.85; margin-top:0;'>{t['about_text']}</p>",
            unsafe_allow_html=True,
        )

    _logo_b64 = get_logo_base64("assets/logo.png")
    _logo_img_html = (
        f'<img class="mubeen-logo-banner" src="data:image/png;base64,{_logo_b64}" alt="Mubeen AI" />'
        if _logo_b64 else ""
    )

    st.markdown(
        f"""
        <div class="mubeen-header" dir="{lang_dir}">
            {_logo_img_html}
            <div class="mubeen-app-title">{t['app_name']}</div>
            <div class="mubeen-app-rule"></div>
            <div class="mubeen-app-tagline">{t['tagline']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.current_page == "quiz":
        render_quiz(t, rtl, lang_dir, st.session_state.lang)
        return

    # ===== Home Page =====
    st.markdown(
        f"""<div class="mubeen-hint" dir="{lang_dir}">✦ {t['events_hint']}</div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<h2 style='font-family:Amiri, serif; color:#1B4D3E; text-align:{'right' if rtl else 'left'};'>{t['events_title']}</h2>",
        unsafe_allow_html=True,
    )

    event_options = {
        loc["key"]: f"{i+1}. {location_name(loc, st.session_state.lang)}"
        for i, loc in enumerate(LOCATIONS)
    }
    default_index = 0
    if st.session_state.selected_key in event_options:
        default_index = list(event_options.keys()).index(st.session_state.selected_key)

    chosen_key = st.selectbox(
        label=t["select_event"],
        options=list(event_options.keys()),
        format_func=lambda k: event_options[k],
        index=default_index,
        key="event_selector",
    )
    st.session_state.selected_key = chosen_key

    selected = next((loc for loc in LOCATIONS if loc["key"] == chosen_key), None)
    if selected:
        st.markdown(
            f"""
            <div class="mubeen-card" dir="{lang_dir}" style="margin-top:14px;">
                <div class="mubeen-mosaic-strip"></div>
                <div class="milestone-body">
                    <div class="milestone-title">{location_name(selected, st.session_state.lang)}</div>
                    <div class="milestone-subtitle">{location_subtitle(selected, st.session_state.lang)}</div>
                    <div class="milestone-desc">{location_context(selected, st.session_state.lang)}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='border:1px solid #C5A059; opacity:0.4; margin-top:20px;'>",
                unsafe_allow_html=True)

    st.markdown(
        f"<h2 style='font-family:Amiri, serif; color:#1B4D3E; text-align:{'right' if rtl else 'left'};'>{t['chat_title']}</h2>",
        unsafe_allow_html=True,
    )

    if st.session_state.pending_prompt:
        prompt_text = st.session_state.pending_prompt
        st.session_state.pending_prompt = None
        st.session_state.chat_history.append({"role": "user", "content": prompt_text})
        with st.spinner(t["spinner"]):
            system_instruction = build_system_instruction(st.session_state.lang)
            prompt = build_user_prompt(st.session_state.lang, prompt_text)
            answer = call_ai(prompt, system_instruction)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state.chat_history:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(
                    f"""
                    <div class="mubeen-user-msg" dir="{lang_dir}">
                        👤 {msg['content']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                formatted = format_answer_markdown(msg["content"])
                st.markdown(
                    f"""
                    <div class="mubeen-ai-answer" dir="{lang_dir}">
                        <div class="ai-label">Mubeen AI</div>
                        <div class="ai-body">{formatted}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown(
        f"<p style='color:#45514A; font-weight:700; font-size:0.92rem; text-align:{'right' if rtl else 'left'}; margin-top:18px; margin-bottom:8px;'>{t['suggestions']}</p>",
        unsafe_allow_html=True,
    )

    sugg_list = SUGGESTIONS.get(st.session_state.lang, SUGGESTIONS["en"])
    cols = st.columns(2)
    for i, sug in enumerate(sugg_list):
        with cols[i % 2]:
            if st.button(sug, key=f"sug_{i}", use_container_width=True):
                st.session_state.pending_prompt = sug
                st.rerun()

    # ===== Chat Input (fixed at bottom) =====
    user_input = st.chat_input(t["chat_placeholder"])

    if user_input and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
        with st.spinner(t["spinner"]):
            system_instruction = build_system_instruction(st.session_state.lang)
            prompt = build_user_prompt(st.session_state.lang, user_input.strip())
            answer = call_ai(prompt, system_instruction)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()


if __name__ == "__main__":
    main()
