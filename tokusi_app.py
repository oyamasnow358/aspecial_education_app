import streamlit as st
import base64
import time

# ==========================================
# 1. ページ設定
# ==========================================
st.set_page_config(
    page_title="MieeL",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. 画像処理
# ==========================================
def get_img_as_base64(file):
    try:
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None


logo_path = "MieeL.png"
logo_b64 = get_img_as_base64(logo_path)
# ロゴ画像がない場合はプレースホルダー
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img">' if logo_b64 else '<div class="logo-placeholder">🌟</div>'


# ==========================================
# 3. CSSデザイン (白ベース・視認性特化・アニメーション維持)
# ==========================================
def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = f"""
    <style>
        /* --- 全体フォント --- */
        html, body, [class*="css"] {{
            font-family: 'Noto Sans JP', sans-serif !important;
        }}

        /* --- 背景 (白95%透過で画像をうっすら表示) --- */
        [data-testid="stAppViewContainer"] {{
            background-color: #ffffff;
            background-image: linear-gradient(rgba(255,255,255,0.92), rgba(255,255,255,0.92)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-attachment: fixed;
        }}

        /* --- 文字色 (黒・くっきり) --- */
        h1, h2, h3, h4, h5, h6 {{
            color: #0f172a !important; /* 濃いネイビーブラック */
            text-shadow: none !important;
        }}
        p, span, div, label {{
            color: #333333 !important;
            text-shadow: none !important;
        }}

        /* 
           ================================================================
           ★ サイドバーのデザイン (白半透明) ★
           ================================================================
        */
        [data-testid="stSidebar"] {{
            /* 背景: 白の半透明 */
            background-color: rgba(255, 255, 255, 0.85) !important;
            
            /* すりガラス効果 */
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            
            /* 境界線 */
            border-right: 1px solid #e2e8f0 !important;
        }}
        
        /* サイドバー内の文字 */
        [data-testid="stSidebar"] * {{
            color: #333333 !important;
            text-shadow: none !important;
        }}
        /* サイドバーの閉じるボタン */
        [data-testid="stSidebarNavCollapseButton"] {{
            color: #333333 !important;
        }}

        /* 
           ================================================================
           ★ アニメーション定義 (下からフワッと)
           ================================================================
        */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(40px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* 
           ================================================================
           ★ カードデザイン (白背景・影付き)
           ================================================================
        */
        .MieeL-card {{
            background-color: #ffffff;
            border: 2px solid #e2e8f0; /* 薄いグレーの枠線 */
            border-radius: 15px 15px 0 0;
            padding: 25px;
            margin-top: 20px;
            
            /* 影をつけて浮き上がらせる */
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            
            /* アニメーション設定 */
            opacity: 0; 
            animation-name: fadeInUp;
            animation-duration: 0.8s;
            animation-fill-mode: forwards;
            animation-timing-function: cubic-bezier(0.2, 0.8, 0.2, 1);
            
            min-height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }}
        
        .MieeL-card:hover {{
            border-color: #4a90e2; /* ホバーで青枠 */
            background-color: #f8fafc; /* ホバーでわずかに色を変える */
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(74, 144, 226, 0.15); /* 青い影 */
            transition: all 0.3s ease;
        }}

        .card-title {{
            font-size: 1.4rem;
            font-weight: 900;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 10px;
            margin-bottom: 10px;
            color: #0f172a;
        }}
        
        .card-desc {{
            font-size: 1rem;
            line-height: 1.6;
            color: #475569;
        }}

        /* --- ボタン --- */
        .stButton > button {{
            width: 100%;
            background-color: #ffffff !important;
            border: 2px solid #e2e8f0 !important;
            border-top: none !important;
            border-radius: 0 0 15px 15px !important;
            color: #4a90e2 !important;
            font-weight: bold !important;
            padding: 10px !important;
            margin-top: -16px !important;
            transition: all 0.3s ease !important;
            position: relative;
            z-index: 5;
            
            opacity: 0;
            animation-name: fadeInUp;
            animation-duration: 0.8s;
            animation-fill-mode: forwards;
            animation-delay: 1s;
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
            animation: float 6s ease-in-out infinite;
        }}
        
        .logo-img {{
            width: 180px;
            height: auto;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
            margin-right: 30px;
        }}
        
        .main-title {{
            font-size: 5rem;
            font-weight: 900;
            line-height: 1;
            margin: 0;
            color: #0f172a; /* 濃紺 */
            text-shadow: none;
        }}
        
        .sub-title {{
            font-size: 1.5rem;
            color: #475569;
            letter-spacing: 0.2em;
            font-weight: 700;
            margin-top: 10px;
        }}

        /* --- 説明文プレート --- */
        .glass-plate {{
            background-color: #f0f9ff; /* 薄い青 */
            border: 2px solid #4a90e2;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            opacity: 0;
            animation: fadeInUp 1s ease-in-out forwards;
            animation-delay: 0.2s;
        }}

        /* --- ダイアログ(マニュアル) --- */
        div[role="dialog"] {{
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 15px !important;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15) !important;
        }}
        div[role="dialog"] p, div[role="dialog"] li, div[role="dialog"] span, div[role="dialog"] div {{
            color: #333333 !important;
            text-shadow: none !important;
            font-weight: 400 !important;
            line-height: 1.8 !important;
        }}
        div[role="dialog"] h3 {{
            color: #0f172a !important;
            text-shadow: none !important;
            border-bottom: 1px solid #4a90e2 !important;
            padding-bottom: 10px !important;
            margin-bottom: 15px !important;
        }}
        div[role="dialog"] strong {{
            color: #0f172a !important;
            font-weight: 900 !important;
            background-color: #f1f5f9;
            padding: 2px 5px;
            border-radius: 4px;
        }}

        hr {{ border-color: #cbd5e1; }}
        a {{ color: #2563eb !important; font-weight: bold; text-decoration: none; }}
        a:hover {{ text-decoration: underline; color: #1e40af !important; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# ==========================================
# 4. マニュアルデータ
# ==========================================
manuals = {
    "guidance": """
    ### 📚 指導支援内容 マニュアル
    **概要**  
    お子さんの日常生活の困りごとに応じた、具体的な指導・支援のアイデアを検索できます。

    **使い方**  
    1.  **3つのステップで選択**:  
        画面のドロップダウンメニューを「カテゴリー」→「項目」→「詳細」の順に選択します。
    2.  **表示ボタン**:  
        「💡 適した指導・支援を表示」ボタンをクリックします。
    3.  **結果の確認**:  
        表示された内容を確認します。タイトルをクリックすると詳細が開きます。
    """,
    "chart": """
    ### 📊 発達チャート作成 マニュアル
    **概要**  
    発達段階を記録し、レーダーチャートで可視化・保存できます。

    **使い方**  
    1.  **入力**:  
        12のカテゴリーについて、現在の状況に最も近い段階を選択します。「▼ 目安を見る」で詳細を確認できます。
    2.  **作成**:  
        「📊 チャートを作成して書き込む」ボタンをクリックします。
    3.  **保存**:  
        スプレッドシートを開くか、Excel形式でダウンロードして保存します。
    """,
    "analysis": """
    ### 📈 分析方法 マニュアル
    **概要**  
    特別支援教育で活用できる様々な分析方法や療法について調べられます。

    **使い方**  
    *   **方法A**: サイドバーから知りたい療法（ABA、CBTなど）を直接選択します。
    *   **方法B**: メインエリアでお子さんの状況を選択し、有効な療法を検索します。
    """,
    "plan_creation": """
    ### 🤖 計画作成サポート マニュアル
    **概要**  
    生成AI（ChatGPTなど）に支援計画作成を依頼するための「プロンプト（命令文）」を作成します。

    **使い方**  
    1.  **選択**: プロンプトの種類（プランA・B用など）を選びます。
    2.  **入力**: お子さんの実態や課題、参考情報を入力します。
    3.  **生成**: 「プロンプトを生成」を押し、表示された文面をコピーしてAIチャットに貼り付けます。
    """,
    "lesson_plan_ai": """
    ### 📝 AI指導案作成 マニュアル
    **概要**  
    基本情報を入力するだけで、AIを活用して学習指導案（Excel）を自動生成します。

    **使い方**  
    1.  **入力**: 学部学年、教科単元などの基本情報を入力します。
    2.  **AI連携**: 「プロンプトを作成」し、ChatGPT等に入力してコード（JSON）を取得します。
    3.  **出力**: 取得したコードをアプリに入力し、「Excel作成実行」を押してダウンロードします。
    """,
    "guideline_page": """
    ### 📜 指導要領早引き マニュアル
    **概要**  
    学習指導要領の内容を素早く検索して閲覧できます。

    **使い方**  
    *   学部、障害種別（段階）、教科を選択して「表示する」ボタンをクリックしてください。
    """,
    "lesson_card_library": """
    ### 🃏 授業カード マニュアル
    **概要**  
    先生方が実践している授業のアイデアをカード形式で共有・検索できます。

    **使い方**  
    *   検索バーにキーワードを入れるか、ハッシュタグ（#高等部など）をクリックして授業を探します。
    *   カードをクリックすると詳細（略案PDFや動画）が見られます。
    """
}

# ==========================================
# 5. マニュアル表示用ダイアログ
# ==========================================
@st.dialog("📖 マニュアル")
def show_manual(key):
    st.markdown(manuals[key])

# ==========================================
# 6. ページ遷移ロジック
# ==========================================
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

  
# ==========================================
# 7. メインコンテンツ
# ==========================================

# ヘッダー (ロゴ+タイトル)
st.markdown(f"""
    <div class="header-wrapper">
        {logo_html}
        <div class="title-group">
            <h1 class="main-title">MieeL</h1>
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
    <p style="color: #4a90e2; font-weight: bold; margin-top: 15px; font-size: 1rem;">
        ▼ 下の各機能パネル、またはサイドバーのメニューから利用したい機能を選択してください。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📂 各機能の紹介")

# カードを描画する関数 (アニメーション遅延つき)
def render_card(title, desc, delay):
    st.markdown(f"""
    <div class="MieeL-card" style="animation-delay: {delay}s;">
        <div class="card-title">{title}</div>
        <div class="card-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

# --- 3カラムレイアウト ---
col1, col2, col3 = st.columns(3)

with col1:
    # 1. 指導支援内容 (Delay: 0.2s)
    render_card("📚 指導支援内容", "日常生活の困りごとに応じた、具体的な指導・支援のアイデアを検索できます。", 0.2)
    c_btn, c_pop = st.columns([3, 1])
    c_btn.button("使う ➡", on_click=set_page, args=("pages/1_指導支援内容.py",), key="btn_guidance")
    if c_pop.button("📖", key="m_guidance"): show_manual("guidance")

    # 2. 分析方法 (Delay: 0.5s)
    render_card("📈 分析方法", "教育学や心理学に基づいた分析手法の解説とツールです。", 0.5)
    c_btn, c_pop = st.columns([3, 1])
    c_btn.button("使う ➡", on_click=set_page, args=("pages/3_分析方法.py",), key="btn_analysis")
    if c_pop.button("📖", key="m_analysis"): show_manual("analysis")
    
    # 3. 授業カード (Delay: 0.8s)
    render_card("🃏 授業カード", "先生方の授業アイデアを共有・検索できるライブラリです。", 0.8)
    c_btn, c_pop = st.columns([3, 1])
    c_btn.button("使う ➡", on_click=set_page, args=("pages/8_授業カードライブラリー.py",), key="btn_lesson_card_library")
    if c_pop.button("📖", key="m_card"): show_manual("lesson_card_library")

with col2:
    # 4. 発達チャート (Delay: 0.3s)
    render_card("📊 発達チャート", "発達段階を記録し、レーダーチャートで可視化・保存します。", 0.3)
    c_btn, c_pop = st.columns([3, 1])
    c_btn.button("使う ➡", on_click=set_page, args=("pages/2_発達チャート.py",), key="btn_chart")
    if c_pop.button("📖", key="m_chart"): show_manual("chart")
    
    # 5. AI計画作成 (Delay: 0.6s)
    render_card("🤖 AI計画作成", "個別の支援・指導計画作成用のプロンプトを簡単に生成します。", 0.6)
    c_btn, c_pop = st.columns([3, 1])
    c_btn.button("使う ➡", on_click=set_page, args=("pages/4_AIによる支援,指導計画作成.py",), key="btn_plan_creation")
    if c_pop.button("📖", key="m_plan"): show_manual("plan_creation")

    # 9. AIによる指導案作成 (Delay: 0.9s)
    render_card("📝 AI指導案作成", "基本情報を入力するだけで、AIを活用して学習指導案を自動生成します。", 0.9)
    c_btn, c_pop = st.columns([3, 1])
    c_btn.button("使う ➡", on_click=set_page, args=("pages/9_AIによる指導案作成.py",), key="btn_lesson_plan_ai")
    if c_pop.button("📖", key="m_lesson"): show_manual("lesson_plan_ai")

with col3:
    # 6. 学習指導要領 (Delay: 0.4s)
    render_card("📜 指導要領早引き", "学部・段階ごとの学習指導要領の内容を素早く検索できます。", 0.4)
    c_btn, c_pop = st.columns([3, 1])
    c_btn.button("使う ➡", on_click=set_page, args=("pages/6_知的段階_早引き学習指導要領.py",), key="btn_guideline_page")
    if c_pop.button("📖", key="m_guide"): show_manual("guideline_page")

    # 7. 動画ギャラリー (Delay: 0.7s)
    render_card("▶️ 動画ギャラリー", "特別支援教育に関する動画と解説をまとめています。", 0.7)
    st.button("見る ➡", on_click=set_page, args=("pages/7_動画ギャラリー.py",), key="btn_youtube_gallery")

    # 10. フィードバック (Delay: 1.0s)
    render_card("📝 フィードバック", "アプリの改善やご意見をお待ちしています。", 1.0)
    st.button("送る ➡", on_click=set_page, args=("pages/10_フィードバック.py",), key="btn_feedback")


# --- ▼ 関連ツール＆リンク ▼ ---
st.markdown("<br>", unsafe_allow_html=True)

# リンク集もアニメーション
st.markdown("""
<div class="glass-plate" style="padding: 15px; margin-bottom: 20px; border-color: #ffffff; animation-delay: 1.2s;">
    <h3 style="margin-bottom: 0 !important; border: none;">🔗 研究・分析ツール (External Links)</h3>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown("""
    <div class="MieeL-card" style="min-height: auto; animation-delay: 1.3s;">
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
    <div class="MieeL-card" style="min-height: auto; animation-delay: 1.4s;">
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
<div class="glass-plate" style="text-align: center; animation-delay: 1.5s;">
    <h5 style="color: #0f172a;">🗨️ ご意見・ご感想</h5>
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