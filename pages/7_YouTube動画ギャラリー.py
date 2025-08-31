import streamlit as st

# --- ▼ 共通CSSの読み込み（変更なし） ▼ ---
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

        /* st.tabsのカスタムスタイル */
        /* タブのコンテナ */
        .stTabs [data-testid="stDataframeToolbar"] {
            background-color: transparent; /* 背景を透明に */
        }

        /* 個々のタブボタン */
        .stTabs [data-testid="stTab"] {
            background-color: #f0f2f6; /* タブの背景色 */
            border-radius: 8px 8px 0 0; /* 角を丸く */
            margin-right: 5px; /* タブ間のスペース */
            padding: 10px 20px; /* パディング */
            font-weight: bold;
            color: #31333F; /* テキスト色 */
            border: 1px solid #e0e0e0;
            border-bottom: none; /* 下線をなくす */
            transition: all 0.2s ease-in-out;
        }

        /* 選択されていないタブのホバー */
        .stTabs [data-testid="stTab"]:hover:not([aria-selected="true"]) {
            background-color: #e6e6f0;
            color: #8A2BE2;
        }
        
        /* 選択されているタブ */
        .stTabs [aria-selected="true"] {
            background-color: #ffffff !important; /* 選択中のタブは白 */
            border-color: #8A2BE2 !important; /* 選択中のタブのボーダー色 */
            color: #8A2BE2 !important; /* 選択中のタブのテキスト色 */
            border-bottom: 2px solid #ffffff !important; /* 下線と一体化 */
            margin-bottom: -2px; /* 下線と重なるように調整 */
        }

        /* タブの内容表示エリア */
        .stTabs [data-testid="stVerticalBlock"] {
            background-color: rgba(255, 255, 255, 0.95);
            border: 1px solid #e0e0e0;
            border-top: 2px solid #8A2BE2; /* 選択中のタブのアクセント色と合わせる */
            border-radius: 0 0 15px 15px; /* 下側の角を丸く */
            padding: 1.5em;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
            margin-bottom: 20px;
        }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
# --- ▲ 共通CSSの読み込み ▲ ---

st.set_page_config(
    page_title="YouTube動画ギャラリー",
    page_icon="▶️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSSを適用
load_css()

st.title("▶️ YouTube動画ギャラリー")
st.write("気になるトピックを選んで、関連する動画と解説をご覧ください。")

# YouTube動画データ
# 'video_id': YouTubeの動画ID (URLの `watch?v=` の後の部分)
# 'description': 動画に関連する簡単な説明
# 'available': True の場合のみサイドバーに表示される
youtube_data = {
    "ダウン症": {
        "video_id": "a9taFsRWB94", # サンプルID、実際のものに置き換えてください
        "description": "ダウン症に関する基本的な情報、特性、そして支援のポイントを解説します。社会生活や学習における具体的なアプローチについても触れています。",
        "available": True
    },
    "自閉症スペクトラム（ASD）": {
        "video_id": "d1_jbL7C36Q", # サンプルID
        "description": "自閉症スペクトラム障害（ASD）の基本的な理解を深めます。コミュニケーションや社会性の特性、感覚過敏などについて詳しく説明し、効果的な支援方法を提案します。",
        "available": True
    },
    "自閉症スペクトラムの5種類": {
        "video_id": "NhlGDcpYZ3E",
        "description": "現在では「自閉症スペクトラム障害」として診断が統合されていますが、かつてはアスペルガー症候群、カナー型自閉症など、いくつかのタイプに分類されていました。ここでは、それらの歴史的分類とその特徴について解説します。",
        "available": False # 動画がないので非表示
    },
    "応用行動分析（ABA）": {
        "video_id": "CTd1gLHEFYM", # サンプルID
        "description": "応用行動分析（ABA）の基本原則と、それが特別支援教育においてどのように活用されるかを解説します。具体的な行動変容の例や、家庭での応用についても紹介します。",
        "available": True
    },
    "注意欠如・多動症（ADHD）": {
        "video_id": "6LTzAhv_XfU", # サンプルID
        "description": "注意欠如・多動症（ADHD）の特性を理解し、集中力の困難、多動性、衝動性に対する支援策を学びます。学校や家庭での具体的な対応方法についても触れます。",
        "available": True
    },
    "高機能学習障害（LD）": {
        "video_id": "j9_vT7bJ47I", # サンプルID
        "description": "読み書き、計算など特定の学習領域に困難を抱える高機能学習障害（LD）について、その特性と個別の指導法を解説します。ICTを活用した学習支援についても紹介。",
        "available": True
    },
    
    #"卒業後の進路": {
    #    "video_id": "rFjB2v3Hw24", # サンプルID
    #    "description": "特別支援学校卒業後の進路選択について、就労支援、進学、地域生活支援など、様々な選択肢とそれらをサポートする制度について解説します。",
    #    "available": True
    #},
    #"動作法": {
    #    "video_id": None, # 動画がまだない場合
    #    "description": "動作法は、身体運動を通して心の状態を安定させ、自己肯定感を育む支援方法です。ここでは動作法の基本的な考え方と、実践例について解説します。",
    #    "available": False
    #},
    #"最新のICT教材": {
    #    "video_id":  None, # サンプルID
     #   "description": "特別支援教育で活用できる最新のICT教材を紹介します。タブレットアプリ、オンラインツール、ロボット教材など、学習意欲を高めるための多様なツールに焦点を当てます。",
     #   "available": True
    #},
    #"スイッチ教材": {
    #    "video_id":  None, # サンプルID
    #    "description": "重度の肢体不自由や認知発達の遅れがある子どもたちに、意思表示や操作の機会を提供するスイッチ教材について解説します。選び方や活用事例を紹介します。",
    #    "available": True
    #},
}

# --- メインコンテンツエリアにタブを表示 ---

# available=True の項目のみをタブとして表示
available_topics = {k: v for k, v in youtube_data.items() if v["available"]}
sorted_topics = sorted(available_topics.keys()) # 項目名をソート

if not sorted_topics:
    st.info("現在、表示できる動画トピックはありません。新しい動画が追加されるまでお待ちください。")
else:
    # タブを作成
    tabs = st.tabs(sorted_topics)

    # 各タブの内容を定義
    for i, topic_name in enumerate(sorted_topics):
        with tabs[i]:
            topic_data = youtube_data[topic_name]
            
            # タブ内の表示は、既存のカードデザインを踏襲
            with st.container(border=True):
                st.subheader(topic_name)
                st.write(topic_data["description"])

                # 動画IDが存在する場合のみ動画を表示
                if topic_data["video_id"]:
                    st.markdown("#### 関連動画")
                    # Streamlitの st.video を使用してYouTube動画を埋め込み
                    st.video(f"https://www.youtube.com/watch?v={topic_data['video_id']}")
                    
                    # YouTubeへの直接リンクも提供
                    st.markdown(f"動画をYouTubeで見る: [🔗 {topic_name}](https://www.youtube.com/watch?v={topic_data['video_id']})")
                else:
                    st.info("💡 このトピックに関する動画は現在準備中です。ご期待ください！")


# --- ▼ 関連ツール＆リンク（変更なし） ▼ ---
st.markdown("<hr class='footer-hr'>", unsafe_allow_html=True)
with st.container(border=True):
    st.header("関連ツール＆リンク")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### 📁 教育・心理分析ツール")
        st.page_link("https://abaapppy-k7um2qki5kggexf8qkfxjc.streamlit.app/", label="応用行動分析", icon="🔗")
        st.page_link("https://kinoukoudou-ptfpnkq3uqgaorabcyzgf2.streamlit.app/", label="機能的行動評価分析", icon="🔗")

    with c2:
        st.markdown("##### 📁 統計学分析ツール")
        st.page_link("https://annketo12345py-edm3ajzwtsmmuxbm8qbamr.streamlit.app/", label="アンケートデータ、総合統計分析", icon="🔗")
        st.page_link("https://soukan-jlhkdhkradbnxssy29aqte.streamlit.app/", label="相関分析", icon="🔗")
        st.page_link("https://kaikiapp-tjtcczfvlg2pyhd9bjxwom.streamlit.app/", label="多変量回帰分析", icon="🔗")
        st.page_link("https://tkentei-flhmnqnq6dti6oyy9xnktr.streamlit.app/", label="t検定", icon="🔗")
        st.page_link("https://rojisthik-buklkg5zeh6oj2gno746ix.streamlit.app/", label="ロジスティック回帰分析", icon="🔗")
        st.page_link("https://nonparametoric-nkk2awu6yv9xutzrjmrsxv.streamlit.app/", label="ノンパラメトリック統計分析", icon="🔗")

    st.markdown("---")
    st.markdown("##### 🗨️ ご意見・ご感想")
    st.markdown("自立活動の参考指導、各分析ツールにご意見がある方は以下のフォームから送ってください（埼玉県の学校教育関係者のみＳＴアカウントで回答できます）。")
    st.page_link("https://docs.google.com/forms/d/1dKzh90OkxMoWDZXV31FgPvXG5EvNlMFOrsPGvYTSC8/preview", label="アンケートフォーム", icon="📝")

st.markdown("<hr class='footer-hr'>", unsafe_allow_html=True)
st.warning("""
**【利用上の注意】**
それぞれのアプリに記載してある内容、分析ツールのデータや図、表を外部（研究発表など）で利用する場合は、管理者(岩槻はるかぜ特別支援学校 小山)までご相談ください。無断での転記・利用を禁じます。
""")