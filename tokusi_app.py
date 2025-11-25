import streamlit as st
import base64

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
# ロゴ画像のHTML生成
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img">' if logo_b64 else '<div style="font-size:80px;">🌟</div>'


# --- 2. CSSデザイン (今回はHTMLカードに対する直接指定なので確実に効きます) ---
def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = f"""
    <style>
        /* --- 全体リセット --- */
        html, body, [class*="css"] {{
            font-family: 'Noto Sans JP', sans-serif !important;
        }}

        /* --- 背景 (黒) --- */
        [data-testid="stAppViewContainer"] {{
            background-color: #000000;
            background-image: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-attachment: fixed;
        }}

        /* --- 文字色 (白・影付きで最強に見やすく) --- */
        h1, h2, h3, h4, h5, h6, p, span, div, label {{
            color: #ffffff !important;
            text-shadow: 0 2px 4px #000000 !important;
        }}

        /* --- サイドバー --- */
        [data-testid="stSidebar"] {{
            background-color: #0a0a0a !important;
            border-right: 1px solid #444;
        }}

        /* 
           ================================================================
           ★ カスタムHTMLカードのデザイン (これが表示される枠です) ★
           ================================================================
        */
        
        /* アニメーション定義: 下からフワッと */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .mirairo-card {{
            /* 背景: 濃いグレー */
            background-color: #151515;
            
            /* 枠線: 太さ2pxの白い実線 (絶対に見えます) */
            border: 2px solid #ffffff;
            
            /* 形と影 */
            border-radius: 15px 15px 0 0; /* 下はボタンが来るので直角気味に */
            padding: 25px;
            margin-top: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.8);
            
            /* アニメーション適用 */
            animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
            
            /* 高さ調整 */
            min-height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }}
        
        .mirairo-card:hover {{
            border-color: #4a90e2; /* ホバーで青枠に */
            background-color: #000000;
            transform: translateY(-5px);
            transition: all 0.3s ease;
        }}

        .card-title {{
            font-size: 1.4rem;
            font-weight: 900;
            border-bottom: 1px solid #555;
            padding-bottom: 10px;
            margin-bottom: 10px;
            color: #fff;
        }}
        
        .card-desc {{
            font-size: 1rem;
            line-height: 1.6;
            color: #ddd;
        }}

        /* --- ボタンのデザイン修正 --- */
        .stButton > button {{
            width: 100%;
            background-color: #000000 !important;
            border: 2px solid #ffffff !important; /* ボタンも白枠 */
            border-top: none !important; /* 上の線は消してカードと一体化 */
            border-radius: 0 0 15px 15px !important; /* 下側だけ丸く */
            color: #4a90e2 !important;
            font-weight: bold !important;
            padding: 10px !important;
            margin-top: -16px !important; /* 無理やりカードの下にくっつける */
            transition: all 0.3s ease !important;
            position: relative;
            z-index: 5;
        }}
        .stButton > button:hover {{
            background-color: #4a90e2 !important;
            color: #ffffff !important;
            border-color: #4a90e2 !important;
        }}

        /* --- ヘッダーアニメーション --- */
        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}
        
        .header-wrapper {{
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 60px 0;
            animation: float 6s ease-in-out infinite; /* ロゴも文字も一緒に動く */
        }}
        
        .logo-img {{
            width: 180px; /* ロゴ2倍サイズ */
            height: auto;
            filter: drop-shadow(0 0 15px rgba(255,255,255,0.5));
            margin-right: 30px;
        }}
        
        .main-title {{
            font-size: 5rem;
            font-weight: 900;
            line-height: 1;
            margin: 0;
            color: #ffffff; /* タイトル白 */
            text-shadow: 0 0 30px rgba(255, 255, 255, 0.7); /* 白く発光 */
        }}
        
        .sub-title {{
            font-size: 1.5rem;
            color: #ffffff;
            letter-spacing: 0.2em;
            font-weight: 700;
            margin-top: 10px;
        }}

        /* --- 説明文のプレート --- */
        .glass-plate {{
            background-color: rgba(20, 20, 20, 0.95);
            border: 2px solid #4a90e2;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            animation: fadeInUp 1s ease-in-out;
        }}

        hr {{ border-color: #666; }}
        a {{ color: #63b3ed !important; font-weight: bold; text-decoration: none; }}
        a:hover {{ text-decoration: underline; color: #fff !important; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# --- 3. マニュアルデータ ---
manuals = {
    "guidance": """
    ### 📚 指導支援内容 マニュアル
    **使い方:**
    1.  画面のドロップダウンを左から順に選びます。
    2.  「💡 適した指導・支援を表示」をクリック。
    3.  表示された内容を確認します。
    """,
    "chart": """
    ### 📊 発達チャート作成 マニュアル
    **使い方:**
    1.  12のカテゴリーで現在の状況を選択します。
    2.  「📊 チャートを作成」ボタンをクリック。
    3.  スプレッドシートまたはExcel形式でダウンロード。
    """,
    "analysis": """
    ### 📈 分析方法 マニュアル
    **使い方:**
    *   サイドバーから手法（ABAなど）を直接選択、またはメインエリアでお子さんの状況を選んで検索。
    """,
    "plan_creation": """
    ### 🤖 計画作成サポート マニュアル
    **使い方:**
    1.  プロンプトの種類を選択し、実態や課題を入力。
    2.  生成された文面をコピーしてChatGPT等で使用。
    """,
    "lesson_plan_ai": """
    ### 📝 AI指導案作成 マニュアル
    **使い方:**
    1.  基本情報を入力し、プロンプトを作成してAIに入力。
    2.  AIの回答（JSON）を貼り付けてExcelを出力。
    """,
    "guideline_page": """
    ### 📜 指導要領早引き マニュアル
    **使い方:**
    *   学部、障害種別、教科を選択して「表示」をクリック。
    """,
    "lesson_card_library": """
    ### 🃏 授業カード マニュアル
    **使い方:**
    *   検索バーやハッシュタグで実践事例を探せます。
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

# ヘッダー (HTMLで一体化して動かす)
st.markdown(f"""
    <div class="header-wrapper">
        {logo_html}
        <div class="title-group">
            <h1 class="main-title">Mirairo</h1>
            <div class="sub-title">Data-Driven Education Platform</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 説明文 (青枠プレート)
st.markdown("""
<div class="glass-plate">
    <h3>ようこそ！</h3>
    <p style="font-size: 1.1rem; line-height: 1.8;">
        このアプリは、特別支援教育に関わる先生方をサポートするための統合ツールです。<br>
        子どもたち一人ひとりのニーズに合わせた指導や支援のヒントを見つけたり、
        発達段階を記録・分析したり、AIによる計画作成の補助を受けることができます。
    </p>
    <p style="color: #4a90e2; font-weight: bold; margin-top: 15px;">
        ▼ 下の各機能パネル、またはサイドバーのメニューから利用したい機能を選択してください。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📂 各機能の紹介")

# --- 3カラムレイアウト (HTMLカード方式) ---
col1, col2, col3 = st.columns(3)

# カードを描画するヘルパー関数
def render_card(title, desc):
    st.markdown(f"""
    <div class="mirairo-card">
        <div class="card-title">{title}</div>
        <div class="card-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

with col1:
    # 1. 指導支援内容
    render_card("📚 指導支援内容", "日常生活の困りごとに応じた、具体的な指導・支援のアイデアを検索できます。")
    c_btn, c_pop = st.columns([3, 1])
    c_btn.button("使う ➡", on_click=set_page, args=("pages/1_指導支援内容.py",), key="btn_guidance")
    with c_pop.popover("📖"): st.markdown(manuals["guidance"])

    # 2. 分析方法
    render_card("📈 分析方法", "教育学や心理学に基づいた分析手法の解説とツールです。")
    c_btn, c_pop = st.columns([3, 1])
    c_btn.button("使う ➡", on_click=set_page, args=("pages/3_分析方法.py",), key="btn_analysis")
    with c_pop.popover("📖"): st.markdown(manuals["analysis"])
    
    # 3. 授業カード
    render_card("🃏 授業カード", "先生方の授業アイデアを共有・検索できるライブラリです。")
    c_btn, c_pop = st.columns([3, 1])
    c_btn.button("使う ➡", on_click=set_page, args=("pages/8_授業カードライブラリー.py",), key="btn_lesson_card_library")
    with c_pop.popover("📖"): st.markdown(manuals["lesson_card_library"])

with col2:
    # 4. 発達チャート
    render_card("📊 発達チャート", "発達段階を記録し、レーダーチャートで可視化・保存します。")
    c_btn, c_pop = st.columns([3, 1])
    c_btn.button("使う ➡", on_click=set_page, args=("pages/2_発達チャート.py",), key="btn_chart")
    with c_pop.popover("📖"): st.markdown(manuals["chart"])
    
    # 5. AI計画作成
    render_card("🤖 AI計画作成", "個別の支援・指導計画作成用のプロンプトを簡単に生成します。")
    c_btn, c_pop = st.columns([3, 1])
    c_btn.button("使う ➡", on_click=set_page, args=("pages/4_AIによる支援,指導計画作成.py",), key="btn_plan_creation")
    with c_pop.popover("📖"): st.markdown(manuals["plan_creation"])

    # 9. AIによる指導案作成
    render_card("📝 AI指導案作成", "基本情報を入力するだけで、AIを活用して学習指導案を自動生成します。")
    c_btn, c_pop = st.columns([3, 1])
    c_btn.button("使う ➡", on_click=set_page, args=("pages/9_AIによる指導案作成.py",), key="btn_lesson_plan_ai")
    with c_pop.popover("📖"): st.markdown(manuals["lesson_plan_ai"])

with col3:
    # 6. 学習指導要領
    render_card("📜 指導要領早引き", "学部・段階ごとの学習指導要領の内容を素早く検索できます。")
    c_btn, c_pop = st.columns([3, 1])
    c_btn.button("使う ➡", on_click=set_page, args=("pages/6_知的段階_早引き学習指導要領.py",), key="btn_guideline_page")
    with c_pop.popover("📖"): st.markdown(manuals["guideline_page"])

    # 7. 動画ギャラリー
    render_card("▶️ 動画ギャラリー", "特別支援教育に関する動画と解説をまとめています。")
    st.button("見る ➡", on_click=set_page, args=("pages/7_動画ギャラリー.py",), key="btn_youtube_gallery")

    # 10. フィードバック
    render_card("📝 フィードバック", "アプリの改善やご意見をお待ちしています。")
    st.button("送る ➡", on_click=set_page, args=("pages/10_フィードバック.py",), key="btn_feedback")


# --- ▼ 関連ツール＆リンク ▼ ---
st.markdown("<br>", unsafe_allow_html=True)

# リンク集 (こちらもHTMLカード化)
st.markdown("""
<div class="glass-plate" style="padding: 15px; margin-bottom: 20px; border-color: #ffffff;">
    <h3 style="margin-bottom: 0 !important; border: none;">🔗 研究・分析ツール (External Links)</h3>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown("""
    <div class="mirairo-card" style="min-height: auto;">
        <div class="card-title" style="font-size: 1.2rem;">📁 教育・心理分析</div>
        <div class="card-desc">
            <ul style="padding-left: 20px; margin: 0;">
                <li><a href="https://abaapppy-k7um2qki5kggexf8qkfxjc.streamlit.app/" target="_blank">応用行動分析 (ABA)</a></li>
                <li><a href="https://kinoukoudou-ptfpnkq3uqgaorabcyzgf2.streamlit.app/" target="_blank">機能的行動評価</a></li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="mirairo-card" style="min-height: auto;">
        <div class="card-title" style="font-size: 1.2rem;">📁 統計学分析</div>
        <div class="card-desc">
            <ul style="padding-left: 20px; margin: 0;">
                <li><a href="https://annketo12345py-edm3ajzwtsmmuxbm8qbamr.streamlit.app/" target="_blank">アンケートデータ統計分析</a></li>
                <li><a href="https://soukan-jlhkdhkradbnxssy29aqte.streamlit.app/" target="_blank">相関分析</a></li>
                <li><a href="https://kaikiapp-tjtcczfvlg2pyhd9bjxwom.streamlit.app/" target="_blank">多変量回帰分析</a></li>
                <li><a href="https://tkentei-flhmnqnq6dti6oyy9xnktr.streamlit.app/" target="_blank">t検定</a></li>
                <li><a href="https://rojisthik-buklkg5zeh6oj2gno746ix.streamlit.app/" target="_blank">ロジスティック回帰分析</a></li>
                <li><a href="https://nonparametoric-nkk2awu6yv9xutzrjmrsxv.streamlit.app/" target="_blank">ノンパラメトリック分析</a></li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# アンケート
st.markdown("""
<div class="glass-plate" style="text-align: center;">
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