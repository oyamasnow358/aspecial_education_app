import streamlit as st
import os
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
st.set_page_config(page_title="分析方法", page_icon="📈", layout="wide")

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
    "ABA（応用行動分析）": "pages2/aba.md",
    "FBA/PBS（機能的アセスメント/ポジティブ行動支援）": "pages2/fba_pbs.md",
    "CBT（認知行動療法）": "pages2/cbt.md",
    "ソーシャルスキルトレーニング": "pages2/sst.md",
    "感覚統合療法": "pages2/sensory_integration.md",
    "PECS（絵カード交換式コミュニケーション）": "pages2/pecs.md",
    "動作法": "pages2/dousahou.md",
    "TEACCH": "pages2/teacch.md",
    "SEL（社会情動的学習）": "pages2/sel.md",
    "マインドフルネス": "pages2/mindfulness.md",
    "プレイセラピー": "pages2/play_therapy.md",
    "アートセラピー": "pages2/art_therapy.md",
    "ミュージックセラピー": "pages2/music_therapy.md",
    "セルフモニタリング":"pages2/self_monitar.md",
    "統計学的分析方法":"pages2/toukei.md",
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

with st.sidebar:
    st.header("療法・分析法から探す")
    # ラジオボタンで選択されたらセッションステートを更新
    selected_in_sidebar = st.radio(
        "一覧から選択:",
        list(methods.keys()),
        index=None,
        key="sidebar_radio"
    )
    if selected_in_sidebar:
        st.session_state.selected_method = selected_in_sidebar

st.subheader("児童・生徒の実態から探す")
condition = st.selectbox("実態を選んでください", list(student_conditions.keys()))

st.write("💡 **この実態に適した療法・分析法:**")
cols = st.columns(3)
col_idx = 0
for method in student_conditions[condition]:
    if method in methods:
        if cols[col_idx % 3].button(method, key=f"btn_{method}"):
            st.session_state.selected_method = method
            # ボタンが押されたら再実行して表示を更新
            st.rerun()
    col_idx += 1


# --- 詳細表示 ---
if st.session_state.selected_method:
    st.markdown("---")
    st.header(f"解説：{st.session_state.selected_method}")
    
    with st.container(border=True):
        file_path = methods.get(st.session_state.selected_method)
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
            # ダウンロード部分は元のコードと同様に実装（ファイルパスは要確認）
        elif method == "統計学的分析方法":
            st.info("##### 🛠️ 統計学 分析ツール一覧")
            st.page_link("https://annketo12345py-edm3ajzwtsmmuxbm8qbamr.streamlit.app/", label="アンケートデータ、総合統計分析", icon="🔗")
            st.page_link("https://soukan-jlhkdhkradbnxssy29aqte.streamlit.app/", label="相関分析", icon="🔗")
            st.page_link("https://kaikiapp-tjtcczfvlg2pyhd9bjxwom.streamlit.app/", label="多変量回帰分析", icon="🔗")
            st.page_link("https://rojisthik-buklkg5zeh6oj2gno746ix.streamlit.app/", label="ロジスティック回帰分析ツール", icon="🔗")
            st.page_link("https://nonparametoric-nkk2awu6yv9xutzrjmrsxv.streamlit.app/", label="ノンパラメトリック統計分析ツール", icon="🔗")
            st.page_link("https://tkentei-flhmnqnq6dti6oyy9xnktr.streamlit.app/", label="t検定", icon="🔗")