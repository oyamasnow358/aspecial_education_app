import streamlit as st
# guideline_data.pyをインポート (ファイル名が違う場合は修正してください)
from guideline_data import data

# ==========================================
# 0. ページ設定
# ==========================================
st.set_page_config(
    page_title="Mirairo - 学習指導要領",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. デザイン定義 (ライトモード・白背景・視認性重視)
# ==========================================
def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = """
    <style>
        /* --- 全体フォント --- */
        html, body, [class*="css"] {
            font-family: 'Noto Sans JP', sans-serif !important;
            color: #333333 !important; /* 文字色は濃いグレー（ほぼ黒） */
        }

        /* --- 背景 (白ベース + 画像透過) --- */
        [data-testid="stAppViewContainer"] {
            background-color: #ffffff;
            /* 白の透過グラデーションを重ねて背景画像をうっすら表示 */
            background-image: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-attachment: fixed;
        }

        /* --- 文字色 (黒・視認性重視) --- */
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50 !important; /* 見出しは少し青みがかった黒 */
            font-weight: 700 !important;
            text-shadow: none !important; /* 影は削除してくっきりさせる */
        }
        p, span, div, label, .stMarkdown {
            color: #333333 !important;
            text-shadow: none !important;
        }

        /* --- サイドバー (白系) --- */
        [data-testid="stSidebar"] {
            background-color: rgba(245, 247, 250, 0.9) !important; /* 薄いグレー */
            border-right: 1px solid #e0e0e0;
        }
        [data-testid="stSidebarNavCollapseButton"] { color: #333 !important; }

        /* --- 機能カード (白背景・影付き) --- */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        [data-testid="stBorderContainer"] {
            background-color: #ffffff !important; /* 真っ白なカード */
            border: 1px solid #e0e0e0 !important; /* 薄いグレーの枠線 */
            border-radius: 12px !important;
            padding: 20px !important;
            margin-bottom: 20px !important;
            /* 浮き上がるような影 */
            box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
            
            animation: fadeInUp 0.6s ease-out forwards;
        }
        
        [data-testid="stBorderContainer"]:hover {
            border-color: #4a90e2 !important; /* ホバーで青枠 */
            box-shadow: 0 8px 20px rgba(74, 144, 226, 0.15) !important; /* 青い影 */
            transform: translateY(-3px);
            transition: all 0.3s ease;
        }

        /* --- ボタン --- */
        .stButton > button {
            width: 100%;
            background-color: #ffffff !important;
            border: 2px solid #4a90e2 !important;
            color: #4a90e2 !important;
            font-weight: bold !important;
            border-radius: 30px !important;
            transition: all 0.3s ease !important;
        }
        .stButton > button:hover {
            background-color: #4a90e2 !important;
            color: #ffffff !important;
        }
        
        /* Primaryボタン */
        .stButton > button[kind="primary"] {
            background-color: #4a90e2 !important;
            color: #ffffff !important;
            border: none !important;
            box-shadow: 0 4px 10px rgba(74, 144, 226, 0.3);
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #357abd !important; /* 濃い青 */
            transform: scale(1.02);
        }

        /* --- セレクトボックス・ラジオボタン --- */
        /* 入力エリアの背景を白に */
        div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            border-color: #d1d5db !important;
            color: #333 !important;
        }
        
        /* ラジオボタンの選択肢 */
        div[role="radiogroup"] label {
            background-color: #ffffff !important;
            border: 1px solid #e5e7eb !important;
            color: #333 !important;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 5px;
            transition: all 0.2s;
        }
        div[role="radiogroup"] label:hover {
            background-color: #f0f9ff !important; /* 薄い青 */
            border-color: #4a90e2 !important;
        }

        /* --- エキスパンダー --- */
        .streamlit-expanderHeader {
            background-color: #f8f9fa !important;
            color: #333 !important;
            border-radius: 8px !important;
            border: 1px solid #e0e0e0;
        }
        .streamlit-expanderContent {
            background-color: #ffffff !important;
            border: 1px solid #e0e0e0;
            border-top: none;
            border-radius: 0 0 8px 8px;
            color: #333 !important;
        }

        /* --- 説明文ボックス --- */
        .info-box {
            background-color: #ffffff;
            border-left: 5px solid #4a90e2;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }

        /* --- 戻るボタン --- */
        .back-link a {
            display: inline-block;
            padding: 8px 16px;
            background: #ffffff;
            border: 1px solid #4a90e2;
            border-radius: 20px;
            color: #4a90e2 !important;
            text-decoration: none;
            margin-bottom: 20px;
            transition: all 0.3s;
            font-weight: bold;
        }
        .back-link a:hover {
            background: #4a90e2;
            color: #ffffff !important;
        }
        
        hr { border-color: #e0e0e0; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# --- ▼ 戻るボタン ▼ ---
st.markdown('<div class="back-link"><a href="Home" target="_self">« TOPページに戻る</a></div>', unsafe_allow_html=True)

# ==========================================
# 2. ロジック・ヘルパー関数
# ==========================================
def format_guideline_text(text):
    if not isinstance(text, str): return ""
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
st.title("📜 知的段階　早引き学習指導要領")

# 説明文エリア（白背景で見やすく）
st.markdown("""
<div class="info-box">
    学習指導要領の内容を一瞬でピンポイント検索。<br>
    学部、段階（障害種別）、教科を選択すると、関連する学習指導要領の内容が表示されます。
</div>
""", unsafe_allow_html=True)

# --- 選択肢 (カード内) ---
with st.container(border=True):
    st.subheader("検索条件の選択")
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_gakubu = st.selectbox("**1. 学部を選択**", options=list(data.keys()), on_change=reset_display_state)

    with col2:
        shubetsu_options = list(data[selected_gakubu].keys())
        selected_shubetsu = st.selectbox("**2. 段階（障害種別）を選択**", options=shubetsu_options, on_change=reset_display_state)

    is_chiteki = "知的障害者" in selected_shubetsu
    if is_chiteki:
        with col3:
            kyoka_options = ["選択してください"] + list(data[selected_gakubu][selected_shubetsu].keys())
            selected_kyoka = st.selectbox("**3. 教科を選択**", options=kyoka_options, on_change=reset_display_state)
    else:
        selected_kyoka = None

    st.markdown("<br>", unsafe_allow_html=True)

    # --- 表示ボタン ---
    show_button_enabled = (not is_chiteki) or (is_chiteki and selected_kyoka != "選択してください")

    if show_button_enabled:
        if st.button("表示する", type="primary", use_container_width=True):
            st.session_state.show_results = True
    else:
        st.warning("ステップ3で教科を選択してください。")

# --- 結果表示エリア ---
if st.session_state.get('show_results', False):
    st.markdown("---")
    st.header(f"表示結果：{selected_gakubu} - {selected_shubetsu}" + (f" - {selected_kyoka}" if is_chiteki and selected_kyoka else ""))
    
    # 結果をカードで表示
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