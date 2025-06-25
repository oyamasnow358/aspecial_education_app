import streamlit as st

# --- ▼ 共通CSSの読み込み ▼ ---
def load_css():
    """カスタムCSSを読み込む関数"""
    css = """
    <style>
        /* --- 背景画像の設定 --- */
        /* ご用意された画像のURLを下の 'url(...)' 内に貼り付けてください */
        /* 例: url("https://i.imgur.com/your_image.jpg"); */
        [data-testid="stAppViewContainer"] > .main {
            background-image: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), url("https://i.imgur.com/CTSCBYi.png");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        /* サイドバーの背景を少し透過 */
        [data-testid="stSidebar"] {
            background-color: rgba(240, 242, 246, 0.9);
        }

        /* --- 全体のフォント --- */
        html, body, [class*="st-"] {
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
        }

        /* --- 見出しのスタイル --- */
        h1 {
            color: #2c3e50; /* ダークブルー */
            text-align: center;
            padding-bottom: 20px;
            font-weight: bold;
        }
        h2 {
            color: #34495e; /* 少し明るいダークブルー */
            border-left: 6px solid #8A2BE2; /* 紫のアクセント */
            padding-left: 12px;
            margin-top: 40px;
        }
        h3 {
            color: #34495e;
            border-bottom: 2px solid #4a90e2; /* 青のアクセント */
            padding-bottom: 8px;
            margin-top: 30px;
        }

        /* --- カードデザイン (st.container(border=True)のスタイル) --- */
        div[data-testid="stVerticalBlock"] div.st-emotion-cache-1r6slb0 {
            background-color: rgba(255, 255, 255, 0.95);
            border: 1px solid #e0e0e0;
            border-radius: 15px;
            padding: 1.5em 1.5em;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
            transition: box-shadow 0.3s ease-in-out, transform 0.3s ease-in-out;
            margin-bottom: 20px; /* カード間の余白 */
        }
        div[data-testid="stVerticalBlock"] div.st-emotion-cache-1r6slb0:hover {
            box-shadow: 0 10px 20px rgba(74, 144, 226, 0.2);
            transform: translateY(-5px);
        }
        
        /* --- ボタンのスタイル --- */
        .stButton>button {
            border: 2px solid #4a90e2;
            border-radius: 25px;
            color: #4a90e2;
            background-color: #ffffff;
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            border-color: #8A2BE2;
            color: white;
            background-color: #8A2BE2;
            transform: scale(1.05);
        }
        /* Primaryボタン */
        .stButton>button[kind="primary"] {
            background-color: #4a90e2;
            color: white;
            border: none;
        }
        .stButton>button[kind="primary"]:hover {
            background-color: #357ABD;
            border-color: #357ABD;
            transform: scale(1.05);
        }

        /* --- st.infoのカスタムスタイル --- */
        .st-emotion-cache-1wivap1 { /* st.infoのコンテナ */
             background-color: rgba(232, 245, 253, 0.7); /* 淡い青 */
             border-left: 5px solid #4a90e2;
             border-radius: 8px;
        }

        /* --- フッターの区切り線 --- */
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


st.set_page_config(page_title="指導支援内容", page_icon="📚", layout="wide")

# CSSを適用
load_css()

st.title("📚 指導支援内容の参照")
st.write("ここでは、日常生活における実態や障害の状況から適した指導支援の方法を探すことができます。")

# 画像URL
img_dressing = "https://i.imgur.com/t4RLTeG.jpeg"
img_sign_language = "https://i.imgur.com/gqmXyNT.png"
img_hasizo = "https://i.imgur.com/FW4CF0E.jpeg"

# 指導データ (本来は別ファイル(例: data.json)から読み込むのが望ましい)
guidance_data = {
    # (省略されたデータはそのまま)
}
if not guidance_data: # データがない場合のダミー
    guidance_data = {
        "身体の動き": {
            "姿勢・動作のコントロール": ["衣服の着脱練習", "食事の練習"],
            "手指の操作": ["指文字練習"]
        },
        "コミュニケーション":{
            "意思の伝達": ["PECSを使った支援", "サインを使った支援"]
        }
    }

with st.container(border=True):
    st.info("下のメニューから順番に選択して、適した支援方法を見つけましょう。")
    
    cols = st.columns(3)
    selected_detail = None
    detail_data = None
    
    with cols[0]:
        selected_category = st.selectbox("**ステップ1：** カテゴリーを選択", list(guidance_data.keys()), help="大まかな分類を選びます。")
    
    with cols[1]:
        if selected_category:
            selected_subcategory = st.selectbox("**ステップ2：** 項目を選択", list(guidance_data[selected_category].keys()), help="具体的な困りごとを選びます。")
    
    with cols[2]:
        if selected_category and selected_subcategory:
            subcategory_data = guidance_data[selected_category][selected_subcategory]
            if isinstance(subcategory_data, dict):
                selected_detail = st.selectbox(
                    "**ステップ3：** 詳細を選択",
                    list(subcategory_data.keys()),
                    help="さらに詳しい支援内容を選びます。"
                )
                detail_data = subcategory_data.get(selected_detail)
            elif isinstance(subcategory_data, list):
                selected_detail = selected_subcategory # 詳細がない場合はサブカテゴリ名をそのまま使う
                detail_data = subcategory_data

if st.button("💡 適した指導・支援を表示", type="primary", use_container_width=True):
    if detail_data:
        st.markdown('<hr class="footer-hr">', unsafe_allow_html=True)
        st.header(f"📌 「{selected_detail}」に適した指導・支援")

        with st.container(border=True):
            for item in detail_data:
                if isinstance(item, dict):
                   with st.expander(f"**{item.get('title', 'タイトルなし')}**"):
                        for detail in item.get('details', []):
                            st.write(f"✓ {detail}")
                else:
                    st.write(f"✓ {item}")

        # 関連画像の表示
        st.subheader("🖼️ 関連教材・イメージ")
        with st.container(border=True):
            if "衣服の着脱練習" in selected_detail:
                st.image(img_dressing, caption="衣服の着脱練習の教材", use_container_width=True)
            if "指文字練習" in selected_detail:
                st.image(img_sign_language, caption="指文字", width=300)
            if "食事の練習" in selected_detail:
                st.image(img_hasizo, caption="箸ゾーくん（箸の練習に最適）", use_container_width=True)
            
            # 画像がない場合のメッセージ
            if not any(s in selected_detail for s in ["衣服の着脱練習", "指文字練習", "食事の練習"]):
                st.write("この項目に関連する画像は現在ありません。")
    else:
        st.warning("表示するデータがありません。選択内容を確認してください。")