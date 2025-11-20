# page_title: TOPページ
import streamlit as st

st.set_page_config(
    page_title="TOPページ",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ▼ 共通CSSの読み込み（修正版） ▼ ---
def load_css():
    """カスタムCSSを読み込む関数"""
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    css = """
    <style>
        /* --- 全体フォント設定 --- */
        body {
            font-family: 'Noto Sans JP', sans-serif !important;
        }
        /* Streamlitの全てのテキスト要素にフォントを適用 */
        html, body, [class*="css"] {
            font-family: 'Noto Sans JP', sans-serif !important;
        }

        /* --- カラーパレット変数 --- */
        :root {
            --primary-color: #6a1b9a; /* 深い紫 */
            --secondary-color: #ab47bc; /* 少し明るい紫 */
            --accent-color: #4a90e2; /* 鮮やかな青 */
            --text-color-dark: #2c3e50;
            --text-color-light: #34495e;
            --bg-light: rgba(240, 242, 246, 0.95);
            --card-bg: rgba(255, 255, 255, 0.98);
            --border-light: #e0e0e0;
        }

        /* --- 背景画像の設定 --- */
        [data-testid="stAppViewContainer"] > .main {
            background-image: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        /* サイドバーの背景を少し透過 */
        [data-testid="stSidebar"] {
            background-color: var(--bg-light);
        }
        
        /* --- ▼ サイドバーの閉じるボタンをカスタマイズ ▼ --- */
        [data-testid="stSidebarNavCollapseButton"] {
            position: relative !important;
            width: 2.2rem !important; /* 少し大きく */
            height: 2.2rem !important; /* 少し大きく */
            top: 10px !important; /* 上から少し離す */
            left: 10px !important; /* 左から少し離す */
            border-radius: 50% !important; /* 丸く */
            background-color: rgba(255,255,255,0.7) !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        [data-testid="stSidebarNavCollapseButton"] * {
            display: none !important;
            visibility: hidden !important;
        }
        [data-testid="stSidebarNavCollapseButton"]::before {
            content: '«' !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            position: absolute !important;
            width: 100% !important;
            height: 100% !important;
            top: 0 !important;
            left: 0 !important;
            font-size: 20px !important; /* フォントサイズ調整 */
            font-weight: bold !important;
            color: var(--primary-color) !important;
            transition: background-color 0.2s, color 0.2s, transform 0.2s !important;
            border-radius: 50% !important;
        }
        [data-testid="stSidebarNavCollapseButton"]:hover::before {
            background-color: var(--primary-color) !important;
            color: white !important;
            transform: scale(1.1); /* ホバーで少し拡大 */
        }
        /* --- ▲ サイドバーのカスタマイズここまで ▲ --- */


        /* --- 見出しのスタイル --- */
        h1 {
            color: var(--primary-color);
            text-align: center;
            padding-bottom: 25px; /* 余白を少し増やす */
            font-weight: 700; /* より太く */
            font-size: 2.8em; /* サイズを大きく */
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        h2 {
            color: var(--text-color-dark);
            border-left: 8px solid var(--primary-color); /* 紫のアクセントを太く */
            padding-left: 15px; /* 余白を増やす */
            margin-top: 50px; /* 上部余白を増やす */
            font-weight: 600;
            font-size: 1.8em;
        }
        h3 {
            color: var(--text-color-light);
            border-bottom: 2px solid var(--secondary-color); /* 紫のアクセント */
            padding-bottom: 10px;
            margin-top: 35px;
            font-weight: 500;
            font-size: 1.4em;
        }

        /* --- カードデザイン (st.container(border=True)のスタイル) --- */
        div[data-testid="stVerticalBlock"] div.st-emotion-cache-1r6slb0 { /* Streamlitのカードコンテナセレクタ */
            background-color: var(--card-bg);
            border: 1px solid var(--border-light);
            border-radius: 18px; /* 角を少し丸く */
            padding: 1.8em 1.8em; /* 内側の余白を増やす */
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); /* 影を強調 */
            transition: box-shadow 0.3s ease-in-out, transform 0.3s ease-in-out;
            margin-bottom: 25px; /* カード間の余白を増やす */
        }
        div[data-testid="stVerticalBlock"] div.st-emotion-cache-1r6slb0:hover {
            box-shadow: 0 12px 25px rgba(var(--primary-color-rgb, 106, 27, 154), 0.2); /* ホバー時の影をブランドカラーに */
            transform: translateY(-8px); /* ホバーで少し浮き上がる */
        }
        /* カード内の見出し調整 */
        div[data-testid="stVerticalBlock"] div.st-emotion-cache-1r6slb0 h3 {
            border-bottom: none;
            padding-bottom: 0;
            margin-top: 0;
            color: var(--primary-color);
            font-size: 1.5em; /* カード内のH3を調整 */
            font-weight: 600;
            text-align: center; /* カード内のH3を中央寄せに */
            margin-bottom: 15px;
        }
        div[data-testid="stVerticalBlock"] div.st-emotion-cache-1r6slb0 p {
            font-size: 0.95em;
            line-height: 1.6;
            color: var(--text-color-light);
            text-align: center; /* カード内のテキストも中央寄せ */
        }
        
        /* --- ボタンのスタイル --- */
        .stButton>button {
            border: 2px solid var(--accent-color);
            border-radius: 30px; /* より丸く */
            color: var(--accent-color);
            background-color: #ffffff;
            padding: 12px 28px; /* パディングを増やす */
            font-weight: bold;
            font-size: 1.05em; /* フォントサイズを少し大きく */
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
        .stButton>button:hover {
            border-color: var(--primary-color); /* ホバーで紫に */
            color: white;
            background-color: var(--primary-color);
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(var(--primary-color-rgb, 106, 27, 154), 0.3);
        }
        /* Primaryボタン */
        .stButton>button[kind="primary"] {
            background-color: var(--accent-color);
            color: white;
            border: none;
            box-shadow: 0 4px 8px rgba(var(--accent-color-rgb, 74, 144, 226), 0.2);
        }
        .stButton>button[kind="primary"]:hover {
            background-color: var(--primary-color); /* ホバーで紫に */
            border-color: var(--primary-color);
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(var(--primary-color-rgb, 106, 27, 154), 0.3);
        }

        /* --- st.infoのカスタムスタイル --- */
        .st-emotion-cache-1wivap1 {
             background-color: rgba(232, 245, 253, 0.8); /* 少し透過度を調整 */
             border-left: 6px solid var(--accent-color);
             border-radius: 10px;
             padding: 1em 1.5em;
             box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* st.expanderのデフォルトアイコン（文字化けしているもの）を非表示にする */
        [data-testid="stExpanderToggleIcon"] {
            display: none;
        }

        /* --- フッターの区切り線 --- */
        .footer-hr {
            border: none;
            height: 4px; /* 太く */
            background: linear-gradient(to right, var(--accent-color), var(--primary-color)); /* グラデーション */
            margin-top: 50px; /* 余白を増やす */
            margin-bottom: 30px;
            border-radius: 2px;
        }

        /* 関連ツール＆リンクのカードデザイン */
        .related-tools-card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-light);
            border-radius: 18px;
            padding: 1.5em;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
            margin-bottom: 20px;
            transition: box-shadow 0.3s ease-in-out, transform 0.3s ease-in-out;
        }
        .related-tools-card:hover {
            box-shadow: 0 10px 20px rgba(var(--accent-color-rgb, 74, 144, 226), 0.2);
            transform: translateY(-5px);
        }
        .related-tools-card h5 {
            color: var(--primary-color);
            font-weight: 600;
            font-size: 1.3em;
            margin-bottom: 15px;
            border-bottom: 1px dashed var(--border-light);
            padding-bottom: 10px;
        }
        .related-tools-card .st-emotion-cache-ch5fgy { /* st.page_linkのコンテナ */
            margin-bottom: 8px;
        }
        .related-tools-card .st-emotion-cache-ch5fgy a { /* st.page_linkのリンクテキスト */
            color: var(--text-color-light);
            text-decoration: none;
            font-weight: 400;
            transition: color 0.2s;
        }
        .related-tools-card .st-emotion-cache-ch5fgy a:hover {
            color: var(--primary-color);
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
# --- ▲ 共通CSSの読み込み ▲ ---

# --- マニュアルのテキストデータ ---
manuals = {
    "guidance": """
    ### 📚 指導支援内容 マニュアル
    このページでは、お子さんの日常生活の困りごとに応じた、具体的な指導・支援のアイデアを検索することができます。
    #### **使い方**
    1.  **3つのステップで項目を選択**
        -   画面に表示される3つのドロップダウンメニューを左から順番に選択していきます。
        -   **ステップ1**で大まかなカテゴリー（例：「コミュニケーション」）を選ぶと、**ステップ2**でより具体的な項目（例：「要求の伝え方」）が選べるようになります。同様に**ステップ3**でさらに詳細な内容を選択します。
    2.  **指導・支援内容の表示**
        -   3つの項目を選択し終えたら、**「💡 適した指導・支援を表示」** ボタンをクリックします。
    3.  **結果の確認**
        -   ボタンの下に、選択した項目に対する指導・支援の具体的な内容が表示されます。
        -   内容はいくつかの項目に分かれており、タイトルをクリック（タップ）すると詳細な説明が開きます。
    """,
    "chart": """
    ### 📊 発達チャート作成 マニュアル
    お子さんの現在の発達段階を記録し、レーダーチャートで視覚的に確認したり、次のステップの目安をまとめた資料を作成・保存したりすることができます。
    #### **使い方**
    1.  **発達段階の入力**
        -   「認知力・操作」「言語理解」など、12のカテゴリーが表示されます。
        -   それぞれのカテゴリーについて、現在の状況に最も近い発達段階の選択肢（ラジオボタン）をクリックしてチェックを入れます。
    2.  **目安の確認（任意）**
        -   各カテゴリーの選択肢の下にある **「▼ 目安を見る」** をクリックすると、それぞれの発達段階でどのようなことができるかの目安が表示されます。
    3.  **チャートの作成とデータ書き込み**
        -   すべてのカテゴリーを選択し終えたら、フォームの一番下にある **「📊 チャートを作成して書き込む」** ボタンをクリックします。
        -   これにより、入力されたデータがGoogleスプレッドシートに送信され、自動的にチャートが更新されます。
    4.  **結果の確認と保存**
        -   **「🌐 スプレッドシートでチャートを確認」**：ブラウザでスプレッドシートを開きます。
        -   **「💾 Excel形式でダウンロード」**：入力内容を含むファイルをダウンロードします。
    """,
    "analysis": """
    ### 📈 分析方法 マニュアル
    特別支援教育で活用できる様々な分析方法や療法について、その概要や関連ツールを調べることができます。
    #### **使い方**
    **方法A：療法・分析法から直接探す**
    1.  サイドバー（メニュー）から療法・分析法（ABA、CBTなど）を選択します。
    2.  知りたい項目のラジオボタンをクリックすると、その解説が表示されます。
    **方法B：お子さんの実態から探す**
    1.  メインエリア上部のドロップダウンメニューから、お子さんの状況を選択します。
    2.  有効とされる療法・分析法のボタンが表示されるので、クリックして解説を読みます。
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
    4.  **生成AIで文章を作成**
        -   ChatGPTなどを開き、プロンプトを貼り付けて文章を生成させます。
    """,
    "lesson_plan_ai": """
    ### 📝 AIによる指導案作成 マニュアル
    学習指導案を「基本情報の入力」だけで、ChatGPT等のAIを使って自動生成し、Excelファイルとして出力するツールです。
    #### **使い方**
    1.  **基本情報の入力**
        -   学部学年、教科単元、日時などを入力します。目標や評価基準は空欄でもAIが補完します。
    2.  **プロンプトを作成**
        -   ボタンを押して、AIへの命令文（プロンプト）を生成し、コピーします。
    3.  **AIで回答を作成**
        -   コピーした命令文をChatGPTやGeminiに貼り付けます。
        -   AIが生成したJSONコード（プログラム用データ）をコピーします。
    4.  **Excel出力**
        -   AIの回答をアプリの入力欄に貼り付け、「Excel作成実行」ボタンを押します。
        -   完成した指導案ファイル（Excel）がダウンロードされます。
    """,
    "guideline_page": """
    ### 📜 知的段階（学習指導要領） マニュアル
    学習指導要領の中から、必要な部分を素早く探し出して閲覧することができます。
    #### **使い方**
    1.  **項目を選択**
        -   学部、障害種別（段階）、教科を選択します。
    2.  **内容の表示**
        -   **「表示する」** ボタンをクリックすると、該当する学習指導要領の内容（目標、各段階の指導内容など）が表示されます。
    """,
    "lesson_card_library": """
    ### 🃏 授業カードライブラリー マニュアル
    先生方が実践している授業のアイデアをカード形式で共有・検索できる機能です。
    #### **使い方**
    1.  **検索・絞り込み**
        -   検索バーやハッシュタグ（#高等部 #買い物など）を使って授業を探せます。
    2.  **一覧表示**
        -   授業のタイトル、ねらい、写真などがカード形式で一覧表示されます。
    3.  **詳細ページの閲覧**
        -   カードをクリックすると詳細が表示され、指導略案PDFや動画リンクなどを確認できます。
    """
}


# CSSを適用
load_css()

# ページ遷移を管理するための関数
def set_page(page):
    st.session_state.page_to_visit = page


# st.session_stateをチェックしてページ遷移を実行
if "page_to_visit" in st.session_state:
    page = st.session_state.page_to_visit
    del st.session_state.page_to_visit
    st.switch_page(page)

    
# st.session_stateの初期化
if 'current_lesson_id' not in st.session_state:
    st.session_state.current_lesson_id = None
if 'show_all_flow' not in st.session_state: 
    st.session_state.show_all_flow = False
if 'show_create_form' not in st.session_state:
    st.session_state.show_create_form = False

  
# --- メインコンテンツ ---
st.title("🌟 特別支援教育サポートアプリ")

# メインイメージ
st.image("https://i.imgur.com/AbUxfxP.png", caption="子どもたちの「できた！」を支援する", use_container_width=True)

st.header("ようこそ！")
st.write("""
このアプリは、特別支援教育に関わる先生方をサポートするためのツールです。
子どもたち一人ひとりのニーズに合わせた指導や支援のヒントを見つけたり、
発達段階を記録・分析したり、AIによる計画作成の補助を受けたりすることができます。

**下の各機能やサイドバーのメニューから、利用したい機能を選択してください。**
""")

st.header("各機能の紹介")

# --- 3カラムレイアウト ---
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
    
    # 5. AI計画作成 (プロンプト作成)
    with st.container(border=True):
        st.markdown("### 🤖 AIによる支援,指導計画作成", unsafe_allow_html=True)
        st.write("フォーム入力で、個別の支援・指導計画のプロンプトを簡単に作成します。", )
        b_col1, b_col2 = st.columns(2)
        b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/4_AIによる支援,指導計画作成.py",), key="btn_plan_creation", use_container_width=True)
        with b_col2.popover("📖 マニュアル", use_container_width=True):
            st.markdown(manuals["plan_creation"])

    # 9. AIによる指導案作成 (NEW!)
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

    # 10. フィードバック (UPDATED!)
    with st.container(border=True):
        st.markdown("### 📝 フィードバック")
        st.write("アプリの改善やご意見をお待ちしています。")
        st.button("この機能を使う ➡", on_click=set_page, args=("pages/10_フィードバック.py",), key="btn_feedback", use_container_width=True)


# --- ▼ 関連ツール＆リンク ▼ ---
st.markdown("<hr class='footer-hr'>", unsafe_allow_html=True)

st.header("関連ツール＆リンク")
c1, c2 = st.columns(2)
with c1:
    #st.markdown('<div class="related-tools-card">', unsafe_allow_html=True) 
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
st.markdown('</div>', unsafe_allow_html=True) # カードの閉じタグ

st.markdown("<hr class='footer-hr'>", unsafe_allow_html=True)
st.warning("""
**【利用上の注意】**
それぞれのアプリに記載してある内容、分析ツールのデータや図、表を外部（研究発表など）で利用する場合は、管理者(岩槻はるかぜ特別支援学校 小山)までご相談ください。無断での転記・利用を禁じます。
""")