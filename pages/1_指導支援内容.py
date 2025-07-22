      
import streamlit as st
import json

# --- ▼ 共通CSSの読み込み (変更なし) ▼ ---
def load_css():
    """カスタムCSSを読み込む関数"""
    css = """
    <style>
        /* --- 背景画像の設定 --- */
        [data-testid="stAppViewContainer"] > .main {
            background-image: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), url("https://i.imgur.com/CTSCBYi.png");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        /* (以下、元のCSSと同じなので省略) */
        .footer-hr {
            border: none;
            height: 3px;
            background: linear-gradient(to right, #4a90e2, #8A2BE2);
            margin-top: 40px;
            margin-bottom: 20px;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
# --- ▲ 共通CSSの読み込み ▲ ---


# --- ▼ 外部JSONデータを読み込む関数 (新規追加) ▼ ---
@st.cache_data
def load_guidance_data(filepath="guidance_data.json"):
    """指導データをJSONファイルから読み込む"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# --- ▲ 外部JSONデータを読み込む関数 ▲ ---


# --- アプリケーション本体 ---
st.set_page_config(page_title="指導支援内容", page_icon="📚", layout="wide")

# CSSを適用
load_css()

# データを読み込む
guidance_data = load_guidance_data()

st.title("📚 指導支援内容の参照")
st.write("ここでは、日常生活における実態や障害の状況から適した指導支援の方法を探すことができます。")


# --- ▼ 選択UI部分 (ロジックはほぼ同じ) ▼ ---
with st.container(border=True):
    st.info("下のメニューから順番に選択して、適した支援方法を見つけましょう。")
    
    cols = st.columns(3)
    selected_detail_key = None
    detail_data = None
    
    with cols[0]:
        # ステップ1: カテゴリー選択
        categories = list(guidance_data.keys())
        selected_category = st.selectbox("**ステップ1：** カテゴリーを選択", categories, help="大まかな分類を選びます。")
    
    with cols[1]:
        # ステップ2: 項目選択
        if selected_category:
            subcategories = list(guidance_data[selected_category].keys())
            selected_subcategory = st.selectbox("**ステップ2：** 項目を選択", subcategories, help="具体的な困りごとを選びます。")
    
    with cols[2]:
        # ステップ3: 詳細選択
        if selected_category and selected_subcategory:
            detail_items = list(guidance_data[selected_category][selected_subcategory].keys())
            selected_detail_key = st.selectbox(
                "**ステップ3：** 詳細を選択",
                detail_items,
                help="さらに詳しい支援内容を選びます。"
            )
            # 選択された詳細データを取得
            detail_data = guidance_data[selected_category][selected_subcategory].get(selected_detail_key)

# --- ▲ 選択UI部分 ▲ ---


# --- ▼ 表示ボタンと結果表示 (ロジックを修正) ▼ ---
if st.button("💡 適した指導・支援を表示", type="primary", use_container_width=True):
    if detail_data:
        st.markdown('<hr class="footer-hr">', unsafe_allow_html=True)
        st.header(f"📌 「{selected_detail_key}」に適した指導・支援")

        # 指導内容の表示
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

        # 関連画像の表示 (データから動的に取得)
        image_info = detail_data.get("image")
        st.subheader("🖼️ 関連教材・イメージ")
        with st.container(border=True):
            if image_info and image_info.get("url"):
                st.image(image_info["url"], caption=image_info.get("caption"), use_container_width=True)
            else:
                st.write("この項目に関連する画像は現在ありません。")
    else:
        st.warning("表示するデータがありません。選択内容を確認してください。")
# --- ▲ 表示ボタンと結果表示 ▲ ---

    