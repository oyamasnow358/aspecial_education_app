import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 0. ページ設定
# ==========================================
st.set_page_config(
    page_title="Mirairo - フィードバック",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. デザイン定義 (Mirairo共通・白枠線・アニメーション)
# ==========================================
def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = """
    <style>
        /* --- 全体 --- */
        html, body, [class*="css"] {
            font-family: 'Noto Sans JP', sans-serif !important;
        }

        /* --- 背景 (黒) --- */
        [data-testid="stAppViewContainer"] {
            background-color: #000000;
            background-image: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-attachment: fixed;
        }

        /* --- 文字色 (白・影付き) --- */
        h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown {
            color: #ffffff !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.9) !important;
        }

        /* --- サイドバー --- */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        [data-testid="stSidebarNavCollapseButton"] { color: #fff !important; }

        /* --- 機能カード (白枠・アニメーション) --- */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        [data-testid="stBorderContainer"] {
            background-color: #151515 !important;
            border: 2px solid #ffffff !important;
            border-radius: 16px !important;
            padding: 20px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.8) !important;
            animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        }
        
        [data-testid="stBorderContainer"]:hover {
            border-color: #4a90e2 !important;
            background-color: #000000 !important;
            transform: translateY(-5px);
            box-shadow: 0 0 20px rgba(74, 144, 226, 0.4) !important;
            transition: all 0.3s ease;
        }

        /* --- タブのデザイン調整 --- */
        .stTabs [data-testid="stTab"] {
            background-color: transparent;
            border: 1px solid #555;
            border-bottom: none;
            color: #ccc;
            border-radius: 5px 5px 0 0;
            transition: all 0.3s;
        }
        .stTabs [data-testid="stTab"]:hover {
            color: #4a90e2;
            border-color: #4a90e2;
        }
        .stTabs [data-testid="stTab"][aria-selected="true"] {
            background-color: #4a90e2;
            color: #fff;
            border: none;
        }
        
        /* --- infoボックス --- */
        [data-testid="stAlert"] {
            background-color: rgba(74, 144, 226, 0.15) !important;
            border: 1px solid #4a90e2 !important;
            color: #fff !important;
        }

        /* --- 戻るボタン --- */
        .back-link a {
            display: inline-block;
            padding: 8px 16px;
            background: rgba(255,255,255,0.1);
            border: 1px solid #fff;
            border-radius: 20px;
            color: #fff !important;
            text-decoration: none;
            margin-bottom: 20px;
            transition: all 0.3s;
        }
        .back-link a:hover {
            background: #fff;
            color: #000 !important;
        }
        
        hr { border-color: #666; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# --- ▼ 戻るボタン ▼ ---
st.markdown('<div class="back-link"><a href="Home" target="_self">« TOPページに戻る</a></div>', unsafe_allow_html=True)

# ==========================================
# 2. メインコンテンツ
# ==========================================
st.title("📝 フィードバック")

st.markdown("""
<div style="background: rgba(255,255,255,0.05); border: 1px solid #fff; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
    アプリの改善や、新しい指導実践の共有など、皆様からのご意見をお待ちしています。<br>
    下のタブから使いやすい方のフォームを選択してご入力ください。
</div>
""", unsafe_allow_html=True)

# タブの作成
tab1, tab2 = st.tabs(["Microsoft Forms", "Google Forms"])

with tab1:
    with st.container(border=True):
        st.subheader("Microsoft Forms")
        form_url_ms = "https://forms.office.com/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAMAANa6zUxUQjRFQ1NRUFhJODhKVFMzUkdVVzVCR0JEVS4u&embed=true"
        components.iframe(form_url_ms, height=800, scrolling=True)

with tab2:
    with st.container(border=True):
        st.subheader("Google Forms")
        form_url_google = "https://docs.google.com/forms/d/1xXzq0vJ9E5FX16CFNoTzg5VAyX6eWsuN8Xl5qEwJFTc/preview"
        components.iframe(form_url_google, height=800, scrolling=True)