import streamlit as st
import random
import os
import time

# 1. 頁面基本設定
st.set_page_config(page_title="獅群真心話大冒險", page_icon="💡", layout="centered")

GLOBAL_BG_URL = "https://images.pexels.com/photos/33828271/pexels-photo-33828271.jpeg"

# 2. 讀取題庫邏輯
def load_questions(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

warmup_questions = load_questions("warmup_questions.txt")
formal_questions = load_questions("formal_questions.txt")

# 3. UI 頂部與選單
st.title("獅群真心話大冒險")
selected_team = st.selectbox("請選擇組別：", ["第一組", "第二組", "第三組", "第四組"])

# 4. 動態注入 CSS 
st.markdown(f"""
<style>
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}

.stApp {{
    background-image: linear-gradient(rgba(0, 0, 0, 0.55), rgba(0, 0, 0, 0.55)), url("{GLOBAL_BG_URL}"); 
    background-size: cover; 
    background-position: center; 
    background-attachment: fixed;
}}

h1 {{
    font-size: 42px !important; 
    color: #FFFFFF !important; 
    font-weight: 900 !important; 
    text-align: center !important;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5) !important; 
    margin-bottom: 30px !important;
}}

label[data-testid="stWidgetLabel"] p {{
    color: #FFFFFF !important; 
    font-size: 16px !important; 
    font-weight: 600 !important; 
    text-shadow: 1px 1px 4px rgba(0,0,0,0.6) !important;
}}

div[data-baseweb="select"] > div,
button[kind="primary"] {{
    background-color: rgba(255, 255, 255, 0.85) !important; 
    backdrop-filter: blur(12px) !important; 
    -webkit-backdrop-filter: blur(12px) !important; 
    border: 1px solid rgba(255, 255, 255, 0.6) !important; 
    border-radius: 12px !important;
}}

div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] p {{
    color: #1E293B !important;
    font-size: 18px !important;
    font-weight: 800 !important;
}}

button[kind="primary"] {{
    padding: 12px 0px !important;
    margin-top: 15px !important;
    margin-bottom: 10px !important;
}}
button[kind="primary"]:hover {{
    background-color: rgba(255, 255, 255, 1) !important; 
    border-color: #FFFFFF !important; 
}}
/* 🚀 在這裡將按鈕文字加到最粗 (900) 並且稍微放大 */
button[kind="primary"] div {{
    color: #1E293B !important;
    font-size: 22px !important; 
    font-weight: 900 !important;
}}

.question-card {{
    background-color: rgba(255, 255, 255, 0.85) !important; 
    backdrop-filter: blur(12px) !important; 
    -webkit-backdrop-filter: blur(12px) !important; 
    border: 1px solid rgba(255, 255, 255, 0.6) !important; 
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important; 
    border-radius: 20px !important; 
    padding: 40px 30px !important; 
    margin: 20px 0px !important; 
    text-align: center !important; 
    font-size: 30px !important; 
    font-weight: 800 !important; 
    color: #1E293B !important; 
    line-height: 1.5 !important; 
    word-wrap: break-word !important;
}}
.
