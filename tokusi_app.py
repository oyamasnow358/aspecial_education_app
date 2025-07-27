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
            background-image: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        /* サイドバーの背景を少し透過 */
        [data-testid="stSidebar"] {
            background-color: rgba(240, 242, 246, 0.9);
        }
        /* サイドバーの閉じるボタンのアイコンを強制的に変更 */
        [data-testid="stSidebarNavCollapseButton"]::after { content: '«' !important; }
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


st.set_page_config(
    page_title="特別支援教育サポートアプリ",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSSを適用
load_css()



# ページ遷移を管理するための関数
def set_page(page):
    st.session_state.page_to_visit = page

# ページ遷移を管理するための関数
def set_page(page):
    st.session_state.page_to_visit = page

# st.session_stateをチェックしてページ遷移を実行
if "page_to_visit" in st.session_state:
    page = st.session_state.page_to_visit
    del st.session_state.page_to_visit
    st.switch_page(page)

st.title("🌟 特別支援教育サポートアプリ")

# メインイメージ
st.image("https://i.imgur.com/AbUxfxP.png", caption="子どもたちの「できた！」を支援する", use_container_width=True)

st.header("ようこそ！")
st.write("""
このアプリは、特別支援教育に関わる先生方をサポートするためのツールです。
子どもたち一人ひとりのニーズに合わせた指導や支援のヒントを見つけたり、
発達段階を記録・分析したりすることができます。

**サイドバーのメニューから、利用したい機能を選択してください。**
""")

st.header("各機能の紹介")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("### 📚 指導支援内容")
        st.write("日常生活の困りごとに応じた、具体的な指導・支援のアイデアを検索できます。")
        st.button("この機能を使う ➡", on_click=set_page, args=("pages/1_指導支援内容.py",), key="btn_guidance")

    with st.container(border=True):
        st.markdown("### 📈 分析方法")
        st.write("教育学や心理学に基づいた様々な分析方法の解説と、実践で使えるツールを提供します。")
        st.button("この機能を使う ➡", on_click=set_page, args=("pages/3_分析方法.py",), key="btn_analysis")

with col2:
    with st.container(border=True):
        st.markdown("### 📊 発達チャート作成")
        st.write("お子さんの発達段階を記録し、レーダーチャートで視覚的に確認・保存できます。")
        st.button("この機能を使う ➡", on_click=set_page, args=("pages/2_発達チャート.py",), key="btn_chart")

    with st.container(border=True):
        st.markdown("### 📊 AIによる対話")
        st.write("支援方法やと個別の支援計画の作成など")
        st.button("この機能を使う ➡", on_click=set_page, args=("pages/5_AIによる対話.py",), key="btn_chart")

    with st.container(border=True):
        st.markdown("### 📝 フィードバック")
        st.write("アプリの改善や、新しい指導実践の共有など、皆様からのご意見をお待ちしています。")
        st.button("この機能を使う ➡", on_click=set_page, args=("pages/4_フィードバック.py",), key="btn_feedback")

# --- ▼ 機能紹介を均等にするため、列の外に新しい機能を追加 ▼ ---
st.markdown("---")
with st.container(border=True):
    st.markdown("### 🤖 AIによる対話 <span style='color: #8A2BE2; font-size: 0.8em; font-weight: bold;'>NEW!</span>", unsafe_allow_html=True)
    st.write("入力フォームや対話を通じて、AIが個別の指導計画作成や指導のヒントを提案します。")
    # ボタンを中央に配置するための列
    b_col1, b_col2, b_col3 = st.columns([1,2,1])
    with b_col2:
        st.button("この機能を使ってみる ➡", on_click=set_page, args=("pages/5_AIによる対話.py",), key="btn_ai_chat", type="primary", use_container_width=True)
st.markdown("---")

with st.container(border=True):
    st.header("関連ツール＆リンク")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### 📁 教育・心理分析ツール")
        st.page_link("https://abaapppy-k7um2qki5kggexf8qkfxjc.streamlit.app/", label="応用行動分析", icon="🔗")
        st.page_link("https://kinoukoudou-ptfpnkq3uqgaorabcyzgf2.streamlit.app/", label="機能的行動評価分析", icon="🔗")

    with c2:
        st.markdown("##### 📁 統計学分析ツール")
        st.page_link("https://annketo12345py-edm3ajzwtsmmuxbm8qbamr.streamlit.app/", label="アンケートデータ、総合統計分析", icon="🔗")
        st.page_link("https://soukan-jlhkdhkradbnxssy29aqte.streamlit.app/", label="相関分析", icon="🔗")
        st.page_link("https://kaikiapp-tjtcczfvlg2pyhd9bjxwom.streamlit.app/", label="多変量回帰分析", icon="🔗")
        st.page_link("https://tkentei-flhmnqnq6dti6oyy9xnktr.streamlit.app/", label="t検定", icon="🔗")
        st.page_link("https://rojisthik-buklkg5zeh6oj2gno746ix.streamlit.app/", label="ロジスティック回帰分析", icon="🔗")
        st.page_link("https://nonparametoric-nkk2awu6yv9xutzrjmrsxv.streamlit.app/", label="ノンパラメトリック統計分析", icon="🔗")

    st.markdown("---")
    st.markdown("##### 🗨️ ご意見・ご感想")
    st.markdown("自立活動の参考指導、各分析ツールにご意見がある方は以下のフォームから送ってください（埼玉県の学校教育関係者のみＳＴアカウントで回答できます）。")
    st.page_link("https://docs.google.com/forms/d/1dKzh90OkxMoWDZXV31FgPvXG5EvNlMFOrvSPGvYTSC8/preview", label="アンケートフォーム", icon="📝")

st.markdown("---")
st.warning("""
**【利用上の注意】**
それぞれのアプリに記載してある内容、分析ツールのデータや図、表を外部（研究発表など）で利用する場合は、管理者(岩槻はるかぜ特別支援学校 小山)までご相談ください。無断での転記・利用を禁じます。
""")