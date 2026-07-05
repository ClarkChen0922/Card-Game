import streamlit as st
import random
import os

# 1. 頁面基本設定 (適合手機瀏覽的 centered 佈局)
st.set_page_config(
    page_title="問題字卡產生器",
    page_icon="💡",
    layout="centered"
)

# 2. 注入 Mobile-First 的客製化 CSS
st.markdown("""
<style>
    /* 隱藏預設選單與 Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 改進標題與提示文字的大小與對比度 */
    .stTitle {
        font-size: 42px !important; /* 放大標題 */
        color: white !important;      /* 改為白色，確保清晰 */
        font-weight: 800;
    }
    .stMarkdown p {
        font-size: 22px !important; /* 放大提示文字 */
        color: #E2E8F0 !important; /* 改為淺灰色，提高對比 */
    }

    /* 增強型題目卡牌 UI 設計 - 字大、有實體感 */
    .question-card {
        background-color: #FFFFFF;  /* 純白背景 */
        border-radius: 30px;        /* 更圓潤的邊角 */
        padding: 60px 40px;         /* 增加大量內距，留白高級 */
        margin: 30px 0px;
        /* 更明顯的柔和陰影，營造 floating 的卡片感 */
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        text-align: center;
        /* 文字大幅放大，主導畫面 */
        font-size: 38px !important;  
        font-weight: 800 !important;
        color: #1E293B;             /* 深色字體，高對比度 */
        line-height: 1.5;
        word-wrap: break-word;
        border: 1px solid #E2E8F0;  /* 淡淡的邊框 */
    }
    
    /* 調整按鈕樣式使其更好按 */
    .stButton>button {
        font-size: 20px !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 3. 定義團隊與對應檔案的字典
TEAM_FILES = {
    "Team A": "team_a.txt",
    "Team B": "team_b.txt",
    "Team C": "team_c.txt",
    "Team D": "team_d.txt"
}

# 4. 讀取題庫的邏輯 (加上快取，避免重複讀取磁碟)
@st.cache_data
def load_questions(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            # 讀取非空白行並去除換行符號
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

# 5. UI 元件建構
st.title("💡 換位思考工作坊")

# 下拉選單選擇團隊
selected_team = st.selectbox("請選擇你的團隊：", list(TEAM_FILES.keys()))

# 初始化 session_state，用於保存當前抽到的題目
if "current_question" not in st.session_state:
    st.session_state.current_question = None

# 抽題按鈕 (使用 type="primary" 與 use_container_width=True 滿版顯示好點擊)
if st.button("🎲 點我隨機抽題", type="primary", use_container_width=True):
    filename = TEAM_FILES[selected_team]
    questions = load_questions(filename)
    
    if questions:
        # 隨機抽取一題並存入 session_state
        st.session_state.current_question = random.choice(questions)
    else:
        st.session_state.current_question = f"錯誤：找不到或無法讀取 {filename}，請通知主辦單位。"

# 6. 顯示卡片區域
if st.session_state.current_question:
    # 呈現抽出的題目卡片
    st.markdown(f'<div class="question-card">{st.session_state.current_question}</div>', unsafe_allow_html=True)
else:
    # 尚未抽題時的提示畫面
    st.markdown('<div class="question-card hint-text">👆<br>請點擊上方按鈕抽出你的專屬問題</div>', unsafe_allow_html=True)
