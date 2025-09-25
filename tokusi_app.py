import streamlit as st
import json
from streamlit_lottie import st_lottie
import time # time.sleep を使用するためにインポート

# --- ▼ 共通CSSの読み込み（変更なし） ▼ ---
def load_css():
    """カスタムCSSを読み込む関数"""
    css = """
    <style>
        /* --- 背景画像の設定 --- */
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
                /* --- ▼ サイドバーの閉じるボタンをカスタマイズ（最終版）▼ --- */
        [data-testid="stSidebarNavCollapseButton"] {
            position: relative !important;
            width: 2rem !important;
            height: 2rem !important;
        }
        /* 元のアイコンを完全に非表示にする */
        [data-testid="stSidebarNavCollapseButton"] * {
            display: none !important;
            visibility: hidden !important;
        }
        /* カスタムアイコン「«」を疑似要素として追加 */
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
            font-size: 24px !important;
            font-weight: bold !important;
            color: #31333F !important;
            transition: background-color 0.2s, color 0.2s !important;
            border-radius: 0.5rem;
        }
        [data-testid="stSidebarNavCollapseButton"]:hover::before {
            background-color: #F0F2F6 !important;
            color: #8A2BE2 !important;
        }
        /* --- ▲ サイドバーのカスタマイズここまで ▲ --- */


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
        .st-emotion-cache-1wivap1 {
             background-color: rgba(232, 245, 253, 0.7);
             border-left: 5px solid #4a90e2;
             border-radius: 8px;
        }
        
        /* st.expanderのデフォルトアイコン（文字化けしているもの）を非表示にする */
        [data-testid="stExpanderToggleIcon"] {
            display: none;
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

# --- マニュアルのテキストデータ（変更なし） ---
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
        -   内容によっては、支援のイメージがしやすいように関連する教材などの画像が表示されることもあります。
    """,
    "chart": """
    ### 📊 発達チャート作成 マニュアル
    お子さんの現在の発達段階を記録し、レーダーチャートで視覚的に確認したり、次のステップの目安をまとめた資料を作成・保存したりすることができます。
    #### **使い方**
    1.  **発達段階の入力**
        -   「認知力・操作」「言語理解」など、12のカテゴリーが表示されます。
        -   それぞれのカテゴリーについて、現在の状況に最も近い発達段階の選択肢（ラジオボタン）をクリックしてチェックを入れます。
    2.  **目安の確認（任意）**
        -   各カテゴリーの選択肢の下にある **「▼ 目安を見る」** をクリックすると、それぞれの発達段階でどのようなことができるかの目安が表示されます。選択に迷った際にご活用ください。
    3.  **チャートの作成とデータ書き込み**
        -   すべてのカテゴリーを選択し終えたら、フォームの一番下にある **「📊 チャートを作成して書き込む」** ボタンをクリックします。
        -   これにより、入力されたデータがGoogleスプレッドシートに送信され、自動的にチャートが更新されます。
    4.  **結果の確認と保存**
        -   処理が完了すると、画面下部に結果エリアが表示されます。
        -   **「🌐 スプレッドシートでチャートを確認」** ボタン：クリックすると、更新されたレーダーチャートや詳細なデータが記録されたGoogleスプレッドシートをブラウザで開きます。
        -   **「💾 Excel形式でダウンロード」** ボタン：クリックすると、チャートや入力内容を含むファイルがExcel形式でダウンロード用に生成されます。生成が終わると表示される **「🔽 ダウンロード準備完了」** ボタンを押して、ご自身のPCに保存してください。
    """,
    "analysis": """
    ### 📈 分析方法 マニュアル
    特別支援教育で活用できる様々な分析方法や療法について、その概要や関連ツールを調べることができます。
    #### **使い方**
    このページでは、2つの方法で情報を探すことができます。
    **方法A：療法・分析法から直接探す**
    1.  画面の左側にあるサイドバー（メニュー）に、様々な療法・分析法（ABA、CBTなど）が一覧で表示されています。
    2.  知りたい項目のラジオボタンをクリックすると、画面右側のメインエリアにその解説が表示されます。
    **方法B：お子さんの実態から探す**
    1.  メインエリア上部にある **「児童・生徒の実態から探す」** の下のドロップダウンメニューから、お子さんの状況に最も近いものを選択します（例：「対人関係が苦手」）。
    2.  選択すると、その実態に対して有効とされる療法・分析法のボタンが下に表示されます。
    3.  知りたい療法・分析法のボタンをクリックすると、その下に詳しい解説が表示されます。
    #### **表示される内容**
    -   各療法・分析法の基本的な考え方や、どのようなお子さんに有効かなどの解説が読めます。
    -   内容によっては、参考となる画像や、すぐに使えるオンライン分析ツール（統計学やアンケート分析、応用行動分析など）へのリンク、参考文献などが表示されることもあります。
    """,
    "plan_creation": """
    ### 🤖 計画作成サポート マニュアル
    個別の支援計画や指導計画の文章を作成する際に、生成AI（ChatGPTなど）に依頼するための**「命令文（プロンプト）」**を簡単に作成できるツールです。
    #### **使い方**
    1.  **プロンプトの種類を選択**
        -   このページには、作成したい文章の種類に応じて5つのプロンプト生成フォームがあります。
        -   **プロンプト①〜③**は、プランAやプランBの作成に適しています。プロンプト①でAIが生成した答えを、プロンプト②の入力欄に貼り付けて使うなど、順番に活用すると効果的です。
        -   **プロンプト④**は、教科ごとの評価（振り返り文）を作成するのに役立ちます。
        -   **プロンプト⑤**は、前期や後期の総合所見を作成するために使います。
    2.  **情報を入力**
        -   各フォームのテキストエリアに、お子さんの実態や課題、参考となる資料の内容などを入力します。
    3.  **プロンプトを生成**
        -   入力が終わったら、**「プロンプトを生成」** ボタンをクリックします。
        -   ボタンの下に、AIへの命令文（プロンプト）が整形されて表示されます。
    4.  **生成AIで文章を作成**
        -   表示されたプロンプトの右上にあるコピーボタンで全文をコピーします。
        -   ページ上部にある **「ChatGPT を開いて文章作成を始める ↗」** ボタンなどをクリックしてChatGPTを開き、コピーしたプロンプトを貼り付けて送信します。
        -   AIが計画書のたたき台となる文章を生成します。
    **【重要】**
    このツールはAIへの命令文を作る補助をするものです。生成された文章はあくまで **たたき台** として扱い、必ずご自身の専門的な知見に基づいて内容の修正・追記を行ってください。
    """,
    "guideline_page": """
    ### 📜 知的段階（学習指導要領） マニュアル
    学習指導要領の中から、必要な部分を素早く探し出して閲覧することができます。
    #### **使い方**
    1.  **3つのステップで項目を選択**
        -   **「1. 学部を選択」** で「小学部」または「中学部」を選びます。
        -   **「2. 段階（障害種別）を選択」** で、「知的障害者」またはそれ以外の障害種別を選びます。
        -   **「知的障害者」を選んだ場合のみ、「3. 教科を選択」** のメニューが表示されますので、見たい教科を選んでください。
    2.  **内容の表示**
        -   項目を選択し終えたら、**「表示する」** ボタンをクリックします。
    3.  **結果の確認**
        -   ボタンの下に、指定した条件に該当する学習指導要領の内容が表示されます。
        -   内容は「目標」「各段階」「指導計画の作成と内容の取扱い」などに整理されて表示されます。
        -   「各段階」の内容はタブ形式で切り替えて閲覧できます。
    """,
    "lesson_card_library": """
    ### 🃏 授業カードライブラリー マニュアル
    先生方が実践している授業のアイデアをカード形式で共有・検索できる機能です。
    A4縦をスマホで見やすいイメージに圧縮し、必要な情報が「見た瞬間にわかる」工夫がされています。
    #### **使い方**
    1.  **検索・絞り込み**
        -   画面上部の検索バーやタグフィルターを使って、興味のある授業カードを探します。
        -   #高等部 #知的中度 #買い物 など、ハッシュタグ形式で絞り込みが可能です。
    2.  **授業カードの一覧表示**
        -   Pinterestのようなカード形式で、授業の全体像が一覧で表示されます。
        -   各カードには、タイトル、ねらい、対象、所要時間、工夫のポイント、ハッシュタグなどが簡潔にまとめられています。
        -   活動中の写真や教材の画像も表示され、視覚的に内容を把握できます。
    3.  **詳細ページの閲覧**
        -   気になる授業カードをクリックすると、詳細ページが開きます。
        -   詳細ページでは、指導略案PDF、配布資料、活動の様子の動画リンクなど、より詳しい情報が閲覧できます。
    4.  **将来的には...**
        -   「いいね」や「ブックマーク」機能、コメント機能を追加し、先生方同士で知見を共有できるコミュニティ機能への発展も検討中です。
    """
}

st.set_page_config(
    page_title="特別支援教育サポートアプリ",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSSを適用
load_css()

# Lottieアニメーションを読み込む関数
@st.cache_data
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Streamlit Cloudではログに出力されることが多いので、st.errorは控えめに
        # st.error(f"Error: {filepath} not found.") 
        return None
    except json.JSONDecodeError:
        # st.error(f"Error: Could not decode JSON from {filepath}. Is it a valid Lottie JSON?")
        return None

# Lottieアニメーションファイル
lottie_animation = load_lottiefile("animation.json")

# ページ遷移を管理するための関数
def set_page(page):
    st.session_state.page_to_visit = page

# st.session_stateをチェックしてページ遷移を実行
if "page_to_visit" in st.session_state:
    page = st.session_state.page_to_visit
    del st.session_state.page_to_visit
    st.switch_page(page)

# アニメーションを一度だけ表示するためのフラグ
if "animation_shown" not in st.session_state:
    st.session_state.animation_shown = False

# --- アニメーション表示ロジック ---
if not st.session_state.animation_shown and lottie_animation:
    # プレースホルダーを定義し、アニメーションを表示する
    animation_placeholder = st.empty()
    with animation_placeholder:
        # アニメーションを中央に表示するためにカラムを使用
        _, col_anim, _ = st.columns([1, 2, 1])

        with col_anim:
            st.markdown("<div style='text-align: center;'><h1>読み込み中...</h1></div>", unsafe_allow_html=True) # 読み込みメッセージ
            st_lottie(
                lottie_animation,
                speed=1,
                loop=False, # 一度だけ再生
                quality="high",
                height="500px",
                width="700px",
                key="initial_animation"
            )
        
        # アニメーションの再生時間に合わせて待機時間を調整
        # 例：アニメーションが約3秒なら、time.sleep(3)
        # ここでは固定で3秒待つことにします。必要に応じて調整してください。
        time.sleep(3) 
        
    # アニメーションが指定時間表示された後、プレースホルダーをクリア
    animation_placeholder.empty()
    st.session_state.animation_shown = True
    st.rerun() # メインコンテンツをロードするために再実行

else: # アニメーションが表示済み、またはアニメーションファイルがない場合
    st.title("🌟 特別支援教育サポートアプリ")

    # メインイメージ
    st.image("https://i.imgur.com/AbUxfxP.png", caption="子どもたちの「できた！」を支援する", use_container_width=True)

    st.header("ようこそ！")
    st.write("""
    このアプリは、特別支援教育に関わる先生方をサポートするためのツールです。
    子どもたち一人ひとりのニーズに合わせた指導や支援のヒントを見つけたり、
    発達段階を記録・分析したり、AIによる計画作成の補助を受けたりすることができます。

    **サイドバーのメニューから、利用したい機能を選択してください。**
    """)

    st.header("各機能の紹介")


    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("### 📚 指導支援内容")
            st.write("日常生活の困りごとに応じた、具体的な指導・支援のアイデアを検索できます。")
            b_col1, b_col2 = st.columns(2)
            b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/1_指導支援内容.py",), key="btn_guidance", use_container_width=True)
            with b_col2.popover("📖 マニュアル", use_container_width=True):
                st.markdown(manuals["guidance"])

    # ... (以下のメインコンテンツ部分は変更なし) ...

        with st.container(border=True):
            st.markdown("### 📈 分析方法")
            st.write("教育学や心理学に基づいた様々な分析方法の解説と、実践で使えるツールを提供します。")
            b_col1, b_col2 = st.columns(2)
            b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/3_分析方法.py",), key="btn_analysis", use_container_width=True)
            with b_col2.popover("📖 マニュアル", use_container_width=True):
                st.markdown(manuals["analysis"])
        
        with st.container(border=True):
            st.markdown("### 🃏 授業カードライブラリー") # 新しい機能
            st.write("先生方の授業アイデアを共有・検索できる、視覚的な授業カード集です。")
            b_col1, b_col2 = st.columns(2)
            b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/8_授業カードライブラリー.py",), key="btn_lesson_card_library", use_container_width=True)
            with b_col2.popover("📖 マニュアル", use_container_width=True):
                st.markdown(manuals["lesson_card_library"])

    with col2:
        with st.container(border=True):
            st.markdown("### 📊 発達チャート作成")
            st.write("お子さんの発達段階を記録し、レーダーチャートで視覚的に確認・保存できます。")
            b_col1, b_col2 = st.columns(2)
            b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/2_発達チャート.py",), key="btn_chart", use_container_width=True)
            with b_col2.popover("📖 マニュアル", use_container_width=True):
                st.markdown(manuals["chart"])
        
        with st.container(border=True):
            st.markdown("### 🤖 計画作成サポート", unsafe_allow_html=True)
            st.write("フォーム入力で、個別の支援・指導計画のプロンプトを簡単に作成します。")
            b_col1, b_col2 = st.columns(2)
            b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/4_個別の支援計画・指導計画作成支援.py",), key="btn_plan_creation", use_container_width=True)
            with b_col2.popover("📖 マニュアル", use_container_width=True):
                st.markdown(manuals["plan_creation"])

    with col3:
        with st.container(border=True):
            st.markdown("### 📜 知的段階（学習指導要領）")
            st.write("学部・段階・教科を選択し、学習指導要領の内容を確認できます。")
            b_col1, b_col2 = st.columns(2)
            b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/6_知的段階_学習指導要領.py",), key="btn_guideline_page", use_container_width=True)
            with b_col2.popover("📖 マニュアル", use_container_width=True):
                st.markdown(manuals["guideline_page"])

        with st.container(border=True):
            st.markdown("### ▶️ 動画ギャラリー")
            st.write("特別支援教育に関する動画と解説をまとめています。")
            st.button("この機能を使う ➡", on_click=set_page, args=("pages/7_動画ギャラリー.py",), key="btn_youtube_gallery", use_container_width=True)
        
        with st.container(border=True):
            st.markdown("### 📝 フィードバック")
            st.write("アプリの改善やご意見をお待ちしています。")
            st.button("この機能を使う ➡", on_click=set_page, args=("pages/9_フィードバック.py",), key="btn_feedback", use_container_width=True)

    st.markdown("<hr class='footer-hr'>", unsafe_allow_html=True)
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

    st.markdown("<hr class='footer-hr'>", unsafe_allow_html=True)
    st.warning("""
    **【利用上の注意】**
    それぞれのアプリに記載してある内容、分析ツールのデータや図、表を外部（研究発表など）で利用する場合は、管理者(岩槻はるかぜ特別支援学校 小山)までご相談ください。無断での転記・利用を禁じます。
    """)