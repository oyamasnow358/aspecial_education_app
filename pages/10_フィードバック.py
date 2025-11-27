import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path

# ==========================================
# 0. ページ設定
# ==========================================
st.set_page_config(
    page_title="MieeL - フィードバック",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. 画像処理 (ロゴ読み込み)
# ==========================================
def get_img_as_base64(file):
    try:
        # 画像パスを絶対パスで解決
        script_path = Path(__file__)
        app_root = script_path.parent.parent
        img_path = app_root / file
        
        with open(img_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

logo_path = "MieeL2.png" 
logo_b64 = get_img_as_base64(logo_path)
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img">' if logo_b64 else '<div class="logo-placeholder">📝</div>'


# ==========================================
# 2. デザイン定義 (MieeLスタイル・白ベース・アニメーション)
# ==========================================
def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = f"""
    <style>
        /* --- 全体フォント --- */
        html, body, [class*="css"] {{
            font-family: 'Noto Sans JP', sans-serif !important;
            color: #333333 !important;
        }}

        /* --- 背景 (白92%透過・画像あり) --- */
        [data-testid="stAppViewContainer"] {{
            background-color: #ffffff;
            background-image: linear-gradient(rgba(255,255,255,0.92), rgba(255,255,255,0.92)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-attachment: fixed;
            padding-left: 20px;
            padding-right: 20px;
        }}

        /* --- 文字色 (濃紺・くっきり) --- */
        h1, h2, h3, h4, h5, h6 {{
            color: #0f172a !important; /* 濃いネイビーブラック */
            font-weight: 700 !important;
            text-shadow: none !important;
        }}
        p, span, div, label, .stMarkdown {{
            color: #333333 !important;
            text-shadow: none !important;
        }}

        /* --- サイドバー (すりガラス効果) --- */
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid #e2e8f0 !important;
        }}
        [data-testid="stSidebar"] * {{
            color: #333333 !important;
        }}

        /* 
           ================================================================
           ★ アニメーション定義
           ================================================================
        */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(40px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}

        /* 
           ================================================================
           ★ 機能カード (白背景・影付き・ぬるっと出現)
           ================================================================
        */
        [data-testid="stBorderContainer"] {{
            background-color: #ffffff !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 15px !important;
            padding: 25px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
            
            /* アニメーション適用 */
            opacity: 0; 
            animation-name: fadeInUp;
            animation-duration: 0.8s;
            animation-fill-mode: forwards;
            animation-timing-function: cubic-bezier(0.2, 0.8, 0.2, 1);
        }}

        [data-testid="stBorderContainer"]:hover {{
            border-color: #4a90e2 !important;
            background-color: #f8fafc !important;
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(74, 144, 226, 0.15) !important;
            transition: all 0.3s ease;
        }}

        /* --- タブのデザイン調整 --- */
        .stTabs [data-testid="stTab"] {{
            background-color: transparent;
            border-bottom: 2px solid transparent;
            color: #64748b;
            font-weight: bold;
            transition: all 0.3s;
        }}
        .stTabs [data-testid="stTab"]:hover {{
            color: #4a90e2;
        }}
        .stTabs [data-testid="stTab"][aria-selected="true"] {{
            color: #4a90e2;
            border-bottom: 3px solid #4a90e2;
        }}

        /* --- 説明文ボックス --- */
        .info-box {{
            background-color: #f0f9ff;
            border: 2px solid #4a90e2;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(74,144,226,0.1);
            margin-bottom: 25px;
            color: #0c4a6e;
            animation: fadeInUp 0.8s ease-out forwards;
        }}

        /* --- 戻るボタン (指定デザイン) --- */
        .back-link {{
            margin-bottom: 20px;
        }}
        .back-link a {{
            display: inline-block;
            padding: 10px 20px;
            background: #ffffff;
            border: 2px solid #e2e8f0;
            border-radius: 25px;
            color: #4a90e2 !important;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        .back-link a:hover {{
            background: #4a90e2;
            color: #ffffff !important;
            border-color: #4a90e2;
            box-shadow: 0 4px 10px rgba(74, 144, 226, 0.2);
        }}
        
        /* --- ヘッダーレイアウト --- */
        .header-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-bottom: 40px;
            padding: 40px 0;
            border-bottom: 2px solid #f1f5f9;
            animation: float 6s ease-in-out infinite;
        }}
        .logo-img {{
            width: 80px;
            height: auto;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
        }}
        .logo-placeholder {{
            font-size: 3rem;
            margin-right: 15px;
            animation: float 6s ease-in-out infinite;
        }}
        .page-title {{
            font-size: 3rem;
            font-weight: 900;
            color: #0f172a;
            margin: 0;
            line-height: 1.2;
        }}
        
        hr {{ border-color: #cbd5e1; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# ==========================================
# 3. メインコンテンツ
# ==========================================

# --- 戻るボタン (★正しいリンクに変更済み) ---
st.markdown('<div class="back-link"><a href="https://aspecialeducationapp-6iuvpdfjbflp4wyvykmzey.streamlit.app/" target="_self">« TOPページに戻る</a></div>', unsafe_allow_html=True)

# ヘッダー (ロゴ + タイトル)
st.markdown(f"""
    <div class="header-container">
        {logo_html}
        <h1 class="page-title">フィードバック</h1>
    </div>
""", unsafe_allow_html=True)

# 説明文 (白背景・青枠デザイン)
st.markdown("""
<div class="info-box">
    <strong>💬 ご協力のお願い</strong><br>
    アプリの改善や、新しい指導実践の共有など、皆様からのご意見をお待ちしています。<br>
    下のタブから使いやすい方のフォームを選択してご入力ください。
</div>
""", unsafe_allow_html=True)

# タブの作成
tab1, tab2 = st.tabs(["Microsoft Forms", "Google Forms"])

with tab1:
    # ぬるっと動く白枠カード
    with st.container(border=True):
        st.subheader("Microsoft Forms")
        form_url_ms = "https://forms.office.com/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAMAANa6zUxUQjRFQ1NRUFhJODhKVFMzUkdVVzVCR0JEVS4u&embed=true"
        components.iframe(form_url_ms, height=800, scrolling=True)

with tab2:
    # ぬるっと動く白枠カード
    with st.container(border=True):
        st.subheader("Google Forms")
        form_url_google = "https://docs.google.com/forms/d/1xXzq0vJ9E5FX16CFNoTzg5VAyX6eWsuN8Xl5qEwJFTc/preview"
        components.iframe(form_url_google, height=800, scrolling=True)