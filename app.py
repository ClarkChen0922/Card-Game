import streamlit as st
import random
import os

# 1. 頁面基本設定
st.set_page_config(
    page_title="問題字卡產生器",
    page_icon="💡",
    layout="centered"
)

# 2. 定義團隊、對應檔案與專屬漸層背景
TEAM_INFO = {
    "Team A": {
        "file": "team_a.txt",
        "bg_gradient": "linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)"  # 沉穩藍
    },
    "Team B": {
        "file": "team_b.txt",
        "bg_gradient": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)"  # 活力綠
    },
    "Team C": {
        "file": "team_c.txt",
        "bg_gradient": "linear-gradient(135deg, #f2994a 0%, #f2c94c 100%)"  # 溫暖黃
    },
    "Team D": {
        "file": "team_d.txt",
        "bg_gradient": "linear-gradient(135deg, #ed213a 0%, #93291e 100%)"  # 熱情紅
    }
}

# 3. 讀取題庫的邏輯
@st.cache_data
def load_questions(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

# 4. 畫面頂部 UI (讓使用者先選擇團隊)
st.title("💡 換位思考工作坊")
selected_team = st.selectbox("請選擇你的團隊：", list(TEAM_INFO.keys()))

# 5. 動態注入 CSS (根據選擇的團隊改變背景)
# 注意這裡使用了 {{ }} 來跳脫 Python f-string 的大括號
current_bg = TEAM_INFO[selected_team]["bg_gradient"]

st.markdown(f"""
<style>
    /* 隱藏預設選單與 Footer */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* 動態替換整個 App 的背景漸層 */
    .stApp {{
        background: {current_bg};
        background-size: cover;
        background-attachment: fixed;
        transition: background 0.5s ease-in-out; /* 增加漸變轉場動畫，切換更滑順 */
    }}

    /* 確保標題與下拉選單的提示文字在深色漸層上依然清晰 (白色) */
    .stTitle {{
        font-size: 42px !important;
        color: #FFFFFF !important;
        font-weight: 800;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.3);
    }}
    label {{
        color: #FFFFFF !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }}

    /* 增強型題目卡牌 UI 設計 - 維持純白實體感 */
    .question-card {{
        background-color: #FFFFFF;
        border-radius: 30px;
        padding: 60px 40px;
        margin: 30px 0px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
        text-align: center;
        font-size: 38px !important;  
        font-weight: 800 !important;
        color: #1E293B;
        line-height: 1.5;
        word-wrap: break-word;
    }}
    
    /* 尚未抽題的提示文字顏色 */
    .hint-text {{
        color: #94A3B8 !important;
        font-size: 22px !important;
    }}
    
    /* 調整按鈕樣式使其更好按 */
    .stButton>button {{
        font-size: 20px !important;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px 0px;
    }}
</style>
""", unsafe_allow_html=True)

# 6. 核心狀態與抽題邏輯
# 使用 session_state 來確保畫面重整時，題目與當前選擇的團隊連動
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "last_team" not in st.session_state:
    st.session_state.last_team = selected_team

# 如果使用者切換了團隊，清空當前畫面上的題目卡片
if st.session_state.last_team != selected_team:
    st.session_state.current_question = None
    st.session_state.last_team = selected_team

# 抽題按鈕
if st.button("🎲 點我隨機抽題", type="primary", use_container_width=True):
    filename = TEAM_INFO[selected_team]["file"]
    questions = load_questions(filename)
    
    if questions:
        st.session_state.current_question = random.choice(questions)
    else:
        st.session_state.current_question = f"錯誤：找不到或無法讀取 {filename}，請通知主辦單位。"

# 7. 顯示卡片區域
if st.session_state.current_question:
    # 呈現抽出的題目卡片
    st.markdown(f'<div class="question-card">{st.session_state.current_question}</div>', unsafe_allow_html=True)
else:
    # 尚未抽題時的提示畫面
    st.markdown('<div class="question-card hint-text">👆<br>請點擊上方按鈕抽出你的專屬問題</div>', unsafe_allow_html=True)
