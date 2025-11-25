import streamlit as st
import os

# --- 1. ページ設定 (必ず最初に記述) ---
st.set_page_config(
    page_title="Mirairo - 分析方法", 
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. デザイン定義 (Mirairo共通のダークモード・白枠線デザイン) ---
def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = """
    <style>
        /* --- 全体フォント --- */
        html, body, [class*="css"] {
            font-family: 'Noto Sans JP', sans-serif !important;
        }

        /* --- 背景 (黒ベース + 画像) --- */
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

        /* --- サイドバー (半透明) --- */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        /* サイドバー閉じるボタン */
        [data-testid="stSidebarNavCollapseButton"] {
            color: #fff !important;
        }

        /* 
           ================================================================
           ★ 機能カードのデザイン (白枠・アニメーション) ★
           ================================================================
        */
        
        /* アニメーション定義 */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        [data-testid="stBorderContainer"] {
            background-color: #151515 !important;
            border: 2px solid #ffffff !important; /* 白い太枠 */
            border-radius: 16px !important;
            padding: 20px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.8) !important;
            
            /* アニメーション適用 */
            animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        }

        /* ホバー時の動き */
        [data-testid="stBorderContainer"]:hover {
            border-color: #4a90e2 !important;
            transform: translateY(-5px);
            background-color: #000000 !important;
            box-shadow: 0 0 20px rgba(74, 144, 226, 0.4) !important;
            transition: all 0.3s ease;
        }

        /* --- ボタンのデザイン --- */
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

        /* --- 説明文プレート (Glass Plate) --- */
        .glass-plate {
            background-color: rgba(20, 20, 20, 0.8);
            border: 2px solid #4a90e2;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            animation: fadeInUp 1s ease-in-out;
        }

        /* --- 戻るボタンのリンク --- */
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

        /* セレクトボックスの調整 */
        div[data-baseweb="select"] > div {
            background-color: #222 !important;
            color: #fff !important;
            border-color: #555 !important;
        }
        
        hr { border-color: #666; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# CSS適用
load_css()

# --- ▼ 戻るボタン ▼ ---
st.markdown('<div class="back-link"><a href="Home" target="_self">« TOPページに戻る</a></div>', unsafe_allow_html=True)

st.title("📈 分析方法")

# --- 推奨ツールエリア (プレートデザイン) ---
st.markdown("""
<div class="glass-plate">
    <h4 style="color: #4a90e2 !important; margin-top: 0;">✨ 特にオススメ！アンケート分析ツール</h4>
    <p>Google FormsやMicrosoft Formsアンケートをグラフ化したり、統計学的に分析するツールです！<br>
    アンケートをまとめたい人、研究論文や課題研究を行っている人にはご活用ください。</p>
</div>
""", unsafe_allow_html=True)

st.page_link("https://annketo12345py-edm3ajzwtsmmuxbm8qbamr.streamlit.app/", label="📝 アンケートデータ、総合統計分析ツールを開く", icon="🔗")

# イメージ画像
img_stats_tools_chart = "https://i.imgur.com/ASnp6PS.png"
st.image(img_stats_tools_chart, caption="データ分析をサポートするツール群", use_container_width=True)


# --- データ定義 ---
# 画像URL
img_dousa = [
    "https://i.imgur.com/SwjfDft.png", "https://i.imgur.com/LqbE9Nf.png",
    "https://i.imgur.com/XLwjXFE.png", "https://i.imgur.com/2MfaBxc.png",
]
img_mindfulness = "https://i.imgur.com/zheqhdv.png"
img_pecs = "https://i.imgur.com/Hw4PIKo.jpeg"
img_cbt = "https://i.imgur.com/vnMHFNE.png"

# 療法・分析法データ
methods = {
    "ABA（応用行動分析）※ツール有": {"file": "pages2/aba.md", "description": "行動の原理を応用し、望ましい行動を促進します。"},
    "FBA/PBS（機能的アセスメント/ポジティブ行動支援）※ツール有": {"file": "pages2/fba_pbs.md", "description": "問題行動の原因を探り、前向きな支援計画を立てます。"},
    "CBT（認知行動療法）": {"file": "pages2/cbt.md", "description": "思考パターンに焦点を当て、感情や行動の改善を目指します。"},
    "ソーシャルスキルトレーニング": {"file": "pages2/sst.md", "description": "対人関係で役立つスキルを効果的に学びます。"},
    "感覚統合療法": {"file": "pages2/sensory_integration.md", "description": "感覚の処理能力を高め、日常生活の適応を助けます。"},
    "PECS（絵カード交換式コミュニケーション）": {"file": "pages2/pecs.md", "description": "絵カードを使ってコミュニケーション能力を育みます。"},
    "動作法": {"file": "pages2/dousahou.md", "description": "身体の動きを通じて心身のバランスを整えます。"},
    "TEACCH": {"file": "pages2/teacch.md", "description": "構造化された環境で自閉症スペクトラムの子どもを支援します。"},
    "SEL（社会情動的学習）": {"file": "pages2/sel.md", "description": "感情の理解と管理、他者との共感を育む学習です。"},
    "マインドフルネス": {"file": "pages2/mindfulness.md", "description": "今ここに意識を集中し、心の平静を保つ練習です。"},
    "プレイセラピー": {"file": "pages2/play_therapy.md", "description": "遊びを通して子どもの感情を表現し、問題を解決します。"},
    "アートセラピー": {"file": "pages2/art_therapy.md", "description": "芸術表現を通じて自己理解と癒しを深めます。"},
    "ミュージックセラピー": {"file": "pages2/music_therapy.md", "description": "音楽の力で心身の健康を促進し、感情を豊かにします。"},
    "セルフモニタリング": {"file": "pages2/self_monitar.md", "description": "自身の行動や感情を記録し、客観的に分析します。"},
    "統計学的分析方法 ※ツール有": {"file": "pages2/toukei.md", "description": "データに基づいて教育実践を客観的に評価します。"},
}

# 実態対応データ
student_conditions = {
    "言葉で気持ちを伝えるのが難しい": ["プレイセラピー", "アートセラピー", "PECS（絵カード交換式コミュニケーション）"],
    "感情のコントロールが苦手": ["CBT（認知行動療法）", "SEL（社会情動的学習）", "マインドフルネス"],
    "対人関係が苦手": ["ソーシャルスキルトレーニング", "TEACCH"],
    "学習の集中が続かない": ["ABA（応用行動分析）", "感覚統合療法", "セルフモニタリング"],
    "行動の問題がある": ["FBA/PBS（機能的アセスメント/ポジティブ行動支援）", "ABA（応用行動分析）"],
    "身体に課題がある": ["動作法"],
    "統計的な分析をしたい": ["統計学的分析方法"],
}

# --- UI状態管理 ---
if "selected_method" not in st.session_state:
    st.session_state.selected_method = None
if "show_toukei_description" not in st.session_state:
    st.session_state.show_toukei_description = False
if "show_analysis_methods" not in st.session_state:
    st.session_state.show_analysis_methods = False
if "show_student_conditions" not in st.session_state:
    st.session_state.show_student_conditions = False


# --- 1. 分析方法の一覧から探す ---
st.markdown("---")
if st.button("📂 「分析方法の一覧から探す」を表示/非表示", key="toggle_analysis_methods"):
    st.session_state.show_analysis_methods = not st.session_state.show_analysis_methods

if st.session_state.show_analysis_methods:
    st.subheader("分析方法の一覧")
    st.caption("気になる分析方法をクリックして詳細をご覧ください。")

    # 3列グリッド (カードデザイン適用)
    cols_count = 3
    cols = st.columns(cols_count)
    
    for i, (method_name, method_info) in enumerate(methods.items()):
        with cols[i % cols_count]:
            # st.container(border=True) を使うことで白枠・アニメーションが適用される
            with st.container(border=True):
                st.markdown(f"**{method_name}**")
                st.caption(f"{method_info['description']}")
                if st.button("詳細を見る ➡", key=f"method_btn_{method_name}", type="primary" if st.session_state.selected_method == method_name else "secondary"):
                    st.session_state.selected_method = method_name
                    if method_name == "統計学的分析方法":
                        st.session_state.show_toukei_description = True
                    else:
                        st.session_state.show_toukei_description = False
                    st.rerun()


# --- 2. 児童・生徒の実態から探す ---
st.markdown("---")
if st.button("👦 「児童・生徒の実態から探す」を表示/非表示", key="toggle_student_conditions"):
    st.session_state.show_student_conditions = not st.session_state.show_student_conditions

if st.session_state.show_student_conditions:
    st.subheader("児童・生徒の実態から探す")
    condition = st.selectbox("▼ 実態を選んでください", list(student_conditions.keys()))

    st.write("💡 **この実態に適した療法・分析法:**")
    
    # 結果表示用カラム
    cols_for_condition = st.columns(3)
    for i, method in enumerate(student_conditions[condition]):
        if method in methods:
            with cols_for_condition[i % 3]:
                with st.container(border=True):
                    st.markdown(f"**{method}**")
                    if st.button("詳細を見る ➡", key=f"btn_condition_{method}"):
                        st.session_state.selected_method = method
                        if method == "統計学的分析方法":
                            st.session_state.show_toukei_description = True
                        else:
                            st.session_state.show_toukei_description = False
                        st.rerun()


# --- 詳細表示エリア ---
if st.session_state.selected_method:
    st.markdown("---")
    
    # 白枠コンテナの中に詳細を表示
    with st.container(border=True):
        st.header(f"解説：{st.session_state.selected_method}")
        
        safe_method_id = st.session_state.selected_method.replace(" ", "-").replace("（", "").replace("）", "").replace("/", "-").replace("・", "-")
        
        # 自動スクロール用JS
        st.markdown(f"""
            <script>
                setTimeout(function() {{
                    var element = window.parent.document.querySelector('.element-container h2');
                    if(element) element.scrollIntoView({{behavior: 'smooth'}});
                }}, 300);
            </script>
        """, unsafe_allow_html=True)

        # テキスト読み込み
        if st.session_state.selected_method == "統計学的分析方法":
            if st.button("説明文を表示/非表示", key="toggle_toukei"):
                st.session_state.show_toukei_description = not st.session_state.show_toukei_description
            if st.session_state.show_toukei_description:
                file_path = methods.get(st.session_state.selected_method)["file"]
                if file_path and os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        st.markdown(f.read(), unsafe_allow_html=True)
        else:
            file_path = methods.get(st.session_state.selected_method)["file"]
            if file_path and os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    st.markdown(f.read(), unsafe_allow_html=True)
            else:
                st.warning("準備中です。")

        # 個別画像・リンク表示
        method = st.session_state.selected_method

        if method == "CBT（認知行動療法）":
            st.image(img_cbt, caption="認知の歪みの例", use_container_width=True)
        elif method == "PECS（絵カード交換式コミュニケーション）":
            st.image(img_pecs, caption="PECSの例", use_container_width=True)
        elif method == "マインドフルネス":
            st.image(img_mindfulness, caption="マインドフルネスの活動例", use_container_width=True)
        elif method == "動作法":
            st.write("**【指導例画像】**")
            img_cols = st.columns(2)
            for i, img_url in enumerate(img_dousa):
                img_cols[i % 2].image(img_url, caption=f"生徒{i+1}", use_container_width=True)
        elif method == "ABA（応用行動分析）":
            st.info("##### 🛠️ 簡単分析ツール")
            st.page_link("https://abaapppy-k7um2qki5kggexf8qkfxjc.streamlit.app/", label="応用行動分析ツール", icon="🔗")
        elif method == "FBA/PBS（機能的アセスメント/ポジティブ行動支援）":
            st.info("##### 🛠️ 分析ツールと参考資料")
            st.page_link("https://kinoukoudou-ptfpnkq3uqgaorabcyzgf2.streamlit.app/", label="機能的行動評価分析ツール", icon="🔗")
        elif method == "統計学的分析方法":
            st.info("##### 🛠️ 統計学 分析ツール一覧")
            st.page_link("https://soukan-jlhkdhkradbnxssy29aqte.streamlit.app/", label="相関分析", icon="🔗")
            st.page_link("https://kaikiapp-tjtcczfvlg2pyhd9bjxwom.streamlit.app/", label="多変量回帰分析", icon="🔗")
            st.page_link("https://rojisthik-buklkg5zeh6oj2gno746ix.streamlit.app/", label="ロジスティック回帰分析", icon="🔗")
            st.page_link("https://nonparametoric-nkk2awu6yv9xutzrjmrsxv.streamlit.app/", label="ノンパラメトリック分析", icon="🔗")
            st.page_link("https://tkentei-flhmnqnq6dti6oyy9xnktr.streamlit.app/", label="t検定", icon="🔗")


# --- フッター ---
st.markdown('<hr>', unsafe_allow_html=True)

with st.expander("🔗 全ての統計学ツールリンクを表示"):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### 📁 教育・心理分析")
        st.page_link("https://abaapppy-k7um2qki5kggexf8qkfxjc.streamlit.app/", label="応用行動分析", icon="🔗")
        st.page_link("https://kinoukoudou-ptfpnkq3uqgaorabcyzgf2.streamlit.app/", label="機能的行動評価", icon="🔗")
    with c2:
        st.markdown("##### 📁 統計学分析")
        st.page_link("https://annketo12345py-edm3ajzwtsmmuxbm8qbamr.streamlit.app/", label="アンケート分析", icon="🔗")
        st.page_link("https://soukan-jlhkdhkradbnxssy29aqte.streamlit.app/", label="相関分析", icon="🔗")
        st.page_link("https://kaikiapp-tjtcczfvlg2pyhd9bjxwom.streamlit.app/", label="多変量回帰分析", icon="🔗")
        st.page_link("https://tkentei-flhmnqnq6dti6oyy9xnktr.streamlit.app/", label="t検定", icon="🔗")
        st.page_link("https://rojisthik-buklkg5zeh6oj2gno746ix.streamlit.app/", label="ロジスティック回帰", icon="🔗")
        st.page_link("https://nonparametoric-nkk2awu6yv9xutzrjmrsxv.streamlit.app/", label="ノンパラメトリック", icon="🔗")

st.markdown("---")
st.page_link("https://docs.google.com/forms/d/1dKzh90OkxMoWDZXV31FgPvXG5EvNlMFOrvSPGvYTSC8/preview", label="🗨️ ご意見・ご感想 (アンケートフォーム)", icon="📝")

st.warning("【利用上の注意】無断での転記・利用を禁じます。研究発表等での利用は管理者までご相談ください。")