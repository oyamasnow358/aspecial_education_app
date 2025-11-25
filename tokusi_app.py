import streamlit as st
import base64
import os

# --- 1. ページ設定 ---
st.set_page_config(
    page_title="Mirairo",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 画像処理 (ロゴ用) ---
def get_img_as_base64(file):
    try:
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

logo_path = "mirairo.png"
logo_b64 = get_img_as_base64(logo_path)
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img">' if logo_b64 else '<div class="logo-placeholder">🌟</div>'


# --- 2. CSSデザイン (視認性・可読性 特化版) ---
def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = f"""
    <style>
        /* --- 基本設定 --- */
        html, body, [class*="css"] {{
            font-family: 'Noto Sans JP', sans-serif !important;
        }}

        /* --- 背景設定 --- */
        [data-testid="stAppViewContainer"] {{
            background-color: #000000;
            /* 背景画像の設定 */
            background-image: url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-position: center center;
            background-attachment: fixed;
        }}
        /* 背景の上に黒いフィルターを重ねて全体を少し暗くする */
        [data-testid="stAppViewContainer"]::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6); /* ここで暗さを調整 */
            z-index: 0;
            pointer-events: none;
        }}

        /* --- サイドバー (完全に不透明な黒にして文字を見やすく) --- */
        [data-testid="stSidebar"] {{
            background-color: #0a0a0a !important; /* 真っ黒に近い色 */
            border-right: 1px solid #333;
            z-index: 1;
        }}
        /* サイドバー内の文字色を白に強制 */
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] span, 
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label {{
            color: #ffffff !important;
        }}

        /* --- 説明文用の「濃い」ガラスプレート --- */
        /* ここがポイント：文字の背景に濃い色を敷く */
        .glass-container {{
            background-color: rgba(20, 20, 20, 0.85); /* ほぼ不透明な黒 */
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            color: #ffffff; /* 文字色 */
            line-height: 1.8; /* 行間を広げて読みやすく */
            font-size: 1.05rem;
        }}
        
        /* --- 機能カード (st.container) --- */
        [data-testid="stBorderContainer"] {{
            background-color: rgba(30, 30, 30, 0.9) !important; /* カード内も濃い黒 */
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 12px !important;
            padding: 20px !important;
        }}
        /* カード内の文字色 */
        [data-testid="stBorderContainer"] p, 
        [data-testid="stBorderContainer"] h3 {{
            color: #ffffff !important;
        }}
        /* カードのキャプション(説明文) */
        [data-testid="stBorderContainer"] div[data-testid="stCaptionContainer"] {{
            color: #cccccc !important; /* 薄いグレー */
            font-size: 0.9rem !important;
        }}

        /* --- ヘッダーアニメーション --- */
        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-8px); }}
            100% {{ transform: translateY(0px); }}
        }}
        .header-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            padding: 50px 0;
            animation: float 6s ease-in-out infinite;
            position: relative;
            z-index: 1;
        }}
        .logo-img {{
            width: 90px;
            height: auto;
            filter: drop-shadow(0 0 10px rgba(255,255,255,0.5));
        }}
        .main-title {{
            font-size: 4.5rem;
            font-weight: 900;
            line-height: 1;
            margin: 0;
            color: #ffffff; /* タイトルは真っ白 */
            text-shadow: 0 0 15px rgba(255, 255, 255, 0.6); /* 白く発光 */
        }}
        .sub-title {{
            font-size: 1.1rem;
            color: #cbd5e0;
            letter-spacing: 0.15em;
            margin-top: 8px;
            font-weight: 500;
        }}

        /* --- ボタン --- */
        .stButton > button {{
            width: 100%;
            background-color: #000000 !important;
            border: 1px solid #4a90e2 !important;
            color: #4a90e2 !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
        }}
        .stButton > button:hover {{
            background-color: #4a90e2 !important;
            color: #ffffff !important;
        }}

        /* --- その他 --- */
        h1, h2, h3 {{
            color: #ffffff !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }}
        a {{ color: #63b3ed !important; font-weight: bold; }}
        hr {{ border-color: #555; }}
        
        /* サイドバーの閉じるボタン */
        [data-testid="stSidebarCollapseButton"] {{
            color: #ffffff !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# --- 3. マニュアルデータ ---
manuals = {
    "guidance": """
    ### 📚 指導支援内容 マニュアル
    お子さんの日常生活の困りごとに応じた、具体的な指導・支援のアイデアを検索します。
    **使い方:**
    1.  **3つのステップで選択**: 画面のドロップダウンを左から順に選びます。
    2.  **表示ボタン**: 「💡 適した指導・支援を表示」をクリック。
    3.  **確認**: 表示された内容を確認します。
    """,
    "chart": """
    ### 📊 発達チャート作成 マニュアル
    発達段階を記録し、レーダーチャートで可視化・保存します。
    **使い方:**
    1.  **入力**: 12のカテゴリーで現在の状況を選択します。
    2.  **作成**: 「📊 チャートを作成」ボタンをクリック。
    3.  **保存**: スプレッドシートまたはExcel形式でダウンロード可能です。
    """,
    "analysis": """
    ### 📈 分析方法 マニュアル
    教育学・心理学に基づいた分析手法の解説です。
    **使い方:**
    *   **方法A**: サイドバーから手法（ABAなど）を直接選択。
    *   **方法B**: メインエリアでお子さんの状況を選んで検索。
    """,
    "plan_creation": """
    ### 🤖 計画作成サポート マニュアル
    個別の支援・指導計画作成用のプロンプト（AIへの命令文）を作成します。
    **使い方:**
    1.  プロンプトの種類を選択。
    2.  実態や課題を入力。
    3.  生成された文面をコピーしてChatGPT等で使用。
    """,
    "lesson_plan_ai": """
    ### 📝 AI指導案作成 マニュアル
    基本情報から学習指導案を自動生成します。
    **使い方:**
    1.  学部・単元などの基本情報を入力。
    2.  プロンプトを作成し、AIに入力。
    3.  AIの回答（JSON）を貼り付けてExcelを出力。
    """,
    "guideline_page": """
    ### 📜 指導要領早引き マニュアル
    学習指導要領の内容を素早く検索します。
    **使い方:**
    *   学部、障害種別、教科を選択して「表示」をクリック。
    """,
    "lesson_card_library": """
    ### 🃏 授業カード マニュアル
    授業のアイデアを共有・検索するライブラリです。
    **使い方:**
    *   検索バーやハッシュタグで実践事例を探せます。
    """
}

# --- 4. ロジック ---
def set_page(page):
    st.session_state.page_to_visit = page

if "page_to_visit" in st.session_state:
    page = st.session_state.page_to_visit
    del st.session_state.page_to_visit
    st.switch_page(page)
    
if 'current_lesson_id' not in st.session_state:
    st.session_state.current_lesson_id = None
if 'show_all_flow' not in st.session_state: 
    st.session_state.show_all_flow = False
if 'show_create_form' not in st.session_state:
    st.session_state.show_create_form = False

  
# --- 5. メインコンテンツ ---

# ヘッダー (アニメーション)
st.markdown(f"""
    <div class="header-container">
        {logo_html}
        <div class="title-box">
            <h1 class="main-title">Mirairo</h1>
            <div class="sub-title">Data-Driven Education Platform</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ▼▼▼ 修正ポイント：説明文を「glass-container」クラスで囲む ▼▼▼
# これにより、背景に濃い色のプレートが敷かれ、文字が白くはっきりと表示されます。
st.markdown("""
<div class="glass-container">
    <h3>ようこそ！</h3>
    <p>
        このアプリは、特別支援教育に関わる先生方をサポートするための統合ツールです。<br>
        子どもたち一人ひとりのニーズに合わせた指導や支援のヒントを見つけたり、
        発達段階を記録・分析したり、AIによる計画作成の補助を受けることができます。
    </p>
    <p style="color: #4a90e2; font-weight: bold; margin-top: 10px;">
        ▼ 下の各機能パネル、またはサイドバーのメニューから利用したい機能を選択してください。
    </p>
</div>
""", unsafe_allow_html=True)

st.subheader("📂 各機能の紹介")

# --- 3カラムレイアウト (カード内の文字も見やすく調整済み) ---
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("### 📚 指導支援内容")
        st.caption("日常生活の困りごとに応じた、具体的な指導・支援のアイデアを検索できます。")
        c_btn, c_pop = st.columns([2, 1])
        c_btn.button("使う ➡", on_click=set_page, args=("pages/1_指導支援内容.py",), key="btn_guidance")
        with c_pop.popover("📖"):
            st.markdown(manuals["guidance"])

    with st.container(border=True):
        st.markdown("### 📈 分析方法")
        st.caption("教育学や心理学に基づいた分析手法の解説とツールです。")
        c_btn, c_pop = st.columns([2, 1])
        c_btn.button("使う ➡", on_click=set_page, args=("pages/3_分析方法.py",), key="btn_analysis")
        with c_pop.popover("📖"):
            st.markdown(manuals["analysis"])
    
    with st.container(border=True):
        st.markdown("### 🃏 授業カード") 
        st.caption("先生方の授業アイデアを共有・検索できるライブラリです。")
        c_btn, c_pop = st.columns([2, 1])
        c_btn.button("使う ➡", on_click=set_page, args=("pages/8_授業カードライブラリー.py",), key="btn_lesson_card_library")
        with c_pop.popover("📖"):
            st.markdown(manuals["lesson_card_library"])

with col2:
    with st.container(border=True):
        st.markdown("### 📊 発達チャート")
        st.caption("発達段階を記録し、レーダーチャートで視覚的に確認・保存できます。")
        c_btn, c_pop = st.columns([2, 1])
        c_btn.button("使う ➡", on_click=set_page, args=("pages/2_発達チャート.py",), key="btn_chart")
        with c_pop.popover("📖"):
            st.markdown(manuals["chart"])
    
    with st.container(border=True):
        st.markdown("### 🤖 AI計画作成")
        st.caption("個別の支援・指導計画作成用のプロンプトを簡単に生成します。")
        c_btn, c_pop = st.columns([2, 1])
        c_btn.button("使う ➡", on_click=set_page, args=("pages/4_AIによる支援,指導計画作成.py",), key="btn_plan_creation")
        with c_pop.popover("📖"):
            st.markdown(manuals["plan_creation"])

    with st.container(border=True):
        st.markdown("### 📝 AI指導案作成")
        st.caption("基本情報を入力するだけで、AIを活用して学習指導案を自動生成します。")
        c_btn, c_pop = st.columns([2, 1])
        c_btn.button("使う ➡", on_click=set_page, args=("pages/9_AIによる指導案作成.py",), key="btn_lesson_plan_ai")
        with c_pop.popover("📖"):
            st.markdown(manuals["lesson_plan_ai"])

with col3:
    with st.container(border=True):
        st.markdown("### 📜 指導要領早引き")
        st.caption("学部・段階ごとの学習指導要領の内容を素早く検索できます。")
        c_btn, c_pop = st.columns([2, 1])
        c_btn.button("使う ➡", on_click=set_page, args=("pages/6_知的段階_早引き学習指導要領.py",), key="btn_guideline_page")
        with c_pop.popover("📖"):
            st.markdown(manuals["guideline_page"])

    with st.container(border=True):
        st.markdown("### ▶️ 動画ギャラリー")
        st.caption("特別支援教育に関する動画と解説をまとめています。")
        st.button("見る ➡", on_click=set_page, args=("pages/7_動画ギャラリー.py",), key="btn_youtube_gallery")

    with st.container(border=True):
        st.markdown("### 📝 フィードバック")
        st.caption("アプリの改善やご意見をお待ちしています。")
        st.button("送る ➡", on_click=set_page, args=("pages/10_フィードバック.py",), key="btn_feedback")


# --- ▼ 関連ツール＆リンク ▼ ---
st.markdown("<br>", unsafe_allow_html=True)

# リンク集のエリアもglass-containerで囲んで見やすく
st.markdown("""
<div class="glass-container">
    <h3 style="border-bottom:none;">🔗 研究・分析ツール (External Links)</h3>
    <p style="margin-bottom:0;">研究論文作成やデータ分析に活用できる外部ツール集です。</p>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    with st.container(border=True):
        st.markdown("##### 📁 教育・心理分析")
        st.markdown("- [応用行動分析 (ABA)](https://abaapppy-k7um2qki5kggexf8qkfxjc.streamlit.app/)")
        st.markdown("- [機能的行動評価](https://kinoukoudou-ptfpnkq3uqgaorabcyzgf2.streamlit.app/)")

with c2:
    with st.container(border=True):
        st.markdown("##### 📁 統計学分析")
        st.markdown("- [アンケートデータ統計分析](https://annketo12345py-edm3ajzwtsmmuxbm8qbamr.streamlit.app/)")
        st.markdown("- [相関分析](https://soukan-jlhkdhkradbnxssy29aqte.streamlit.app/)")
        st.markdown("- [多変量回帰分析](https://kaikiapp-tjtcczfvlg2pyhd9bjxwom.streamlit.app/)")
        st.markdown("- [t検定](https://tkentei-flhmnqnq6dti6oyy9xnktr.streamlit.app/)")
        st.markdown("- [ロジスティック回帰分析](https://rojisthik-buklkg5zeh6oj2gno746ix.streamlit.app/)")
        st.markdown("- [ノンパラメトリック分析](https://nonparametoric-nkk2awu6yv9xutzrjmrsxv.streamlit.app/)")

st.markdown("---")

# アンケートと注意書きも同様にプレート化
st.markdown("""
<div class="glass-container" style="text-align: center;">
    <h5 style="color: #fff;">🗨️ ご意見・ご感想</h5>
    <p>自立活動の参考指導、各分析ツールにご意見がある方は以下のフォームから送ってください。<br>
    (埼玉県の学校教育関係者のみＳＴアカウントで回答できます)</p>
    <a href="https://docs.google.com/forms/d/1dKzh90OkxMoWDZXV31FgPvXG5EvNlMFOrvSPGvYTSC8/preview" target="_blank" 
       style="display: inline-block; background: #4a90e2; color: white !important; padding: 12px 30px; border-radius: 30px; text-decoration: none; font-weight: bold; margin-top: 15px;">
       アンケートフォームを開く 📝
    </a>
</div>
""", unsafe_allow_html=True)

st.info("""
**【利用上の注意】**
それぞれのアプリに記載してある内容、分析ツールのデータや図、表を外部（研究発表など）で利用する場合は、
管理者(岩槻はるかぜ特別支援学校 小山)までご相談ください。無断での転記・利用を禁じます。
""")