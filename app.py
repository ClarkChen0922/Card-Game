import streamlit as st
import random
import os

# 1. 頁面基本設定
st.set_page_config(page_title="問題字卡產生器", page_icon="💡", layout="centered")

# 2. 讀取外部 CSS 檔案的函式 (絕對路徑防護)
def load_css(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# 全域背景圖片網址
GLOBAL_BG_URL = "https://images.pexels.com/photos/33828271/pexels-photo-33828271.jpeg"

# 3. 讀取「單一總題庫」邏輯
def load_all_questions(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

all_questions = load_all_questions("all_questions.txt")

# 4. UI 頂部
st.title("💡 換位思考工作坊")

# 5. 動態注入 (毛玻璃特效 + 版面推移)
st.markdown(f"""
<style>
    /* 稍微調降全域黑色遮罩的濃度，讓獅子更亮眼 */
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.15)), url("{GLOBAL_BG_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* 🦁 將按鈕區塊往下推，避開獅子的眼睛 (留白美學) */
    div.stButton {{
        margin-top: 180px !important; 
    }}
    
    /* 字卡毛玻璃特效 (半透明白 + 模糊) */
    .question-card {{
        background-color: rgba(255, 255, 255, 0.65) !important; 
        backdrop-filter: blur(12px) !important;                
        -webkit-backdrop-filter: blur(12px) !important;        
        border: 1px solid rgba(255, 255, 255, 0.6) !important; 
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important; 
    }}

    /* 覆蓋原本的紅色按鈕，改為毛玻璃特效 */
    button[kind="primary"] {{
        background-color: rgba(255, 255, 255, 0.65) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
        color: #1E293B !important;  
    }}
    
    /* 按鈕懸停 (Hover) 時的微調 */
    button[kind="primary"]:hover {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        border-color: #FFFFFF !important;
        color: #000000 !important;
    }}
    
    /* 確保按鈕內的字體夠粗夠清楚 */
    button[kind="primary"] div {{
        font-size: 22px !important;
        font-weight: 900 !important;
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
        current_dir = os.path.dirname(os.path.abspath(__file__))
        error_msg = f"錯誤：無法讀取檔案。程式正在尋找的路徑為：<br>{os.path.join(current_dir, 'all_questions.txt')}"
        st.session_state.current_question = error_msg

# 7. 顯示卡片區域
if st.session_state.current_question:
    st.markdown(f'<div class="question-card">{st.session_state.current_question}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="question-card hint-text">👆<br>請點擊上方按鈕抽出你的專屬問題</div>', unsafe_allow_html=True)
