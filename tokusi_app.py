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

# --- 画像をBase64エンコードする関数 (HTMLで表示するため) ---
def get_img_as_base64(file):
    try:
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# ロゴ画像のパス (同じフォルダにある前提)
logo_path = "mirairo.png"
logo_b64 = get_img_as_base64(logo_path)

# 画像がない場合の代替アイコン
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img">' if logo_b64 else '<div class="logo-placeholder">🌟</div>'


# --- 2. CSSデザイン (視認性と統一感の強化) ---
def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = f"""
    <style>
        /* --- 全体設定 --- */
        html, body, [class*="css"] {{
            font-family: 'Noto Sans JP', sans-serif !important;
            color: #e0e0e0 !important;
        }}

        /* --- 背景設定 (黒ベース) --- */
        [data-testid="stAppViewContainer"] {{
            background-color: #050505;
            background-image: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #000000 100%);
        }}
        [data-testid="stSidebar"] {{
            background-color: #000000;
            border-right: 1px solid #333;
        }}

        /* --- ヘッダーアニメーション (ロゴ+タイトル) --- */
        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}
        
        .header-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 25px;
            padding: 60px 0 40px 0;
            animation: float 6s ease-in-out infinite; /* 全体がゆらゆら動く */
        }}
        
        .logo-img {{
            width: 100px;
            height: auto;
            object-fit: contain;
            filter: drop-shadow(0 0 10px rgba(255,255,255,0.3));
        }}
        
        .logo-placeholder {{
            font-size: 80px;
        }}

        .title-box {{
            display: flex;
            flex-direction: column;
        }}
        
        .main-title {{
            font-size: 5rem;
            font-weight: 900;
            line-height: 1;
            margin: 0;
            background: linear-gradient(135deg, #fff 0%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
            text-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        
        .sub-title {{
            font-size: 1.1rem;
            color: #94a3b8;
            letter-spacing: 0.2em;
            margin-top: 5px;
            font-weight: 400;
        }}

        /* --- 機能カード (線引きを明確に) --- */
        [data-testid="stBorderContainer"] {{
            background-color: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important; /* 白っぽい薄い線 */
            border-radius: 16px !important;
            padding: 20px !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            transition: border-color 0.3s, transform 0.3s;
        }}
        
        /* ホバー時に枠線を光らせる */
        [data-testid="stBorderContainer"]:hover {{
            border-color: #4a90e2 !important; /* 青く光る */
            box-shadow: 0 0 15px rgba(74, 144, 226, 0.2);
            transform: translateY(-2px);
        }}

        /* --- 見出しデザイン --- */
        h3 {{
            color: #fff !important;
            font-weight: 700 !important;
            border-bottom: 1px solid #333;
            padding-bottom: 10px;
            margin-bottom: 15px !important;
        }}

        /* --- ボタンデザイン --- */
        .stButton > button {{
            width: 100%;
            background: transparent !important;
            border: 1px solid #4a90e2 !important;
            color: #4a90e2 !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
        }}
        .stButton > button:hover {{
            background: #4a90e2 !important;
            color: #fff !important;
            box-shadow: 0 0 15px rgba(74, 144, 226, 0.6);
        }}

        /* --- マニュアル(Expander)のデザイン --- */
        .streamlit-expanderHeader {{
            background-color: rgba(255,255,255,0.05) !important;
            border-radius: 8px !important;
            color: #fff !important;
        }}
        
        /* --- リンクのデザイン --- */
        a {{
            color: #63b3ed !important;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
            color: #90cdf4 !important;
        }}

        /* フッター線 */
        hr {{
            border-color: #333;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# CSS適用
load_css()

# --- 3. マニュアルデータ (内容はそのまま) ---
manuals = {
    "guidance": """
    ### 📚 指導支援内容 マニュアル
    このページでは、お子さんの日常生活の困りごとに応じた、具体的な指導・支援のアイデアを検索することができます。
    #### **使い方**
    1.  **3つのステップで項目を選択**
        -   画面に表示される3つのドロップダウンメニューを左から順番に選択していきます。
    2.  **指導・支援内容の表示**
        -   3つの項目を選択し終えたら、**「💡 適した指導・支援を表示」** ボタンをクリックします。
    3.  **結果の確認**
        -   ボタンの下に、選択した項目に対する指導・支援の具体的な内容が表示されます。
    """,
    "chart": """
    ### 📊 発達チャート作成 マニュアル
    お子さんの現在の発達段階を記録し、レーダーチャートで視覚的に確認したり、次のステップの目安をまとめた資料を作成・保存したりすることができます。
    #### **使い方**
    1.  **発達段階の入力**
        -   「認知力・操作」「言語理解」など、12のカテゴリーが表示されます。
    2.  **目安の確認（任意）**
        -   各カテゴリーの選択肢の下にある **「▼ 目安を見る」** をクリックすると目安が表示されます。
    3.  **チャートの作成とデータ書き込み**
        -   すべてのカテゴリーを選択し終えたら、フォームの一番下にある **「📊 チャートを作成して書き込む」** ボタンをクリックします。
    """,
    "analysis": """
    ### 📈 分析方法 マニュアル
    特別支援教育で活用できる様々な分析方法や療法について、その概要や関連ツールを調べることができます。
    #### **使い方**
    **方法A：療法・分析法から直接探す**
    1.  サイドバー（メニュー）から療法・分析法（ABA、CBTなど）を選択します。
    **方法B：お子さんの実態から探す**
    1.  メインエリア上部のドロップダウンメニューから、お子さんの状況を選択します。
    """,
    "plan_creation": """
    ### 🤖 計画作成サポート マニュアル
    個別の支援計画や指導計画の文章を作成する際に、生成AI（ChatGPTなど）に依頼するための**「命令文（プロンプト）」**を簡単に作成できるツールです。
    #### **使い方**
    1.  **プロンプトの種類を選択**
        -   プランA・B用、評価用、総合所見用などから選択します。
    2.  **情報を入力**
        -   お子さんの実態や課題、参考情報を入力します。
    3.  **プロンプトを生成**
        -   **「プロンプトを生成」** ボタンをクリックし、表示された文面をコピーします。
    """,
    "lesson_plan_ai": """
    ### 📝 AIによる指導案作成 マニュアル
    学習指導案を「基本情報の入力」だけで、ChatGPT等のAIを使って自動生成し、Excelファイルとして出力するツールです。
    #### **使い方**
    1.  **基本情報の入力**
        -   学部学年、教科単元、日時などを入力します。
    2.  **プロンプトを作成**
        -   ボタンを押して、AIへの命令文（プロンプト）を生成し、コピーします。
    3.  **AIで回答を作成**
        -   コピーした命令文をChatGPTやGeminiに貼り付けます。
    4.  **Excel出力**
        -   AIの回答をアプリの入力欄に貼り付け、「Excel作成実行」ボタンを押します。
    """,
    "guideline_page": """
    ### 📜 知的段階（学習指導要領） マニュアル
    学習指導要領の中から、必要な部分を素早く探し出して閲覧することができます。
    #### **使い方**
    1.  **項目を選択**
        -   学部、障害種別（段階）、教科を選択します。
    2.  **内容の表示**
        -   **「表示する」** ボタンをクリックすると、該当する学習指導要領の内容が表示されます。
    """,
    "lesson_card_library": """
    ### 🃏 授業カードライブラリー マニュアル
    先生方が実践している授業のアイデアをカード形式で共有・検索できる機能です。
    #### **使い方**
    1.  **検索・絞り込み**
        -   検索バーやハッシュタグ（#高等部 #買い物など）を使って授業を探せます。
    2.  **一覧表示**
        -   授業のタイトル、ねらい、写真などがカード形式で一覧表示されます。
    """
}

# --- 4. ページ遷移ロジック ---
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

# ▼ ヘッダーエリア (HTML/CSSで一体化させて動かす)
# 画像と文字を一つのdivに入れ、CSSの animation: float で一緒に動かします。
st.markdown(f"""
    <div class="header-container">
        {logo_html}
        <div class="title-box">
            <h1 class="main-title">Mirairo</h1>
            <div class="sub-title">Data-Driven Education Platform</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 概要テキスト
st.write("""
**Mirairo（ミライロ）へようこそ。**  
このプラットフォームは、特別支援教育に関わる先生方をサポートするために開発されました。  
「経験」や「勘」にデータという「根拠」をプラスし、指導案作成から分析までを一元化します。
""")

st.divider()
st.markdown("### 📂 各機能の紹介")

# --- 3カラムレイアウト (カードデザイン適用) ---
col1, col2, col3 = st.columns(3)

with col1:
    # 1. 指導支援内容
    with st.container(border=True):
        st.markdown("### 📚 指導支援内容")
        st.caption("困りごとに応じた指導・支援のアイデアを検索")
        col_btn, col_pop = st.columns([1, 1])
        col_btn.button("使う ➡", on_click=set_page, args=("pages/1_指導支援内容.py",), key="btn_guidance", use_container_width=True)
        with col_pop.popover("📖 説明"):
            st.markdown(manuals["guidance"])

    # 2. 分析方法
    with st.container(border=True):
        st.markdown("### 📈 分析方法")
        st.caption("教育学・心理学に基づいた分析手法の解説")
        col_btn, col_pop = st.columns([1, 1])
        col_btn.button("使う ➡", on_click=set_page, args=("pages/3_分析方法.py",), key="btn_analysis", use_container_width=True)
        with col_pop.popover("📖 説明"):
            st.markdown(manuals["analysis"])
    
    # 3. 授業カード
    with st.container(border=True):
        st.markdown("### 🃏 授業カード") 
        st.caption("授業アイデアを共有・検索できるライブラリ")
        col_btn, col_pop = st.columns([1, 1])
        col_btn.button("使う ➡", on_click=set_page, args=("pages/8_授業カードライブラリー.py",), key="btn_lesson_card_library", use_container_width=True)
        with col_pop.popover("📖 説明"):
            st.markdown(manuals["lesson_card_library"])

with col2:
    # 4. 発達チャート
    with st.container(border=True):
        st.markdown("### 📊 発達チャート")
        st.caption("発達段階を記録し、レーダーチャートで可視化")
        col_btn, col_pop = st.columns([1, 1])
        col_btn.button("使う ➡", on_click=set_page, args=("pages/2_発達チャート.py",), key="btn_chart", use_container_width=True)
        with col_pop.popover("📖 説明"):
            st.markdown(manuals["chart"])
    
    # 5. AI計画作成
    with st.container(border=True):
        st.markdown("### 🤖 AI計画作成")
        st.caption("個別の支援・指導計画プロンプトを作成")
        col_btn, col_pop = st.columns([1, 1])
        col_btn.button("使う ➡", on_click=set_page, args=("pages/4_AIによる支援,指導計画作成.py",), key="btn_plan_creation", use_container_width=True)
        with col_pop.popover("📖 説明"):
            st.markdown(manuals["plan_creation"])

    # 9. AIによる指導案作成
    with st.container(border=True):
        st.markdown("### 📝 AI指導案作成")
        st.caption("基本情報から学習指導案を自動生成・出力")
        col_btn, col_pop = st.columns([1, 1])
        col_btn.button("使う ➡", on_click=set_page, args=("pages/9_AIによる指導案作成.py",), key="btn_lesson_plan_ai", use_container_width=True)
        with col_pop.popover("📖 説明"):
            st.markdown(manuals["lesson_plan_ai"])

with col3:
    # 6. 学習指導要領
    with st.container(border=True):
        st.markdown("### 📜 指導要領早引き")
        st.caption("学部・段階ごとの内容を素早く検索")
        col_btn, col_pop = st.columns([1, 1])
        col_btn.button("使う ➡", on_click=set_page, args=("pages/6_知的段階_早引き学習指導要領.py",), key="btn_guideline_page", use_container_width=True)
        with col_pop.popover("📖 説明"):
            st.markdown(manuals["guideline_page"])

    # 7. 動画ギャラリー
    with st.container(border=True):
        st.markdown("### ▶️ 動画ギャラリー")
        st.caption("特別支援教育に関する動画と解説まとめ")
        st.button("見る ➡", on_click=set_page, args=("pages/7_動画ギャラリー.py",), key="btn_youtube_gallery", use_container_width=True)

    # 10. フィードバック
    with st.container(border=True):
        st.markdown("### 📝 フィードバック")
        st.caption("アプリの改善要望やバグ報告はこちら")
        st.button("送る ➡", on_click=set_page, args=("pages/10_フィードバック.py",), key="btn_feedback", use_container_width=True)


# --- ▼ 関連ツール＆リンク ▼ ---
st.markdown("<hr class='footer-hr'>", unsafe_allow_html=True)

st.header("🔗 研究・分析ツール (External Links)")
st.write("研究論文やデータ分析に活用できる外部ツール集です。")

c1, c2 = st.columns(2)
with c1:
    st.markdown("##### 📁 教育・心理分析")
    st.markdown("- [応用行動分析 (ABA)](https://abaapppy-k7um2qki5kggexf8qkfxjc.streamlit.app/)")
    st.markdown("- [機能的行動評価](https://kinoukoudou-ptfpnkq3uqgaorabcyzgf2.streamlit.app/)")

with c2:
    st.markdown("##### 📁 統計学分析")
    st.markdown("- [アンケートデータ統計分析](https://annketo12345py-edm3ajzwtsmmuxbm8qbamr.streamlit.app/)")
    st.markdown("- [相関分析](https://soukan-jlhkdhkradbnxssy29aqte.streamlit.app/)")
    st.markdown("- [多変量回帰分析](https://kaikiapp-tjtcczfvlg2pyhd9bjxwom.streamlit.app/)")
    st.markdown("- [t検定](https://tkentei-flhmnqnq6dti6oyy9xnktr.streamlit.app/)")
    st.markdown("- [ロジスティック回帰分析](https://rojisthik-buklkg5zeh6oj2gno746ix.streamlit.app/)")
    st.markdown("- [ノンパラメトリック分析](https://nonparametoric-nkk2awu6yv9xutzrjmrsxv.streamlit.app/)")

st.markdown("<br>", unsafe_allow_html=True)
st.info("""
**【利用上の注意】**
それぞれのアプリに記載してある内容、分析ツールのデータや図、表を外部（研究発表など）で利用する場合は、
管理者(岩槻はるかぜ特別支援学校 小山)までご相談ください。無断での転記・利用を禁じます。
""")