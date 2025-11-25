import streamlit as st

# ==========================================
# 0. ページ設定
# ==========================================
st.set_page_config(
    page_title="Mirairo - 動画ギャラリー",
    page_icon="▶️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. デザイン定義 (Mirairo共通・白枠線・アニメーション)
# ==========================================
def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = """
    <style>
        /* --- 全体 --- */
        html, body, [class*="css"] {
            font-family: 'Noto Sans JP', sans-serif !important;
        }

        /* --- 背景 (黒) --- */
        [data-testid="stAppViewContainer"] {
            background-color: #000000;
            background-image: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-attachment: fixed;
        }

        /* --- 文字色 (白・影付き) --- */
        h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown, .stRadio label {
            color: #ffffff !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.9) !important;
        }

        /* --- サイドバー --- */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        [data-testid="stSidebarNavCollapseButton"] { color: #fff !important; }

        /* --- 機能カード (白枠・アニメーション) --- */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        [data-testid="stBorderContainer"] {
            background-color: #151515 !important;
            border: 2px solid #ffffff !important;
            border-radius: 16px !important;
            padding: 20px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.8) !important;
            animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        }
        
        [data-testid="stBorderContainer"]:hover {
            border-color: #4a90e2 !important;
            background-color: #000000 !important;
            transform: translateY(-5px);
            box-shadow: 0 0 20px rgba(74, 144, 226, 0.4) !important;
            transition: all 0.3s ease;
        }

        /* --- ボタン --- */
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

        /* --- タブのデザイン調整 --- */
        .stTabs [data-testid="stTab"] {
            background-color: transparent;
            border: 1px solid #555;
            border-bottom: none;
            color: #ccc;
            border-radius: 5px 5px 0 0;
        }
        .stTabs [data-testid="stTab"][aria-selected="true"] {
            background-color: #4a90e2;
            color: #fff;
            border: none;
        }
        .stTabs [data-testid="stVerticalBlock"] {
            background-color: transparent;
            border: none;
            box-shadow: none;
        }

        /* --- 戻るボタン --- */
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
        
        hr { border-color: #666; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# --- ▼ 戻るボタン ▼ ---
st.markdown('<div class="back-link"><a href="Home" target="_self">« TOPページに戻る</a></div>', unsafe_allow_html=True)

st.title("▶️ YouTube動画ギャラリー")
st.markdown("""
<div style="background: rgba(255,255,255,0.05); border: 1px solid #fff; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
    気になるトピックを選んで、関連する動画と解説をご覧ください。
</div>
""", unsafe_allow_html=True)

# ==========================================
# 2. データ定義
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
# 3. メインコンテンツ (タブ表示)
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
            
            # カードデザインで表示
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
# 4. フッター (リンク集)
# ==========================================
with st.expander("🔗 関連ツール＆リンク"):
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