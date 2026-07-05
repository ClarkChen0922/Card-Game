import streamlit as st
import random
import os

# 1. 頁面基本設定
st.set_page_config(page_title="問題字卡產生器", page_icon="💡", layout="centered")

# 2. 讀取外部 CSS 檔案的函式
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 載入靜態樣式基礎設施 (排版、陰影、字體大小等)
load_css("style.css")

# ==========================================
# 📌 你的指令區：在這裡貼上你的 CSS 圖片網址
# ==========================================
GLOBAL_BG_URL = "https://images.pexels.com/photos/33828271/pexels-photo-33828271.jpeg"

# 3. 定義團隊、對應檔案與「專屬字卡顏色」
TEAM_INFO = {
    "Team A": {"file": "team_a.txt", "card_bg": "#F0F8FF"},  # 冰川淺藍
    "Team B": {"file": "team_b.txt", "card_bg": "#F5FFFA"},  # 薄荷淺綠
    "Team C": {"file": "team_c.txt", "card_bg": "#FFFFF0"},  # 象牙淺黃
    "Team D": {"file": "team_d.txt", "card_bg": "#FFF0F5"}   # 玫瑰淺粉
}

# 4. 讀取題庫邏輯
@st.cache_data
def load_questions(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

# 5. UI 頂部
st.title("💡 換位思考工作坊")
selected_team = st.selectbox("請選擇你的團隊：", list(TEAM_INFO.keys()))

# 6. 動態注入 (統一背景圖 + 動態字卡顏色)
current_card_bg = TEAM_INFO[selected_team]["card_bg"]
st.markdown(f"""
<style>
    /* 全域背景圖片 */
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url("{GLOBAL_BG_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* 動態覆蓋字卡的背景顏色 */
    .question-card {{
        background-color: {current_card_bg} !important;
        transition: background-color 0.4s ease; /* 變色時的平滑轉場 */
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
