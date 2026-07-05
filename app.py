import streamlit as st
import random
import os

# 1. 頁面基本設定 (適合手機瀏覽的 centered 佈局)
st.set_page_config(
    page_title="問題字卡產生器",
    page_icon="💡",
    layout="centered"
)

# 你可以在這裡替換成你喜歡的圖片網址
bg_img_url = "https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=1080&auto=format&fit=crop"

st.markdown(f"""
<style>
    /* 替換整個 App 的背景 */
    .stApp {{
        /* 使用 linear-gradient 疊加一層半透明黑色遮罩，確保字卡與按鈕清晰可見 */
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url("{bg_img_url}");
        background-size: cover;          /* 讓圖片填滿整個螢幕 */
        background-position: center;     /* 圖片置中 */
        background-repeat: no-repeat;    /* 防止圖片重複拼接 */
        background-attachment: fixed;    /* 讓背景在滑動時固定住 (對手機端體驗很好) */
    }}
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
