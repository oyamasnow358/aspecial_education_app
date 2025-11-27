import streamlit as st
import json
import base64
from pathlib import Path

# ==========================================
# 0. ページ設定
# ==========================================
st.set_page_config(
    page_title="MieeL - 指導支援内容", 
    page_icon="📚", 
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
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img">' if logo_b64 else '<div class="logo-placeholder">🌟</div>'


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
            font-weight: 900 !important;
            text-shadow: none !important;
        }}
        p, span, div, label, li {{
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
            border: 2px solid #e2e8f0 !important; /* 薄いグレーの枠線 */
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

        /* --- 入力フォーム --- */
        .stSelectbox div[data-baseweb="select"] {{
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }}
        .stSelectbox div[data-baseweb="select"]:hover {{
            border-color: #4a90e2 !important;
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
            animation: float 6s ease-in-out infinite;
        }}
        .logo-img {{
            width: 100px;
            height: auto;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
        }}
        .page-title {{
            font-size: 3rem;
            font-weight: 900;
            color: #0f172a;
            margin: 0;
            line-height: 1.2;
        }}
        
        /* エキスパンダー */
        .streamlit-expanderHeader {{
            background-color: #f8fafc !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            color: #0f172a !important;
        }}
        .streamlit-expanderContent {{
            background-color: #ffffff !important;
            color: #333333 !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# ==========================================
# 3. データ読み込み
# ==========================================
@st.cache_data
def load_guidance_data():
    """指導データをJSONファイルから読み込む"""
    try:
        script_path = Path(__file__)
        app_root = script_path.parent.parent
        json_path = app_root / "guidance_data.json"

        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        st.error(f"**【エラー】 `guidance_data.json` が見つかりません！** Path: `{json_path}`")
        st.stop()
    except json.JSONDecodeError:
        st.error("**【エラー】 JSONファイルの形式が正しくありません。**")
        st.stop()

guidance_data = load_guidance_data()

# ==========================================
# 4. メインコンテンツ
# ==========================================

# --- 戻るボタン (★指定されたHTMLコード) ---
st.markdown('<div class="back-link"><a href="https://aspecialeducationapp-6iuvpdfjbflp4wyvykmzey.streamlit.app/" target="_self">« TOPページに戻る</a></div>', unsafe_allow_html=True)

# ヘッダー (ロゴ + タイトル)
st.markdown(f"""
    <div class="header-container">
        {logo_html}
        <h1 class="page-title">指導支援内容の参照</h1>
    </div>
""", unsafe_allow_html=True)

# 説明文 (青枠アラート風デザイン)
st.markdown("""
<div style="background-color: #f0f9ff; border: 2px solid #4a90e2; padding: 20px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(74,144,226,0.1); text-align: center;">
    <h4 style="margin: 0; color: #0f172a;">🎯 使い方</h4>
    <p style="margin-top: 5px; color: #334155;">日常生活における実態や障害の状況から、適した指導支援の方法を3ステップで検索できます。</p>
</div>
""", unsafe_allow_html=True)


# --- ▼ 選択UI部分 (ぬるっと動くカード) ▼ ---
with st.container(border=True):
    st.markdown("### 🔍 検索メニュー")
    
    cols = st.columns(3)
    selected_detail_key = None
    detail_data = None
    
    with cols[0]:
        # ステップ1: カテゴリー選択
        categories = list(guidance_data.keys())
        selected_category = st.selectbox("**Step 1：** カテゴリー", categories, help="大まかな分類を選びます。")
    
    with cols[1]:
        # ステップ2: 項目選択
        if selected_category:
            subcategories = list(guidance_data[selected_category].keys())
            selected_subcategory = st.selectbox("**Step 2：** 項目", subcategories, help="具体的な困りごとを選びます。")
    
    with cols[2]:
        # ステップ3: 詳細選択
        if selected_category and selected_subcategory:
            detail_items = list(guidance_data[selected_category][selected_subcategory].keys())
            selected_detail_key = st.selectbox(
                "**Step 3：** 詳細",
                detail_items,
                help="さらに詳しい支援内容を選びます。"
            )
            detail_data = guidance_data[selected_category][selected_subcategory].get(selected_detail_key)

# --- ▲ 選択UI部分 ▲ ---


# --- ▼ 表示ボタンと結果表示 ▼ ---
st.markdown("<br>", unsafe_allow_html=True)

# ボタンエリア (カードで囲んで強調)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if st.button("💡 適した指導・支援を表示", type="primary"):
        display_results = True
    else:
        display_results = False

if display_results:
    if detail_data:
        st.markdown("---")
        st.markdown(f"<h2 style='text-align: center; margin-bottom: 20px;'>📌 「{selected_detail_key}」の指導・支援</h2>", unsafe_allow_html=True)

        # 指導内容の表示 (ぬるっと動くカード)
        with st.container(border=True):
            st.subheader("📝 指導内容")
            items_list = detail_data.get("items", [])
            if not items_list:
                st.write("この項目には詳細な支援内容が登録されていません。")

            for item in items_list:
                if isinstance(item, dict):
                   # 辞書型の場合はアコーディオンで表示
                   with st.expander(f"**{item.get('title', 'タイトルなし')}**"):
                        for detail in item.get('details', []):
                            st.write(f"✓ {detail}")
                else:
                    # 文字列の場合はそのまま表示
                    st.write(f"✓ {item}")

        # 関連画像の表示 (ある場合のみ、カード表示)
        image_info = detail_data.get("image")
        if image_info and image_info.get("url"):
            with st.container(border=True):
                st.subheader("🖼️ 関連教材・イメージ")
                st.image(image_info["url"], caption=image_info.get("caption"), use_container_width=True)
    else:
        st.warning("表示するデータがありません。選択内容を確認してください。")