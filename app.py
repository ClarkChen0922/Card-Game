import streamlit as st
import random
import os
import time

# 1. 頁面基本設定
st.set_page_config(page_title="Lion換位思考工作坊", page_icon="💡", layout="centered")

# 2. 讀取外部 CSS 檔案的函式
def load_css(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# 全域背景圖片網址
GLOBAL_BG_URL = "https://images.pexels.com/photos/33828271/pexels-photo-33828271.jpeg"

# 3. 讀取題庫邏輯
def load_questions(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

# 載入兩份題庫
warmup_questions = load_questions("warmup_questions.txt")
formal_questions = load_questions("formal_questions.txt")

# 4. UI 頂部與題庫選擇
st.title("💡 Lion換位思考工作坊")

selected_mode = st.radio(
    "請選擇當前階段：",
    ["🌞 暖身題", "🔥 正式題"],
    horizontal=True
)

# 5. 動態注入 CSS
st.markdown(f"""
<style>
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.15)), url("{GLOBAL_BG_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* 強制將 Radio 按鈕的所有文字 (包含標題與選項) 設為白色與粗體 */
    div.stRadio p {{
        color: #FFFFFF !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.8) !important;
    }}
    
    /* 🦁 將按鈕區塊微調至獅子眼睛下方 (從 350px 往上拉回 240px) */
    div.stButton {{
        margin-top: 240px !important; 
        margin-bottom: 20px !important; 
    }}
    
    .question-card {{
        background-color: rgba(255, 255, 255, 0.65) !important; 
        backdrop-filter: blur(12px) !important;                
        -webkit-backdrop-filter: blur(12px) !important;        
        border: 1px solid rgba(255, 255, 255, 0.6) !important; 
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important; 
    }}

    button[kind="primary"] {{
        background-color: rgba(255, 255, 255, 0.65) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
        color: #1E293B !important;  
    }}
    
    button[kind="primary"]:hover {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        border-color: #FFFFFF !important;
        color: #000000 !important;
    }}
    
    button[kind="primary"] div {{
        font-size: 22px !important;
        font-weight: 900 !important;
    }}
</style>
""", unsafe_allow_html=True)

# 6. 核心狀態初始化
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "last_mode" not in st.session_state:
    st.session_state.last_mode = selected_mode
if "warmup_q1_drawn" not in st.session_state:
    st.session_state.warmup_q1_drawn = False

# 當切換題庫階段
