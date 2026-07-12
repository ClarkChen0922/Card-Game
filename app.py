import streamlit as st
import random
import os
import time

# 1. 頁面基本設定
st.set_page_config(page_title="Lion 換位思考工作坊", page_icon="💡", layout="centered")

# 全域背景圖片網址
GLOBAL_BG_URL = "https://images.pexels.com/photos/33828271/pexels-photo-33828271.jpeg"

# 2. 讀取題庫邏輯 (絕對路徑防護)
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

# 3. UI 頂部與題庫選擇
st.title("💡 Lion 換位思考工作坊")

selected_mode = st.radio(
    "請選擇當前階段：",
    ["🌞 暖身題", "🔥 正式題"],
    horizontal=True
)

# 4. 動態注入 CSS
st.markdown(f"""
<style>
    #MainMenu {{visibility: hidden;}}  
    footer {{visibility: hidden;}} 

    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.15)), url("{GLOBAL_BG_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    h1 {{
        font-size: 42px !important;
        color: #FFFFFF !important;         
        font-weight: 900 !important;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8) !important; 
    }}

    div.stRadio p {{
        color: #FFFFFF !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.8) !important;
    }}
    
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
        border-radius: 30px !important;           
        padding: 60px 40px !important;            
        margin: 30px 0px !important;              
        text-align: center !important;            
        font-size: 38px !important;    
        font-weight: 800 !important;   
        color: #1E293B !important;                
        line-height: 1.5 !important;              
        word-wrap: break-word !important; 
    }}

    .hint-text {{
        color: #475569 !important;     
        font-size: 24px !important;    
    }}

    button[kind="primary"] {{
        background-color: rgba(255, 255, 255, 0.65) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
        color: #1E293B !important;  
        border-radius: 12px !important;
        padding: 10px 0px !important;
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

# 5. 核心狀態初始化
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "last_mode" not in st.session_state:
    st.session_state.last_mode = selected_mode

# 追蹤暖身題第一題是否已經強制出過
if "warmup_q1_drawn" not in st.session_state:
    st.session_state.warmup_q1_drawn = False

# ==========================================
# 📌 抽牌池 (Pool) 系統初始化
# ==========================================
# 建立暖身題牌池 (排除第
