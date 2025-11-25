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

# --- 画像処理 ---
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


# --- 2. CSSデザイン (枠線明確化 & ヌルっとアニメーション) ---
def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = f"""
    <style>
        /* --- 全体フォント --- */
        html, body, [class*="css"] {{
            font-family: 'Noto Sans JP', sans-serif !important;
        }}

        /* --- 背景設定 --- */
        [data-testid="stAppViewContainer"] {{
            background-color: #000000;
            background-image: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-position: center center;
            background-attachment: fixed;
        }}

        /* --- 文字色: 白固定 & 影付き --- */
        .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
        .stMarkdown h4, .stMarkdown h5, .stMarkdown h6, .stMarkdown li, 
        .stCaptionContainer, div {{
            color: #ffffff !important;
            text-shadow: 0 2px 5px rgba(0,0,0, 0.9) !important;
        }}

        /* --- サイドバー --- */
        [data-testid="stSidebar"] {{
            background-color: #080808 !important;
            border-right: 1px solid #333;
        }}
        [data-testid="stSidebar"] * {{
            color: #ffffff !important;
        }}

        /* 
           =========================================
           ★ ここが修正ポイント！機能カードのデザイン ★
           =========================================
        */
        [data-testid="stBorderContainer"] {{
            /* 背景: 濃い黒で塗りつぶす */
            background-color: rgba(20, 20, 20, 0.95) !important;
            
            /* 枠線: 白く太くして境界をはっきりさせる */
            border: 2px solid rgba(255, 255, 255, 0.5) !important;
            
            /* 形と影 */
            border-radius: 16px !important;
            padding: 25px !important;
            margin-bottom: 25px; /* 下のカードとの間隔 */
            box-shadow: 0 10px 30px rgba(0,0,0,0.8); /* 濃い影で浮き上がらせる */
            
            /* ヌルっと動くための設定 */
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            
            /* 出現アニメーション */
            animation: slideUp 0.8s ease-out forwards;
            opacity: 0; /* アニメーション前は透明 */
        }}

        /* ホバー時のヌルっとした動き */
        [data-testid="stBorderContainer"]:hover {{
            border-color: #4a90e2 !important; /* 青く光る */
            transform: translateY(-8px) scale(1.02); /* ふわっと浮く */
            box-shadow: 0 20px 40px rgba(74, 144, 226, 0.3); /* 青い光の影 */
            background-color: #000000 !important;
        }}

        /* --- アニメーション定義 (下からヌルっと出る) --- */
        @keyframes slideUp {{
            from {{ opacity: 0; transform: translateY(40px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* 要素ごとに出現タイミングをずらす (疑似的なStagger効果) */
        div.element-container:nth-child(1) [data-testid="stBorderContainer"] {{ animation-delay: 0.1s; }}
        div.element-container:nth-child(2) [data-testid="stBorderContainer"] {{ animation-delay: 0.2s; }}
        div.element-container:nth-child(3) [data-testid="stBorderContainer"] {{ animation-delay: 0.3s; }}
        div.element-container:nth-child(4) [data-testid="stBorderContainer"] {{ animation-delay: 0.4s; }}

        /* --- ヘッダー (ゆらゆら) --- */
        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}
        .header-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 30px;
            padding: 60px 0;
            animation: float 6s ease-in-out infinite;
        }}
        .logo-img {{
            width: 180px;
            height: auto;
            filter: drop-shadow(0 0 15px rgba(255,255,255,0.6));
        }}
        .main-title {{
            font-size: 5rem;
            font-weight: 900;
            line-height: 1;
            margin: 0;
            color: #ffffff !important;
            text-shadow: 0 0 25px rgba(255, 255, 255, 0.7);
        }}
        .sub-title {{
            font-size: 1.2rem;
            color: #ffffff !important;
            letter-spacing: 0.2em;
            margin-top: 10px;
            font-weight: 700;
        }}

        /* --- 説明文プレート --- */
        .glass-container {{
            background-color: rgba(0, 0, 0, 0.8);
            border: 2px solid #4a90e2;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 40px;
            color: #ffffff !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            
            /* これもヌルっと出す */
            animation: slideUp 1s ease-out forwards;
        }}

        /* --- ボタン --- */
        .stButton > button {{
            width: 100%;
            background-color: transparent !important;
            border: 2px solid #4a90e2 !important;
            color: #4a90e2 !important;
            font-weight: 900 !important;
            border-radius: 30px !important; /* 丸くしてモダンに */
            padding: 10px 20px !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        }}
        .stButton > button:hover {{
            background-color: #4a90e2 !important;
            color: #ffffff !important;
            box-shadow: 0 0 15px rgba(74, 144, 226, 0.6);
            transform: scale(1.05);
        }}

        /* --- 見出しの線 --- */
        h3 {{
            border-bottom: 2px solid #fff;
            padding-bottom: 10px;
            margin-bottom: 20px !important;
        }}
        
        hr {{ border-color: #666; }}
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

# 説明文エリア
st.markdown("""
<div class="glass-container">
    <h3>ようこそ！</h3>
    <p style="font-size: 1.1rem; line-height: 1.8;">
        このアプリは、特別支援教育に関わる先生方をサポートするための統合ツールです。<br>
        子どもたち一人ひとりのニーズに合わせた指導や支援のヒントを見つけたり、
        発達段階を記録・分析したり、AIによる計画作成の補助を受けることができます。
    </p>
    <p style="color: #4a90e2 !important; font-weight: bold; margin-top: 15px; font-size: 1rem;">
        ▼ 下の各機能パネル、またはサイドバーのメニューから利用したい機能を選択してください。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📂 各機能の紹介")

# --- 3カラムレイアウト ---
# st.container(border=True) がCSSで強力にカスタマイズされています
col1, col2, col3 = st.columns(3)

with col1:
    # 1. 指導支援内容
    with st.container(border=True):
        st.markdown("### 📚 指導支援内容")
        st.markdown("日常生活の困りごとに応じた、具体的な指導・支援のアイデアを検索できます。")
        c_btn, c_pop = st.columns([2, 1])
        c_btn.button("使う ➡", on_click=set_page, args=("pages/1_指導支援内容.py",), key="btn_guidance")
        with c_pop.popover("📖"):
            st.markdown(manuals["guidance"])

    # 2. 分析方法
    with st.container(border=True):
        st.markdown("### 📈 分析方法")
        st.markdown("教育学や心理学に基づいた分析手法の解説とツールです。")
        c_btn, c_pop = st.columns([2, 1])
        c_btn.button("使う ➡", on_click=set_page, args=("pages/3_分析方法.py",), key="btn_analysis")
        with c_pop.popover("📖"):
            st.markdown(manuals["analysis"])
    
    # 3. 授業カード
    with st.container(border=True):
        st.markdown("### 🃏 授業カード") 
        st.markdown("先生方の授業アイデアを共有・検索できるライブラリです。")
        c_btn, c_pop = st.columns([2, 1])
        c_btn.button("使う ➡", on_click=set_page, args=("pages/8_授業カードライブラリー.py",), key="btn_lesson_card_library")
        with c_pop.popover("📖"):
            st.markdown(manuals["lesson_card_library"])

with col2:
    # 4. 発達チャート
    with st.container(border=True):
        st.markdown("### 📊 発達チャート")
        st.markdown("発達段階を記録し、レーダーチャートで可視化・保存します。")
        c_btn, c_pop = st.columns([2, 1])
        c_btn.button("使う ➡", on_click=set_page, args=("pages/2_発達チャート.py",), key="btn_chart")
        with c_pop.popover("📖"):
            st.markdown(manuals["chart"])
    
    # 5. AI計画作成
    with st.container(border=True):
        st.markdown("### 🤖 AI計画作成")
        st.markdown("個別の支援・指導計画作成用のプロンプトを簡単に生成します。")
        c_btn, c_pop = st.columns([2, 1])
        c_btn.button("使う ➡", on_click=set_page, args=("pages/4_AIによる支援,指導計画作成.py",), key="btn_plan_creation")
        with c_pop.popover("📖"):
            st.markdown(manuals["plan_creation"])

    # 9. AIによる指導案作成
    with st.container(border=True):
        st.markdown("### 📝 AI指導案作成")
        st.markdown("基本情報を入力するだけで、AIを活用して学習指導案を自動生成します。")
        c_btn, c_pop = st.columns([2, 1])
        c_btn.button("使う ➡", on_click=set_page, args=("pages/9_AIによる指導案作成.py",), key="btn_lesson_plan_ai")
        with c_pop.popover("📖"):
            st.markdown(manuals["lesson_plan_ai"])

with col3:
    # 6. 学習指導要領
    with st.container(border=True):
        st.markdown("### 📜 指導要領早引き")
        st.markdown("学部・段階ごとの学習指導要領の内容を素早く検索できます。")
        c_btn, c_pop = st.columns([2, 1])
        c_btn.button("使う ➡", on_click=set_page, args=("pages/6_知的段階_早引き学習指導要領.py",), key="btn_guideline_page")
        with c_pop.popover("📖"):
            st.markdown(manuals["guideline_page"])

    # 7. 動画ギャラリー
    with st.container(border=True):
        st.markdown("### ▶️ 動画ギャラリー")
        st.markdown("特別支援教育に関する動画と解説をまとめています。")
        st.button("見る ➡", on_click=set_page, args=("pages/7_動画ギャラリー.py",), key="btn_youtube_gallery")

    # 10. フィードバック
    with st.container(border=True):
        st.markdown("### 📝 フィードバック")
        st.markdown("アプリの改善やご意見をお待ちしています。")
        st.button("送る ➡", on_click=set_page, args=("pages/10_フィードバック.py",), key="btn_feedback")


# --- ▼ 関連ツール＆リンク ▼ ---
st.markdown("<br>", unsafe_allow_html=True)

# リンク集
st.markdown("""
<div class="glass-container" style="padding: 15px; margin-bottom: 20px; border-color: #ffffff;">
    <h3 style="margin-bottom: 0 !important; border: none;">🔗 研究・分析ツール (External Links)</h3>
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

# アンケート
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