import streamlit as st
# guideline_data.pyをインポート
from guideline_data import data
import base64
from pathlib import Path

# ==========================================
# 0. ページ設定
# ==========================================
st.set_page_config(
    page_title="MieeL - 学習指導要領",
    page_icon="📜",
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
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img">' if logo_b64 else '<div class="logo-placeholder">📜</div>'


# ==========================================
# 2. デザイン定義 (MieeLスタイル・ぬるっと動くアニメーション)
# ==========================================
def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = f"""
    <style>
        /* --- 全体フォント --- */
        html, body, [class*="css"] {{
            font-family: 'Noto Sans JP', sans-serif !important;
            color: #1a1a1a !important; /* 文字色はほぼ黒でくっきり */
            line-height: 1.8 !important; /* 行間を広げて読みやすく */
        }}

        /* --- 背景 (白92%透過で画像あり) --- */
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
            margin-bottom: 0.5em !important;
        }}
        
        /* 本文 */
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
           ★ アニメーション定義 (下からフワッと)
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
           ★ コンテナデザイン (白背景・影付き・アニメーション)
           ================================================================
        */
        [data-testid="stBorderContainer"] {{
            background-color: #ffffff !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 15px !important;
            padding: 25px !important;
            margin-bottom: 25px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
            
            /* アニメーション適用 */
            opacity: 0; 
            animation-name: fadeInUp;
            animation-duration: 0.8s;
            animation-fill-mode: forwards;
            animation-timing-function: cubic-bezier(0.2, 0.8, 0.2, 1);
        }}
        
        /* コンテナの出現タイミングをずらす */
        div.element-container:nth-of-type(1) [data-testid="stBorderContainer"] {{ animation-delay: 0.1s; }}
        div.element-container:nth-of-type(2) [data-testid="stBorderContainer"] {{ animation-delay: 0.3s; }}
        div.element-container:nth-of-type(3) [data-testid="stBorderContainer"] {{ animation-delay: 0.5s; }}

        [data-testid="stBorderContainer"]:hover {{
            border-color: #4a90e2 !important;
            background-color: #f8fafc !important;
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(74, 144, 226, 0.15) !important;
            transition: all 0.3s ease;
        }}

        /* --- ボタン --- */
        .stButton > button {{
            width: 100%;
            background-color: #ffffff !important;
            border: 2px solid #e2e8f0 !important;
            color: #4a90e2 !important;
            font-weight: bold !important;
            border-radius: 30px !important;
            padding: 10px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
        }}
        .stButton > button:hover {{
            background-color: #4a90e2 !important;
            color: #ffffff !important;
            border-color: #4a90e2 !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(74, 144, 226, 0.2) !important;
        }}
        
        /* Primaryボタン */
        .stButton > button[kind="primary"] {{
            background-color: #4a90e2 !important;
            color: #ffffff !important;
            border: 2px solid #4a90e2 !important;
        }}
        .stButton > button[kind="primary"]:hover {{
            background-color: #2563eb !important;
            border-color: #2563eb !important;
        }}

        /* --- 入力フォーム (白背景) --- */
        div[data-baseweb="select"] > div {{
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 10px !important;
            color: #333 !important;
        }}
        div[data-baseweb="select"] > div:hover {{
            border-color: #4a90e2 !important;
        }}
        
        /* ラジオボタン */
        div[role="radiogroup"] label {{
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            color: #334155 !important;
            padding: 12px !important;
            border-radius: 10px;
            margin-bottom: 8px;
            transition: all 0.2s;
        }}
        div[role="radiogroup"] label:hover {{
            background-color: #e0f2fe !important;
            border-color: #4a90e2 !important;
            color: #0284c7 !important;
        }}

        /* --- エキスパンダー --- */
        .streamlit-expanderHeader {{
            background-color: #f8fafc !important; /* 薄いグレー */
            color: #0f172a !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            border: 1px solid #e2e8f0;
        }}
        .streamlit-expanderContent {{
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0;
            border-top: none;
            color: #333 !important;
            padding: 20px !important;
        }}

        /* --- 説明文ボックス (青枠) --- */
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
            width: 100px;
            height: auto;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
        }}
        .logo-placeholder {{
            font-size: 4rem;
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

# --- ▼ 戻るボタン (★正しいリンクに変更済み) ▼ ---
st.markdown('<div class="back-link"><a href="https://aspecialeducationapp-6iuvpdfjbflp4wyvykmzey.streamlit.app/" target="_self">« TOPページに戻る</a></div>', unsafe_allow_html=True)

# ==========================================
# 2. ロジック・ヘルパー関数
# ==========================================
def format_guideline_text(text):
    if not isinstance(text, str): return ""
    # 見やすくするために全角スペースを調整し、改行を反映
    processed_text = text.replace("　", "&nbsp;&nbsp;")
    processed_text = processed_text.replace("\n", "  \n")
    return processed_text

def reset_display_state():
    """選択肢が変更されたときに、表示状態をリセットする"""
    if 'show_results' in st.session_state:
        st.session_state.show_results = False

# ==========================================
# 3. メインコンテンツ
# ==========================================

# ヘッダー (ロゴ + タイトル)
st.markdown(f"""
    <div class="header-container">
        {logo_html}
        <h1 class="page-title">知的段階 学習指導要領</h1>
    </div>
""", unsafe_allow_html=True)

# 説明文エリア
st.markdown("""
<div class="info-box">
    <strong>🎯 使い方：</strong><br>
    学習指導要領の内容を一瞬でピンポイント検索できます。<br>
    下のボックスから「学部」「段階（障害種別）」「教科」を選択してください。
</div>
""", unsafe_allow_html=True)

# --- 選択肢 (カード内・ぬるっと動く) ---
with st.container(border=True):
    st.subheader("🔍 検索条件の選択")
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_gakubu = st.selectbox("1. 学部を選択", options=list(data.keys()), on_change=reset_display_state)

    with col2:
        shubetsu_options = list(data[selected_gakubu].keys())
        selected_shubetsu = st.selectbox("2. 段階（障害種別）を選択", options=shubetsu_options, on_change=reset_display_state)

    is_chiteki = "知的障害者" in selected_shubetsu
    if is_chiteki:
        with col3:
            kyoka_options = ["選択してください"] + list(data[selected_gakubu][selected_shubetsu].keys())
            selected_kyoka = st.selectbox("3. 教科を選択", options=kyoka_options, on_change=reset_display_state)
    else:
        selected_kyoka = None

    st.markdown("<br>", unsafe_allow_html=True)

    # --- 表示ボタン ---
    show_button_enabled = (not is_chiteki) or (is_chiteki and selected_kyoka != "選択してください")

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if show_button_enabled:
            if st.button("表示する", type="primary"):
                st.session_state.show_results = True
        else:
            if is_chiteki:
                st.warning("⚠️ ステップ3で教科を選択してください。")

# --- 結果表示エリア ---
if st.session_state.get('show_results', False):
    st.markdown("---")
    st.markdown(f"<h3 style='text-align:center;'>📄 表示結果</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-weight:bold; color:#4a90e2;'>{selected_gakubu} - {selected_shubetsu}" + (f" - {selected_kyoka}" if is_chiteki and selected_kyoka else "") + "</p>", unsafe_allow_html=True)
    
    # 結果をぬるっと動くカードで表示
    with st.container(border=True):
        # 知的障害者以外の場合
        if not is_chiteki:
            shubetsu_data = data[selected_gakubu][selected_shubetsu]
            st.subheader("全体")
            st.markdown(format_guideline_text(shubetsu_data.get("全体", "データがありません。")), unsafe_allow_html=True)

            if "全体" in shubetsu_data:
                for key, value in shubetsu_data.items():
                    if key != "全体":
                        with st.expander(f"**{key}**"):
                            st.markdown(format_guideline_text(value), unsafe_allow_html=True)
        
        # 知的障害者の場合
        elif is_chiteki and selected_kyoka and selected_kyoka != "選択してください":
            kyoka_data = data[selected_gakubu][selected_shubetsu][selected_kyoka]
            
            if "目標" in kyoka_data:
                st.subheader("🎯 目標")
                st.markdown(format_guideline_text(kyoka_data["目標"]), unsafe_allow_html=True)

            dankai_keys = sorted([key for key in kyoka_data.keys() if "段階" in key])
            
            if dankai_keys:
                st.markdown("---")
                st.subheader("📖 段階を選択してください")
                
                selected_dankai = st.radio(
                    "表示する段階を選択:",
                    options=dankai_keys,
                    horizontal=True,
                    label_visibility="collapsed",
                    key=f"radio_{selected_gakubu}_{selected_kyoka}"
                )

                if selected_dankai:
                    dankai_data = kyoka_data[selected_dankai]
                    
                    # 段階ごとの内容を表示（ここもカードで囲む）
                    st.markdown(f"#### 【{selected_dankai}】")
                    with st.container(border=True):
                        if "目標" in dankai_data:
                            st.markdown("##### **目標**")
                            st.markdown(format_guideline_text(dankai_data["目標"]), unsafe_allow_html=True)
                        if "内容" in dankai_data:
                            st.markdown("##### **内容**")
                            st.markdown(format_guideline_text(dankai_data["内容"]), unsafe_allow_html=True)

            if "指導計画の作成と内容の取扱い" in kyoka_data:
                with st.expander("**指導計画の作成と内容の取扱い**"):
                    st.markdown(format_guideline_text(kyoka_data["指導計画の作成と内容の取扱い"]), unsafe_allow_html=True)
            
            overall_plan_key = next((key for key in kyoka_data if "全体指導計画" in key), None)
            if overall_plan_key:
                 with st.expander(f"**{overall_plan_key}**"):
                    st.markdown(format_guideline_text(kyoka_data[overall_plan_key]), unsafe_allow_html=True)