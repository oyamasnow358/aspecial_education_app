import streamlit as st
import base64
import os
from pathlib import Path

# ==========================================
# 0. ページ設定
# ==========================================
st.set_page_config(
    page_title="MieeL - 動画ギャラリー",
    page_icon="▶️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. 画像処理 (ロゴ読み込み)
# ==========================================
def get_img_as_base64(file):
    try:
        # 画像パスを絶対パスで解決
        script_path = Path(__file__)
        app_root = script_path.parent.parent
        img_path = app_root / file
        
        with open(img_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

logo_path = "MieeL2.png"
logo_b64 = get_img_as_base64(logo_path)
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img">' if logo_b64 else '<div class="logo-placeholder">▶️</div>'

# ==========================================
# 2. デザイン定義 (白ベース・視認性重視 + アニメーション)
# ==========================================
def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = f"""
    <style>
        /* --- 全体フォント --- */
        html, body, [class*="css"] {{
            font-family: 'Noto Sans JP', sans-serif !important;
            color: #1a1a1a !important;
            line-height: 1.6 !important;
        }}

        /* --- 背景 (白92%透過・画像あり) --- */
        [data-testid="stAppViewContainer"] {{
            background-color: #ffffff;
            background-image: linear-gradient(rgba(255,255,255,0.92), rgba(255,255,255,0.92)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-attachment: fixed;
            padding-left: 20px;
            padding-right: 20px;
        }}

        /* --- 見出し (濃紺・くっきり) --- */
        h1, h2, h3, h4, h5, h6 {{
            color: #0f172a !important;
            font-weight: 700 !important;
            text-shadow: none !important;
        }}
        p, span, div, label, .stMarkdown {{
            color: #333333 !important;
            text-shadow: none !important;
        }}
        
        /* --- ヘッダーアニメーション --- */
        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}
        
        .header-container {{
            display: flex;
            align-items: center;
            justify-content: center; /* 中央寄せ */
            gap: 20px;
            padding: 40px 0;
            border-bottom: 2px solid #f1f5f9;
            margin-bottom: 30px;
            animation: float 6s ease-in-out infinite;
        }}
        
        .logo-img {{
            width: 80px;
            height: auto;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
        }}
        .logo-placeholder {{
            font-size: 4rem;
            margin-right: 15px;
            animation: float 6s ease-in-out infinite;
        }}
        
        .page-title {{
            font-size: 3rem;
            font-weight: 900;
            color: #0f172a;
            margin: 0;
            line-height: 1.2;
        }}
        
        .page-subtitle {{
            font-size: 1.2rem;
            color: #475569;
            font-weight: bold;
            margin-top: 5px;
        }}

        /* --- サイドバー (すりガラス効果) --- */
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid #e2e8f0 !important;
        }}
        [data-testid="stSidebar"] * {{
            color: #333333 !important;
        }}

        /* --- 機能カード (白背景・影付き・ぬるっと出現) --- */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(40px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        [data-testid="stBorderContainer"] {{
            background-color: #ffffff !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 15px !important;
            padding: 25px !important;
            margin-bottom: 25px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
            
            opacity: 0; 
            animation-name: fadeInUp;
            animation-duration: 0.8s;
            animation-fill-mode: forwards;
            animation-timing-function: cubic-bezier(0.2, 0.8, 0.2, 1);
        }}
        
        [data-testid="stBorderContainer"]:hover {{
            border-color: #4a90e2 !important;
            background-color: #f8fafc !important;
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(74, 144, 226, 0.15) !important;
            transition: all 0.3s ease;
        }}

        /* --- タブ --- */
        .stTabs [data-testid="stTab"] {{
            background-color: transparent;
            border-bottom: 2px solid transparent;
            color: #64748b;
            font-weight: bold;
            transition: all 0.3s;
        }}
        .stTabs [data-testid="stTab"]:hover {{
            color: #4a90e2;
        }}
        .stTabs [data-testid="stTab"][aria-selected="true"] {{
            color: #4a90e2;
            border-bottom: 3px solid #4a90e2;
        }}
        
        /* --- ボタン --- */
        .stButton > button {{
            width: 100%;
            background-color: #ffffff !important;
            border: 2px solid #e2e8f0 !important;
            color: #4a90e2 !important;
            font-weight: bold !important;
            border-radius: 30px !important;
            padding: 10px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
        }}
        .stButton > button:hover {{
            background-color: #4a90e2 !important;
            color: #ffffff !important;
            border-color: #4a90e2 !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(74, 144, 226, 0.2) !important;
        }}

        /* --- 説明文ボックス --- */
        .info-box {{
            background-color: #f0f9ff;
            border: 2px solid #4a90e2;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(74,144,226,0.1);
            margin-bottom: 25px;
            color: #0c4a6e;
            animation: fadeInUp 0.8s ease-out forwards;
        }}

        /* --- 戻るボタン (指定デザイン) --- */
        .back-link {{
            margin-bottom: 20px;
        }}
        .back-link a {{
            display: inline-block;
            padding: 10px 20px;
            background: #ffffff;
            border: 2px solid #e2e8f0;
            border-radius: 25px;
            color: #4a90e2 !important;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        .back-link a:hover {{
            background: #4a90e2;
            color: #ffffff !important;
            border-color: #4a90e2;
            box-shadow: 0 4px 10px rgba(74, 144, 226, 0.2);
        }}
        
        /* エキスパンダー */
        .streamlit-expanderHeader {{
            background-color: #f8fafc !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            color: #0f172a !important;
        }}
        .streamlit-expanderContent {{
            background-color: #ffffff !important;
            color: #333333 !important;
        }}
        
        hr {{ border-color: #cbd5e1; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# --- ▼ 戻るボタン (★正しいリンクに変更済み) ▼ ---
st.markdown('<div class="back-link"><a href="https://aspecialeducationapp-6iuvpdfjbflp4wyvykmzey.streamlit.app/" target="_self">« TOPページに戻る</a></div>', unsafe_allow_html=True)

# ==========================================
# 3. メインコンテンツ (ロゴ入りヘッダー)
# ==========================================

st.markdown(f"""
    <div class="header-container">
        {logo_html}
        <div>
            <h1 class="page-title">YouTube動画ギャラリー</h1>
            <div class="page-subtitle">MieeL Video Library</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>🎯 使い方：</strong><br>
    気になるトピックのタブを選んで、関連する動画と解説をご覧ください。
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. データ定義
# ==========================================
youtube_data = {
    "ダウン症": {
        "video_id": "7gBd_iYF7TI", 
        "description": "ダウン症に関する基本的な情報、特性、そして支援のポイントを解説します。社会生活や学習における具体的なアプローチについても触れています。",
        "available": True
    },
    "自閉症スペクトラム（ASD）": {
        "video_id": "FyFmvcWrrvM", 
        "description": "自閉症スペクトラム障害（ASD）の基本的な理解を深めます。コミュニケーションや社会性の特性、感覚過敏などについて詳しく説明し、効果的な支援方法を提案します。",
        "available": True
    },
    "自閉症スペクトラムの5種類": {
        "video_id": "b7nnOId_NVo",
        "description": "かつての分類（アスペルガー症候群、カナー型自閉症など）とその特徴について解説します。",
        "available": True
    },
    "応用行動分析（ABA）": {
        "video_id": "CTd1gLHEFYM", 
        "description": "応用行動分析（ABA）の基本原則と、それが特別支援教育においてどのように活用されるかを解説します。",
        "available": True
    },
    "注意欠如・多動症（ADHD）": {
        "video_id": "pzM3-J1LUG4", 
        "description": "ADHDの特性を理解し、集中力の困難、多動性、衝動性に対する具体的な支援策を学びます。",
        "available": True
    },
    "高機能学習障害（LD）": {
        "video_id": "j9_vT7bJ47I", 
        "description": "読み書き、計算など特定の学習領域に困難を抱えるLDについて、その特性と個別の指導法を解説します。",
        "available": True
    },
    "卒業後の進路": {
        "video_id": "rFjB2v3Hw24", 
        "description": "特別支援学校卒業後の進路選択について、就労支援、進学、地域生活支援などを解説します。",
        "available": False
    },
    "動作法": {
        "video_id": None, 
        "description": "身体運動を通して心の状態を安定させ、自己肯定感を育む支援方法です。",
        "available": False
    },
    "最新のICT教材": {
        "video_id":  None, 
        "description": "タブレットアプリ、オンラインツール、ロボット教材など、学習意欲を高めるための多様なツールを紹介します。",
        "available": False
    },
    "スイッチ教材": {
        "video_id":  None, 
        "description": "重度の肢体不自由や認知発達の遅れがある子どもたちへのスイッチ教材活用事例を紹介します。",
        "available": False
    },
}

# ==========================================
# 5. タブ表示エリア
# ==========================================

# available=True の項目のみをタブとして表示
available_topics = {k: v for k, v in youtube_data.items() if v["available"]}
sorted_topics = sorted(available_topics.keys()) 

if not sorted_topics:
    st.info("現在、表示できる動画トピックはありません。")
else:
    # タブを作成
    tabs = st.tabs(sorted_topics)

    # 各タブの内容を定義
    for i, topic_name in enumerate(sorted_topics):
        with tabs[i]:
            topic_data = youtube_data[topic_name]
            
            # ぬるっと動く白枠カードで表示
            with st.container(border=True):
                st.subheader(topic_name)
                st.write(topic_data["description"])

                if topic_data["video_id"]:
                    st.markdown("#### 📺 関連動画")
                    st.video(f"https://www.youtube.com/watch?v={topic_data['video_id']}")
                    st.markdown(f"動画をYouTubeで見る: [🔗 {topic_name}](https://www.youtube.com/watch?v={topic_data['video_id']})")
                else:
                    st.info("💡 このトピックに関する動画は現在準備中です。")

st.markdown("---")

# ==========================================
# 6. フッター (リンク集)
# ==========================================
with st.expander("🔗 関連ツール＆リンク"):
    # リンク集もカードデザインで
    with st.container(border=True):
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