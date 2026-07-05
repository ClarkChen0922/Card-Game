import streamlit as st
import random
import os

# 1. 頁面基本設定
st.set_page_config(
    page_title="問題字卡產生器",
    page_icon="💡",
    layout="centered"
)

# 2. 讀取外部 CSS 檔案的函式
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 載入靜態樣式
load_css("style.css")

# 3. 定義團隊、對應檔案與專屬漸層背景
TEAM_INFO = {
    "Team A": {"file": "team_a.txt", "bg": "linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)"},
    "Team B": {"file": "team_b.txt", "bg": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)"},
    "Team C": {"file": "team_c.txt", "bg": "linear-gradient(135deg, #f2994a 0%, #f2c94c 100%)"},
    "Team D": {"file": "team_d.txt", "bg": "linear-gradient(135deg, #ed213a 0%, #93291e 100%)"}
}

# 4. 讀取題庫的邏輯
@st.cache_data
def load_questions(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

# 5. 畫面頂部 UI
st.title("💡 換位思考工作坊")
selected_team = st.selectbox("請選擇你的團隊：", list(TEAM_INFO.keys()))

# 6. 動態注入背景 (保留動態切換的功能)
current_bg = TEAM_INFO[selected_team]["bg"]
st.markdown(f"""
<style>
    .stApp {{
        background: {current_bg};
        background-size: cover;
        background-attachment: fixed;
        transition: background 0.5s ease-in-out;
    }}
</style>
""", unsafe_allow_html=True)

# 7. 核心狀態與抽題邏輯
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "last_team" not in st.session_state:
    st.session_state.last_team = selected_team

if st.session_state.last_team != selected_team:
    st.session_state.current_question = None
    st.session_state.last_team = selected_team

if st.button("🎲 點我隨機抽題", type="primary", use_container_width=True):
    filename = TEAM_INFO[selected_team]["file"]
    questions = load_questions(filename)
    
    if questions:
        st.session_state.current_question = random.choice(questions)
    else:
        st.session_state.current_question = f"錯誤：找不到或無法讀取 {filename}，請檢查檔案。"

# 8. 顯示卡片區域
if st.session_state.current_question:
    st.markdown(f'<div class="question-card">{st.session_state.current_question}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="question-card hint-text">👆<br>請點擊上方按鈕抽出你的專屬問題</div>', unsafe_allow_html=True)
