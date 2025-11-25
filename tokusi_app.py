import streamlit as st
from PIL import Image
import base64
import os

# --- 1. ページ設定 ---
st.set_page_config(
    page_title="Mirairo",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSSデザイン (視認性とアニメーション強化) ---
def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = """
    <style>
        /* --- 全体フォント・色設定 --- */
        html, body, [class*="css"], .stMarkdown, .stText, p, div, label, h1, h2, h3, h4, h5, h6 {
            font-family: 'Noto Sans JP', sans-serif !important;
            color: #ffffff !important; /* 文字は強制的に白 */
            text-shadow: 0 2px 4px rgba(0,0,0,0.9) !important; /* 文字の周りに濃い影をつけて見やすく */
        }

        /* --- 背景設定 (画像をかなり薄く) --- */
        [data-testid="stAppViewContainer"] {
            background-color: #000000;
        }
        [data-testid="stAppViewContainer"] > .main {
            /* 黒のカバー率を92%にして画像を薄くする */
            background-image: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-position: center center;
            background-attachment: fixed;
        }
        
        /* --- サイドバー (黒背景ではっきりさせる) --- */
        [data-testid="stSidebar"] {
            background-color: rgba(10, 10, 10, 0.98) !important;
            border-right: 1px solid #333;
        }
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
            text-shadow: none !important;
        }

        /* --- アニメーション (ふわふわ動く) --- */
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-12px); }
            100% { transform: translateY(0px); }
        }
        .floating-element {
            animation: float 5s ease-in-out infinite;
            display: inline-block;
        }

        /* --- Mirairo タイトルデザイン --- */
        .mirairo-header-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            padding: 40px 0;
        }
        .mirairo-title {
            font-size: 4.5rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: 0.05em;
            background: -webkit-linear-gradient(45deg, #fff, #a5b4fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 4px 10px rgba(0,0,0,0.5) !important;
        }
        .mirairo-sub {
            font-size: 1.2rem;
            color: #cbd5e0 !important;
            letter-spacing: 0.1em;
            margin-top: 5px;
            text-align: center;
        }

        /* --- カードデザイン (文字を見やすく) --- */
        div[data-testid="stVerticalBlock"] div.st-emotion-cache-1r6slb0 {
            background-color: rgba(20, 20, 20, 0.6); /* 背景を少し濃く */
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 16px;
            padding: 20px;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        }
        div[data-testid="stVerticalBlock"] div.st-emotion-cache-1r6slb0:hover {
            background-color: rgba(40, 40, 40, 0.8);
            border-color: #4a90e2;
            transform: translateY(-3px);
        }
        
        /* 見出しの色調整 */
        h3 { border-bottom: 1px solid #555 !important; padding-bottom: 10px; }

        /* --- ボタンデザイン --- */
        .stButton > button {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 1px solid #555 !important;
            border-radius: 30px !important;
            padding: 10px 24px !important;
            transition: all 0.3s ease !important;
            font-weight: bold !important;
        }
        .stButton > button:hover {
            border-color: #4a90e2 !important;
            color: #4a90e2 !important;
            background-color: #1a1a1a !important;
            box-shadow: 0 0 15px rgba(74, 144, 226, 0.4);
        }
        
        /* リンクスタイル */
        a { color: #63b3ed !important; font-weight: bold; }
        
        /* フッターの線 */
        .footer-hr {
            border: none;
            height: 1px;
            background: linear-gradient(to right, transparent, #4a90e2, transparent);
            margin: 40px 0;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# CSSを適用
load_css()

# --- 3. マニュアルデータ (元のまま) ---
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

# --- 4. ロジック部分 ---

# ページ遷移関数
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

  
# --- 5. メインコンテンツ (タイトル部分を修正) ---

# ロゴとタイトルを横並びで表示＆アニメーション
col_logo, col_title = st.columns([1, 4])

with col_logo:
    # ロゴ画像の読み込み (mirairo.png が同じフォルダにある想定)
    # なければプレースホルダーを表示
    try:
        st.markdown('<div class="floating-element">', unsafe_allow_html=True)
        st.image("mirairo.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div class="floating-element" style="font-size:80px;">🌟</div>', unsafe_allow_html=True)

with col_title:
    st.markdown("""
        <div class="floating-element" style="width:100%;">
            <h1 class="mirairo-title">Mirairo</h1>
            <div class="mirairo-sub">Data-Driven Education Platform</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.header("ようこそ！")
st.write("""
このアプリは、特別支援教育に関わる先生方をサポートするためのツールです。
子どもたち一人ひとりのニーズに合わせた指導や支援のヒントを見つけたり、
発達段階を記録・分析したり、AIによる計画作成の補助を受けたりすることができます。

**下の各機能やサイドバーのメニューから、利用したい機能を選択してください。**
""")

st.header("各機能の紹介")

# --- 3カラムレイアウト (内容は元のまま) ---
col1, col2, col3 = st.columns(3)

with col1:
    # 1. 指導支援内容
    with st.container(border=True):
        st.markdown("### 📚 指導支援内容")
        st.write("日常生活の困りごとに応じた、具体的な指導・支援のアイデアを検索できます。")
        b_col1, b_col2 = st.columns(2)
        b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/1_指導支援内容.py",), key="btn_guidance", use_container_width=True)
        with b_col2.popover("📖 マニュアル", use_container_width=True):
            st.markdown(manuals["guidance"])

    # 2. 分析方法
    with st.container(border=True):
        st.markdown("### 📈 分析方法")
        st.write("教育学や心理学に基づいた様々な分析方法の解説と、実践で使えるツールを提供します。")
        b_col1, b_col2 = st.columns(2)
        b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/3_分析方法.py",), key="btn_analysis", use_container_width=True)
        with b_col2.popover("📖 マニュアル", use_container_width=True):
            st.markdown(manuals["analysis"])
    
    # 3. 授業カード
    with st.container(border=True):
        st.markdown("### 🃏 授業カードライブラリー") 
        st.write("先生方の授業アイデアを共有・検索できる、視覚的な授業カード集です。")
        b_col1, b_col2 = st.columns(2)
        b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/8_授業カードライブラリー.py",), key="btn_lesson_card_library", use_container_width=True)
        with b_col2.popover("📖 マニュアル", use_container_width=True):
            st.markdown(manuals["lesson_card_library"])

with col2:
    # 4. 発達チャート
    with st.container(border=True):
        st.markdown("### 📊 発達チャート作成")
        st.write("お子さんの発達段階を記録し、レーダーチャートで視覚的に確認・保存できます。")
        b_col1, b_col2 = st.columns(2)
        b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/2_発達チャート.py",), key="btn_chart", use_container_width=True)
        with b_col2.popover("📖 マニュアル", use_container_width=True):
            st.markdown(manuals["chart"])
    
    # 5. AI計画作成
    with st.container(border=True):
        st.markdown("### 🤖 AIによる支援,指導計画作成", unsafe_allow_html=True)
        st.write("フォーム入力で、個別の支援・指導計画のプロンプトを簡単に作成します。", )
        b_col1, b_col2 = st.columns(2)
        b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/4_AIによる支援,指導計画作成.py",), key="btn_plan_creation", use_container_width=True)
        with b_col2.popover("📖 マニュアル", use_container_width=True):
            st.markdown(manuals["plan_creation"])

    # 9. AIによる指導案作成
    with st.container(border=True):
        st.markdown("### 📝 AIによる指導案作成")
        st.write("AIを活用して、Excel形式の学習指導案を半自動で作成・出力します。")
        b_col1, b_col2 = st.columns(2)
        b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/9_AIによる指導案作成.py",), key="btn_lesson_plan_ai", use_container_width=True)
        with b_col2.popover("📖 マニュアル", use_container_width=True):
            st.markdown(manuals["lesson_plan_ai"])

with col3:
    # 6. 学習指導要領
    with st.container(border=True):
        st.markdown("### 📜 知的段階_早引き学習指導要領")
        st.write("学部・段階・教科を選択し、学習指導要領の内容を確認できます。")
        b_col1, b_col2 = st.columns(2)
        b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/6_知的段階_早引き学習指導要領.py",), key="btn_guideline_page", use_container_width=True)
        with b_col2.popover("📖 マニュアル", use_container_width=True):
            st.markdown(manuals["guideline_page"])

    # 7. 動画ギャラリー
    with st.container(border=True):
        st.markdown("### ▶️ 動画ギャラリー")
        st.write("特別支援教育に関する動画と解説をまとめています。")
        st.button("この機能を使う ➡", on_click=set_page, args=("pages/7_動画ギャラリー.py",), key="btn_youtube_gallery", use_container_width=True)

    # 10. フィードバック
    with st.container(border=True):
        st.markdown("### 📝 フィードバック")
        st.write("アプリの改善やご意見をお待ちしています。")
        st.button("この機能を使う ➡", on_click=set_page, args=("pages/10_フィードバック.py",), key="btn_feedback", use_container_width=True)


# --- ▼ 関連ツール＆リンク (元のまま) ▼ ---
st.markdown("<hr class='footer-hr'>", unsafe_allow_html=True)

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

st.markdown("<hr class='footer-hr'>", unsafe_allow_html=True)
st.warning("""
**【利用上の注意】**
それぞれのアプリに記載してある内容、分析ツールのデータや図、表を外部（研究発表など）で利用する場合は、管理者(岩槻はるかぜ特別支援学校 小山)までご相談ください。無断での転記・利用を禁じます。
""")