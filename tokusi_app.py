import streamlit as st
from PIL import Image
import time

# --- ページ設定 ---
st.set_page_config(
    page_title="Mirairo - Data-Driven Education",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed" # メニューはメイン画面で操作するため閉じ気味に
)

# --- 状態管理 (画面遷移用) ---
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'HOME'

def change_view(view_name):
    st.session_state.current_view = view_name

def go_home():
    st.session_state.current_view = 'HOME'

# ページ遷移用関数 (既存のpagesフォルダへの遷移)
def set_page(page_name):
    st.switch_page(page_name)

# --- ▼ CSSデザイン (Mirairoテーマ) ▼ ---
def load_css():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        /* 全体フォント */
        html, body, [class*="css"] {
            font-family: 'Noto Sans JP', sans-serif;
        }
        
        /* カラー定義 */
        :root {
            --primary: #6a1b9a;
            --accent: #4a90e2;
            --bg-dark: #0e1117;
            --text-light: #fafafa;
            --card-bg: rgba(255, 255, 255, 0.05);
            --card-hover: rgba(255, 255, 255, 0.1);
        }

        /* タイトルスタイル */
        .mirairo-title {
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            background: linear-gradient(to right, #fff, #a5b4fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2em;
            letter-spacing: 0.05em;
        }
        .mirairo-subtitle {
            font-size: 1.2rem;
            color: #a0aec0;
            margin-bottom: 2em;
            border-left: 4px solid var(--accent);
            padding-left: 15px;
        }

        /* カードボタンスタイル (st.buttonのハック) */
        div.stButton > button {
            width: 100%;
            border: 1px solid rgba(250, 250, 250, 0.1) !important;
            background-color: var(--card-bg) !important;
            color: var(--text-light) !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            text-align: left !important;
            transition: all 0.3s ease !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: flex-start !important;
            height: auto !important;
        }
        div.stButton > button:hover {
            background-color: var(--card-hover) !important;
            border-color: var(--accent) !important;
            transform: translateY(-3px);
            box-shadow: 0 4px 20px rgba(74, 144, 226, 0.2);
        }
        div.stButton > button p {
            font-size: 1.2rem !important;
            font-weight: bold !important;
        }

        /* 戻るボタンのスタイル */
        .back-btn div.stButton > button {
            background-color: transparent !important;
            border: 1px solid #555 !important;
            padding: 0.5rem 1rem !important;
            width: auto !important;
        }

        /* アニメーション (ゆらぎ) */
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        .floating-logo {
            animation: float 4s ease-in-out infinite;
        }
        
        /* 情報カードのスタイル */
        .info-card {
            background-color: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
        }
        .info-title {
            font-weight: bold;
            color: var(--accent);
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
        }
        
        /* リンクのスタイル */
        a {
            color: var(--accent) !important;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# --- ▼ 画面描画ロジック ▼ ---

# 1. ヘッダー (常に表示)
c1, c2 = st.columns([1, 5])
with c1:
    # ロゴ画像 (ゆらゆらアニメーション付き)
    st.markdown('<div class="floating-logo">', unsafe_allow_html=True)
    st.image("https://i.imgur.com/AbUxfxP.png", use_container_width=True) # ※Mirairoロゴがあれば差し替えてください
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<h1 class="mirairo-title">Mirairo</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="mirairo-subtitle">
        Data-Driven Education.<br>
        指導案作成から統計分析までを一元化したプラットフォーム。
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 2. ビューの切り替え処理
if st.session_state.current_view == 'HOME':
    # === ホーム画面 (メニュー一覧) ===
    
    st.write("##### 📍 MENU SELECT")
    
    # グリッドレイアウト
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📂 Mirairo アプリ\n\n現場の困りごとを解決するツール群"):
            change_view('APPS')
        if st.button("🏫 導入校\n\n岩槻はるかぜ特別支援学校について"):
            change_view('SCHOOL')

    with col2:
        if st.button("📖 アプリマニュアル\n\n詳しい使い方・ガイド"):
            change_view('MANUAL')
        if st.button("📊 分析ツール\n\n研究論文・データ分析用 (外部連携)"):
            change_view('TOOLS')

    with col3:
        if st.button("🤝 つながり\n\nNetwork & Administrator"):
            change_view('NETWORK')

elif st.session_state.current_view == 'APPS':
    # === Mirairo アプリ一覧 ===
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← HOMEに戻る"):
        go_home()
    st.markdown('</div>', unsafe_allow_html=True)

    st.header("📂 Mirairo アプリ")
    st.write("利用したいアプリケーションを選択してください。")

    row1 = st.columns(2)
    with row1[0]:
        st.info("🔍 日常の困りごとに")
        if st.button("指導支援内容 検索 ➡"):
            set_page("pages/1_指導支援内容.py")
    with row1[1]:
        st.info("📊 発達の記録・可視化")
        if st.button("発達チャート作成 ➡"):
            set_page("pages/2_発達チャート.py")

    row2 = st.columns(2)
    with row2[0]:
        st.info("📝 AIで指導案作成")
        if st.button("AIによる指導案作成 ➡"):
            set_page("pages/9_AIによる指導案作成.py")
    with row2[1]:
        st.info("🤖 計画作成プロンプト")
        if st.button("AI計画作成サポート ➡"):
            set_page("pages/4_AIによる支援,指導計画作成.py")

    row3 = st.columns(2)
    with row3[0]:
        st.info("📜 学習指導要領")
        if st.button("知的段階 早引き ➡"):
            set_page("pages/6_知的段階_早引き学習指導要領.py")
    with row3[1]:
        st.info("🃏 授業・動画")
        c_a, c_b = st.columns(2)
        with c_a:
            if st.button("授業カード ➡"):
                set_page("pages/8_授業カードライブラリー.py")
        with c_b:
            if st.button("動画ギャラリー ➡"):
                set_page("pages/7_動画ギャラリー.py")

elif st.session_state.current_view == 'MANUAL':
    # === マニュアル ===
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← HOMEに戻る"):
        go_home()
    st.markdown('</div>', unsafe_allow_html=True)

    st.header("📖 アプリマニュアル")
    
    with st.expander("📚 指導支援内容 マニュアル", expanded=True):
        st.markdown(manuals["guidance"])
    with st.expander("📊 発達チャート作成 マニュアル"):
        st.markdown(manuals["chart"])
    with st.expander("🤖 AI計画作成サポート マニュアル"):
        st.markdown(manuals["plan_creation"])
    with st.expander("📝 AI指導案作成 マニュアル"):
        st.markdown(manuals["lesson_plan_ai"])
    with st.expander("📜 知的段階 早引き マニュアル"):
        st.markdown(manuals["guideline_page"])
    with st.expander("🃏 授業カードライブラリー マニュアル"):
        st.markdown(manuals["lesson_card_library"])
    with st.expander("📈 分析方法 マニュアル"):
        st.markdown(manuals["analysis"])

elif st.session_state.current_view == 'NETWORK':
    # === つながり (管理者紹介) ===
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← HOMEに戻る"):
        go_home()
    st.markdown('</div>', unsafe_allow_html=True)

    st.header("🤝 つながり (Network)")

    # 管理者カード
    st.markdown("""
    <div class="info-card" style="border-left: 5px solid #4a90e2;">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="background-color: #333; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px;">👤</div>
            <div>
                <div style="color: #4a90e2; font-size: 0.8em; font-weight: bold; letter-spacing: 2px;">ADMINISTRATOR</div>
                <div style="font-size: 1.8em; font-weight: bold;">KOYAMA</div>
                <div style="color: #aaa;">Special Education Teacher / App Developer</div>
            </div>
        </div>
        <hr style="border-color: rgba(255,255,255,0.1);">
        <p style="line-height: 1.6;">
            特別支援教育×データサイエンス。<br>
            現場の「感覚」や「経験」を、データという「根拠」で支えるためのツール開発を行っています。<br>
            埼玉県立岩槻はるかぜ特別支援学校 教諭。
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🌐 Information Tech Teachers")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">IT Teacher A</div>
            <div>High School Info Dept.</div>
            <div style="font-size: 0.9em; color: #888;">Network Specialist</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">IT Teacher B</div>
            <div>Special Ed. Coordinator</div>
            <div style="font-size: 0.9em; color: #888;">iPad Utilization Expert</div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_view == 'SCHOOL':
    # === 導入校 ===
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← HOMEに戻る"):
        go_home()
    st.markdown('</div>', unsafe_allow_html=True)

    st.header("🏫 導入校 (Introduction)")
    
    st.markdown("""
    <div class="info-card">
        <h3 style="margin-top:0;">埼玉県立岩槻はるかぜ特別支援学校</h3>
        <p>
            知的障害のある児童生徒が通う特別支援学校です。<br>
            ICTの積極的な活用や、データに基づいた指導の実践研究を行っています。
        </p>
        <div style="display:flex; gap:10px; margin-top:10px;">
            <span style="background:rgba(255,255,255,0.1); padding:2px 8px; border-radius:4px; font-size:0.8em;">小学部</span>
            <span style="background:rgba(255,255,255,0.1); padding:2px 8px; border-radius:4px; font-size:0.8em;">中学部</span>
            <span style="background:rgba(255,255,255,0.1); padding:2px 8px; border-radius:4px; font-size:0.8em;">高等部</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💡 Future Curriculum Design")
    st.info("""
    **【次年度予定】教育課程の未来デザイン研究**
    
    次年度より開始される研究プロジェクトの詳細をここに掲載予定です。
    データ利活用によるカリキュラム・マネジメントの実践事例などを発信していきます。
    """)

elif st.session_state.current_view == 'TOOLS':
    # === 分析ツール (研究者向け) ===
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← HOMEに戻る"):
        go_home()
    st.markdown('</div>', unsafe_allow_html=True)

    st.header("📊 分析ツール (For Researchers)")
    st.write("研究論文作成やデータ分析に活用できる専門ツール集です。")

    # ツールリスト
    tools = [
        {"name": "応用行動分析 (ABA)", "url": "https://abaapppy-k7um2qki5kggexf8qkfxjc.streamlit.app/"},
        {"name": "機能的行動評価", "url": "https://kinoukoudou-ptfpnkq3uqgaorabcyzgf2.streamlit.app/"},
        {"name": "アンケート統計分析", "url": "https://annketo12345py-edm3ajzwtsmmuxbm8qbamr.streamlit.app/"},
        {"name": "多変量回帰分析", "url": "https://kaikiapp-tjtcczfvlg2pyhd9bjxwom.streamlit.app/"},
        {"name": "t検定・統計ツール", "url": "https://tkentei-flhmnqnq6dti6oyy9xnktr.streamlit.app/"},
        {"name": "ノンパラメトリック分析", "url": "https://nonparametoric-nkk2awu6yv9xutzrjmrsxv.streamlit.app/"},
    ]

    cols = st.columns(2)
    for i, tool in enumerate(tools):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="info-card" style="padding: 15px;">
                <div style="font-weight:bold; margin-bottom:5px;">{tool['name']}</div>
                <a href="{tool['url']}" target="_blank" style="font-size:0.9em;">🔗 ツールを開く</a>
            </div>
            """, unsafe_allow_html=True)

# --- フッター ---
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8em;">
    &copy; 2025 Mirairo Project. All Rights Reserved.<br>
    Administrator: KOYAMA (Iwatsuki Harukaze Special Needs School)
</div>
""", unsafe_allow_html=True)