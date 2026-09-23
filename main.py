"""
Mubeen AI (مُبين AI) — Smart platform for the Prophetic Seerah in world languages.
Gemini + Groq — Smooth, fast, and reliable UI.
"""

import os
from typing import Optional

import requests
import streamlit as st

# ---------------------------------------------------------------------------
# 1. PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Mubeen AI | مُبين AI",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# 2. LOCATIONS DATABASE
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
         "ar": "في مكة وُلد النبي ﷺ ونشأ، وفيها نزل الوحي عليه أول مرة، ومنها انطلقت دعوة التوحيد رغم اشتداد الأذى على المسلمين الأوائل.",
         "en": "In Makkah the Prophet ﷺ was born and raised, the first revelation descended upon him.",
         "ur": "مکہ مکرمہ میں نبی ﷺ کی ولادت ہوئی اور پرورش پائی، یہیں پہلی وحی نازل ہوئی۔",
         "id": "Di Makkah Nabi ﷺ dilahirkan dan dibesarkan, wahyu pertama turun di sini.",
         "tr": "Mekke'de Peygamber ﷺ doğdu ve büyüdü, ilk vahiy burada indi.",
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
         "ur": "غارِ حرا میں نبی ﷺ عبادت کیا کرتے تھے، یہیں جبریل علیہ السلام پہلی آیات لے کر نازل ہوئے۔",
         "id": "Di Gua Hira Nabi ﷺ berkhalwat; di sana Jibril turun dengan ayat pertama.",
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
         "ar": "خرج النبي ﷺ إلى الطائف بعد اشتداد أذى قريش، يدعو ثقيفًا إلى الإسلام، فردّوه وأغروا به سفهاءهم.",
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
         "ur": "ہجرت کے موقع پر نبی ﷺ قباء میں ٹھہرے اور مسجدِ قباء قائم کی۔",
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
         "ar": "هاجر النبي ﷺ إلى المدينة فبنى المسجد النبوي، وآخى بين المهاجرين والأنصار، وكتب الصحيفة.",
         "en": "The Prophet ﷺ migrated to Madinah, built the Prophet's Mosque.",
         "ur": "نبی ﷺ مدینہ ہجرت کی، مسجدِ نبوی تعمیر فرمائی، اور مواخات قائم کی۔",
         "id": "Nabi ﷺ berhijrah ke Madinah, membangun Masjid Nabawi.",
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
         "ar": "في السنة الثانية للهجرة وقعت غزوة بدر، فأيّد الله المسلمين رغم قلتهم، فكانت يوم الفرقان.",
         "en": "In the 2nd year after Hijrah, the Battle of Badr took place.",
         "ur": "دوسری ہجری میں غزوۂ بدر پیش آیا، اللہ نے مسلمانوں کو فتح دی۔",
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
         "ar": "في السنة الثالثة للهجرة وقعت غزوة أحد، فكانت درسًا في طاعة الأمر، واستُشهد فيها سبعون من الصحابة.",
         "en": "In the 3rd year after Hijrah the Battle of Uhud occurred.",
         "ur": "تیسری ہجری میں غزوۂ اُحد پیش آیا، جو اطاعت کا سبق تھا۔",
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
                  "ur": "غزوۂ خندق (احزاب)", "id": "Perang Khandaq",
                  "tr": "Hendek Savaşı", "fr": "Bataille de la Tranchée",
                  "es": "Batalla de la Trinchera", "ru": "Битва у рва",
                  "zh": "壕沟战役", "hi": "ग़ज़्वा-ए-ख़ंदक़"},
     "context": {
         "ar": "في السنة الخامسة للهجرة تحزّبت القبائل على المدينة، فحفر المسلمون الخندق بأمر النبي ﷺ.",
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
         "ar": "في السنة السابعة للهجرة فتح المسلمون حصون خيبر، وأعطى النبي ﷺ الراية لعلي رضي الله عنه.",
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
         "ar": "في السنة الثامنة للهجرة وقعت غزوة مؤتة، واستُشهد فيها القادة الثلاثة: زيد وجعفر وابن رواحة رضي الله عنهم.",
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
         "ar": "في السنة التاسعة للهجرة خرج النبي ﷺ في غزوة تبوك في حرّ شديد وعسرة، وبلغ تبوك دون قتال.",
         "en": "In the 9th year after Hijrah the Prophet ﷺ set out for Tabuk.",
         "ur": "نویں ہجری میں نبی ﷺ شدید گرمی میں غزوۂ تبوک کے لیے نکلے۔",
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
         "ar": "في السنة العاشرة للهجرة حجّ النبي ﷺ حجة الوداع، وخطب في عرفة خطبةً جامعة، ونزلت: ﴿الْيَوْمَ أَكْمَلْتُ لَكُمْ دِينَكُمْ﴾.",
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
# 3. TRANSLATIONS — مع النصوص المحدثة
# ---------------------------------------------------------------------------
UI_TEXT = {
    "ar": {"app_name": "مُبين AI",
           "tagline": "منصة ذكية تخدم السيرة النبوية بلغات العالم",
           "select_lang": "اختر اللغة",
           "events_title": "أحداث السيرة والغزوات والمعارك",
           "select_event": "اختر الحدث",
           "chat_title": "اسأل مُبين AI",
           "chat_placeholder": "اكتب سؤالك حول السيرة النبوية...",
           "chat_button": "إرسال",
           "spinner": "جارٍ البحث في كتاب «الرحيق المختوم»...",
           "about_title": "عن الموقع",
           "about_text": "موقع يعتمد على كتاب «الرحيق المختوم» للشيخ صفي الرحمن المباركفوري، ويقدم تجربة تفاعلية لاستكشاف أحداث السيرة النبوية بلغات متعددة.",
           "events_hint": "اختر حدثاً من القائمة لقراءة نبذة عنه، أو اسأل مُبين AI مباشرة.",
           "suggestions": "💡 اقتراحات سريعة",
           "menu": "القائمة",
           "close_menu": "إغلاق",
           "rtl": True, "dir": "rtl"},
    "en": {"app_name": "Mubeen AI",
           "tagline": "A smart platform serving the Prophetic Seerah in world languages",
           "select_lang": "Select Language",
           "events_title": "Seerah Events, Battles & Expeditions",
           "select_event": "Select an event",
           "chat_title": "Ask Mubeen AI",
           "chat_placeholder": "Type your question about the Seerah...",
           "chat_button": "Send",
           "spinner": "Searching 'The Sealed Nectar'...",
           "about_title": "About the Site",
           "about_text": "A site grounded in 'The Sealed Nectar' by Safiur Rahman Mubarakpuri, offering an interactive experience to explore the events of the Prophetic Seerah in multiple languages.",
           "events_hint": "Select an event to read an excerpt, or ask Mubeen AI directly.",
           "suggestions": "💡 Quick prompts",
           "menu": "Menu",
           "close_menu": "Close",
           "rtl": False, "dir": "ltr"},
    "ur": {"app_name": "مبین AI",
           "tagline": "عالمی زبانوں میں سیرت نبوی کی خدمت کرنے والا ذہین پلیٹ فارم",
           "select_lang": "زبان منتخب کریں",
           "events_title": "سیرت کے واقعات، غزوات اور معرکے",
           "select_event": "واقعہ منتخب کریں",
           "chat_title": "مبین AI سے پوچھیں",
           "chat_placeholder": "سیرت نبوی کے بارے میں اپنا سوال لکھیں...",
           "chat_button": "بھیجیں",
           "spinner": "«الرحيق المختوم» میں تلاش ہو رہی ہے...",
           "about_title": "سائٹ کے بارے میں",
           "about_text": "یہ سائٹ شیخ صفی الرحمن مبارکپوری کی کتاب «الرحيق المختوم» پر مبنی ہے، اور کثیر زبانوں میں سیرت نبوی کے واقعات کو دریافت کرنے کا ایک تفاعلی تجربہ پیش کرتی ہے۔",
           "events_hint": "کوئی واقعہ منتخب کریں یا مبین AI سے براہِ راست پوچھیں۔",
           "suggestions": "💡 فوری تجاویز",
           "menu": "مینو",
           "close_menu": "بند کریں",
           "rtl": True, "dir": "rtl"},
    "id": {"app_name": "Mubeen AI",
           "tagline": "Platform cerdas yang melayani Sirah Nabawiyah dalam bahasa dunia",
           "select_lang": "Pilih Bahasa",
           "events_title": "Peristiwa, Perang & Ekspedisi Sirah",
           "select_event": "Pilih peristiwa",
           "chat_title": "Tanya Mubeen AI",
           "chat_placeholder": "Tulis pertanyaan Anda tentang Sirah...",
           "chat_button": "Kirim",
           "spinner": "Menelusuri 'The Sealed Nectar'...",
           "about_title": "Tentang Situs",
           "about_text": "Situs yang bersumber dari 'The Sealed Nectar' karya Safiur Rahman Mubarakpuri, menawarkan pengalaman interaktif untuk menjelajahi peristiwa Sirah Nabawiyah dalam berbagai bahasa.",
           "events_hint": "Pilih peristiwa atau tanya Mubeen AI langsung.",
           "suggestions": "💡 Saran cepat",
           "menu": "Menu",
           "close_menu": "Tutup",
           "rtl": False, "dir": "ltr"},
    "tr": {"app_name": "Mubeen AI",
           "tagline": "Siyer-i Nebi'ye dünya dillerinde hizmet eden akıllı platform",
           "select_lang": "Dil Seçin",
           "events_title": "Siyer Olayları, Savaşlar ve Seferler",
           "select_event": "Bir olay seçin",
           "chat_title": "Mubeen AI'ya Sor",
           "chat_placeholder": "Siyer hakkında sorunuzu yazın...",
           "chat_button": "Gönder",
           "spinner": "'The Sealed Nectar' taranıyor...",
           "about_title": "Site Hakkında",
           "about_text": "Safiur Rahman Mubarakpuri'nin 'The Sealed Nectar' eserine dayanan, Siyer-i Nebi olaylarını birden çok dilde keşfetmek için etkileşimli deneyim sunan bir site.",
           "events_hint": "Bir olay seçin veya Mubeen AI'ya sorun.",
           "suggestions": "💡 Hızlı öneriler",
           "menu": "Menü",
           "close_menu": "Kapat",
           "rtl": False, "dir": "ltr"},
    "fr": {"app_name": "Mubeen AI",
           "tagline": "Plateforme intelligente au service de la Sîra dans les langues du monde",
           "select_lang": "Choisir la langue",
           "events_title": "Événements, Batailles & Expéditions de la Sîra",
           "select_event": "Sélectionner un événement",
           "chat_title": "Demander à Mubeen AI",
           "chat_placeholder": "Écrivez votre question sur la Sîra...",
           "chat_button": "Envoyer",
           "spinner": "Recherche dans 'The Sealed Nectar'...",
           "about_title": "À propos du site",
           "about_text": "Un site basé sur 'The Sealed Nectar' de Safiur Rahman Mubarakpuri, offrant une expérience interactive pour explorer les événements de la Sîra en plusieurs langues.",
           "events_hint": "Sélectionnez un événement ou demandez à Mubeen AI.",
           "suggestions": "💡 Suggestions rapides",
           "menu": "Menu",
           "close_menu": "Fermer",
           "rtl": False, "dir": "ltr"},
    "es": {"app_name": "Mubeen AI",
           "tagline": "Plataforma inteligente al servicio de la Sira en los idiomas del mundo",
           "select_lang": "Seleccionar idioma",
           "events_title": "Eventos, Batallas y Expediciones de la Sira",
           "select_event": "Selecciona un evento",
           "chat_title": "Pregunta a Mubeen AI",
           "chat_placeholder": "Escribe tu pregunta sobre la Sira...",
           "chat_button": "Enviar",
           "spinner": "Buscando en 'The Sealed Nectar'...",
           "about_title": "Acerca del sitio",
           "about_text": "Un sitio basado en 'The Sealed Nectar' de Safiur Rahman Mubarakpuri, que ofrece una experiencia interactiva para explorar los eventos de la Sira en varios idiomas.",
           "events_hint": "Selecciona un evento o pregunta a Mubeen AI.",
           "suggestions": "💡 Sugerencias rápidas",
           "menu": "Menú",
           "close_menu": "Cerrar",
           "rtl": False, "dir": "ltr"},
    "ru": {"app_name": "Mubeen AI",
           "tagline": "Умная платформа, служащая Сире на языках мира",
           "select_lang": "Выберите язык",
           "events_title": "События, битвы и походы Сиры",
           "select_event": "Выберите событие",
           "chat_title": "Спросить Mubeen AI",
           "chat_placeholder": "Напишите вопрос о Сире...",
           "chat_button": "Отправить",
           "spinner": "Поиск в 'The Sealed Nectar'...",
           "about_title": "О сайте",
           "about_text": "Сайт основан на книге 'The Sealed Nectar' Сафиура Рахмана Мубаракпури и предлагает интерактивный опыт изучения событий Сиры на разных языках.",
           "events_hint": "Выберите событие или спросите Mubeen AI.",
           "suggestions": "💡 Быстрые подсказки",
           "menu": "Меню",
           "close_menu": "Закрыть",
           "rtl": False, "dir": "ltr"},
    "zh": {"app_name": "Mubeen AI",
           "tagline": "以世界多种语言服务先知传记的智能平台",
           "select_lang": "选择语言",
           "events_title": "先知传记事件、战役与远征",
           "select_event": "选择事件",
           "chat_title": "询问 Mubeen AI",
           "chat_placeholder": "请输入您关于先知传记的问题...",
           "chat_button": "发送",
           "spinner": "正在检索《The Sealed Nectar》...",
           "about_title": "关于本站",
           "about_text": "本站基于 Safiur Rahman Mubarakpuri 的《The Sealed Nectar》，提供多语言互动体验，探索先知传记的事件。",
           "events_hint": "选择事件或直接询问 Mubeen AI。",
           "suggestions": "💡 快速提示",
           "menu": "菜单",
           "close_menu": "关闭",
           "rtl": False, "dir": "ltr"},
    "hi": {"app_name": "Mubeen AI",
           "tagline": "विश्व की भाषाओं में सीरत की सेवा करने वाला स्मार्ट प्लेटफ़ॉर्म",
           "select_lang": "भाषा चुनें",
           "events_title": "सीरत की घटनाएँ, लड़ाइयाँ और अभियान",
           "select_event": "घटना चुनें",
           "chat_title": "Mubeen AI से पूछें",
           "chat_placeholder": "सीरत के बारे में अपना प्रश्न लिखें...",
           "chat_button": "भेजें",
           "spinner": "'The Sealed Nectar' में खोज रहे हैं...",
           "about_title": "साइट के बारे में",
           "about_text": "यह साइट सफ़ीउर रहमान मुबारकपुरी की 'The Sealed Nectar' पर आधारित है, और कई भाषाओं में सीरत की घटनाओं को जानने का इंटरैक्टिव अनुभव प्रदान करती है।",
           "events_hint": "कोई घटना चुनें या Mubeen AI से पूछें।",
           "suggestions": "💡 त्वरित सुझाव",
           "menu": "मेनू",
           "close_menu": "बंद करें",
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
           "ما العبر من غزوة أحد؟", "كيف كانت أخلاق النبي ﷺ مع أهل مكة؟"],
    "en": ["What are the lessons from the Battle of Badr?",
           "What wisdom is found in the Treaty of Hudaybiyyah?",
           "What lessons came from the Battle of Uhud?",
           "How was the Prophet's ﷺ character with the people of Makkah?"],
    "ur": ["غزوۂ بدر کے فوائد کیا ہیں؟", "صلح حدیبیہ سے کیا سبق ملتا ہے؟",
           "غزوۂ اُحد سے کیا عبرت ہے؟", "نبی ﷺ کا اخلاق اہلِ مکہ کے ساتھ کیسا تھا؟"],
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
# 4. SESSION STATE
# ---------------------------------------------------------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_key" not in st.session_state:
    st.session_state.selected_key = LOCATIONS[0]["key"]
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None
if "menu_open" not in st.session_state:
    st.session_state.menu_open = False

# ---------------------------------------------------------------------------
# 5. HELPERS
# ---------------------------------------------------------------------------
def location_name(loc: dict, lang: str) -> str:
    return loc["name"].get(lang, loc["name"]["en"])


def location_subtitle(loc: dict, lang: str) -> str:
    return loc["subtitle"].get(lang, loc["subtitle"]["en"])


def location_context(loc: dict, lang: str) -> str:
    return loc["context"].get(lang, loc["context"]["en"])


def _get_secret(name: str) -> Optional[str]:
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
# 6. AI — Gemini + Groq fallback
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


def call_gemini(prompt: str, system_instruction: str) -> str:
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
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    temperature=0.3,
                ),
            )
            text = getattr(response, "text", None)
            if text and text.strip():
                return text.strip()
        except Exception:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.3,
                    ),
                )
                text = getattr(response, "text", None)
                if text and text.strip():
                    return text.strip()
            except Exception:
                continue
    return ""


def call_groq(prompt: str, system_instruction: str) -> str:
    groq_key = _get_secret("GROQ_API_KEY")
    if not groq_key:
        return ""

    for model_name in ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]:
        try:
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2048,
                },
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


def call_ai(prompt: str, system_instruction: str) -> str:
    answer = call_gemini(prompt, system_instruction)
    if answer and len(answer) > 20:
        return answer
    answer = call_groq(prompt, system_instruction)
    if answer and len(answer) > 20:
        return answer
    return (
        "⚠️ تعذّر الحصول على إجابة حالياً. "
        "يرجى المحاولة مرة أخرى بعد لحظات."
    )


# ---------------------------------------------------------------------------
# 7. SYSTEM INSTRUCTION
# ---------------------------------------------------------------------------
def build_system_instruction(lang_code: str) -> str:
    target_lang = LANG_NAMES_FOR_PROMPT.get(lang_code, "Arabic (العربية)")
    return f"""أنت "مُبين AI" — مساعد متخصص حصرياً في السيرة النبوية، ومصدرك الأساسي هو كتاب «الرحيق المختوم» للشيخ صفي الرحمن المباركفوري.

📖 قواعد الدقة:
1. اعتمد أولاً على المعلومات الموثقة من «الرحيق المختوم» وكتب السيرة المعتمدة.
2. إذا لم تكن المعلومة موجودة، قل بوضوح: "هذه المعلومة ليست في المصدر الذي أعتمد عليه".
3. لا تخترع أحداثاً أو تواريخ أو أسماء.

💡 قاعدة الفوائد:
- عندما يُسأل عن "فائدة" أو "درس" أو "حكمة" — أجب بوضوح.
- ميّز بين: (أ) المنصوص عليه في الكتاب، (ب) الدروس المستنبطة.

📝 قواعد التنسيق:
- ابدأ بجواب مباشر في سطر واحد.
- استخدم عناوين فرعية بصيغة `**العنوان**`.
- عند استخدام قائمة، استخدم نوعاً واحداً فقط.
- اترك سطراً فارغاً بين كل فقرة.
- اختم بخلاصة تحت `**الخلاصة:**`.

🌍 اللغة:
- أجب بالكامل بلغة **{target_lang}**.
- لا تخلط بين اللغات.

🚫 ممنوعات:
- لا تخترع أحاديث أو أسانيد."""


def build_user_prompt(lang_code: str, question: str) -> str:
    target_lang = LANG_NAMES_FOR_PROMPT.get(lang_code, "Arabic (العربية)")
    return f"""أجب على السؤال التالي باللغة {target_lang} بدقة عالية:

السؤال: {question}

تذكير:
- ابدأ بجواب مباشر.
- استخدم عناوين ونقاط منظمة.
- إذا لم تجد المعلومة، اعترف بذلك بوضوح.
- اختم بخلاصة قصيرة."""


# ---------------------------------------------------------------------------
# 8. CSS
# ---------------------------------------------------------------------------
def inject_css(lang_dir: str, rtl: bool):
    align = "right" if rtl else "left"
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&family=Amiri:wght@400;700&display=swap');

        html, body, [class*="css"], .stApp {{
            background-color: #FDFBF7 !important;
            font-family: 'Cairo', 'Amiri', sans-serif !important;
        }}

        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 1400px !important;
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Amiri', 'Cairo', serif !important;
            color: #1B4D3E !important;
        }}

        p, span, div, label, li, a, button, input, textarea, select {{
            font-family: 'Cairo', 'Amiri', sans-serif !important;
        }}

        section[data-testid="stSidebar"] {{
            display: none !important;
        }}

        [data-testid="stSidebarCollapsedControl"],
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapseButton"] {{
            display: none !important;
        }}

        #MainMenu, footer {{ visibility: hidden; }}
        [data-testid="stDecoration"], [data-testid="stStatusWidget"] {{
            display: none !important;
        }}
        header[data-testid="stHeader"] {{
            background: transparent !important;
            height: 0 !important;
        }}
        header[data-testid="stHeader"] * {{
            font-size: 0 !important;
            visibility: hidden !important;
        }}

        .mubeen-card {{
            background: #FFFFFF;
            border: 1px solid #C5A059;
            border-radius: 12px;
            padding: 16px 18px;
            margin-bottom: 12px;
            box-shadow: 0 4px 14px rgba(197, 160, 89, 0.12);
            text-align: {align};
        }}
        .mubeen-card .milestone-title {{
            color: #1B4D3E;
            font-family: 'Amiri', serif;
            font-size: 1.3rem;
            font-weight: 700;
        }}
        .mubeen-card .milestone-subtitle {{
            color: #C5A059;
            font-size: 0.95rem;
            margin-top: 4px;
        }}
        .mubeen-card .milestone-desc {{
            color: #2a2a2a;
            font-size: 1rem;
            margin-top: 12px;
            line-height: 2;
        }}

        .mubeen-user-msg {{
            background: #F5F2EB;
            border: 1px solid #C5A059;
            border-right: 6px solid #C5A059;
            border-radius: 14px;
            padding: 12px 18px;
            margin: 8px 0;
            text-align: {align};
            color: #1B4D3E;
            font-weight: 600;
            font-size: 1rem;
        }}

        .mubeen-ai-answer {{
            background: linear-gradient(135deg, #FFFFFF 0%, #FBF7EC 100%);
            border: 2px solid #C5A059;
            border-right: 6px solid #1B4D3E;
            border-radius: 14px;
            padding: 18px 22px;
            margin: 8px 0 18px 0;
            box-shadow: 0 6px 18px rgba(197, 160, 89, 0.15);
            text-align: {align};
        }}
        .mubeen-ai-answer .ai-label {{
            color: #1B4D3E;
            font-weight: 700;
            font-size: 1rem;
            display: inline-block;
            margin-bottom: 12px;
            padding-bottom: 6px;
            border-bottom: 2px solid #C5A059;
        }}
        .mubeen-ai-answer .ai-body {{
            color: #1a1a1a;
            font-size: 1.02rem;
            line-height: 2.1;
        }}
        .mubeen-ai-answer .ai-body strong {{
            color: #1B4D3E;
            font-weight: 700;
            font-size: 1.05rem;
        }}
        .mubeen-ai-answer .ai-body h3 {{
            color: #1B4D3E !important;
            font-family: 'Amiri', serif !important;
            font-size: 1.15rem !important;
            margin: 14px 0 6px 0 !important;
            border-bottom: 1px solid #E8D9B8;
            padding-bottom: 4px;
        }}

        .mubeen-header {{
            background: linear-gradient(90deg, #1B4D3E 0%, #2c6a58 100%);
            border: 2px solid #C5A059;
            border-radius: 14px;
            padding: 18px 22px;
            color: #FFFFFF;
            margin-bottom: 18px;
            box-shadow: 0 10px 26px rgba(27, 77, 62, 0.25);
            text-align: {align};
        }}
        .mubeen-header h1 {{
            color: #FFFFFF !important;
            margin: 0;
            font-family: 'Amiri', serif;
            font-size: 2rem;
        }}
        .mubeen-header p {{
            color: #F3EBD8;
            margin: 6px 0 0 0;
            font-size: 0.95rem;
        }}

        .mubeen-hint {{
            background: #FFFFFF;
            border: 1px solid #C5A059;
            border-radius: 10px;
            padding: 10px 14px;
            margin-bottom: 14px;
            color: #666;
            font-size: 0.9rem;
            text-align: {align};
        }}

        /* أزرار */
        .stButton > button {{
            background-color: #1B4D3E !important;
            color: #FFFFFF !important;
            border: 1px solid #C5A059 !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            padding: 0.6rem 1rem !important;
            width: 100%;
        }}
        .stButton > button:hover {{
            background-color: #143a2e !important;
        }}
        .stFormSubmitButton > button {{
            background-color: #1B4D3E !important;
            color: #FFFFFF !important;
            border: 1px solid #C5A059 !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            padding: 0.6rem 1rem !important;
        }}

        .stTextInput input, .stTextArea textarea,
        .stSelectbox div[data-baseweb="select"] > div {{
            border: 1px solid #C5A059 !important;
            border-radius: 10px !important;
            background-color: #FFFFFF !important;
        }}

        /* Checkbox تنسيق أنيق */
        div[data-testid="stCheckbox"] label {{
            color: #1B4D3E !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
        }}

        @media (max-width: 900px) {{
            .block-container {{
                padding-left: 0.7rem !important;
                padding-right: 0.7rem !important;
            }}
            .mubeen-header h1 {{ font-size: 1.5rem !important; }}
            .mubeen-header p {{ font-size: 0.82rem !important; }}
            h2 {{ font-size: 1.3rem !important; }}
            .mubeen-ai-answer .ai-body {{ font-size: 0.95rem; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# 9. SIDEBAR — باستخدام checkbox (سريع، بدون rerun)
# ---------------------------------------------------------------------------
def render_inline_menu(t: dict):
    """قائمة مدمجة تستخدم checkbox للفتح/الإغلاق السريع (بدون rerun)."""

    # checkbox يعمل بدون st.rerun - سريع جداً
    menu_open = st.checkbox(
        f"☰  {t['menu']}" if not st.session_state.menu_open else f"✕  {t['close_menu']}",
        value=st.session_state.menu_open,
        key="menu_checkbox",
    )

    # تحديث الحالة (Streamlit يتعامل مع التغيير تلقائياً)
    if menu_open != st.session_state.menu_open:
        st.session_state.menu_open = menu_open

    # إذا القائمة مفتوحة — نعرضها كعمود جانبي
    if st.session_state.menu_open:
        col_side, col_main = st.columns([1, 3], gap="large")

        with col_side:
            st.markdown(
                f"""
                <div style="background:#F5F2EB; border:3px solid #1B4D3E;
                            border-radius:14px; padding:18px 16px; margin-top:12px;
                            text-align:center;">
                    <h1 style="color:#1B4D3E; font-family:'Amiri', serif;
                               margin:0; font-size:1.5rem;">{t['app_name']}</h1>
                    <p style="color:#C5A059; font-size:0.8rem; margin-top:4px;">{t['tagline']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"<label style='color:#1B4D3E; font-weight:700; font-size:0.95rem; margin-top:14px; display:block;'>{t['select_lang']}</label>",
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

            st.markdown(
                "<hr style='border: 1px solid #C5A059; opacity:0.4; margin: 14px 0;'>",
                unsafe_allow_html=True,
            )

            st.markdown(
                f"<h4 style='color:#1B4D3E; font-family:Amiri, serif; font-size:1rem; margin-bottom:6px;'>{t['about_title']}</h4>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p style='font-size:0.82rem; color:#555; line-height:1.6; margin-top:0;'>{t['about_text']}</p>",
                unsafe_allow_html=True,
            )

        return col_main

    return st.container()


# ---------------------------------------------------------------------------
# 10. HELPER: تحويل Markdown
# ---------------------------------------------------------------------------
def format_answer_markdown(text: str) -> str:
    import html as html_lib
    import re

    safe = html_lib.escape(text)
    safe = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe)
    safe = re.sub(r"^### (.+)$", r"<h3>\1</h3>", safe, flags=re.MULTILINE)
    safe = re.sub(r"^## (.+)$", r"<h3>\1</h3>", safe, flags=re.MULTILINE)
    safe = re.sub(r"^# (.+)$", r"<h3>\1</h3>", safe, flags=re.MULTILINE)

    parts = safe.split("\n\n")
    formatted_parts = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if p.startswith("<h3"):
            formatted_parts.append(p)
        else:
            formatted_parts.append(f"<p>{p.replace(chr(10), '<br>')}</p>")

    return "".join(formatted_parts)


# ---------------------------------------------------------------------------
# 11. MAIN APP
# ---------------------------------------------------------------------------
def main():
    t = UI_TEXT[st.session_state.lang]
    rtl = t["rtl"]
    lang_dir = t["dir"]

    inject_css(lang_dir, rtl)

    main_area = render_inline_menu(t)

    with main_area:
        st.markdown(
            f"""
            <div class="mubeen-header" dir="{lang_dir}">
                <h1>{t['app_name']}</h1>
                <p>{t['tagline']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""<div class="mubeen-hint" dir="{lang_dir}">{t['events_hint']}</div>""",
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
            title = location_name(selected, st.session_state.lang)
            subtitle = location_subtitle(selected, st.session_state.lang)
            context = location_context(selected, st.session_state.lang)
            st.markdown(
                f"""
                <div class="mubeen-card" dir="{lang_dir}" style="border-color:#1B4D3E; margin-top:14px;">
                    <div class="milestone-title">{title}</div>
                    <div class="milestone-subtitle">{subtitle}</div>
                    <div class="milestone-desc">{context}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            "<hr style='border:1px solid #C5A059; opacity:0.4; margin-top:20px;'>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<h2 style='font-family:Amiri, serif; color:#1B4D3E; text-align:{'right' if rtl else 'left'};'>{t['chat_title']}</h2>",
            unsafe_allow_html=True,
        )

        if st.session_state.pending_prompt:
            prompt_text = st.session_state.pending_prompt
            st.session_state.pending_prompt = None
            st.session_state.chat_history.append(
                {"role": "user", "content": prompt_text}
            )
            with st.spinner(t["spinner"]):
                system_instruction = build_system_instruction(st.session_state.lang)
                prompt = build_user_prompt(st.session_state.lang, prompt_text)
                answer = call_ai(prompt, system_instruction)
            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer}
            )
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

        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input(
                t["chat_title"],
                placeholder=t["chat_placeholder"],
                label_visibility="collapsed",
            )
            submitted = st.form_submit_button(t["chat_button"])

        if submitted and user_input.strip():
            st.session_state.chat_history.append(
                {"role": "user", "content": user_input.strip()}
            )
            with st.spinner(t["spinner"]):
                system_instruction = build_system_instruction(st.session_state.lang)
                prompt = build_user_prompt(st.session_state.lang, user_input.strip())
                answer = call_ai(prompt, system_instruction)
            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer}
            )
            st.rerun()

        st.markdown(
            f"<p style='color:#666; font-size:0.9rem; text-align:{'right' if rtl else 'left'}; margin-top:18px; margin-bottom:8px;'>{t['suggestions']}</p>",
            unsafe_allow_html=True,
        )

        sugg_list = SUGGESTIONS.get(st.session_state.lang, SUGGESTIONS["en"])
        cols = st.columns(2)
        for i, sug in enumerate(sugg_list):
            with cols[i % 2]:
                if st.button(sug, key=f"sug_{i}", use_container_width=True):
                    st.session_state.pending_prompt = sug
                    st.rerun()


if __name__ == "__main__":
    main()
