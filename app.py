import streamlit as st
import random
import os
import time  # 引入時間模組來製作動畫延遲

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
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.15)), url("{GLOBAL_BG_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    div.stButton {{
        margin-top: 180px !important; 
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

# 建立一個佔位符 (Placeholder)，這是讓動畫和最終結果能在同一個位子無縫切換的關鍵
card_placeholder = st.empty()

# 7. 抽題按鈕與骰子動畫邏輯
if st.button("🎲 點我隨機抽題", type="primary", use_container_width=True):
    if all_questions:
        # === 動畫階段 ===
        dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
        for _ in range(12):  # 快速切換 12 個影格
            face = random.choice(dice_faces)
            # 在佔位符中渲染動畫畫面
            card_placeholder.markdown(
                f'<div class="question-card">'
                f'<span style="font-size: 80px; color: #1E293B;">{face}</span><br>'
                f'<span style="font-size: 22px; color: #475569; font-weight: bold;">命運的骰子轉動中...</span>'
                f'</div>', 
                unsafe_allow_html=True
            )
            time.sleep(0.08)  # 每個影格停留 0.08 秒
            
        # === 結算階段 ===
        # 取得隨機題目的索引值 (0 到 41)
        selected_idx = random.randint(0, len(all_questions) - 1)
        # 動態生成題號 (將索引值 +1，並補零至兩位數，例如 01, 07, 42)
        q_num = selected_idx + 1
        q_text = all_questions[selected_idx]
        
        # 將題號與題目組裝成高級的 HTML 格式
        st.session_state.current_question = (
            f'<div style="font-size: 18px; color: #475569; font-weight: 800; margin-bottom: 15px; letter-spacing: 2px;">'
            f'QUESTION {q_num:02d}'
            f'</div>'
            f'{q_text}'
        )
    else:
        st.session_state.current_question = "錯誤：無法讀取 all_questions.txt"

# 8. 最終畫面渲染 (無論有沒有點擊按鈕，都會把最新的狀態顯示在佔位符上)
if st.session_state.current_question:
    card_placeholder.markdown(f'<div class="question-card">{st.session_state.current_question}</div>', unsafe_allow_html=True)
else:
    card_placeholder.markdown('<div class="question-card hint-text">👆<br>請點擊上方按鈕抽出你的專屬問題</div>', unsafe_allow_html=True)
