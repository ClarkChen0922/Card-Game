import streamlit as st
import random
import os
import time

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
st.title("💡 換位思考工作坊")

# 使用水平排列的單選按鈕來切換題庫
selected_mode = st.radio(
    "請選擇當前階段：",
    ["🌞 暖身題", "🔥 正式題"],
    horizontal=True
)

# 5. 動態注入 (確保 Radio 按鈕在深色背景上也清晰可見)
st.markdown(f"""
<style>
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.15)), url("{GLOBAL_BG_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* 設定 Radio 按鈕的文字顏色為白色 */
    div.row-widget.stRadio > label {{
        color: #FFFFFF !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.8) !important;
    }}
    div[role="radiogroup"] label {{
        color: #FFFFFF !important;
        font-weight: bold !important;
    }}
    
    /* 🦁 將按鈕區塊大幅往下推，避開獅子完整的臉部 */
    div.stButton {{
        margin-top: 350px !important; 
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
# 追蹤暖身題是否已經抽過第一題
if "warmup_q1_drawn" not in st.session_state:
    st.session_state.warmup_q1_drawn = False

# 當切換題庫階段時，自動清空畫面上的舊題目
if st.session_state.last_mode != selected_mode:
    st.session_state.current_question = None
    st.session_state.last_mode = selected_mode

# 7. 畫面佈局：先畫出按鈕，再建立卡片的佔位符
draw_button_clicked = st.button("🎲 點我隨機抽題", type="primary", use_container_width=True)
card_placeholder = st.empty()

# 8. 抽題按鈕與骰子動畫邏輯
if draw_button_clicked:
    # 根據選擇的模式決定使用的題庫
    active_questions = warmup_questions if selected_mode == "🌞 暖身題" else formal_questions
    
    if active_questions:
        # === 動畫階段 ===
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
            
        # === 結算階段 ===
        if selected_mode == "🌞 暖身題":
            if not st.session_state.warmup_q1_drawn:
                # 第一次抽暖身題，強制鎖定 index 0 (第 1 題)
                selected_idx = 0
                st.session_state.warmup_q1_drawn = True
            else:
                # 之後抽暖身題，從 index 1 到最後一題之間隨機抽取，避免重複大合照
                selected_idx = random.randint(1, len(active_questions) - 1)
        else:
            # 正式題：完全隨機抽取
            selected_idx = random.randint(0, len(active_questions) - 1)
            
        q_num = selected_idx + 1
        q_text = active_questions[selected_idx]
        
        st.session_state.current_question = (
            f'<div style="font-size: 18px; color: #475569; font-weight: 800; margin-bottom: 15px; letter-spacing: 2px;">'
            f'QUESTION {q_num:02d}'
            f'</div>'
            f'{q_text}'
        )
    else:
        st.session_state.current_question = f"錯誤：找不到對應的題庫檔案，請確認檔名是否正確。"

# 9. 最終畫面渲染
if st.session_state.current_question:
    card_placeholder.markdown(f'<div class="question-card">{st.session_state.current_question}</div>', unsafe_allow_html=True)
else:
    card_placeholder.markdown('<div class="question-card hint-text">👆<br>請點擊上方按鈕抽出你的專屬問題</div>', unsafe_allow_html=True)
