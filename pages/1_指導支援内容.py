import streamlit as st
import json
import base64
from pathlib import Path

# ==========================================
# 0. ページ設定
# ==========================================
st.set_page_config(
    page_title="Mirairo - 指導支援内容", 
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

logo_path = "mirairo2.png" 
logo_b64 = get_img_as_base64(logo_path)
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img">' if logo_b64 else '<div class="logo-placeholder">🌟</div>'


# ==========================================
# 2. デザイン定義 (★白背景・ライトモード固定★)
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
            color: #1a1a1a !important; /* 文字色はくっきり黒 */
            line-height: 1.6 !important;
        }}

        /* --- 背景 (白95%透過で画像をうっすら表示) --- */
        [data-testid="stAppViewContainer"] {{
            background-color: #ffffff;
            background-image: linear-gradient(rgba(255,255,255,0.95), rgba(255,255,255,0.95)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-attachment: fixed;
        }}

        /* --- 文字色 (黒・視認性重視) --- */
        h1, h2, h3, h4, h5, h6 {{
            color: #0f172a !important; /* 濃紺 */
            font-weight: 700 !important;
            text-shadow: none !important;
        }}
        p, span, div, label, .stMarkdown {{
            color: #333333 !important;
            text-shadow: none !important;
        }}

        /* --- サイドバー (白) --- */
        [data-testid="stSidebar"] {{
            background-color: #ffffff !important;
            border-right: 1px solid #e2e8f0;
        }}
        [data-testid="stSidebarNavCollapseButton"] {{ color: #333 !important; }}

        /* --- 機能カード (白背景・影付き) --- */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        [data-testid="stBorderContainer"] {{
            background-color: #ffffff !important; /* 白背景 */
            border: 1px solid #cbd5e1 !important; /* 薄いグレーの枠 */
            border-radius: 12px !important;
            padding: 25px !important;
            margin-bottom: 25px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
            
            animation: fadeInUp 0.6s ease-out forwards;
        }}
        
        [data-testid="stBorderContainer"]:hover {{
            border-color: #4a90e2 !important;
            box-shadow: 0 8px 24px rgba(74, 144, 226, 0.15) !important;
            transform: translateY(-2px);
            transition: all 0.3s ease;
        }}

        /* --- ボタン --- */
        .stButton > button {{
            width: 100%;
            background-color: #ffffff !important;
            border: 2px solid #4a90e2 !important;
            color: #4a90e2 !important;
            font-weight: bold !important;
            border-radius: 30px !important;
            transition: all 0.3s ease !important;
        }}
        .stButton > button:hover {{
            background-color: #4a90e2 !important;
            color: #ffffff !important;
        }}
        
        /* Primaryボタン */
        .stButton > button[kind="primary"] {{
            background-color: #4a90e2 !important;
            color: #ffffff !important;
            border: 2px solid #4a90e2 !important;
            box-shadow: 0 4px 6px rgba(74, 144, 226, 0.2);
        }}
        .stButton > button[kind="primary"]:hover {{
            background-color: #2563eb !important;
            color: #ffffff !important;
            transform: scale(1.02);
        }}

        /* --- セレクトボックス (白背景) --- */
        div[data-baseweb="select"] > div {{
            background-color: #ffffff !important;
            border-color: #cbd5e1 !important;
            color: #333 !important;
        }}
        div[data-baseweb="popover"] div {{
            background-color: #ffffff !important;
            color: #333 !important;
        }}
        
        /* --- エキスパンダー --- */
        .streamlit-expanderHeader {{
            background-color: #f1f5f9 !important;
            color: #334155 !important;
            border-radius: 8px !important;
            border: 1px solid #e2e8f0;
        }}
        .streamlit-expanderContent {{
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0;
            border-top: none;
            border-radius: 0 0 8px 8px;
            color: #333 !important;
        }}

        /* --- infoボックス --- */
        [data-testid="stAlert"] {{
            background-color: #f0f9ff !important;
            border: 1px solid #bae6fd !important;
            color: #0369a1 !important;
        }}

        /* --- 戻るボタン --- */
        .back-link a {{
            display: inline-block;
            padding: 10px 20px;
            background: #ffffff;
            border: 1px solid #4a90e2;
            border-radius: 25px;
            color: #4a90e2 !important;
            text-decoration: none;
            margin-bottom: 20px;
            transition: all 0.3s;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        .back-link a:hover {{
            background: #4a90e2;
            color: #ffffff !important;
            box-shadow: 0 4px 8px rgba(74, 144, 226, 0.2);
        }}
        
        /* --- ヘッダー (ロゴ) --- */
        .header-container {{
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 2px solid #f1f5f9;
        }}
        .logo-img {{
            width: 80px;
            height: auto;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
        }}
        .page-title {{
            font-size: 2.2rem;
            font-weight: 900;
            color: #0f172a;
            margin: 0;
        }}
        
        hr {{ border-color: #cbd5e1; }}
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

# --- 戻るボタン (★正しいリンクに変更済み) ---
st.markdown('<div class="back-link"><a href="https://aspecialeducationapp-6iuvpdfjbflp4wyvykmzey.streamlit.app/" target="_self">« TOPページに戻る</a></div>', unsafe_allow_html=True)

# ヘッダー (ロゴ + タイトル)
st.markdown(f"""
    <div class="header-container">
        {logo_html}
        <h1 class="page-title">📚 指導支援内容の参照</h1>
    </div>
""", unsafe_allow_html=True)

# 説明文
st.markdown("""
<div style="background: #f0f9ff; border-left: 6px solid #4a90e2; padding: 20px; border-radius: 6px; margin-bottom: 20px; color: #0c4a6e;">
    日常生活における実態や障害の状況から、適した指導支援の方法を探すことができます。
</div>
""", unsafe_allow_html=True)


# --- ▼ 選択UI部分 (白枠カード) ▼ ---
with st.container(border=True):
    st.info("下のメニューから順番に選択して、適した支援方法を見つけましょう。")
    
    cols = st.columns(3)
    selected_detail_key = None
    detail_data = None
    
    with cols[0]:
        # ステップ1: カテゴリー選択
        categories = list(guidance_data.keys())
        selected_category = st.selectbox("**ステップ1：** カテゴリー", categories, help="大まかな分類を選びます。")
    
    with cols[1]:
        # ステップ2: 項目選択
        if selected_category:
            subcategories = list(guidance_data[selected_category].keys())
            selected_subcategory = st.selectbox("**ステップ2：** 項目", subcategories, help="具体的な困りごとを選びます。")
    
    with cols[2]:
        # ステップ3: 詳細選択
        if selected_category and selected_subcategory:
            detail_items = list(guidance_data[selected_category][selected_subcategory].keys())
            selected_detail_key = st.selectbox(
                "**ステップ3：** 詳細",
                detail_items,
                help="さらに詳しい支援内容を選びます。"
            )
            detail_data = guidance_data[selected_category][selected_subcategory].get(selected_detail_key)

# --- ▲ 選択UI部分 ▲ ---


# --- ▼ 表示ボタンと結果表示 ▼ ---
st.markdown("<br>", unsafe_allow_html=True)

if st.button("💡 適した指導・支援を表示", type="primary", use_container_width=True):
    if detail_data:
        st.markdown("---")
        st.header(f"📌 「{selected_detail_key}」に適した指導・支援")

        # 指導内容の表示 (白枠カード)
        with st.container(border=True):
            items_list = detail_data.get("items", [])
            if not items_list:
                st.write("この項目には詳細な支援内容が登録されていません。")

            for item in items_list:
                if isinstance(item, dict):
                   with st.expander(f"**{item.get('title', 'タイトルなし')}**"):
                        for detail in item.get('details', []):
                            st.write(f"✓ {detail}")
                else:
                    st.write(f"✓ {item}")

        # 関連画像の表示
        image_info = detail_data.get("image")
        if image_info and image_info.get("url"):
            st.subheader("🖼️ 関連教材・イメージ")
            with st.container(border=True):
                st.image(image_info["url"], caption=image_info.get("caption"), use_container_width=True)
    else:
        st.warning("表示するデータがありません。選択内容を確認してください。")