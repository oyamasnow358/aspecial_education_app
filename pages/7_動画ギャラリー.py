import streamlit as st
import base64
import os

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
# 1. 画像処理 (ロゴ読み込み)
# ==========================================
def get_img_as_base64(file):
    try:
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

logo_path = "mirairo.png"
logo_b64 = get_img_as_base64(logo_path)
# ロゴ画像がない場合はプレースホルダーを表示
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img">' if logo_b64 else '<div style="font-size:50px;">🌟</div>'

# ==========================================
# 2. デザイン定義 (白ベース・視認性重視 + ロゴアニメーション)
# ==========================================
def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = """
    <style>
        /* --- 全体フォント --- */
        html, body, [class*="css"] {
            font-family: 'Noto Sans JP', sans-serif !important;
            color: #1a1a1a !important;
            line-height: 1.6 !important;
        }

        /* --- 背景 (白95%透過) --- */
        [data-testid="stAppViewContainer"] {
            background-color: #ffffff;
            background-image: linear-gradient(rgba(255,255,255,0.95), rgba(255,255,255,0.95)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-attachment: fixed;
        }

        /* --- 見出し --- */
        h1, h2, h3, h4, h5, h6 {
            color: #0f172a !important;
            font-weight: 700 !important;
            text-shadow: none !important;
        }
        
        /* --- ヘッダーアニメーション (ロゴとタイトル) --- */
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-6px); }
            100% { transform: translateY(0px); }
        }
        
        .header-container {
            display: flex;
            align-items: center;
            gap: 20px;
            padding-bottom: 20px;
            border-bottom: 2px solid #f1f5f9;
            margin-bottom: 30px;
            animation: float 6s ease-in-out infinite; /* ゆらゆら動く */
        }
        
        .logo-img {
            width: 80px; /* ロゴサイズ */
            height: auto;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
        }
        
        .page-title {
            font-size: 2.2rem;
            font-weight: 900;
            color: #0f172a;
            margin: 0;
            line-height: 1.2;
        }
        
        .page-subtitle {
            font-size: 1rem;
            color: #64748b;
            font-weight: 500;
        }

        /* --- サイドバー --- */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #e2e8f0;
        }
        [data-testid="stSidebarNavCollapseButton"] { color: #333 !important; }

        /* --- 機能カード (白背景・影付き) --- */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        [data-testid="stBorderContainer"] {
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 12px !important;
            padding: 25px !important;
            margin-bottom: 25px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
            animation: fadeInUp 0.6s ease-out forwards;
        }
        
        [data-testid="stBorderContainer"]:hover {
            border-color: #4a90e2 !important;
            box-shadow: 0 8px 24px rgba(74, 144, 226, 0.15) !important;
            transform: translateY(-2px);
            transition: all 0.3s ease;
        }

        /* --- タブ --- */
        .stTabs [data-testid="stTab"] {
            background-color: transparent;
            border-bottom: 2px solid #e2e8f0;
            color: #64748b;
            font-weight: 600;
        }
        .stTabs [data-testid="stTab"][aria-selected="true"] {
            color: #4a90e2;
            border-bottom: 2px solid #4a90e2;
        }
        
        /* --- ボタン --- */
        .stButton > button {
            width: 100%;
            background-color: #ffffff !important;
            border: 2px solid #4a90e2 !important;
            color: #4a90e2 !important;
            font-weight: bold !important;
            border-radius: 30px !important;
            transition: all 0.3s ease !important;
        }
        .stButton > button:hover {
            background-color: #4a90e2 !important;
            color: #ffffff !important;
        }

        /* --- 説明文ボックス --- */
        .info-box {
            background-color: #f0f9ff;
            border-left: 6px solid #4a90e2;
            padding: 20px;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 25px;
            color: #0c4a6e;
        }

        /* --- 戻るボタン --- */
        .back-link a {
            display: inline-block;
            padding: 10px 20px;
            background: #ffffff;
            border: 1px solid #4a90e2;
            border-radius: 25px;
            color: #4a90e2 !important;
            text-decoration: none;
            margin-bottom: 20px;
            transition: all 0.3s;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .back-link a:hover {
            background: #4a90e2;
            color: #ffffff !important;
            box-shadow: 0 4px 8px rgba(74, 144, 226, 0.3);
        }
        
        hr { border-color: #cbd5e1; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# --- ▼ 戻るボタン ▼ ---
st.markdown('<div class="back-link"><a href="Home" target="_self">« TOPページに戻る</a></div>', unsafe_allow_html=True)

# ==========================================
# 3. メインコンテンツ (ロゴ入りヘッダー)
# ==========================================

# st.title の代わりにカスタムHTMLヘッダーを使用
st.markdown(f"""
    <div class="header-container">
        {logo_html}
        <div>
            <h1 class="page-title">YouTube動画ギャラリー</h1>
            <div class="page-subtitle">Mirairo Video Library</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>使い方：</strong><br>
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
            
            # カードデザインで表示 (白背景・影付き)
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