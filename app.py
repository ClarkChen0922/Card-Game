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

# 3. UI 頂部與選單 (移除階段選擇，改為全自動)
st.title("獅群真心話大冒險")
selected_team = st.selectbox("請選擇組別：", ["第一組", "第二組", "第三組", "第四組"])

# 4. 動態注入 CSS (極簡化防彈版)
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

/* 色塊統一 */
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
button[kind="primary"] div {{
    color: #1E293B !important;
    font-size: 20px !important; 
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
.hint-text {{color: #475569 !important; font-size: 20px !important;}}

@keyframes roll-dice {{
    0%   {{ content: '⚀'; transform: rotate(0deg) scale(1); }}
    16%  {{ content: '⚂'; transform: rotate(15deg) scale(1.1); }}
    33%  {{ content: '⚄'; transform: rotate(-15deg) scale(1); }}
    50%  {{ content: '⚅'; transform: rotate(20deg) scale(1.1); }}
    66%  {{ content: '⚁'; transform: rotate(-20deg) scale(1); }}
    83%  {{ content: '⚃'; transform: rotate(10deg) scale(1.1); }}
    100% {{ content: '⚀'; transform: rotate(0deg) scale(1); }}
}}
.dice-anim::after {{
    content: '⚀';
    animation: roll-dice 0.3s infinite linear;
    display: inline-block;
    font-size: 80px;
    color: #1E293B;
}}

div[data-testid="stExpander"] {{
    background-color: rgba(210, 214, 220, 0.85) !important; 
    border-radius: 10px !important;
    margin-top: 50px !important;
    border: none !important;
}}
div[data-testid="stExpander"] p {{
    color: #475569 !important; 
    text-shadow: none !important;
    font-weight: bold !important;
}}
</style>
""", unsafe_allow_html=True)

# 5. 單機狀態初始化
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "last_team" not in st.session_state:
    st.session_state.last_team = selected_team

if st.session_state.last_team != selected_team:
    st.session_state.current_question = None
    st.session_state.last_team = selected_team

# ==========================================
# 📌 雲端共用牌池 (加入輪流切換邏輯)
# ==========================================
@st.cache_resource
def get_shared_pools():
    return {}

shared_pools = get_shared_pools()

def init_pools():
    for team in ["第一組", "第二組", "第三組", "第四組"]:
        if team not in shared_pools:
            w_pool = list(range(len(warmup_questions))) if warmup_questions else []
            f_pool = list(range(len(formal_questions))) if formal_questions else []
            random.shuffle(w_pool)
            random.shuffle(f_pool)
            shared_pools[team] = {
                "warmup": w_pool,
                "formal": f_pool,
                "next_draw": "warmup"  # 新增：紀錄下一張該抽什麼
            }

init_pools()

# 6. 畫面佈局
draw_button_clicked = st.button("🎲 點擊抽取題目", type="primary", use_container_width=True)
card_placeholder = st.empty()

# 7. 抽題按鈕與骰子動畫邏輯
if draw_button_clicked:
    current_team_state = shared_pools[selected_team]
    
    # 判斷這回合該抽哪一種題庫
    current_type = current_team_state["next_draw"]
    
    card_placeholder.markdown(
        f'<div class="question-card">'
        f'<div class="dice-anim"></div><br>'
        f'<span style="font-size: 22px; color: #475569; font-weight: bold;">抽取中...</span>'
        f'</div>', 
        unsafe_allow_html=True
    )
    time.sleep(0.8)  
        
    try:
        if current_type == "warmup" and warmup_questions:
            if len(current_team_state["warmup"]) == 0:
                pool = list(range(len(warmup_questions)))
                random.shuffle(pool)
                current_team_state["warmup"] = pool
            
            selected_idx = current_team_state["warmup"].pop()
            q_text = warmup_questions[selected_idx]
            tag = "🧊 暖身題"
            # 抽完暖身題，設定下次抽正式題
            current_team_state["next_draw"] = "formal"
            
        elif current_type == "formal" and formal_questions:
            if len(current_team_state["formal"]) == 0:
                pool = list(range(len(formal_questions)))
                random.shuffle(pool)
                current_team_state["formal"] = pool
            
            selected_idx = current_team_state["formal"].pop()
            q_text = formal_questions[selected_idx]
            tag = "🎯 正式題"
            # 抽完正式題，設定下次抽暖身題
            current_team_state["next_draw"] = "warmup"
            
        q_num = selected_idx + 1
        
        st.session_state.current_question = (
            f'<div style="font-size: 16px; color: #64748B; font-weight: 800; margin-bottom: 15px; letter-spacing: 2px;">'
            f'{tag} - QUESTION {q_num:02d}'
            f'</div>'
            f'{q_text}'
        )
    except IndexError:
        shared_pools.clear()
        st.session_state.current_question = None
        st.rerun()

# 8. 最終畫面渲染
if st.session_state.current_question:
    card_placeholder.markdown(f'<div class="question-card">{st.session_state.current_question}</div>', unsafe_allow_html=True)
else:
    card_placeholder.markdown('<div class="question-card hint-text">👆<br>準備好了嗎？點擊上方按鈕</div>', unsafe_allow_html=True)

# 9. 主持人專區
with st.expander("⚙️ 主持人專區 (測試與重置)"):
    st.write("活動開始前，若已經測試抽過，請點擊下方按鈕將雲端進度歸零。")
    if st.button("🔄 重置全場進度", type="secondary", use_container_width=True):
        shared_pools.clear()
        st.session_state.current_question = None
        st.rerun()
