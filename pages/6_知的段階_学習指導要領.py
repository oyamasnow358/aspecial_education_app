# pages/6_知的段階_学習指導要領.py
import streamlit as st
# ステップ1で作成したデータファイルをインポート
from guideline_data import data

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
        
        /* --- st.infoのカスタムスタイル --- */
        .st-emotion-cache-1wivap1 {
             background-color: rgba(232, 245, 253, 0.7);
             border-left: 5px solid #4a90e2;
             border-radius: 8px;
        }
        
        /* --- st.expanderのデフォルトアイコン（文字化けしているもの）を非表示にする */
        [data-testid="stExpanderToggleIcon"] {
            display: none;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
# --- ▲ 共通CSSの読み込み ▲ ---

# ▼▼▼【ここから修正・追加】▼▼▼
def format_guideline_text(text):
    """
    学習指導要領のテキストの改行とインデントを維持して表示するためのフォーマット関数
    - 全角スペースをHTMLのエンティティに変換してインデントを表現
    - 改行コードをMarkdownの強制改行に変換
    """
    if not isinstance(text, str):
        return ""
    
    # 全角スペースをインデントとして保持するために変換します。
    # 全角1文字を半角スペース2つ分の幅として `&nbsp;&nbsp;` に置き換えます。
    processed_text = text.replace("　", "&nbsp;&nbsp;")
    
    # 改行をMarkdownの強制改行（半角スペース2つ + 改行）に変換します。
    processed_text = processed_text.replace("\n", "  \n")
    
    return processed_text
# ▲▲▲【ここまで修正・追加】▲▲▲

st.set_page_config(
    page_title="知的段階（学習指導要領）",
    page_icon="📜",
    layout="wide",
)

load_css()

st.title("📜 知的段階（学習指導要領）")

st.info("学部、段階（障害種別）、教科を選択すると、関連する学習指導要領の内容が表示されます。")

# --- 選択肢（変更なし） ---
col1, col2, col3 = st.columns(3)

with col1:
    # 学部選択
    selected_gakubu = st.selectbox(
        "**1. 学部を選択**",
        options=list(data.keys())
    )

with col2:
    # 段階（障害種別）選択
    shubetsu_options = list(data[selected_gakubu].keys())
    selected_shubetsu = st.selectbox(
        "**2. 段階（障害種別）を選択**",
        options=shubetsu_options
    )

# 知的障害者の場合のみ教科選択を表示
is_chiteki = "知的障害者" in selected_shubetsu
if is_chiteki:
    with col3:
        kyoka_options = list(data[selected_gakubu][selected_shubetsu].keys())
        selected_kyoka = st.selectbox(
            "**3. 教科を選択**",
            options=kyoka_options
        )
else:
    selected_kyoka = None


st.markdown("---")


# --- 内容表示 ---
if st.button("表示する", type="primary", use_container_width=True):
    st.header(f"表示結果：{selected_gakubu} - {selected_shubetsu}" + (f" - {selected_kyoka}" if is_chiteki else ""))
    
    with st.container(border=True):
        # ▼▼▼【ここから修正】▼▼▼
        # 知的障害者以外の場合の表示
        if not is_chiteki:
            shubetsu_data = data[selected_gakubu][selected_shubetsu]
            st.subheader("全体")
            # format_guideline_text関数を適用
            st.markdown(format_guideline_text(shubetsu_data.get("全体", "データがありません。")), unsafe_allow_html=True)

            if "全体" in shubetsu_data:
                # 各障害種別の詳細を表示
                for key, value in shubetsu_data.items():
                    if key != "全体":
                        with st.expander(f"**{key}**"):
                            # format_guideline_text関数を適用
                            st.markdown(format_guideline_text(value), unsafe_allow_html=True)

        # 知的障害者の場合の表示
        else:
            if selected_kyoka:
                kyoka_data = data[selected_gakubu][selected_shubetsu][selected_kyoka]
                
                # 目標
                if "目標" in kyoka_data:
                    st.subheader("🎯 目標")
                    # format_guideline_text関数を適用
                    st.markdown(format_guideline_text(kyoka_data["目標"]), unsafe_allow_html=True)

                # 各段階をタブで表示
                段階keys = [key for key in kyoka_data.keys() if "段階" in key]
                if 段階keys:
                    tabs = st.tabs(段階keys)
                    for i, dankai_key in enumerate(段階keys):
                        with tabs[i]:
                            dankai_data = kyoka_data[dankai_key]
                            if "目標" in dankai_data:
                                st.markdown("#### **目標**")
                                # format_guideline_text関数を適用
                                st.markdown(format_guideline_text(dankai_data["目標"]), unsafe_allow_html=True)
                            if "内容" in dankai_data:
                                st.markdown("#### **内容**")
                                # format_guideline_text関数を適用
                                st.markdown(format_guideline_text(dankai_data["内容"]), unsafe_allow_html=True)

                # 指導計画の作成と内容の取扱い
                if "指導計画の作成と内容の取扱い" in kyoka_data:
                    with st.expander("**指導計画の作成と内容の取扱い**"):
                        # format_guideline_text関数を適用
                        st.markdown(format_guideline_text(kyoka_data["指導計画の作成と内容の取扱い"]), unsafe_allow_html=True)
                
                # 全体指導計画 (小学部、中学部でキーが異なる場合も考慮)
                overall_plan_key = next((key for key in kyoka_data if "全体指導計画" in key), None)
                if overall_plan_key:
                     with st.expander(f"**{overall_plan_key}**"):
                        # format_guideline_text関数を適用
                        st.markdown(format_guideline_text(kyoka_data[overall_plan_key]), unsafe_allow_html=True)

            else:
                st.warning("教科を選択してください。")
        # ▲▲▲【ここまで修正】▲▲▲