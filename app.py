# app.py
# تطبيق مسار | Masar App - المحتوى المرئي الهادف للأطفال واليافعين
# تطوير المهندسة: رنا وعدالله محمد

import streamlit as st
import base64
from channels_data import CHANNELS
import random
import urllib.parse

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="مَسَار | المحتوى المرئي الهادف للأطفال واليافعين",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. دالة تحويل صورة الشعار إلى Base64
@st.cache_data
def get_image_as_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return None

logo_base64 = get_image_as_base64("masar_logo.png")

# 3. تهيئة حالات الجلسة (Session State)
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# قائمة نصائح تربوية متجددة لأولياء الأمور
PARENT_TIPS = [
    "حدد وقتاً معيناً يومياً لاستخدام الشاشات (مثلاً ساعة واحدة) ويفضل أن يكون بعد إتمام الواجبات المنزلية.",
    "شارك طفلك مشاهدة المحتوى ومناقشته؛ هذا يعزز الفهم ويقوي أواصر التواصل والتفاهم بينكما.",
    "استخدم أدوات الرقابة الأبوية وتطبيقات التصفية لحجب المحتوى غير اللائق وضمان بيئة تصفح آمنة.",
    "شجع طفلك على ممارسة أنشطة حركية ورياضية وقراءة الكتب الحقيقية للحد من الإدمان الرقمي.",
    "اجعل غرف النوم مناطق خالية من الأجهزة الذكية ليلاً لمساعدة طفلك في الحصول على نوم صحي وعميق.",
    "كن قدوة حسنة لطفلك في استخدام الهواتف الذكية؛ فالأطفال يقلدون سلوكيات آبائهم تلقائياً.",
    "ركز على القنوات التفاعلية التي تطلب من الطفل القيام بأنشطة يدوية أو حل مشكلات بدلاً من التلقي السلبي."
]

if "tip_index" not in st.session_state:
    st.session_state.tip_index = random.randint(0, len(PARENT_TIPS) - 1)

# 4. إعداد السمات البصرية (Dynamic Themes)
THEME_CONFIGS = {
    "سماوي كلاسيكي 🌊": {
        "bg_gradient": "linear-gradient(135deg, #f0f4f9 0%, #e2ebf8 100%)",
        "text_color": "#0f172a",
        "primary_color": "#1d4ed8",
        "primary_hover": "#1e40af",
        "card_bg": "rgba(255, 255, 255, 0.85)",
        "card_border": "rgba(255, 255, 255, 0.8)",
        "sidebar_bg": "#f8fafc",
        "desc_color": "#475569",
        "shadow": "0 10px 25px -5px rgba(29, 78, 216, 0.08), 0 8px 10px -6px rgba(29, 78, 216, 0.04)",
        "btn_visit_bg": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
        "btn_visit_hover": "linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)",
        "stat_card_bg": "rgba(255, 255, 255, 0.7)",
        "tag_bg": "rgba(29, 78, 216, 0.08)",
        "tag_color": "#1d4ed8"
    },
    "غروب دافئ 🌅": {
        "bg_gradient": "linear-gradient(135deg, #fff7ed 0%, #ffedd5 50%, #fed7aa 100%)",
        "text_color": "#431407",
        "primary_color": "#ea580c",
        "primary_hover": "#c2410c",
        "card_bg": "rgba(255, 255, 255, 0.88)",
        "card_border": "rgba(255, 255, 255, 0.9)",
        "sidebar_bg": "#fffbeb",
        "desc_color": "#7c2d12",
        "shadow": "0 10px 25px -5px rgba(234, 88, 12, 0.1)",
        "btn_visit_bg": "linear-gradient(135deg, #f97316 0%, #ea580c 100%)",
        "btn_visit_hover": "linear-gradient(135deg, #ea580c 0%, #c2410c 100%)",
        "stat_card_bg": "rgba(255, 255, 255, 0.75)",
        "tag_bg": "rgba(234, 88, 12, 0.1)",
        "tag_color": "#c2410c"
    },
    "نعناع هادئ 🌿": {
        "bg_gradient": "linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)",
        "text_color": "#064e3b",
        "primary_color": "#16a34a",
        "primary_hover": "#15803d",
        "card_bg": "rgba(255, 255, 255, 0.88)",
        "card_border": "rgba(255, 255, 255, 0.9)",
        "sidebar_bg": "#f0fdf4",
        "desc_color": "#14532d",
        "shadow": "0 10px 25px -5px rgba(22, 163, 74, 0.1)",
        "btn_visit_bg": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
        "btn_visit_hover": "linear-gradient(135deg, #059669 0%, #047857 100%)",
        "stat_card_bg": "rgba(255, 255, 255, 0.75)",
        "tag_bg": "rgba(22, 163, 74, 0.1)",
        "tag_color": "#15803d"
    },
    "فضاء مظلم 🌌": {
        "bg_gradient": "linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e1b4b 100%)",
        "text_color": "#f8fafc",
        "primary_color": "#818cf8",
        "primary_hover": "#6366f1",
        "card_bg": "rgba(17, 24, 39, 0.75)",
        "card_border": "rgba(255, 255, 255, 0.1)",
        "sidebar_bg": "#0f172a",
        "desc_color": "#cbd5e1",
        "shadow": "0 10px 30px 0 rgba(0, 0, 0, 0.5)",
        "btn_visit_bg": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
        "btn_visit_hover": "linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)",
        "stat_card_bg": "rgba(30, 41, 59, 0.75)",
        "tag_bg": "rgba(129, 140, 248, 0.15)",
        "tag_color": "#a5b4fc"
    }
}

# 5. الشريط الجانبي (Sidebar)
with st.sidebar:
    if logo_base64:
        st.markdown(f"""
            <div style="text-align: center; margin-top: 10px; margin-bottom: 12px;">
                <img src="data:image/png;base64,{logo_base64}" style="width: 85px; height: 85px; border-radius: 50%; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15); border: 2px solid white;">
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; font-weight: 700;'>🧭 تطبيق مَسَار</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify; font-size: 0.9rem; line-height: 1.6; opacity: 0.9;'>دليلك الموثوق لتوجيه الأطفال والشباب نحو قنوات ومحتوى مرئي تعليمي وتثقيفي هادف يبني شخصيتهم ويطور قدراتهم.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    selected_theme = st.selectbox(
        "🎨 اختر سمة التطبيق:",
        options=list(THEME_CONFIGS.keys()),
        index=0
    )
    
    st.markdown("---")
    
    # نصيحة اليوم التربوية
    st.markdown("##### 💡 نصيحة اليوم لأولياء الأمور:")
    st.info(PARENT_TIPS[st.session_state.tip_index])
    if st.button("نصيحة أخرى 🔄", key="next_tip_btn"):
        st.session_state.tip_index = (st.session_state.tip_index + 1) % len(PARENT_TIPS)
        st.rerun()

    st.markdown("---")
    
    # بطاقة المطور
    st.markdown("""
        <div style="text-align: center; padding: 14px; background: rgba(255, 255, 255, 0.05); border-radius: 16px; border: 1px solid rgba(255,255,255,0.1);">
            <p style="font-size: 0.9rem; font-weight: bold; margin-bottom: 6px;">💻 تطوير وإشراف</p>
            <p style="font-size: 0.85rem; line-height: 1.5; margin: 0;">
                المهندسة المتخصصة في الذكاء الاصطناعي<br>
                <span style="font-weight: 700; color: #1d4ed8;">رنا وعدالله محمد</span><br>
                <span style="font-size: 0.75rem; opacity: 0.7;">إصدار MVP 2.0 ✨ • © 2026</span>
            </p>
            <div style="margin-top: 10px;">
                <a href="https://github.com/ranaawaad/masar_kids" target="_blank" style="text-decoration: none; font-size: 0.8rem; font-weight: 600; background: rgba(0,0,0,0.06); padding: 4px 10px; border-radius: 12px; color: inherit;">
                    🐙 Github Repo ➔
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)

tc = THEME_CONFIGS[selected_theme]

# 6. حقن خط Cairo وتنسيقات CSS المتقدمة (UI/UX overhaul)
st.markdown(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        /* التنسيق الأساسي */
        html, body, [data-testid="stAppViewContainer"], .stApp {{
            font-family: 'Cairo', sans-serif !important;
            background: {tc['bg_gradient']} !important;
            color: {tc['text_color']} !important;
            direction: rtl;
        }}

        * {{
            direction: rtl;
            text-align: right;
        }}

        /* إخفاء القوائم الافتراضية */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}

        /* حاوية العرض الرئيسية */
        .block-container {{
            padding-top: 1.2rem !important;
            padding-bottom: 2.5rem !important;
            max-width: 680px !important;
            margin: auto;
        }}

        /* الشريط الجانبي */
        [data-testid="stSidebar"] {{
            background-color: {tc['sidebar_bg']} !important;
            border-inline-start: 1px solid {tc['card_border']} !important;
        }}

        /* رأس الصفحة والتصميم */
        .header-box {{
            text-align: center !important;
            background: {tc['card_bg']};
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid {tc['card_border']};
            border-radius: 24px;
            padding: 24px 20px;
            margin-bottom: 20px;
            box-shadow: {tc['shadow']};
        }}
        .header-box h1 {{
            color: {tc['primary_color']} !important;
            font-weight: 800;
            font-size: 2.3rem;
            margin-bottom: 6px;
            text-align: center !important;
        }}
        .header-box p {{
            color: {tc['desc_color']} !important;
            font-size: 1.05rem;
            line-height: 1.6;
            margin-bottom: 12px;
            text-align: center !important;
        }}
        .safe-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: {tc['tag_bg']};
            color: {tc['tag_color']};
            font-size: 0.82rem;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 20px;
        }}

        /* بطاقات الإحصائيات الأربعة */
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: {tc['stat_card_bg']};
            border: 1px solid {tc['card_border']};
            border-radius: 16px;
            padding: 12px 8px;
            text-align: center !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            transition: transform 0.2s ease;
        }}
        .stat-card:hover {{
            transform: translateY(-2px);
        }}
        .stat-val {{
            font-size: 1.35rem;
            font-weight: 800;
            color: {tc['primary_color']};
            text-align: center !important;
            line-height: 1.2;
        }}
        .stat-lbl {{
            font-size: 0.78rem;
            font-weight: 600;
            color: {tc['desc_color']};
            text-align: center !important;
            margin-top: 4px;
        }}

        /* بطاقات القنوات المحسّنة */
        div[data-testid="stVerticalBlockBorderContainer"] {{
            background: {tc['card_bg']} !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid {tc['card_border']} !important;
            border-radius: 20px !important;
            padding: 20px !important;
            margin-bottom: 16px !important;
            box-shadow: {tc['shadow']} !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        div[data-testid="stVerticalBlockBorderContainer"]:hover {{
            transform: translateY(-3px) !important;
            border-color: {tc['primary_color']} !important;
            box-shadow: 0 14px 30px rgba(0,0,0,0.08) !important;
        }}

        .channel-type-badge {{
            background: {tc['tag_bg']};
            color: {tc['tag_color']};
            font-size: 0.75rem;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 8px;
            display: inline-block;
            margin-bottom: 8px;
        }}
        .channel-title {{
            color: {tc['primary_color']} !important;
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 8px;
            line-height: 1.4;
        }}
        .channel-desc {{
            color: {tc['desc_color']} !important;
            font-size: 0.94rem;
            margin-bottom: 14px;
            line-height: 1.65;
        }}

        /* وسوم الكلمات المفتاحية (Tags) */
        .tag-pill {{
            display: inline-block;
            background: rgba(0, 0, 0, 0.04);
            color: {tc['desc_color']};
            font-size: 0.75rem;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 6px;
            margin-inline-end: 5px;
            margin-bottom: 10px;
        }}

        /* زر زيارة القناة */
        .btn-visit-link {{
            background: {tc['btn_visit_bg']} !important;
            color: white !important;
            padding: 9px 16px;
            border-radius: 50px;
            font-size: 0.9rem;
            font-weight: 700;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
            width: 100%;
            height: 42px;
            text-align: center !important;
        }}
        .btn-visit-link:hover {{
            transform: scale(1.02);
            box-shadow: 0 6px 18px rgba(220, 38, 38, 0.35);
            background: {tc['btn_visit_hover']} !important;
            color: white !important;
        }}

        /* أزرار Streamlit الثانوية */
        div[data-testid="stButton"] button {{
            border-radius: 50px !important;
            border: 1px solid {tc['primary_color']} !important;
            color: {tc['primary_color']} !important;
            background: rgba(255, 255, 255, 0.1) !important;
            width: 100% !important;
            height: 42px !important;
            font-size: 0.9rem !important;
            font-weight: 700 !important;
            transition: all 0.2s ease !important;
            font-family: 'Cairo', sans-serif !important;
        }}
        div[data-testid="stButton"] button:hover {{
            background: {tc['primary_color']} !important;
            color: white !important;
        }}

        /* تسميات الحقول */
        label[data-testid="stWidgetLabel"] {{
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            color: {tc['text_color']} !important;
        }}

        /* تخصيص زر السجمنت (Segmented Control) */
        div[data-testid="stSegmentedControl"] button {{
            border-radius: 12px !important;
            padding: 8px 14px !important;
            font-size: 0.92rem !important;
            font-weight: 700 !important;
            font-family: 'Cairo', sans-serif !important;
        }}
    </style>
""", unsafe_allow_html=True)

# 7. حوار التحقق لأولياء الأمور (Parental Gate Dialog)
@st.dialog("🔓 بوابة التحقق لأولياء الأمور", dismissible=True)
def parent_gate_dialog():
    st.write("للدخول إلى أدوات ومراجع الرقابة الأبوية، يرجى الإجابة على التحدي التالي للتأكد من عدم وصول الأطفال:")
    
    if "gate_num1" not in st.session_state:
        st.session_state.gate_num1 = random.randint(6, 9)
        st.session_state.gate_num2 = random.randint(6, 9)

    correct_answer = st.session_state.gate_num1 * st.session_state.gate_num2
    st.markdown(f"**السؤال:** كم حاصل ضرب **{st.session_state.gate_num1} × {st.session_state.gate_num2}**؟")
    
    ans = st.number_input("إجابتك الرقمية:", min_value=0, step=1, key="gate_answer_input")
    
    col_submit, col_refresh = st.columns([2, 1])
    with col_submit:
        if st.button("التحقق والدخول ✔️", key="btn_confirm_gate"):
            if ans == correct_answer:
                st.session_state.parent_authenticated = True
                st.success("تم التحقق بنجاح! تم فتح قسم أولياء الأمور.")
                del st.session_state.gate_num1
                del st.session_state.gate_num2
                st.rerun()
            else:
                st.error("إجابة خاطئة! يرجى المحاولة مرة أخرى.")
    with col_refresh:
        if st.button("تغيير 🔄", key="btn_new_gate_q"):
            st.session_state.gate_num1 = random.randint(6, 9)
            st.session_state.gate_num2 = random.randint(6, 9)
            st.rerun()

# 8. حساب الإحصائيات
total_channels = 0
for age in CHANNELS:
    for interest in CHANNELS[age]:
        total_channels += len(CHANNELS[age][interest])

total_categories = sum(len(CHANNELS[age]) for age in CHANNELS)
fav_count = len(st.session_state.favorites)

# 9. الترويسة الرئيسية واللوحة
if logo_base64:
    st.markdown(f"""
        <div style="text-align: center; margin-top: 5px; margin-bottom: -10px;">
            <img src="data:image/png;base64,{logo_base64}" style="width: 95px; height: 95px; border-radius: 50%; box-shadow: 0 4px 18px rgba(0,0,0,0.15); border: 3px solid white;">
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
    <div class="header-box">
        <h1>🧭 مَسَار</h1>
        <p>منصتك التفاعلية لتوجيه الأطفال واليافعين نحو محتوى مرئي آمن، مُنتقى بعناية لبناء الفكر وتطوير المهارات.</p>
        <div class="safe-badge">
            🛡️ محتوى منسّق وموثوق 100% • بيئة آمنة للأبناء
        </div>
    </div>
""", unsafe_allow_html=True)

# 10. شبكة الإحصائيات البصرية
st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-val">📺 {total_channels}</div>
            <div class="stat-lbl">قناة ومصدر</div>
        </div>
        <div class="stat-card">
            <div class="stat-val">💡 {total_categories}</div>
            <div class="stat-lbl">تصنيفاً هادفاً</div>
        </div>
        <div class="stat-card">
            <div class="stat-val">⭐ {fav_count}</div>
            <div class="stat-lbl">قناة محفوظة</div>
        </div>
        <div class="stat-card">
            <div class="stat-val">🔒 100%</div>
            <div class="stat-lbl">رقابة وتدقيق</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 11. قسم القنوات المفضلة (إن وجدت)
if st.session_state.favorites:
    with st.expander(f"⭐ القنوات المحفوظة لديك ({len(st.session_state.favorites)})", expanded=False):
        for fav in st.session_state.favorites:
            col_fav_title, col_fav_del = st.columns([3, 1])
            with col_fav_title:
                st.markdown(f"**{fav.get('type', '📺')} {fav['name']}**")
            with col_fav_del:
                if st.button("حذف", key=f"del_fav_{fav['name']}", icon="🗑️"):
                    st.session_state.favorites = [f for f in st.session_state.favorites if f['name'] != fav['name']]
                    st.rerun()
        
        st.markdown("---")
        
        # مشاركة عبر الواتساب والنسخ
        share_text = "🧭 القنوات المقترحة عبر تطبيق مَسَار لتربية وتوجيه الأطفال:\n\n"
        for idx, fav in enumerate(st.session_state.favorites, 1):
            share_text += f"{idx}. {fav['name']} - {fav['url']}\n"
        share_text += "\nتم اختيار المحتوى بعناية لحماية الأطفال وتنمية مهاراتهم."
        
        wa_link = f"https://api.whatsapp.com/send?text={urllib.parse.quote(share_text)}"
        
        col_wa, col_clear = st.columns([2, 1])
        with col_wa:
            st.markdown(f"""
                <a href="{wa_link}" target="_blank" class="btn-visit-link" style="background: linear-gradient(135deg, #25D366 0%, #128C7E 100%) !important;">
                    💬 مشاركة قائمة المفضلة عبر الواتساب
                </a>
            """, unsafe_allow_html=True)
        with col_clear:
            if st.button("مسح الكل 🗑️", key="clear_all_favs"):
                st.session_state.favorites = []
                st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# 12. محرك البحث الذكي
col_search_input, col_search_scope = st.columns([2, 1])
with col_search_input:
    search_query = st.text_input("🔍 ابحث في القنوات والمواضيع:", placeholder="اكتب اسم القناة، الكلمة المفتاحية (مثلاً: برمجة، علوم)...")
with col_search_scope:
    search_scope = st.selectbox("نطاق البحث:", ["القسم الحالي", "جميع الفئات العمرية"])

st.markdown("<br>", unsafe_allow_html=True)

# 13. اختيار الفئة العمرية (Deep Linking synced)
q_age = st.query_params.get("age", None)
q_interest = st.query_params.get("interest", None)

age_groups = list(CHANNELS.keys())
default_age = age_groups[0]
if q_age in age_groups:
    default_age = q_age

selected_age = st.segmented_control(
    "🧭 اختر الفئة العمرية أو القسم الرئيسي:",
    options=age_groups,
    selection_mode="single",
    default=default_age
)

if selected_age:
    st.query_params["age"] = selected_age

st.markdown("<br>", unsafe_allow_html=True)

# 14. اختيار المجال والاهتمام
if selected_age:
    interests = list(CHANNELS[selected_age].keys())
    default_interest = interests[0]
    if q_interest in interests:
        default_interest = q_interest

    selected_interest = st.segmented_control(
        "💡 اختر مجال الاهتمام:",
        options=interests,
        selection_mode="single",
        default=default_interest
    )

    if selected_interest:
        st.query_params["interest"] = selected_interest

    st.markdown("<br>", unsafe_allow_html=True)

    # تجميع القنوات المفلترة حسب البحث أو التصفح
    matching_channels = []

    if search_query:
        query_lower = search_query.lower()
        
        if search_scope == "جميع الفئات العمرية":
            for age in CHANNELS:
                for int_cat in CHANNELS[age]:
                    for ch in CHANNELS[age][int_cat]:
                        tags_str = " ".join(ch.get("tags", []))
                        if query_lower in ch['name'].lower() or query_lower in ch['description'].lower() or query_lower in tags_str.lower():
                            ch_copy = ch.copy()
                            ch_copy['badge_info'] = f"{age} • {int_cat}"
                            matching_channels.append(ch_copy)
        else:
            if selected_interest:
                for ch in CHANNELS[selected_age][selected_interest]:
                    tags_str = " ".join(ch.get("tags", []))
                    if query_lower in ch['name'].lower() or query_lower in ch['description'].lower() or query_lower in tags_str.lower():
                        ch_copy = ch.copy()
                        ch_copy['badge_info'] = selected_interest
                        matching_channels.append(ch_copy)

    # 15. التحكم بفتح/قفل قسم أولياء الأمور
    if selected_age == "🛡️ دليل وأدوات أولياء الأمور" and not st.session_state.get("parent_authenticated", False):
        st.warning("⚠️ هذا القسم يحتوي على أدوات ومراجع تقنية مخصصة لأولياء الأمور فقط لحماية الأطفال.")
        if st.button("🔓 فتح بوابة التحقق للأهل"):
            parent_gate_dialog()
    else:
        if selected_age == "🛡️ دليل وأدوات أولياء الأمور" and st.session_state.get("parent_authenticated", False):
            if st.button("🔒 قفل بوابة أولياء الأمور"):
                st.session_state.parent_authenticated = False
                st.rerun()

        # تحديد القنوات الواجب عرضها
        if search_query:
            st.markdown(f"##### 🔍 نتائج البحث عن **'{search_query}'** ({len(matching_channels)} قناة):")
            st.markdown("<br>", unsafe_allow_html=True)
            if not matching_channels:
                st.info("لم نجد قنوات تطابق بحثك. جرب كلمات أخرى أو اختر 'جميع الفئات العمرية'.")
            else:
                channels_to_display = matching_channels
        else:
            if selected_interest:
                channels_to_display = []
                for ch in CHANNELS[selected_age][selected_interest]:
                    ch_copy = ch.copy()
                    ch_copy['badge_info'] = selected_interest
                    channels_to_display.append(ch_copy)
                st.markdown(f"##### 📺 القنوات المقترحة في **{selected_interest}**:")
                st.markdown("<br>", unsafe_allow_html=True)
            else:
                channels_to_display = []

        # 16. رندرة وتنسيق بطاقات القنوات بشكل عصري ومبهر
        for channel in channels_to_display:
            with st.container(border=True):
                ch_type = channel.get("type", "📺 قناة تعليمية")
                ch_badge = channel.get("badge_info", "")
                
                st.markdown(f"<span class='channel-type-badge'>{ch_type} • {ch_badge}</span>", unsafe_allow_html=True)
                st.markdown(f"<div class='channel-title'>{channel['name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='channel-desc'>{channel['description']}</div>", unsafe_allow_html=True)
                
                # عرض الوسوم الفرعية (Tags)
                if "tags" in channel and channel["tags"]:
                    tags_html = "".join([f"<span class='tag-pill'>#{t}</span>" for t in channel["tags"]])
                    st.markdown(f"<div>{tags_html}</div>", unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # أزرار التفاعل (زيارة + حفظ)
                col_visit, col_fav = st.columns([1, 1])
                
                with col_visit:
                    st.markdown(f"""
                        <a href="{channel['url']}" target="_blank" class="btn-visit-link">
                            زيارة القناة / المنصة ➔
                        </a>
                    """, unsafe_allow_html=True)
                
                with col_fav:
                    is_in_fav = channel['name'] in [f['name'] for f in st.session_state.favorites]
                    if is_in_fav:
                        if st.button("محفوظة ❤️", key=f"btn_fav_{channel['name']}"):
                            st.session_state.favorites = [f for f in st.session_state.favorites if f['name'] != channel['name']]
                            st.rerun()
                    else:
                        if st.button("حفظ 🤍", key=f"btn_fav_{channel['name']}"):
                            st.session_state.favorites.append(channel)
                            st.rerun()
