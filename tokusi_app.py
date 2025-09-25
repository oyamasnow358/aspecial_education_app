import streamlit as st

# --- ▼ 共通CSSの読み込み（修正版） ▼ ---
def load_css():
    """カスタムCSSとJavaScriptを読み込む関数"""
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

        /* --- フェードインアニメーションのCSS --- */
        .fade-in-section {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s ease-out, transform 0.6s ease-out;
        }
        .fade-in-section.is-visible {
            opacity: 1;
            transform: translateY(0);
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    
    # JavaScriptを埋め込む
    st.markdown("""
    <script>
        // Intersection Observer APIを使用して、要素がビューポートに入ったときにクラスを追加する
        const fadeIns = document.querySelectorAll('.fade-in-section');

        const handleIntersection = (entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target); // 一度表示されたら監視を停止
                }
            });
        };

        const observer = new IntersectionObserver(handleIntersection, {
            root: null, // ビューポートをルートとする
            rootMargin: '0px',
            threshold: 0.1 // 要素の10%が見えたら発火
        });

        fadeIns.forEach(section => {
            observer.observe(section);
        });
    </script>
    """, unsafe_allow_html=True) # ここでJavaScriptを読み込む
# --- ▲ 共通CSSとJSの読み込み ▲ ---

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

# フェードインを適用したい各セクションを `st.markdown` で囲み、`fade-in-section` クラスを付与する
st.markdown('<div class="fade-in-section">', unsafe_allow_html=True)
st.header("ようこそ！")
st.write("""
このアプリは、特別支援教育に関わる先生方をサポートするためのツールです。
子どもたち一人ひとりのニーズに合わせた指導や支援のヒントを見つけたり、
発達段階を記録・分析したり、AIによる計画作成の補助を受けたりすることができます。

**サイドバーのメニューから、利用したい機能を選択してください。**
""")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="fade-in-section">', unsafe_allow_html=True)
st.header("各機能の紹介")
st.markdown('</div>', unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="fade-in-section">', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 📚 指導支援内容")
        st.write("日常生活の困りごとに応じた、具体的な指導・支援のアイデアを検索できます。")
        b_col1, b_col2 = st.columns(2)
        b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/1_指導支援内容.py",), key="btn_guidance", use_container_width=True)
        with b_col2.popover("📖 マニュアル", use_container_width=True):
            st.markdown(manuals["guidance"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fade-in-section">', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 📈 分析方法")
        st.write("教育学や心理学に基づいた様々な分析方法の解説と、実践で使えるツールを提供します。")
        b_col1, b_col2 = st.columns(2)
        b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/3_分析方法.py",), key="btn_analysis", use_container_width=True)
        with b_col2.popover("📖 マニュアル", use_container_width=True):
            st.markdown(manuals["analysis"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="fade-in-section">', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 🃏 授業カードライブラリー") # 新しい機能
        st.write("先生方の授業アイデアを共有・検索できる、視覚的な授業カード集です。")
        b_col1, b_col2 = st.columns(2)
        b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/8_授業カードライブラリー.py",), key="btn_lesson_card_library", use_container_width=True)
        with b_col2.popover("📖 マニュアル", use_container_width=True):
            st.markdown(manuals["lesson_card_library"])
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="fade-in-section">', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 📊 発達チャート作成")
        st.write("お子さんの発達段階を記録し、レーダーチャートで視覚的に確認・保存できます。")
        b_col1, b_col2 = st.columns(2)
        b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/2_発達チャート.py",), key="btn_chart", use_container_width=True)
        with b_col2.popover("📖 マニュアル", use_container_width=True):
            st.markdown(manuals["chart"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="fade-in-section">', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 🤖 計画作成サポート", unsafe_allow_html=True)
        st.write("フォーム入力で、個別の支援・指導計画のプロンプトを簡単に作成します。", )
        b_col1, b_col2 = st.columns(2)
        b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/4_個別の支援計画・指導計画作成支援.py",), key="btn_plan_creation", use_container_width=True)
        with b_col2.popover("📖 マニュアル", use_container_width=True):
            st.markdown(manuals["plan_creation"])
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="fade-in-section">', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 📜 知的段階（学習指導要領）")
        st.write("学部・段階・教科を選択し、学習指導要領の内容を確認できます。")
        b_col1, b_col2 = st.columns(2)
        b_col1.button("この機能を使う ➡", on_click=set_page, args=("pages/6_知的段階_学習指導要領.py",), key="btn_guideline_page", use_container_width=True)
        with b_col2.popover("📖 マニュアル", use_container_width=True):
            st.markdown(manuals["guideline_page"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fade-in-section">', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### ▶️ 動画ギャラリー")
        st.write("特別支援教育に関する動画と解説をまとめています。")
        st.button("この機能を使う ➡", on_click=set_page, args=("pages/7_動画ギャラリー.py",), key="btn_youtube_gallery", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fade-in-section">', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 📝 フィードバック")
        st.write("アプリの改善やご意見をお待ちしています。")
        st.button("この機能を使う ➡", on_click=set_page, args=("pages/9_フィードバック.py",), key="btn_feedback", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# --- ▼ 関連ツール＆リンク（修正版） ▼ ---
st.markdown('<div class="fade-in-section">', unsafe_allow_html=True)
st.markdown("<hr class='footer-hr'>", unsafe_allow_html=True)
st.markdown('<div class="related-tools-card">', unsafe_allow_html=True) # 全体をカードで囲む
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
st.markdown('</div>', unsafe_allow_html=True) # カードの閉じタグ
# --- ▲ 関連ツール＆リンク ▲ ---

st.markdown("<hr class='footer-hr'>", unsafe_allow_html=True)
st.warning("""
**【利用上の注意】**
それぞれのアプリに記載してある内容、分析ツールのデータや図、表を外部（研究発表など）で利用する場合は、管理者(岩槻はるかぜ特別支援学校 小山)までご相談ください。無断での転記・利用を禁じます。
""")