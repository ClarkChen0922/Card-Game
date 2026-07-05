import streamlit as st
import random
import os

# 1. 頁面基本設定
st.set_page_config(page_title="Lion真心話大冒險", page_icon="💡", layout="centered")

# 2. 讀取外部 CSS 檔案的函式
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 載入靜態樣式 (維持原有的 style.css 即可)
load_css("style.css")

# 全域背景圖片網址 (Pexels 團隊意象圖)
GLOBAL_BG_URL = "https://images.pexels.com/photos/33828271/pexels-photo-33828271.jpeg"

# 3. 讀取「單一總題庫」邏輯
@st.cache_data
def load_all_questions(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

# 啟動時即讀取完整的 42 題
all_questions = load_all_questions("all_questions.txt")

# 4. UI 頂部 (移除了下拉選單)
st.title("💡Lion真心話大冒險")

# 5. 動態注入 (統一背景圖 + 純白字卡)
CARD_BG_COLOR = "#FFFFFF"

st.markdown(f"""
<style>
    /* 全域背景圖片，加入遮罩避免吃色 */
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url("{GLOBAL_BG_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* 固定字卡的背景顏色為純白 */
    .question-card {{
        background-color: {CARD_BG_COLOR} !important;
    }}
</style>
""", unsafe_allow_html=True)

# 6. 核心狀態與抽題邏輯
if "current_question" not in st.session_state:
    st.session_state.current_question = None

# 抽題按鈕：直接從 all_questions 中隨機抽取
if st.button("🎲 點我隨機抽題", type="primary", use_container_width=True):
    if all_questions:
        st.session_state.current_question = random.choice(all_questions)
    else:
        st.session_state.current_question = "錯誤：找不到或無法讀取 all_questions.txt，請檢查檔案名稱。"

# 7. 顯示卡片區域
if st.session_state.current_question:
    st.markdown(f'<div class="question-card">{st.session_state.current_question}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="question-card hint-text">👆<br>請點擊上方按鈕抽出你的專屬問題</div>', unsafe_allow_html=True)
