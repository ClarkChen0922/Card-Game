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

# 4. 動態注入 CSS (防彈壓縮版：嚴禁在 style 標籤內留空白行，避免 Markdown 解析錯誤)
st.markdown(f"""
<style>
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
.stApp {{background-image: linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.15)), url("{GLOBAL_BG_URL}"); background-size: cover; background-position: center; background-attachment: fixed;}}
h1 {{font-size: 42px !important; color: #FFFFFF !important; font-weight: 900 !important; text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8) !important;}}
div.stRadio p {{color: #FFFFFF !important; font-size: 18px !important; font-weight: bold !important; text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.8) !important;}}
div.stButton {{margin-top: 240px !important; margin-bottom: 20px !important;}}
.question-card {{background-color: rgba(255, 255, 255, 0.65) !important; backdrop-filter: blur(12px) !important; -webkit-backdrop-filter: blur(12px) !important; border: 1px solid rgba(255, 255, 255, 0.6) !important; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important; border-radius: 30px !important; padding: 60px 40px !important; margin: 30px 0px !important; text-align: center !important; font-size: 38px !important; font-weight: 800 !important; color: #1E293B !important; line-height: 1.5 !important; word-wrap: break-word !important;}}
.hint-text {{color: #475569 !important; font-size: 24px !important;}}
button[kind="primary"] {{background-color: rgba(255, 255, 255, 0.65) !important; backdrop-filter: blur(10px) !important; -webkit-backdrop-filter: blur(10px) !important; border: 1px solid rgba(255, 255, 255, 0.6) !important; color: #1E293B !important; border-radius: 12px !important; padding: 10px 0px !important;}}
button[kind="primary"]:hover {{background-color: rgba(255, 255, 255, 0.85) !important; border-color: #FFFFFF !important; color: #000000 !important;}}
button[kind="primary"] div {{font-size: 22px !important; font-weight: 900 !important;}}
</style>
""", unsafe_allow_html=True)

# 5. 核心狀態初始化
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "last_mode" not in st.session_state:
    st.session_state.last_mode = selected_mode

if "warmup_q1_drawn" not in st.session_state:
    st.session_state.warmup_q1_drawn = False

# ==========================================
# 📌 抽牌池 (Pool) 系統
# ==========================================
if "warmup_pool" not in st.session_state:
    pool = list(range(1, len(warmup_questions))) if warmup_questions else []
    random.shuffle(pool)
    st.session_state.warmup_pool = pool

if "formal_pool" not in st.session_state:
    pool = list(range(len(formal_questions))) if formal_questions else []
    random.shuffle(pool)
    st.session_state.formal_pool = pool

# 切換題庫時清空畫面，但保留牌池進度
if st.session_state.last_mode != selected_mode:
    st.session_state.current_question = None
    st.session_state.last_mode = selected_mode

# 6. 畫面佈局：先畫出按鈕，再建立卡片的佔位符
draw_button_clicked = st.button("🎲 點我隨機抽題", type="primary", use_container_width=True)
card_placeholder = st.empty()

# 7. 抽題按鈕與骰子動畫邏輯
if draw_button_clicked:
    active_questions = warmup_questions if selected_mode == "🌞 暖身題" else formal_questions
    
    if active_questions:
        # 動畫階段
        dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
        for _ in range(12):  
            face = random.choice(dice_faces)
            card_placeholder.markdown(
                f'<div class="question-card">'
                f'<span style="font-size: 80px; color: #1E293B;">{face}</span><br>'
                f'<span style="font-size: 22px; color: #475569; font-weight: bold;">命運的骰子轉動中...</span>'
                f'</div>', 
                unsafe_allow_html=True
            )
            time.sleep(0.08)  
            
        # 結算階段 (不放回抽樣)
        if selected_mode == "🌞 暖身題":
            if not st.session_state.warmup_q1_drawn:
                selected_idx = 0
                st.session_state.warmup_q1_drawn = True
            else:
                if len(st.session_state.warmup_pool) == 0:
                    pool = list(range(len(warmup_questions)))
                    random.shuffle(pool)
                    st.session_state.warmup_pool = pool
                selected_idx = st.session_state.warmup_pool.pop()
        else:
            if len(st.session_state.formal_pool) == 0:
                pool = list(range(len(formal_questions)))
                random.shuffle(pool)
                st.session_state.formal_pool = pool
            selected_idx = st.session_state.formal_pool.pop()
            
        q_num = selected_idx + 1
        q_text = active_questions[selected_idx]
        
        st.session_state.current_question = (
            f'<div style="font-size: 18px; color: #475569; font-weight: 800; margin-bottom: 15px; letter-spacing: 2px;">'
            f'QUESTION {q_num:02d}'
            f'</div>'
            f'{q_text}'
        )
    else:
        st.session_state.current_question = f"錯誤：找不到對應的題庫檔案。"

# 8. 最終畫面渲染
if st.session_state.current_question:
    card_placeholder.markdown(f'<div class="question-card">{st.session_state.current_question}</div>', unsafe_allow_html=True)
else:
    card_placeholder.markdown('<div class="question-card hint-text">👆<br>請點擊上方按鈕抽出你的專屬問題</div>', unsafe_allow_html=True)
