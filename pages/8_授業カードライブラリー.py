import streamlit as st
import pandas as pd
import base64
import re
import io
from io import BytesIO
import xlsxwriter
import hashlib 
import os 

# (※この方法はセキュリティ上、非推奨です。緊急回避策としてのみ使用してください。)
ADMIN_USERNAME = "admin" 
ADMIN_PASSWORD_HASH = hashlib.sha256("snow".encode()).hexdigest() 

def check_password(username, password):
    """ユーザー名とパスワードが管理者と一致するか確認"""
    if username == ADMIN_USERNAME:
        return hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH
    return False


# ページ設定
st.set_page_config(
    page_title="Mirairo - 授業カード",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSSを読み込む関数 (Mirairoデザイン + 授業カード専用スタイル)
def load_css():
    st.markdown(r"""
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
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
        h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown, .stSelectbox label, .stMultiSelect label, li {
            color: #ffffff !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.9) !important;
        }

        /* --- サイドバー (半透明) --- */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        [data-testid="stSidebarNavCollapseButton"] { color: #fff !important; }

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
        
        /* Primaryボタン */
        .stButton > button[kind="primary"] {
            background-color: #4a90e2 !important;
            color: #ffffff !important;
            border: 2px solid #4a90e2 !important;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #ffffff !important;
            color: #4a90e2 !important;
        }

        /* --- 入力フォーム --- */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] > div, .stMultiSelect div[data-baseweb="select"] > div {
            background-color: #222 !important;
            color: #fff !important;
            border-color: #555 !important;
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

        /* 
           ================================================================
           ★ 授業カードのグリッドとカードデザイン (Mirairo仕様)
           ================================================================
        */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .lesson-card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 30px;
            padding: 25px 0;
        }

        .lesson-card {
            background-color: #151515;
            border: 2px solid #ffffff; /* 白い太枠 */
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            display: flex;
            flex-direction: column;
            height: 100%;
            
            /* アニメーション */
            opacity: 0;
            animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
            transition: all 0.3s ease;
        }

        .lesson-card:hover {
            border-color: #4a90e2; /* ホバーで青枠 */
            transform: translateY(-10px) scale(1.02);
            background-color: #000000;
            box-shadow: 0 0 25px rgba(74, 144, 226, 0.4);
            z-index: 10;
        }

        .lesson-card-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-bottom: 1px solid #333;
        }

        .lesson-card-content {
            padding: 20px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .lesson-card-title {
            font-size: 1.4em;
            font-weight: 900;
            color: #ffffff;
            margin-bottom: 8px;
            line-height: 1.4;
            text-shadow: none;
        }

        .lesson-card-catchcopy {
            font-size: 0.95em;
            color: #bbbbbb !important;
            margin-bottom: 15px;
            font-style: italic;
            min-height: 3em;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-shadow: none;
        }

        .lesson-card-goal {
            font-size: 0.9em;
            color: #dddddd !important;
            margin-bottom: 12px;
            border-left: 4px solid #4a90e2;
            padding-left: 10px;
            line-height: 1.5;
            min-height: 60px;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-shadow: none;
        }

        .lesson-card-meta {
            font-size: 0.85em;
            color: #aaa;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }

        .lesson-card-meta span {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 4px 8px;
            border-radius: 4px;
            border: 1px solid #444;
            color: #fff !important;
        }

        .tag-badge {
            display: inline-block;
            background-color: rgba(74, 144, 226, 0.2);
            color: #4a90e2 !important;
            border-radius: 15px;
            padding: 4px 10px;
            font-size: 0.75em;
            margin-right: 5px;
            margin-bottom: 5px;
            border: 1px solid rgba(74, 144, 226, 0.4);
        }

        .card-subject-unit {
            font-size: 0.8em;
            color: #4a90e2 !important;
            font-weight: bold;
            margin-bottom: 10px;
            background-color: rgba(74, 144, 226, 0.1);
            padding: 4px 8px;
            border-radius: 4px;
            display: inline-block;
        }

        /* --- 詳細ページのスタイル --- */
        .detail-header {
            border-bottom: 1px solid #555;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        
        /* コンテナ (白枠) */
        [data-testid="stBorderContainer"] {
            background-color: #151515 !important;
            border: 2px solid #ffffff !important;
            border-radius: 16px !important;
            padding: 20px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.8) !important;
            animation: fadeInUp 0.5s ease-out;
        }

        /* フローのスタイル */
        .flow-section {
            background-color: #222;
            border-left: 4px solid #4a90e2;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 4px;
        }
        .flow-section h4 { color: #4a90e2 !important; margin: 0 0 10px 0; }
        .flow-list li { color: #ddd !important; margin-bottom: 5px; }

        hr { border-color: #666; }
    </style>
    """, unsafe_allow_html=True)

load_css()

# 戻るボタン (TOPページへのリンク)
st.markdown('<div class="back-link"><a href="Home" target="_self">« TOPページに戻る</a></div>', unsafe_allow_html=True)

# lesson_cards.csv の読み込み
LESSON_CARDS_CSV = "lesson_cards.csv"

def load_lesson_data():
    try:
        lesson_data_df = pd.read_csv(
            LESSON_CARDS_CSV,
            converters={
                'introduction_flow': lambda x: [item.strip() for item in x.split(';') if item.strip()] if pd.notna(x) else [],
                'activity_flow': lambda x: [item.strip() for item in x.split(';') if item.strip()] if pd.notna(x) else [],
                'reflection_flow': lambda x: [item.strip() for item in x.split(';') if item.strip()] if pd.notna(x) else [],
                'points': lambda x: [item.strip() for item in x.split(';') if item.strip()] if pd.notna(x) else [],
                'hashtags': lambda x: [item.strip() for item in x.split(',') if item.strip()] if pd.notna(x) else [],
                'material_photos': lambda x: [url.strip() for url in x.split(';') if url.strip()] if pd.notna(x) else [],
                'unit_name': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '単元なし',
                'unit_order': lambda x: int(x) if pd.notna(x) and str(x).strip().isdigit() else 9999,
                'unit_lesson_title': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '',
                'video_link': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '',
                'image': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '',
                'detail_word_url': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '',
                'detail_pdf_url': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '',
                'detail_ppt_url': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '',
                'detail_excel_url': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '',
                'target_grade': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '不明',
                'ict_use': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else 'なし',
                'subject': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else 'その他',
                'group_type': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '全体',
                'catch_copy': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '',
                'goal': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '',
                'disability_type': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '不明',
                'duration': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '不明',
                'materials': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '',
                'developmental_stage': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '不明', # 発達段階を追加
            }
        )

        # 必須カラムの確認とデフォルト値設定
        if 'unit_lesson_title' not in lesson_data_df.columns:
            lesson_data_df['unit_lesson_title'] = lesson_data_df['unit_name']
        else:
            lesson_data_df['unit_lesson_title'] = lesson_data_df.apply(
                lambda row: row['unit_name'] if str(row['unit_lesson_title']).strip() == '' else row['unit_lesson_title'],
                axis=1
            )
        
        # idカラムのユニーク性を保証
        if 'id' not in lesson_data_df.columns:
            lesson_data_df['id'] = range(1, len(lesson_data_df) + 1)
        else:
            lesson_data_df['id'] = lesson_data_df['id'].apply(lambda x: x if pd.notna(x) and isinstance(x, (int, float)) else 0)
            lesson_data_df['id'] = lesson_data_df['id'].astype(int)
            duplicated_ids = lesson_data_df[lesson_data_df.duplicated('id', keep='first')]['id'].unique()
            
            if len(duplicated_ids) > 0:
                st.warning(f"以下のIDが重複しています: {', '.join(map(str, duplicated_ids))}")
                next_id = lesson_data_df['id'].max() + 1
                for dup_id in duplicated_ids:
                    mask = (lesson_data_df['id'] == dup_id) & (~lesson_data_df.index.isin(lesson_data_df[lesson_data_df['id'] == dup_id].index[:1]))
                    lesson_data_df.loc[mask, 'id'] = range(next_id, next_id + mask.sum())
                    next_id += mask.sum()
                st.success("重複IDを修正しました。")
        
        return lesson_data_df.to_dict(orient='records')

    except FileNotFoundError:
        st.error(f"{LESSON_CARDS_CSV} ファイルが見つかりませんでした。pages フォルダと同じ階層に配置してください。")
        return []
    except Exception as e:
        st.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
        st.exception(e)
        return []

# データをロードし、session_stateに保存
if 'lesson_data' not in st.session_state:
    st.session_state.lesson_data = load_lesson_data()

# `lesson_cards.csv`にデータを保存する関数
def save_lesson_data(data):
    df_to_save = pd.DataFrame(data)
    # リスト形式のカラムをセミコロン/カンマ区切り文字列に戻す
    for col in ['introduction_flow', 'activity_flow', 'reflection_flow', 'points', 'material_photos']:
        df_to_save[col] = df_to_save[col].apply(lambda x: ';'.join(x) if isinstance(x, list) else x)
    if 'hashtags' in df_to_save.columns:
        df_to_save['hashtags'] = df_to_save['hashtags'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)

    # 必須カラムを維持し、並び順もテンプレートに合わせる
    for col in LESSON_CARD_COLUMNS:
        if col not in df_to_save.columns:
            df_to_save[col] = None # 存在しないカラムはNoneで追加
    
    df_to_save = df_to_save[LESSON_CARD_COLUMNS] # カラムの並びを固定

    try:
        df_to_save.to_csv(LESSON_CARDS_CSV, index=False, encoding='utf-8-sig')
        st.success("授業カードデータが更新され、CSVファイルに保存されました。")
    except Exception as e:
        st.error(f"CSVファイルの保存中にエラーが発生しました: {e}")
        st.exception(e)

# st.session_stateの初期化
if 'current_lesson_id' not in st.session_state:
    st.session_state.current_lesson_id = None
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'selected_hashtags' not in st.session_state:
    st.session_state.selected_hashtags = []
if 'selected_subject' not in st.session_state:
    st.session_state.selected_subject = "全て"
if 'show_all_flow' not in st.session_state:
    st.session_state.show_all_flow = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# ヘルパー関数
def set_detail_page(lesson_id):
    st.session_state.current_lesson_id = lesson_id
    st.session_state.show_all_flow = False

def back_to_list():
    st.session_state.current_lesson_id = None
    st.session_state.show_all_flow = False

def toggle_all_flow_display():
    st.session_state.show_all_flow = not st.session_state.show_all_flow

def set_page(page_num):
    st.session_state.current_page = page_num
    st.rerun()

# 授業カードのヘッダーカラム定義
LESSON_CARD_COLUMNS = [
    "id", "unit_name", "catch_copy", "goal", "target_grade", "disability_type",
    "developmental_stage", # 発達段階を追加
    "duration", "materials", "introduction_flow", "activity_flow", "reflection_flow", "points", "hashtags",
    "image", "material_photos", "video_link", "detail_word_url", "detail_pdf_url",
    "detail_ppt_url", "detail_excel_url",
    "ict_use", "subject", "group_type", "unit_order", "unit_lesson_title"
]

# Excelテンプレートダウンロード関数
def get_excel_template():
    template_df = pd.DataFrame(columns=LESSON_CARD_COLUMNS)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        template_df.to_excel(writer, index=False, sheet_name='授業カードテンプレート')
        workbook = writer.book
        worksheet = writer.sheets['授業カードテンプレート']
        # ヘッダーにコメントを追加（入力ガイド）
        worksheet.write_comment('B1', '例: 「買い物学習」, 「話し言葉の学習」 (単元名)')
        worksheet.write_comment('C1', '例: 生活スキルを楽しく学ぶ実践的な買い物学習！')
        worksheet.write_comment('D1', '例: お店での買い物の手順を理解し、お金の計算ができるようになる。')
        worksheet.write_comment('E1', '例: 小学部3年')
        worksheet.write_comment('F1', '例: 知的障害')
        worksheet.write_comment('G1', '例: 基礎的段階') # 発達段階のコメントを追加
        worksheet.write_comment('H1', '例: 45分×3コマ')
        worksheet.write_comment('I1', '例: 財布;お金;買い物リスト  (セミコロン区切り)')
        worksheet.write_comment('J1', '例: 課題の提示;本時の目標共有 (セミコロン区切りで複数行)')
        worksheet.write_comment('K1', '例: 商品選び;お金の支払い練習 (セミコロン区切りで複数行)')
        worksheet.write_comment('L1', '例: できたことの共有;次回の課題 (セミコロン区切りで複数行)')
        worksheet.write_comment('M1', '例: スモールステップで指導;具体物を用意 (セミコロン区切り)')
        worksheet.write_comment('N1', '例: 生活単元,自立活動 (カンマ区切り)')
        worksheet.write_comment('O1', 'メインとなる画像URL (無い場合は空欄でOK)')
        worksheet.write_comment('P1', '教材写真などのURL (セミコロン区切り、無い場合は空欄でOK)')
        worksheet.write_comment('Q1', 'YouTubeなどの動画URL (無い場合は空欄でOK)')
        worksheet.write_comment('R1', '指導案WordファイルのダウンロードURL (無い場合は空欄でOK)')
        worksheet.write_comment('S1', '指導案PDFファイルのダウンロードURL (無い場合は空欄でOK)')
        worksheet.write_comment('T1', '指導案PowerPointファイルのダウンロードURL (無い場合は空欄でOK)')
        worksheet.write_comment('U1', '指導案ExcelファイルのダウンロードURL (無い場合は空欄でOK)')
        worksheet.write_comment('V1', 'ICT活用有無 (TRUEまたはFALSE)')
        worksheet.write_comment('W1', '例: 生活単元学習,国語,算数など (教科)')
        worksheet.write_comment('X1', '例: 全体,個別,小グループ  (学習集団の単位)')
        worksheet.write_comment('Y1', '単元内での授業の順序 (数値、小さいほど前)')
        worksheet.write_comment('Z1', '例: 「〜しよう」など、単元内での各授業のタイトル (空欄の場合、単元名が使われます)')
    processed_data = output.getvalue()
    return processed_data

# CSVテンプレートダウンロード関数
def get_csv_template():
    template_df = pd.DataFrame(columns=LESSON_CARD_COLUMNS)
    output = BytesIO()
    template_df.to_csv(output, index=False, encoding='utf-8-sig')
    processed_data = output.getvalue()
    return processed_data

# サイドバー
with st.sidebar:
    st.header("📚 データ登録・管理")
    st.markdown("---")

    # --- 管理者ログインフォーム ---
    if not st.session_state.authenticated:
        st.subheader("管理者ログイン")
        with st.form("login_form"):
            username = st.text_input("ユーザー名")
            password = st.text_input("パスワード", type="password")
            login_button = st.form_submit_button("ログイン")

            if login_button:
                if check_password(username, password):
                    st.session_state.authenticated = True
                    st.success("ログインしました！")
                    st.rerun()
                else:
                    st.error("ユーザー名またはパスワードが間違っています。")
        st.markdown("---")
    else:
        st.success("管理者としてログイン中")
        if st.button("ログアウト", key="logout_button"):
            st.session_state.authenticated = False
            st.rerun()
        st.markdown("---")

        # --- 管理者のみがアクセスできる機能 ---
        st.subheader("ファイルテンプレート")
        st.info("""
        ExcelまたはCSVテンプレートをダウンロードし、入力後にアップロードしてデータを追加できます。
        """)

        try:
            with open("授業カード.xlsm", "rb") as f:
                excel_macro_sample_data = f.read()
            st.download_button(
                label="⬇️ 授業カード 入力用（見本付き）",
                data=excel_macro_sample_data,
                file_name="授業カード.xlsm",
                mime="application/vnd.ms-excel.sheet.macroEnabled.12",
                help="テンプレートをダウンロードして、新しい授業カード情報を入力してください。"
            )
        except FileNotFoundError:
            st.warning("⚠️ '授業カード.xlsm' ファイルが見つかりませんでした。同じ階層に配置してください。")
        except Exception as e:
            st.error(f"Excelマクロファイルの読み込み中にエラーが発生しました: {e}")

        csv_data_for_download = get_csv_template()
        st.download_button(
            label="⬇️ CSVテンプレートをダウンロード",
            data=csv_data_for_download,
            file_name="授業カードテンプレート.csv",
            mime="text/csv",
            help="テンプレートをダウンロードして、新しい授業カード情報を入力してください。"
        )

        uploaded_file = st.file_uploader("⬆️ ファイルをアップロード", type=["xlsx", "csv", "xlsm"], help="入力済みのExcelまたはCSVファイルをアップロードして、データを追加します。", key="admin_uploader")

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xlsm'):
                    # Excelファイルの場合、'自動集計'シートを優先的に読み込む
                    try:
                        new_data_df = pd.read_excel(uploaded_file, sheet_name='自動集計')
                        st.info("「自動集計」シートからデータを読み込みました。")
                    except ValueError:
                        new_data_df = pd.read_excel(uploaded_file)
                        st.info("デフォルトシートからデータを読み込みました。")
                elif uploaded_file.name.endswith('.csv'):
                    new_data_df = pd.read_csv(uploaded_file)
                else:
                    st.error("サポートされていないファイル形式です。Excel (.xlsx, .xlsm) または CSV (.csv) ファイルをアップロードしてください。")
                    st.stop()

                required_cols = ["unit_name", "goal"]
                if not all(col in new_data_df.columns for col in required_cols):
                    st.error(f"ファイルに以下の必須項目が含まれていません: {', '.join(required_cols)}")
                    missing_cols = [col for col in required_cols if col not in new_data_df.columns]
                    st.info(f"不足しているカラム: {', '.join(missing_cols)}")
                else:
                    def process_list_column(df, col_name, separator):
                        if col_name in df.columns:
                            return df[col_name].apply(lambda x: [item.strip() for item in str(x).split(separator) if item.strip()] if pd.notna(x) and str(x).strip() != '' else [])
                        return [[]] * len(df)

                    def process_string_column_df(df, col_name, default_value):
                        if col_name in df.columns:
                            return df[col_name].apply(lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else default_value)
                        return [default_value] * len(df)

                    # カラムが存在しない場合のデフォルト値設定
                    for col in LESSON_CARD_COLUMNS:
                        if col not in new_data_df.columns:
                            if col in ['introduction_flow', 'activity_flow', 'reflection_flow', 'points', 'hashtags', 'material_photos']:
                                new_data_df[col] = [[]] * len(new_data_df)
                            elif col == 'unit_order':
                                new_data_df[col] = 9999
                            elif col == 'ict_use':
                                new_data_df[col] = 'なし'
                            elif col == 'subject':
                                new_data_df[col] = 'その他'
                            elif col == 'group_type':
                                new_data_df[col] = '全体'
                            elif col == 'target_grade':
                                new_data_df[col] = '不明'
                            elif col == 'developmental_stage': # 発達段階のデフォルト値
                                new_data_df[col] = '不明'
                            else:
                                new_data_df[col] = ''

                    new_data_df['unit_order'] = new_data_df['unit_order'].apply(lambda x: int(x) if pd.notna(x) and str(x).strip().isdigit() else 9999)
                    new_data_df['unit_lesson_title'] = new_data_df.apply(
                        lambda row: str(row['unit_lesson_title']).strip() if pd.notna(row['unit_lesson_title']) and str(row['unit_lesson_title']).strip() != '' else row['unit_name'],
                        axis=1
                    )
                    
                    new_data_df['introduction_flow'] = process_list_column(new_data_df, 'introduction_flow', ';')
                    new_data_df['activity_flow'] = process_list_column(new_data_df, 'activity_flow', ';')
                    new_data_df['reflection_flow'] = process_list_column(new_data_df, 'reflection_flow', ';')
                    new_data_df['points'] = process_list_column(new_data_df, 'points', ';')
                    new_data_df['hashtags'] = process_list_column(new_data_df, 'hashtags', ',')
                    new_data_df['material_photos'] = process_list_column(new_data_df, 'material_photos', ';')
                    
                    new_data_df['ict_use'] = process_string_column_df(new_data_df, 'ict_use', 'なし')
                    new_data_df['subject'] = process_string_column_df(new_data_df, 'subject', 'その他')
                    new_data_df['group_type'] = process_string_column_df(new_data_df, 'group_type', '全体')
                    new_data_df['unit_name'] = process_string_column_df(new_data_df, 'unit_name', '単元なし')
                    new_data_df['target_grade'] = process_string_column_df(new_data_df, 'target_grade', '不明')
                    new_data_df['developmental_stage'] = process_string_column_df(new_data_df, 'developmental_stage', '不明') # 発達段階の処理
                    new_data_df['image'] = process_string_column_df(new_data_df, 'image', '')
                    new_data_df['video_link'] = process_string_column_df(new_data_df, 'video_link', '')
                    new_data_df['detail_word_url'] = process_string_column_df(new_data_df, 'detail_word_url', '')
                    new_data_df['detail_pdf_url'] = process_string_column_df(new_data_df, 'detail_pdf_url', '')
                    new_data_df['detail_ppt_url'] = process_string_column_df(new_data_df, 'detail_ppt_url', '')
                    new_data_df['detail_excel_url'] = process_string_column_df(new_data_df, 'detail_excel_url', '')
                    new_data_df['catch_copy'] = process_string_column_df(new_data_df, 'catch_copy', '')
                    new_data_df['goal'] = process_string_column_df(new_data_df, 'goal', '')
                    new_data_df['disability_type'] = process_string_column_df(new_data_df, 'disability_type', '不明')
                    new_data_df['duration'] = process_string_column_df(new_data_df, 'duration', '不明')
                    new_data_df['materials'] = process_string_column_df(new_data_df, 'materials', '')

                    existing_ids = {d['id'] for d in st.session_state.lesson_data}
                    max_id = max(existing_ids) if existing_ids else 0

                    new_entries = []
                    for idx, row in new_data_df.iterrows():
                        current_id = row.get('id')
                        row_id = int(current_id) if pd.notna(current_id) and isinstance(current_id, (int, float)) else 0

                        if row_id == 0 or row_id in existing_ids: # IDがないか、重複している場合
                            max_id += 1
                            row_id = max_id
                        
                        lesson_dict = {col: row[col] for col in LESSON_CARD_COLUMNS if col in row}
                        lesson_dict['id'] = row_id # 割り振られたIDをセット
                        new_entries.append(lesson_dict)
                        existing_ids.add(row_id)

                    st.session_state.lesson_data.extend(new_entries)
                    save_lesson_data(st.session_state.lesson_data) # CSVファイルに保存
                    st.success(f"{len(new_entries)}件の授業カードをファイルから追加しました！")
                    st.rerun()
            except Exception as e:
                st.error(f"ファイルの読み込みまたは処理中にエラーが発生しました: {e}")
                st.exception(e)

        st.markdown("---")


# メインページ
if st.session_state.current_lesson_id is None:
    # --- デザインリニューアル: 白枠コンテナ ---
    with st.container(border=True):
        st.markdown("<h1>🃏 授業カードライブラリー</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.1em; color: #bbb;'>先生方の実践授業アイデアを検索し、日々の指導に役立てましょう！</p>", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("カテゴリーで絞り込み")

        search_col, tag_col = st.columns(2)
        with search_col:
            st.session_state.search_query = st.text_input(
                "キーワードで検索",
                st.session_state.search_query,
                placeholder="例: 買い物、生活単元、小学部",
                key="search_input",
                label_visibility="visible"
            )

        all_hashtags = sorted(list(set(tag for lesson in st.session_state.lesson_data for tag in lesson['hashtags'] if tag)))

        with tag_col:
            st.session_state.selected_hashtags = st.multiselect(
                "ハッシュタグで絞り込み",
                options=all_hashtags,
                default=st.session_state.selected_hashtags,
                placeholder="選択してください",
                label_visibility="visible"
            )

        col_subject, col_filler = st.columns([0.5, 0.5])

        with col_subject:
            all_subjects_raw = sorted(list(set(lesson['subject'] for lesson in st.session_state.lesson_data if 'subject' in lesson and lesson['subject'])))
            all_subjects = ["全て"] + all_subjects_raw

            def update_subject_selection():
                st.session_state.selected_subject = st.session_state.main_page_subject_filter_v4
            
            if st.session_state.selected_subject not in all_subjects:
                st.session_state.selected_subject = "全て"

            try:
                default_subject_index = all_subjects.index(st.session_state.selected_subject)
            except ValueError:
                default_subject_index = 0

            st.selectbox(
                "教科を選択",
                options=all_subjects,
                index=default_subject_index,
                key="main_page_subject_filter_v4",
                on_change=update_subject_selection,
                label_visibility="visible"
            )

    st.markdown("---")

    # Googleフォームリンク
    st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <a href="https://leeson-abfy5bxayhavhoznzexj8r.streamlit.app/" target="_blank" 
               style="display: inline-flex; align-items: center; padding: 15px 30px; background-color: #4285F4; color: white !important; border-radius: 30px; text-decoration: none; font-size: 1.2em; font-weight: bold; box-shadow: 0 5px 15px rgba(0,0,0,0.5);">
               <span style="margin-right: 10px;">📝</span> Googleフォームで授業カードを作成！
            </a>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # フィルタリングロジック (省略なし)
    filtered_lessons = []
    for lesson in st.session_state.lesson_data:
        match_search = True
        match_tags = True
        match_subject = True

        if st.session_state.search_query:
            search_lower = st.session_state.search_query.lower()
            lesson_text = (
                str(lesson.get('unit_name', '')).lower() +
                str(lesson.get('subject', '')).lower() +
                str(lesson.get('catch_copy', '')).lower() +
                str(lesson.get('goal', '')).lower() +
                str(lesson.get('target_grade', '')).lower() +
                str(lesson.get('disability_type', '')).lower() +
                str(lesson.get('developmental_stage', '')).lower() +
                str(lesson.get('duration', '')).lower() +
                str(lesson.get('materials', '')).lower() +
                " ".join(lesson.get('introduction_flow', [])).lower() +
                " ".join(lesson.get('activity_flow', [])).lower() +
                " ".join(lesson.get('reflection_flow', [])).lower() +
                " ".join(lesson.get('points', [])).lower() +
                " ".join(lesson.get('hashtags', [])).lower() +
                str(lesson.get('unit_lesson_title', '')).lower()
            )
            if search_lower not in lesson_text:
                match_search = False

        if st.session_state.selected_hashtags:
            if not all(tag in lesson['hashtags'] for tag in st.session_state.selected_hashtags):
                match_tags = False

        if st.session_state.selected_subject != "全て":
            if lesson.get('subject') != st.session_state.selected_subject:
                match_subject = False

        if match_search and match_tags and match_subject:
            filtered_lessons.append(lesson)

    # ページネーション処理 (省略なし)
    CARDS_PER_PAGE = 9
    total_pages = (len(filtered_lessons) + CARDS_PER_PAGE - 1) // CARDS_PER_PAGE
    if total_pages == 0:
        total_pages = 1

    if st.session_state.current_page > total_pages:
        st.session_state.current_page = total_pages
    if st.session_state.current_page < 1:
        st.session_state.current_page = 1

    start_index = (st.session_state.current_page - 1) * CARDS_PER_PAGE
    end_index = start_index + CARDS_PER_PAGE
    displayed_lessons = filtered_lessons[start_index:end_index]

    # --- 授業カードグリッド表示 (HTML/CSSでデザイン) ---
    st.markdown("<div class='lesson-card-grid'>", unsafe_allow_html=True)
    
    if displayed_lessons:
        # st.columns を使って3列レイアウトの中にHTMLカードを配置
        cols = st.columns(3)
        for i, lesson in enumerate(displayed_lessons):
            with cols[i % 3]:
                display_subject = lesson['subject'] if lesson['subject'] and lesson['subject'] != 'その他' else ''
                display_unit = lesson['unit_name'] if lesson['unit_name'] and lesson['unit_name'] != '単元なし' else ''

                subject_unit_display_html = ""
                if display_subject and display_unit:
                    subject_unit_display_html = f'<div class="card-subject-unit">📖 {display_subject} / {display_unit}</div>'
                elif display_subject:
                    subject_unit_display_html = f'<div class="card-subject-unit">📖 {display_subject}</div>'
                elif display_unit:
                    subject_unit_display_html = f'<div class="card-subject-unit">📖 {display_unit}</div>'

                tags_html = "".join(f'<span class="tag-badge">#{tag}</span>' for tag in lesson.get('hashtags', []) if tag)
                img_src = lesson['image'] if lesson['image'] else 'https://via.placeholder.com/400x200?text=No+Image'

                # HTMLカードの描画
                st.markdown(f"""
                <div class="lesson-card" style="animation-delay: {i * 0.1}s;">
                    <img class="lesson-card-image" src="{img_src}" alt="{lesson['unit_name']}">
                    <div class="lesson-card-content">
                        <div>
                            {subject_unit_display_html}
                            <div class="lesson-card-title">{lesson['unit_name']}</div>
                            <div class="lesson-card-catchcopy">{lesson['catch_copy']}</div>
                            <div class="lesson-card-goal">🎯 ねらい: {lesson['goal']}</div>
                            <div class="lesson-card-meta">
                                <span>🎓 {lesson['target_grade']}</span>
                                <span>🧩 {lesson['disability_type']}</span>
                                <span>🌱 {lesson['developmental_stage']}</span>
                                <span>⏱ {lesson['duration']}</span>
                            </div>
                        </div>
                        <div style="margin-top: 10px;">{tags_html}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 詳細ボタン (カードの下に配置、st.buttonを使うため)
                st.button(f"👇 詳細を見る", key=f"detail_btn_{lesson['id']}", on_click=set_detail_page, args=(lesson['id'],))

    else:
        st.info("条件に合う授業カードは見つかりませんでした。")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # ページネーションUI (省略なし)
    st.markdown("---")
    c_prev, c_num, c_next = st.columns([1, 2, 1])
    if st.session_state.current_page > 1:
        c_prev.button("⏪ 前のページ", key="prev_page_bottom", on_click=set_page, args=(st.session_state.current_page - 1,))
    
    c_num.markdown(f"<div style='text-align:center; font-size:1.2em; font-weight:bold;'>Page {st.session_state.current_page} / {total_pages}</div>", unsafe_allow_html=True)

    if st.session_state.current_page < total_pages:
        c_next.button("次のページ ⏩", key="next_page_bottom", on_click=set_page, args=(st.session_state.current_page + 1,))

    st.markdown("---")

else:  # 詳細ページ (デザインリニューアル)
    selected_lesson = next((lesson for lesson in st.session_state.lesson_data if lesson['id'] == st.session_state.current_lesson_id), None)

    if selected_lesson:
        st.button("↩️ 一覧に戻る", on_click=back_to_list, key="back_to_list_btn_top")

        # --- 詳細情報の白枠コンテナ ---
        with st.container(border=True):
            header_html = f"<h1 class='detail-header'>{selected_lesson['unit_name']}</h1>"
            st.markdown(header_html, unsafe_allow_html=True)
            
            if selected_lesson['catch_copy']:
                st.caption(f"{selected_lesson['catch_copy']}")
            
            st.image(selected_lesson['image'] if selected_lesson['image'] else 'https://via.placeholder.com/800x400?text=No+Image', caption=selected_lesson['unit_name'], use_container_width=True)

            st.markdown("### 授業の流れ")
            if st.button('{} 🔃'.format('流れを非表示' if st.session_state.show_all_flow else '流れを表示'), on_click=toggle_all_flow_display, key=f"toggle_all_flow_{selected_lesson['id']}")):
                pass # ロジックはon_clickで処理済み

            if st.session_state.show_all_flow:
                if selected_lesson['introduction_flow']:
                    intro_html = "<div class='flow-section'><h4>🚀 導入</h4><ol class='flow-list'>"
                    for step in selected_lesson['introduction_flow']:
                        intro_html += f"<li>{step}</li>"
                    intro_html += "</ol></div>"
                    st.markdown(intro_html, unsafe_allow_html=True)

                if selected_lesson['activity_flow']:
                    activity_html = "<div class='flow-section'><h4>💡 活動</h4><ol class='flow-list'>"
                    for step in selected_lesson['activity_flow']:
                        activity_html += f"<li>{step}</li>"
                    activity_html += "</ol></div>"
                    st.markdown(activity_html, unsafe_allow_html=True)

                if selected_lesson['reflection_flow']:
                    reflection_html = "<div class='flow-section'><h4>💭 振り返り</h4><ol class='flow-list'>"
                    for step in selected_lesson['reflection_flow']:
                        reflection_html += f"<li>{step}</li>"
                    reflection_html += "</ol></div>"
                    st.markdown(reflection_html, unsafe_allow_html=True)

            st.markdown("---")

            st.markdown("### 🎯 ねらい")
            st.write(selected_lesson['goal'])
            
            st.markdown("### ℹ️ 基本情報")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**対象学年:** {selected_lesson['target_grade']}")
                st.markdown(f"**障害種別:** {selected_lesson['disability_type']}")
                st.markdown(f"**発達段階:** {selected_lesson.get('developmental_stage', '不明')}")
            with col2:
                st.markdown(f"**時間:** {selected_lesson['duration']}")
                st.markdown(f"**ICT活用:** {selected_lesson.get('ict_use', 'なし')}")
            with col3:
                st.markdown(f"**教科:** {selected_lesson.get('subject', 'その他')}")
                st.markdown(f"**学習集団:** {selected_lesson.get('group_type', '全体')}")

            # 単元のつながりロジック
            if selected_lesson.get('unit_name') and selected_lesson.get('unit_name') != '単元なし':
                unit_name_to_search = selected_lesson['unit_name']
                target_grade_to_match = selected_lesson['target_grade']

                all_lessons_in_unit = [
                    lesson for lesson in st.session_state.lesson_data
                    if lesson.get('unit_name') == unit_name_to_search and
                    lesson.get('target_grade') == target_grade_to_match
                ]

                sorted_lessons_in_unit = sorted(all_lessons_in_unit, key=lambda x: x.get('unit_order', 9999))

                if sorted_lessons_in_unit:
                    st.markdown("---")
                    st.markdown(f"### 📚 「{unit_name_to_search}」の授業の流れ")
                    
                    for lesson_in_unit in sorted_lessons_in_unit:
                        display_title = lesson_in_unit.get('unit_lesson_title') if lesson_in_unit.get('unit_lesson_title') else lesson_in_unit['unit_name']
                        is_current_lesson = (lesson_in_unit['id'] == selected_lesson['id'])

                        if is_current_lesson:
                            st.markdown(f"- **{display_title} 【現在の授業】**")
                        else:
                            if st.button(f"{display_title} へ", key=f"unit_link_{lesson_in_unit['id']}"):
                                set_detail_page(lesson_in_unit['id'])
                                st.rerun()

            st.markdown("---")

            if selected_lesson['materials']:
                st.markdown("### ✂️ 準備物")
                st.write(selected_lesson['materials'])

            if selected_lesson['points']:
                st.markdown("### 💡 指導のポイント")
                for point in selected_lesson['points']:
                    st.markdown(f"- {point}")

            if selected_lesson['hashtags']:
                st.markdown("### #️⃣ ハッシュタグ")
                tags_html_detail = "".join(f'<span class="tag-badge" style="margin-right: 5px;">#{tag}</span>' for tag in selected_lesson.get('hashtags', []) if tag)
                st.markdown(f"<p>{tags_html_detail}</p>", unsafe_allow_html=True)

            if selected_lesson['material_photos']:
                st.markdown("### 📸 授業・教材写真")
                cols = st.columns(3)
                for i, photo_url in enumerate(selected_lesson['material_photos']):
                    with cols[i % 3]:
                        if photo_url.strip():
                            st.image(photo_url, use_container_width=True)

            if selected_lesson['video_link'].strip():
                st.markdown("### ▶️ 参考動画")
                try:
                    st.video(selected_lesson['video_link'])
                except Exception as e:
                    st.warning(f"動画の読み込みエラー: {e}")

            # ダウンロードリンク
            if selected_lesson['detail_word_url'] or selected_lesson['detail_pdf_url'] or selected_lesson['detail_ppt_url'] or selected_lesson['detail_excel_url']:
                st.markdown("### 📄 資料ダウンロード")
                dl_cols = st.columns(4)
                if selected_lesson['detail_word_url']:
                    with dl_cols[0]: st.link_button("📖 Word指導案", selected_lesson["detail_word_url"])
                if selected_lesson['detail_pdf_url']:
                    with dl_cols[1]: st.link_button("📚 PDF指導案", selected_lesson["detail_pdf_url"])
                if selected_lesson['detail_ppt_url']:
                    with dl_cols[2]: st.link_button("📊 PowerPoint", selected_lesson["detail_ppt_url"])
                if selected_lesson['detail_excel_url']:
                    with dl_cols[3]: st.link_button("📈 Excel評価", selected_lesson["detail_excel_url"])

        st.markdown("---")
        st.button("↩️ 一覧に戻る", on_click=back_to_list, key="back_to_list_btn_bottom")
    else:
        st.error("指定された授業カードが見つかりませんでした。")
        st.button("↩️ 一覧に戻る", on_click=back_to_list)