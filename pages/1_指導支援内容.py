import streamlit as st
import json
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
# 1. デザイン定義 (Mirairo共通・白枠・アニメーション)
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
        h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown, .stSelectbox label {
            color: #ffffff !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.9) !important;
        }

        /* --- サイドバー (半透明・すりガラス) --- */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
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

        /* --- ボタン --- */
        .stButton > button {
            width: 100%;
            background-color: #000000 !important;
            border: 2px solid #ffffff !important;
            color: #4a90e2 !important;
            font-weight: bold !important;
            border-radius: 30px !important;
            transition: all 0.3s ease !important;
        }
        .stButton > button:hover {
            border-color: #4a90e2 !important;
            color: #ffffff !important;
            background-color: #4a90e2 !important;
        }
        
        /* Primaryボタン */
        .stButton > button[kind="primary"] {
            background-color: #4a90e2 !important;
            color: #ffffff !important;
            border: 2px solid #4a90e2 !important;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #ffffff !important;
            color: #4a90e2 !important;
        }

        /* --- セレクトボックス (黒背景に) --- */
        div[data-baseweb="select"] > div {
            background-color: #222 !important;
            color: #fff !important;
            border-color: #555 !important;
        }
        div[data-baseweb="popover"] div {
            background-color: #111 !important;
            color: #fff !important;
        }
        
        /* --- エキスパンダー --- */
        .streamlit-expanderHeader {
            background-color: rgba(255,255,255,0.1) !important;
            color: #fff !important;
            border-radius: 8px !important;
            border: 1px solid #555;
        }
        .streamlit-expanderContent {
            background-color: rgba(0,0,0,0.5) !important;
            border: 1px solid #444;
            border-top: none;
            border-radius: 0 0 8px 8px;
        }

        /* --- infoボックス --- */
        [data-testid="stAlert"] {
            background-color: rgba(74, 144, 226, 0.1) !important;
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

# ==========================================
# 2. データ読み込み (パス自動解決版)
# ==========================================
@st.cache_data
def load_guidance_data():
    """指導データをJSONファイルから読み込む（パス自動解決つき）"""
    try:
        # このスクリプトファイル自身の絶対パスを取得
        script_path = Path(__file__)
        # アプリのルートディレクトリのパスを構築 (pagesフォルダの親)
        app_root = script_path.parent.parent
        # 読み込むべきJSONファイルの絶対パスを決定
        json_path = app_root / "guidance_data.json"

        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        st.error(
            f"""
            **【エラー】 `guidance_data.json` が見つかりません！**
            パス: `{json_path}`
            `pages` フォルダの外（Home.pyと同じ階層）にファイルを配置してください。
            """
        )
        st.stop()
    except json.JSONDecodeError:
        st.error("**【エラー】 JSONファイルの形式が正しくありません。**")
        st.stop()

guidance_data = load_guidance_data()

# ==========================================
# 3. メインコンテンツ
# ==========================================

# --- 戻るボタン ---
st.page_link("tokusi_app.py", label="« TOPページに戻る", icon="🏠")

st.title("📚 指導支援内容の参照")
st.markdown("""
<div style="background: rgba(255,255,255,0.05); border: 1px solid #fff; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
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
            # 選択された詳細データを取得
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
            # detail_data は {"items": [...], "image": {...}} という形式
            items_list = detail_data.get("items", [])
            if not items_list:
                st.write("この項目には詳細な支援内容が登録されていません。")

            for item in items_list:
                if isinstance(item, dict):
                   # titleとdetailsを持つオブジェクトの場合
                   with st.expander(f"**{item.get('title', 'タイトルなし')}**"):
                        for detail in item.get('details', []):
                            st.write(f"✓ {detail}")
                else:
                    # 単純な文字列のリストの場合
                    st.write(f"✓ {item}")

        # 関連画像の表示
        image_info = detail_data.get("image")
        if image_info and image_info.get("url"):
            st.subheader("🖼️ 関連教材・イメージ")
            with st.container(border=True):
                st.image(image_info["url"], caption=image_info.get("caption"), use_container_width=True)
    else:
        st.warning("表示するデータがありません。選択内容を確認してください。")