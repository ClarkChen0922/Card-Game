import streamlit as st
import random
import os

# 1. 頁面基本設定
st.set_page_config(page_title="問題字卡產生器", page_icon="💡", layout="centered")

# 2. 讀取外部 CSS 檔案的函式 (加入絕對路徑防護)
def load_css(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# 全域背景圖片網址
GLOBAL_BG_URL = "https://images.pexels.com/photos/33828271/pexels-photo-33828271.jpeg"

# 3. 讀取「單一總題庫」邏輯 (移除快取，並加入絕對路徑防護)
def load_all_questions(filename):
    # 取得 app.py 當下所在的資料夾絕對路徑
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 將資料夾路徑與檔案名稱拼接起來
    file_path = os.path.join(current_dir, filename)
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

# 直接讀取完整的 42 題
all_questions = load_all_questions("all_questions.txt")

# 4. UI 頂部
st.title("💡 換位思考工作坊")

# 5. 動態注入 (統一背景圖 + 純白字卡)
CARD_BG_COLOR = "#FFFFFF"

st.markdown(f"""
<style>
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url("{GLOBAL_BG_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .question-card {{
        background-color: {CARD_BG_COLOR} !important;
    }}
</style>
""", unsafe_allow_html=True)

# 6. 核心狀態與抽題邏輯
if "current_question" not in st.session_state:
    st.session_state.current_question = None

# 抽題按鈕
if st.button("🎲 點我隨機抽題", type="primary", use_container_width=True):
    if all_questions:
        st.session_state.current_question = random.choice(all_questions)
    else:
        # 如果還是錯，把具體的路徑印出來，讓我們知道伺服器到底在找哪裡
        current_dir = os.path.dirname(os.path.abspath(__file__))
        error_msg = f"錯誤：無法讀取檔案。程式正在尋找的路徑為：<br>{os.path.join(current_dir, 'all_questions.txt')}"
        st.session_state.current_question = error_msg

# 7. 顯示卡片區域
if st.session_state.current_question:
    st.markdown(f'<div class="question-card">{st.session_state.current_question}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="question-card hint-text">👆<br>請點擊上方按鈕抽出你的專屬問題</div>', unsafe_allow_html=True)
