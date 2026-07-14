import streamlit as st
import random
import os
import time

# 1. 頁面基本設定
st.set_page_config(page_title=" Lion 能量補給站", page_icon="💡", layout="centered")

# 全域背景圖片網址
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
st.title(" Lion 能量補給站")

selected_team = st.selectbox("請選擇組別：", ["第一組", "第二組", "第三組", "第四組"])
selected_mode = st.radio("請選擇階段：", ["🧊 暖身題", "🎯 正式題"], horizontal=True)

# 4. 動態注入 CSS (達成前三個色塊完美統一，並實作自訂超大打勾框)
st.markdown(f"""
<style>
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}

/* 背景遮罩維持 0.55 的濃度 */
.stApp {{
    background-image: linear-gradient(rgba(0, 0, 0, 0.55), rgba(0, 0, 0, 0.55)), url("{GLOBAL_BG_URL}"); 
    background-size: cover; 
    background-position: center; 
    background-attachment: fixed;
}}

/* 大標題 */
h1 {{
    font-size: 42px !important; 
    color: #FFFFFF !important; 
    font-weight: 900 !important; 
    text-align: center !important;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5) !important; 
    margin-bottom: 30px !important;
}}

/* 標籤文字 (請選擇組別、請選擇階段) 統一為帶陰影的白字 */
label[data-testid="stWidgetLabel"] p {{
    color: #FFFFFF !important; 
    font-size: 16px !important; 
    font-weight: 600 !important; 
    text-shadow: 1px 1px 4px rgba(0,0,0,0.6) !important;
}}

/* ==================================================
   🎯 統一前三個色塊 (1.下拉選單、2.階段選擇、3.抽題按鈕)
   顏色、透明度 (0.85)、毛玻璃模糊度與圓角完全一致
   ================================================== */
div[data-baseweb="select"] > div,
div[role="radiogroup"],
button[kind="primary"] {{
    background-color: rgba(255, 255, 255, 0.85) !important; 
    backdrop-filter: blur(12px) !important; 
    -webkit-backdrop-filter: blur(12px) !important; 
    border: 1px solid rgba(255, 255, 255, 0.6) !important; 
    border-radius: 12px !important;
}}

/* [色塊 1] 下拉選單內部文字 */
div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] p {{
    color: #1E293B !important;
    font-size: 18px !important;
    font-weight: 800 !important;
}}

/* [色塊 2] 階段選擇 (加上內距，使其成為一個完整的色塊) */
div[role="radiogroup"] {{
    padding: 12px 20px !important; 
}}
div[role="radiogroup"] div[data-testid="stMarkdownContainer"] p {{
    color: #1E293B !important;
    font-size: 18px !important;
    font-weight: 800 !important;
}}

/* ✨ [魔法區] 將圓形單選鈕強制改裝為超大方形 Checkbox (打勾框) ✨ */
div[role="radiogroup"] label[data-baseweb="radio"] input + div {{
    width: 32px !important;  /* 放大外框 */
    height: 32px !important;
    border-radius: 8px !important; /* 變為方形 */
    border: 2px solid #94A3B8 !important; 
    position: relative !important;
    background-color: #FFFFFF !important;
    margin-right: 12px !important; 
    transition: all 0.2s ease !important;
}}
/* 隱藏原生黑點 */
div[role="radiogroup"] label[data-baseweb="radio"] input + div > div {{
    display: none !important; 
}}
/* 勾選時的背景色變化 (深藍色) */
div[role="radiogroup"] label[data-baseweb="radio"] input:checked + div {{
    background-color: #1E293B !important;
    border-color: #1E293B !important;
}}
/* 勾選時畫出超大白色勾勾 */
div[role="radiogroup"] label[data-baseweb="radio"] input:checked + div::after {{
    content: '';
    position: absolute;
    width: 8px;
    height: 16px;
    border: solid white;
    border-width: 0 3px 3px 0;
    transform: rotate(45deg);
    top: 3px;
    left: 10px;
}}

/* [色塊 3] 抽題按鈕 */
button[kind="primary"] {{
    padding: 12px 0px !important;
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
div.stButton {{
    margin-top: 25px !important; 
    margin-bottom: 20px !important; 
}}

/* ==================================================
   🎯 第四區塊：問題字卡 (維持 0.85 透明度與大圓角)
   ================================================== */
.question-card {{
    background-color: rgba(255, 255, 255, 0.85) !important; 
    backdrop-filter: blur(12px) !important; 
    -webkit-backdrop-filter: blur(12px) !important; 
    border: 1px solid rgba(255, 255, 255, 0.6) !important; 
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important; 
    border-radius: 20px !important; 
    padding: 50px 30px !important; 
    margin: 20px 0px !important; 
    text-align: center !important; 
    font-size: 32px !important; 
    font-weight: 800 !important; 
    color: #1E293B !important; 
    line-height: 1.5 !important; 
    word-wrap: break-word !important;
}}
.hint-text {{color: #475569 !important; font-size: 20px !important;}}

/* ==================================================
   🎯 第五區塊：主持人專區 (淡灰色)
   ================================================== */
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
if "last_mode" not in st.session_state:
    st.session_state.last_mode = selected_mode
if "last_team" not in st.session_state:
    st.session_state.last_team = selected_team

if st.session_state.last_mode != selected_mode or st.session_state.last_team != selected_team:
    st.session_state.current_question = None
    st.session_state.last_mode = selected_mode
    st.session_state.last_team = selected_team

# ==========================================
# 📌 雲端共用牌池
# ==========================================
@st.cache_resource
def get_shared_pools():
    return {}

shared_pools = get_shared_pools()

def init_pools():
    for team in ["第一組", "第二組", "第三組", "第四組"]:
        if team not in shared_pools:
            w_pool = list(range(1, len(warmup_questions))) if warmup_questions else []
            f_pool = list(range(len(formal_questions))) if formal_questions else []
            random.shuffle(w_pool)
            random.shuffle(f_pool)
            shared_pools[team] = {
                "warmup": w_pool,
                "formal": f_pool,
                "warmup_q1_drawn": False
            }

init_pools()

# 6. 畫面佈局
draw_button_clicked = st.button("🎲 點擊抽取題目", type="primary", use_container_width=True)
card_placeholder = st.empty()

# 7. 抽題按鈕與骰子動畫邏輯
if draw_button_clicked:
    active_questions = warmup_questions if selected_mode == "🧊 暖身題" else formal_questions
    current_team_state = shared_pools[selected_team]
    
    if active_questions:
        # 動畫階段
        dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
        for _ in range(12):  
            face = random.choice(dice_faces)
            card_placeholder.markdown(
                f'<div class="question-card">'
                f'<span style="font-size: 80px; color: #1E293B;">{face}</span><br>'
                f'<span style="font-size: 22px; color: #475569; font-weight: bold;">抽取中...</span>'
                f'</div>', 
                unsafe_allow_html=True
            )
            time.sleep(0.08)  
            
        # 結算階段
        if selected_mode == "🧊 暖身題":
            if not current_team_state["warmup_q1_drawn"]:
                selected_idx = 0
                current_team_state["warmup_q1_drawn"] = True
            else:
                if len(current_team_state["warmup"]) == 0:
                    pool = list(range(1, len(warmup_questions)))
                    random.shuffle(pool)
                    current_team_state["warmup"] = pool
                selected_idx = current_team_state["warmup"].pop()
        else:
            if len(current_team_state["formal"]) == 0:
                pool = list(range(len(formal_questions)))
                random.shuffle(pool)
                current_team_state["formal"] = pool
            selected_idx = current_team_state["formal"].pop()
            
        q_num = selected_idx + 1
        q_text = active_questions[selected_idx]
        
        st.session_state.current_question = (
            f'<div style="font-size: 16px; color: #64748B; font-weight: 800; margin-bottom: 15px; letter-spacing: 2px;">'
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
    card_placeholder.markdown('<div class="question-card hint-text">👆<br>準備好了嗎？點擊上方按鈕</div>', unsafe_allow_html=True)

# 9. 主持人專區
with st.expander("⚙️ 主持人專區 (測試與重置)"):
    st.write("活動開始前，若已經測試抽過，請點擊下方按鈕將雲端進度歸零。")
    if st.button("🔄 重置全場進度", type="secondary", use_container_width=True):
        shared_pools.clear()
        st.session_state.current_question = None
        st.rerun()
