import streamlit as st
import os

# --- ▼ 共通CSSの読み込み ▼ ---
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

        /* 分析方法カードのカスタムスタイル */
        .analysis-card {
            background-color: rgba(255, 255, 255, 0.98);
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
            transition: all 0.2s ease-in-out;
            cursor: pointer;
            text-align: center;
        }
        .analysis-card:hover {
            box-shadow: 0 8px 16px rgba(74, 144, 226, 0.15);
            transform: translateY(-3px);
            background-color: #e6f0fa; /* ホバー時の背景色 */
        }
        .analysis-card h4 {
            color: #34495e;
            margin-top: 0;
            margin-bottom: 10px;
            font-size: 1.1em;
            font-weight: bold;
        }
        .analysis-card p {
            color: #606060;
            font-size: 0.9em;
            line-height: 1.4;
        }
        .analysis-card.selected {
            border: 2px solid #8A2BE2; /* 選択時の強調 */
            box-shadow: 0 0 0 3px rgba(138, 43, 226, 0.3);
            background-color: #f3e8ff; /* 選択時の背景色 */
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- ▲ 共通CSSの読み込み ▲ ---
st.set_page_config(page_title="分析方法", page_icon="📈", layout="wide")

# CSSを読み込む
load_css()

st.title("📈 分析方法")
st.write("ここでは、特別支援教育で使える教育学的、心理学的、統計学的分析方法の解説と、実践で使えるツールを紹介します。")

# --- データ定義 ---
# 画像URL
img_dousa = [
    "https://i.imgur.com/SwjfDft.png",
    "https://i.imgur.com/LqbE9Nf.png",
    "https://i.imgur.com/XLwjXFE.png",
    "https://i.imgur.com/2MfaBxc.png",
]
img_mindfulness = "https://i.imgur.com/zheqhdv.png"
img_pecs = "https://i.imgur.com/Hw4PIKo.jpeg"
img_cbt = "https://i.imgur.com/vnMHFNE.png"

# 療法・分析法とマークダウンファイルの対応
methods = {
    "ABA（応用行動分析）": {"file": "pages2/aba.md", "description": "行動の原理を応用し、望ましい行動を促進します。"},
    "FBA/PBS（機能的アセスメント/ポジティブ行動支援）": {"file": "pages2/fba_pbs.md", "description": "問題行動の原因を探り、前向きな支援計画を立てます。"},
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
    "統計学的分析方法": {"file": "pages2/toukei.md", "description": "データに基づいて教育実践を客観的に評価します。"},
}

# 実態と適した療法の対応
student_conditions = {
    "言葉で気持ちを伝えるのが難しい": ["プレイセラピー", "アートセラピー", "PECS（絵カード交換式コミュニケーション）"],
    "感情のコントロールが苦手": ["CBT（認知行動療法）", "SEL（社会情動的学習）", "マインドフルネス"],
    "対人関係が苦手": ["ソーシャルスキルトレーニング", "TEACCH"],
    "学習の集中が続かない": ["ABA（応用行動分析）", "感覚統合療法", "セルフモニタリング"],
    "行動の問題がある": ["FBA/PBS（機能的アセスメント/ポジティブ行動支援）", "ABA（応用行動分析）"],
    "身体に課題がある": ["動作法"],
    "統計的な分析をしたい": ["統計学的分析方法"],
}

# --- UI ---

# セッションステートで選択を管理
if "selected_method" not in st.session_state:
    st.session_state.selected_method = None

# 分析方法一覧の表示（右側）
st.subheader("分析方法の一覧から探す")
st.write("気になる分析方法をクリックして詳細をご覧ください。")

# 3列で分析方法カードを表示
cols_count = 3
cols = st.columns(cols_count)
col_idx = 0

for method_name, method_info in methods.items():
    with cols[col_idx % cols_count]:
        # カスタムCSSクラスを適用したHTMLボタンを使用
        # Streamlitのボタンはクリック時に再実行されるため、その挙動を利用
        is_selected = " selected" if st.session_state.selected_method == method_name else ""
        
        # Streamlitのformを使うことで、ボタンが押されるまで再実行を遅らせ、まとめて処理できる
        # ただし、今回はボタンクリックで即座に詳細を表示したいため、あえてformを使わない
        if st.button(
            f"**{method_name}**\n\n_{method_info['description']}_", 
            key=f"method_btn_{method_name}",
            use_container_width=True
        ):
            st.session_state.selected_method = method_name
            st.rerun() # 選択されたらすぐに詳細を表示するために再実行

    col_idx += 1


st.markdown("---") # 区切り線

st.subheader("児童・生徒の実態から探す")
condition = st.selectbox("実態を選んでください", list(student_conditions.keys()))

st.write("💡 **この実態に適した療法・分析法:**")
cols_for_condition = st.columns(3)
col_idx_condition = 0
for method in student_conditions[condition]:
    if method in methods:
        if cols_for_condition[col_idx_condition % 3].button(method, key=f"btn_condition_{method}"):
            st.session_state.selected_method = method
            st.rerun()
    col_idx_condition += 1


# --- 詳細表示 ---
if st.session_state.selected_method:
    st.markdown("---")
    st.header(f"解説：{st.session_state.selected_method}")
    
    with st.container(border=True):
        file_path = methods.get(st.session_state.selected_method)["file"]
        # マークダウンファイルの内容を表示
        if file_path and os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                st.markdown(f.read(), unsafe_allow_html=True)
        else:
            st.warning(f"詳細な説明ページは準備中です。(ファイルが見つかりません: {file_path})")

        # 選択された療法に応じたコンテンツを表示
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
            st.markdown("""
            **【出典情報】**
            - **参考文献:** Durand, V. M. (1990). Severe behavior problems: A functional communication training approach. Guilford Press.
            - **Webサイト:** [機能的アセスメント](http://www.kei-ogasawara.com/support/assessment/)
            """)
        elif method == "統計学的分析方法":
            st.info("##### 🛠️ 統計学 分析ツール一覧")
            st.page_link("https://annketo12345py-edm3ajzwtsmmuxbm8qbamr.streamlit.app/", label="アンケートデータ、総合統計分析", icon="🔗")
            st.page_link("https://soukan-jlhkdhkradbnxssy29aqte.streamlit.app/", label="相関分析", icon="🔗")
            st.page_link("https://kaikiapp-tjtcczfvlg2pyhd9bjxwom.streamlit.app/", label="多変量回帰分析", icon="🔗")
            st.page_link("https://rojisthik-buklkg5zeh6oj2gno746ix.streamlit.app/", label="ロジスティック回帰分析ツール", icon="🔗")
            st.page_link("https://nonparametoric-nkk2awu6yv9xutzrjmrsxv.streamlit.app/", label="ノンパラメトリック統計分析ツール", icon="🔗")
            st.page_link("https://tkentei-flhmnqnq6dti6oyy9xnktr.streamlit.app/", label="t検定", icon="🔗")

# フッターの区切り線
st.markdown('<hr class="footer-hr">', unsafe_allow_html=True)