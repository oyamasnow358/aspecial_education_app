import streamlit as st
import pandas as pd
import base64
import re # ハッシュタグ抽出用
import io # Word/Excelファイルダウンロード・アップロード用
from io import BytesIO # Excelアップロード用
import xlsxwriter # エラー解決のためにインポートを追加
import openpyxl # ★追加: Excelファイル操作用
from openpyxl.styles import Alignment # ★追加: セルの結合と中央揃え用

st.set_page_config(
    page_title="授業カードライブラリー",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS for Card Layout and General Styling ---
def load_css():
    """カスタムCSSを読み込む関数"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Poppins:wght@400;600&display=swap');
        
        body {
            font-family: 'Noto Sans JP', sans-serif;
            background-color: #f0f2f6; /* 全体の背景色を調整 */
        }
        [data-testid="stAppViewContainer"] > .main {
            background-color: #f0f2f6; /* メインコンテンツの背景色も合わせる */
            background-image: none; /* 背景画像を削除するか、控えめに */
            padding-top: 30px; /* 全体的な上部パディング */
            padding-bottom: 30px;
        }
        [data-testid="stSidebar"] {
            background-color: #ffffff; /* サイドバーの背景を白に */
            border-right: 1px solid #e0e0e0;
            box-shadow: 2px 0 10px rgba(0,0,0,0.05);
        }
        [data-testid="stHeader"] { /* Streamlitヘッダーの背景色を調整 */
            background-color: #ffffff;
            box-shadow: 0 2px 5px rgba(0,2,0,0.05);
        }
        
        h1, h2, h3, h4, h5, h6 { 
            font-family: 'Poppins', 'Noto Sans JP', sans-serif; /* 見出しはPoppinsを優先 */
            color: #2c3e50; 
            font-weight: 700;
        }
        h1 {
            text-align: center; 
            padding-bottom: 25px;
            font-size: 2.8em; /* H1サイズを調整 */
            color: #4A90E2; /* メインカラーを使用 */
            letter-spacing: -0.5px;
        }
        h2 {
            text-align: left;
            border-left: 6px solid #8A2BE2; /* 紫のアクセント */
            padding-left: 15px;
            margin-top: 45px;
            font-size: 1.9em;
            color: #34495e;
        }
        h3 {
            text-align: left;
            border-bottom: 2px solid #e0e0e0; /* 細い線で区切り */
            padding-bottom: 8px;
            margin-top: 35px;
            font-size: 1.5em;
            color: #34495e;
            display: flex; /* アイコンを横に並べる */
            align-items: center;
        }
        h3 .header-icon {
            margin-right: 10px;
            color: #8A2BE2;
        }
        
        p, li {
            font-size: 1.05em;
            line-height: 1.7;
            color: #333;
        }
        /* --- 戻るボタンのスタイル (位置調整) --- */
        .back-button-container {
            position: relative; /* relativeにして通常のフローで配置 */
            padding-bottom: 20px; /* 下に余白 */
            margin-bottom: -50px; /* 上の要素との重なりを調整 */
        }
        /* Streamlit widget styling */
        .stTextInput>div>div>input, .stMultiSelect>div>div>div, .stSelectbox>div>div {
            border-radius: 12px; /* 少し角丸を小さく */
            padding: 10px 15px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            transition: all 0.2s ease-in-out;
            background-color: #ffffff;
        }
        .stTextInput>div>div>input:focus, .stMultiSelect>div>div>div:focus-within, .stSelectbox>div>div:focus-within {
            border-color: #4A90E2; /* フォーカス時にメインカラー */
            box-shadow: 0 0 0 0.2rem rgba(74,144,226,0.15);
        }
        .stMultiSelect div[data-testid="stMultiSelectOptions"] {
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }
        
        /* Card grid specific styles */
        .lesson-card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(330px, 1fr)); /* カードサイズを調整 */
            gap: 30px; /* カード間の余白 */
            padding: 25px 0;
        }
        .lesson-card {
            background-color: #ffffff;
            border: none;
            border-radius: 18px; /* 角丸を大きく */
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08); /* 影を強調 */
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        }
        .lesson-card:hover {
            transform: translateY(-10px); /* ホバー時の浮き上がりを強調 */
            box-shadow: 0 18px 35px rgba(74, 144, 226, 0.18); /* ホバー時の影をアクセントカラーに */
        }
        .lesson-card-image {
            width: 100%;
            height: 200px; /* 画像の高さを少し高く */
            object-fit: cover; 
            border-bottom: 1px solid #f0f0f0;
        }
        .lesson-card-content {
            padding: 22px; /* パディングを増やす */
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .lesson-card-title {
            font-size: 1.4em; /* フォントサイズを大きく */
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 8px;
            line-height: 1.4;
        }
        .lesson-card-catchcopy {
            font-size: 0.95em;
            color: #6a0dad; /* 紫色 */
            font-weight: 500;
            margin-bottom: 15px;
            line-height: 1.4;
            font-style: italic;
        }
        .lesson-card-goal {
            font-size: 0.9em;
            color: #555;
            margin-bottom: 12px;
            border-left: 4px solid #4a90e2; /* アクセントカラー */
            padding-left: 10px;
            line-height: 1.5;
            min-height: 60px; /* 高さのばらつきを抑える */
            display: flex;
            align-items: center;
        }
        .lesson-card-meta {
            font-size: 0.85em;
            color: #777;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
            margin-top: 10px;
            margin-bottom: 15px;
        }
        .lesson-card-meta span {
            display: flex;
            align-items: center;
            background-color: #f0f8ff; /* 明るい青の背景 */
            padding: 6px 12px;
            border-radius: 10px;
            border: 1px solid #e3f2fd;
        }
        .lesson-card-tags {
            font-size: 0.8em;
            margin-top: 15px;
            min-height: 35px; 
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }
        .tag-badge {
            display: inline-block;
            background-color: #e3f2fd; /* 明るい青 */
            color: #2196f3;
            border-radius: 15px; /* 角丸を大きく */
            padding: 6px 12px;
            font-size: 0.75em;
            white-space: nowrap;
            transition: background-color 0.2s, color 0.2s;
            cursor: pointer;
            border: 1px solid rgba(33, 150, 243, 0.2);
        }
        .tag-badge:hover {
            background-color: #bbdefb;
            color: #1976d2;
        }

        /* Icons for card meta and details */
        .icon {
            margin-right: 8px;
            font-size: 1.2em; /* アイコンサイズを少し大きく */
            color: #8A2BE2; /* アイコンの色 */
        }

        /* Detail Button Styling */
        .stButton>button {
            border: 2px solid #4a90e2;
            border-radius: 25px;
            color: #4a90e2;
            background-color: #ffffff;
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.3s ease;
            margin-top: 20px; /* ボタンとコンテンツの間の余白 */
            width: 100%; /* カード幅いっぱいに */
            box-shadow: 0 4px 10px rgba(74, 144, 226, 0.1);
        }
        .stButton>button:hover {
            border-color: #8A2BE2;
            color: white;
            background-color: #8A2BE2;
            transform: translateY(-3px); 
            box-shadow: 0 8px 15px rgba(138,43,226,0.2);
        }
        
            
        /* Detail page specific styles */
        .detail-header {
            text-align: left; /* これはそのまま */
            margin-bottom: 25px; /* これはそのまま */
        }
        /* このセレクタはst.imageが直接生成するimg要素をターゲットにします */
        /* st.image()ウィジェットが生成するHTMLは div > img の構造を持つことが多いです */
        /* use_container_width=True と合わせて親要素の幅を尊重しつつ高さを設定 */
        [data-testid="stImage"] > img { /* Streamlitの画像ウィジェットの内部imgタグをターゲット */
            width: 100% !important; /* 親要素の幅いっぱいに広げる */
            height: 400px !important; /* 例: 高さを固定値で大きく設定（必要に応じて調整） */
            object-fit: cover !important; /* 画像をトリミングして枠いっぱいに表示 */
            border-radius: 15px !important;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1) !important;
            margin-bottom: 30px !important;
            display: block !important; /* imgがインライン要素であることによる余計な隙間をなくす */
        }
        /* 古い .detail-main-image の定義は削除するか、空のままにしてください。 */
        /* .detail-main-image {
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        } */

  
        
        .detail-section h3 {
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 8px;
            margin-top: 40px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }
        .detail-section p, .detail-section ul, .detail-section ol {
            font-size: 1.05em;
            line-height: 1.7;
            color: #333;
            margin-bottom: 10px;
        }
        .detail-section ul, .detail-section ol {
            margin-left: 25px;
            padding-left: 0;
            list-style-position: inside; /* リストマーカーを内側に */
        }
        .detail-section li {
            margin-bottom: 8px;
            padding-left: 5px; /* マーカーとの間隔 */
        }
        .detail-image-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); /* ギャラリー画像サイズ調整 */
            gap: 20px;
            margin-top: 25px;
            margin-bottom: 35px;
        }
        
        .detail-image-gallery img {
            max-width: 100%;
            height: 220px; /* 固定の高さ */
            object-fit: cover;
            border-radius: 12px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.1);
            transition: transform 0.2s ease-in-out;
        }
        .detail-image-gallery img:hover {
            transform: scale(1.02);
        }
        .stVideo {
            border-radius: 12px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.15);
            margin-top: 25px;
            margin-bottom: 35px;
        }
        .detail-tag-container {
            margin-top: 30px;
            margin-bottom: 30px;
        }
        .stAlert {
            border-radius: 10px;
            font-size: 0.95em;
            background-color: #e6f7ff; /* Alert背景色調整 */
            border-left: 5px solid #4A90E2;
            color: #333;
            padding: 12px 18px;
        }
        .stWarning {
            border-radius: 10px;
            font-size: 0.95em;
            background-color: #fffbe6;
            border-left: 5px solid #faad14;
        }
        .stInfo {
            border-radius: 10px;
            font-size: 0.95em;
            background-color: #e6f7ff;
            border-left: 5px solid #1890ff;
        }

        /* Download button for details page */
        .download-button-wrapper {
            margin-top: 20px;
            margin-bottom: 30px;
            text-align: center;
        }
        .download-button-wrapper a > button {
            background-color: #4A90E2; 
            color: white; 
            border: none; 
            padding: 12px 28px;
            border-radius: 30px; 
            cursor: pointer; 
            font-size: 1.1em; 
            font-weight: bold;
            transition: background-color 0.3s, transform 0.2s, box-shadow 0.3s;
            box-shadow: 0 6px 15px rgba(74, 144, 226, 0.25);
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        .download-button-wrapper a > button:hover {
            background-color: #357ABD; 
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(74, 144, 226, 0.35);
        }
        .download-button-wrapper a > button .icon {
            color: white; /* ダウンロードアイコンの色も白に */
        }
                .card-subject-unit {
            font-size: 0.9em;
            color: #4A90E2; /* メインカラー */
            font-weight: 600;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            background-color: #e6f7ff; /* 明るい背景 */
            padding: 5px 10px;
            border-radius: 8px;
            width: fit-content; /* 内容に合わせて幅を調整 */
            border: 1px solid #cceeff;
        }
        .card-subject-unit .icon {
            margin-right: 6px;
            font-size: 1.1em;
            color: #4A90E2;
        }
                .flow-content-wrapper {
            margin-top: 20px; /* ボタンとコンテンツの間に余白を持たせる */
        }
         
        /* Detail Button Styling (上書きまたは追加) - 既存のものをより具体的に上書き */
        .lesson-card .stButton > button { /* .lesson-card 内のボタンにスタイルを適用 */
            border: 2px solid #4a90e2 !important; /* !important で強制的に適用 */
            border-radius: 25px !important;
            color: #4a90e2 !important;
            background-color: #ffffff !important;
            padding: 10px 24px !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            margin-top: 20px !important;
            width: 100% !important;
            box-shadow: 0 4px 10px rgba(74, 144, 226, 0.1) !important;
        }
        .lesson-card .stButton > button:hover {
            border-color: #357ABD !important; /* ホバー時の色も !important */
            color: white !important;
            background-color: #357ABD !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 15px rgba(74,144,226,0.2) !important;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# --- ▼ 戻るボタンの配置 (メインコンテンツの左上) ▼ ---
# st.columnsを使って、左端に配置する
col_back, _ = st.columns([0.15, 0.85]) # ボタン用に狭いカラムを確保
with col_back:
    # `st.page_link` を使用すると、直接ページに遷移できてより確実です。
    st.page_link("tokusi_app.py", label="« TOPページに戻る", icon="🏠")
# --- ▲ 戻るボタンの配置 ▲ ---

# 'pages'フォルダと同じ階層に lesson_cards.csv を置いてください。
try:
    lesson_data_df = pd.read_csv(
        "lesson_cards.csv",
        converters={
            'introduction_flow': lambda x: x.split(';') if pd.notna(x) else [],
            'activity_flow': lambda x: x.split(';') if pd.notna(x) else [],
            'reflection_flow': lambda x: x.split(';') if pd.notna(x) else [],
            'points': lambda x: x.split(';') if pd.notna(x) else [],
            'hashtags': lambda x: x.split(',') if pd.notna(x) else [],
            # ★変更: material_photosの処理を強化。空文字列を除外する。
            'material_photos': lambda x: [url.strip() for url in x.split(';') if url.strip()] if pd.notna(x) else [],
            'unit_name': lambda x: str(x) if pd.notna(x) else '',
            'unit_order': lambda x: int(x) if pd.notna(x) and str(x).isdigit() else 9999,
            'unit_lesson_title': lambda x: str(x) if pd.notna(x) else '',
            'video_link': lambda x: str(x) if pd.notna(x) else '',
            # ★追加・変更：image, 資料ダウンロードURLも空欄を''として読み込む
            'image': lambda x: str(x) if pd.notna(x) else '', # メイン画像も空文字列処理を追加
            'detail_word_url': lambda x: str(x) if pd.notna(x) else '',
            'detail_pdf_url': lambda x: str(x) if pd.notna(x) else '',
            'detail_ppt_url': lambda x: str(x) if pd.notna(x) else '',
            'detail_excel_url': lambda x: str(x) if pd.notna(x) else '',
        }
    )


    # 新規カラムのデフォルト値設定（もしCSVにカラムがない場合）
    if 'unit_order' not in lesson_data_df.columns:
        lesson_data_df['unit_order'] = 9999

    # === ここが重要な修正点です ===
    # 'unit_lesson_title' が存在しない、または全てNaN/空の場合、'unit_name' から値を設定
    if 'unit_lesson_title' not in lesson_data_df.columns:
        lesson_data_df['unit_lesson_title'] = lesson_data_df['unit_name'].fillna('単元内授業')
    else:
        # 既存だが空欄のunit_lesson_titleをunit_nameで補完
        lesson_data_df['unit_lesson_title'] = lesson_data_df.apply(
            lambda row: row['unit_name'] if pd.isna(row['unit_lesson_title']) or str(row['unit_lesson_title']).strip() == '' else row['unit_lesson_title'],
            axis=1
        )
    # ============================

    # ICT活用有無のTRUE/FALSEをbool型に変換
    if 'ict_use' in lesson_data_df.columns:
        # ICT使用の値をそのまま文字列として保持
        lesson_data_df['ict_use'] = lesson_data_df['ict_use'].astype(str)
    else:
        lesson_data_df['ict_use'] = 'なし' # カラムがない場合はデフォルトで「なし」

    # 'subject', 'unit_name', 'group_type' カラムが存在しない場合、デフォルト値で作成
    if 'subject' not in lesson_data_df.columns:
        lesson_data_df['subject'] = 'その他'
    if 'unit_name' not in lesson_data_df.columns:
        lesson_data_df['unit_name'] = '単元なし'
    # !!! 既存のデータが空文字列の場合に '単元なし' に変換する処理を追加 !!!
    lesson_data_df['unit_name'] = lesson_data_df['unit_name'].apply(lambda x: '単元なし' if str(x).strip() == '' or str(x).lower() == 'nan' else str(x).strip())

    if 'group_type' not in lesson_data_df.columns:
        lesson_data_df['group_type'] = '全体' # 例: 全体, 小グループ, 個別 など

    lesson_data_raw = lesson_data_df.to_dict(orient='records')
except FileNotFoundError:
    st.error("lesson_cards.csv ファイルが見つかりませんでした。pages フォルダと同じ階層に配置してください。")
    st.stop()
except Exception as e:
    st.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
    st.exception(e) # デバッグのために例外の詳細を表示
    st.stop()

# st.session_stateの初期化
if 'current_lesson_id' not in st.session_state:
    st.session_state.current_lesson_id = None
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'selected_hashtags' not in st.session_state:
    st.session_state.selected_hashtags = []
if 'selected_subject' not in st.session_state: # 教科フィルター
    st.session_state.selected_subject = "全て"
if 'selected_unit' not in st.session_state: # 単元フィルターを追加
    st.session_state.selected_unit = "全て"
if 'lesson_data' not in st.session_state:
    st.session_state.lesson_data = lesson_data_raw # アプリ内でデータを更新できるようにセッションステートに保持
if 'show_all_flow' not in st.session_state: # 授業の流れ全体表示フラグ
    st.session_state.show_all_flow = False

# --- Helper Functions ---

def set_detail_page(lesson_id):
    """詳細ページへの遷移をトリガーする関数"""
    st.session_state.current_lesson_id = lesson_id
    st.session_state.show_all_flow = False # 詳細ページに遷移したらフロー表示をリセット

def back_to_list():
    """一覧ページに戻る関数"""
    st.session_state.current_lesson_id = None
    st.session_state.show_all_flow = False # 一覧に戻ったらフロー表示をリセット

def toggle_all_flow_display():
    """授業の流れ全体の表示を切り替える関数"""
    st.session_state.show_all_flow = not st.session_state.show_all_flow


# 授業カードのヘッダーカラム定義
LESSON_CARD_COLUMNS = [
    "id", "unit_name", "catch_copy", "goal", "target_grade", "disability_type", 
    "duration", "materials", "introduction_flow", "activity_flow", "reflection_flow", "points", "hashtags",
    "image", "material_photos", "video_link", "detail_word_url", "detail_pdf_url", 
    "detail_ppt_url", "detail_excel_url", # ★追加: PowerPointとExcelのURLカラム
    "ict_use", "subject", "group_type", "unit_order", "unit_lesson_title" 
]

# Excelテンプレートダウンロード関数
def get_excel_template():
    template_df = pd.DataFrame(columns=LESSON_CARD_COLUMNS)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        template_df.to_excel(writer, index=False, sheet_name='授業カードテンプレート')
        workbook  = writer.book
        worksheet = writer.sheets['授業カードテンプレート']
        # ヘッダーにコメントを追加（入力ガイド）
        worksheet.write_comment('B1', '例: 「買い物学習」, 「話し言葉の学習」 (単元名)') 
        worksheet.write_comment('C1', '例: 生活スキルを楽しく学ぶ実践的な買い物学習！')
        worksheet.write_comment('D1', '例: お店での買い物の手順を理解し、お金の計算ができるようになる。')
        worksheet.write_comment('E1', '例: 小学部3年')
        worksheet.write_comment('F1', '例: 知的障害')
        worksheet.write_comment('G1', '例: 45分×3コマ')
        worksheet.write_comment('H1', '例: 財布;お金;買い物リスト  (セミコロン区切り)')
        worksheet.write_comment('I1', '例: 課題の提示;本時の目標共有 (セミコロン区切りで複数行)')
        worksheet.write_comment('J1', '例: 商品選び;お金の支払い練習 (セミコロン区切りで複数行)')
        worksheet.write_comment('K1', '例: できたことの共有;次回の課題 (セミコロン区切りで複数行)')
        worksheet.write_comment('L1', '例: スモールステップで指導;具体物を用意 (セミコロン区切り)')
        worksheet.write_comment('M1', '例: 生活単元,自立活動 (カンマ区切り)')
        worksheet.write_comment('N1', 'メインとなる画像URL (無い場合は空欄でOK)')
        worksheet.write_comment('O1', '教材写真などのURL (セミコロン区切り、無い場合は空欄でOK)')
        worksheet.write_comment('P1', 'YouTubeなどの動画URL (無い場合は空欄でOK)')
        worksheet.write_comment('Q1', '指導案WordファイルのダウンロードURL (無い場合は空欄でOK)')
        worksheet.write_comment('R1', '指導案PDFファイルのダウンロードURL (無い場合は空欄でOK)')
        worksheet.write_comment('S1', '指導案PowerPointファイルのダウンロードURL (無い場合は空欄でOK)') # ★追加
        worksheet.write_comment('T1', '指導案ExcelファイルのダウンロードURL (無い場合は空欄でOK)')     # ★追加
        worksheet.write_comment('U1', 'TRUEまたはFALSE') # インデックスがずれるため注意
        worksheet.write_comment('V1', '例: 生活単元学習,国語,算数など')
        worksheet.write_comment('W1', '例: 全体,個別,小グループ  (学習集団の単位)')
        worksheet.write_comment('X1', '例: 「〜しよう」など、単元内での各授業のタイトル (空欄の場合、単元名が使われます)') 
    processed_data = output.getvalue()
    return processed_data

# CSVテンプレートダウンロード関数
def get_csv_template():
    template_df = pd.DataFrame(columns=LESSON_CARD_COLUMNS)
    output = BytesIO()
    template_df.to_csv(output, index=False, encoding='utf-8-sig')
    processed_data = output.getvalue()
    return processed_data
# --- Sidebar for Data Entry and Filters ---



# ★ここから新しい関数 `create_and_fill_excel` の追加箇所 (上記で提示した関数の全文をここに移動)
def create_and_fill_excel(
    unit_name, lesson_title, catch_copy, goal, target_grade, disability_type, 
    duration, group_type, subject, introduction_flow, activity_flow, 
    reflection_flow, points, materials, hashtags, ict_use, image, video_link,
    detail_word_url, detail_pdf_url, detail_ppt_url, detail_excel_url
):
    try:
        with open("授業カード.xlsm", "rb") as f:
            excel_template_data = io.BytesIO(f.read())
        
        workbook = openpyxl.load_workbook(excel_template_data, keep_vba=True)
        sheet = workbook.active

        # !!! ここを修正します !!!
        # 結合セルのエラーを回避するため、結合範囲の左上隅に書き込むか、
        # 結合を解除してから書き込み、再度結合する方法を取ります。
        # 今回は、テンプレートの構造を保ちつつ、結合セルでなければ直接書き込み、
        # 結合セルであれば結合範囲の左上隅に書き込むように調整します。
        # 以下は、具体的なセル結合の状況に合わせて調整が必要です。

        # B3とB4が結合されている場合、B3に単元名と授業タイトルを結合して書き込む
        # または、結合を解除してB3, B4にそれぞれ書き込み、再結合
        # ここでは、B3を単元名、B4を授業タイトルと想定して書き込みます。
        # もしB3とB4が完全に結合されていて、そこにタイトルを入れたい場合は、B3にまとめて書き込むことになります。
        
        # まず、結合範囲があるかチェックし、もしあればその範囲を解除する
        # この処理は慎重に行う必要があり、テンプレートの意図を壊さないように注意
        
        # 例: B3とB4が結合されている場合
        # merged_cells = list(sheet.merged_cells)
        # for merged_range in merged_cells:
        #     if 'B3' in merged_range or 'B4' in merged_range:
        #         sheet.unmerge_cells(str(merged_range))
        
        # テンプレートの「セルB3〜B4」が結合されて「単元名」を表示している場合、
        # B3にまとめて書き込むか、テンプレート側で調整が必要です。
        # ここでは、B3に「単元名」を、B4に「授業タイトル」を書き込むと仮定します。
        # もしB3とB4が結合されていて、そこにメインタイトルを入れる場合は、B3にまとめて書き込む。
        # 例: sheet['B3'] = f"{unit_name}\n{lesson_title}"
        
        # 現在のエラーメッセージから、sheet['B3']がMergedCellになっているため、
        # テンプレートの構造を確認し、書き込むべき適切な（非結合または結合範囲の左上隅）セルを探す必要があります。
        # 一旦、B3が「単元名」の代表セル、B4が「授業タイトル」の代表セルと仮定して修正します。
        # もし「授業タイトル」が別のセル (例: B7) にある場合は、そちらに書き込みます。
        
        # テンプレートに合わせたセル番地への書き込み例:
        # ご自身のExcelテンプレートに合わせて、セル番地を正確に指定してください。
        
        # 単元名 (例: B3が単元名の代表セル)
        if 'B3' in sheet.merged_cells: # もしB3が結合セル範囲の一部なら
            for merged_range in sheet.merged_cells:
                if 'B3' in str(merged_range): # 結合範囲がB3を含む場合
                    # 結合範囲の左上隅に書き込む (例: B3)
                    # 結合を一時解除する方が確実だが、シンプルに左上隅に書き込む
                    top_left_cell_ref = str(merged_range).split(':')[0]
                    sheet[top_left_cell_ref] = unit_name 
                    break
            else: # B3が単独セルなら
                sheet['B3'] = unit_name
        else: # B3が単独セルなら
            sheet['B3'] = unit_name

        # 授業タイトル (例: B7が授業タイトル)
        # もしB4がMergedCellでなければB4に書き込むか、テンプレートの指定セルに書き込む
        # エラーログを見るとB3が問題なので、B4は直接書き込めると仮定
        if 'B4' in sheet.merged_cells: # もしB4が結合セル範囲の一部なら
            for merged_range in sheet.merged_cells:
                if 'B4' in str(merged_range): # 結合範囲がB4を含む場合
                    top_left_cell_ref = str(merged_range).split(':')[0]
                    sheet[top_left_cell_ref] = lesson_title 
                    break
            else:
                sheet['B4'] = lesson_title
        else:
            sheet['B4'] = lesson_title
        
        # キャッチコピー (例: C5が代表セル)
        if 'C5' in sheet.merged_cells:
            for merged_range in sheet.merged_cells:
                if 'C5' in str(merged_range):
                    top_left_cell_ref = str(merged_range).split(':')[0]
                    sheet[top_left_cell_ref] = catch_copy
                    break
            else:
                sheet['C5'] = catch_copy
        else:
            sheet['C5'] = catch_copy
        
        # ねらい (例: B8が代表セル)
        if 'B8' in sheet.merged_cells:
            for merged_range in sheet.merged_cells:
                if 'B8' in str(merged_range):
                    top_left_cell_ref = str(merged_range).split(':')[0]
                    sheet[top_left_cell_ref] = goal
                    break
            else:
                sheet['B8'] = goal
        else:
            sheet['B8'] = goal

        # 学部学年 (例: A5)
        sheet['A5'] = target_grade
        # 障害種別 (例: B5)
        sheet['B5'] = disability_type
        # 授業時間 (例: E5)
        sheet['E5'] = duration
        # 学習形態 (例: E3)
        sheet['E3'] = group_type
        # 教科 (例: C3が代表セル)
        if 'C3' in sheet.merged_cells:
            for merged_range in sheet.merged_cells:
                if 'C3' in str(merged_range):
                    top_left_cell_ref = str(merged_range).split(':')[0]
                    sheet[top_left_cell_ref] = subject
                    break
            else:
                sheet['C3'] = subject
        else:
            sheet['C3'] = subject


        # リスト形式のデータを改行区切りで書き込む (セル番地はテンプレートに合わせて調整)
        # 例: B10が導入の流れの代表セルで結合されている場合
        if 'B10' in sheet.merged_cells:
            for merged_range in sheet.merged_cells:
                if 'B10' in str(merged_range):
                    top_left_cell_ref = str(merged_range).split(':')[0]
                    sheet[top_left_cell_ref] = "\n".join([f"- {s}" for s in introduction_flow.split('\n') if s.strip()])
                    break
            else:
                sheet['B10'] = "\n".join([f"- {s}" for s in introduction_flow.split('\n') if s.strip()])
        else:
            sheet['B10'] = "\n".join([f"- {s}" for s in introduction_flow.split('\n') if s.strip()])


        if 'B11' in sheet.merged_cells:
            for merged_range in sheet.merged_cells:
                if 'B11' in str(merged_range):
                    top_left_cell_ref = str(merged_range).split(':')[0]
                    sheet[top_left_cell_ref] = "\n".join([f"- {s}" for s in activity_flow.split('\n') if s.strip()])
                    break
            else:
                sheet['B11'] = "\n".join([f"- {s}" for s in activity_flow.split('\n') if s.strip()])
        else:
            sheet['B11'] = "\n".join([f"- {s}" for s in activity_flow.split('\n') if s.strip()])


        if 'B12' in sheet.merged_cells:
            for merged_range in sheet.merged_cells:
                if 'B12' in str(merged_range):
                    top_left_cell_ref = str(merged_range).split(':')[0]
                    sheet[top_left_cell_ref] = "\n".join([f"- {s}" for s in reflection_flow.split('\n') if s.strip()])
                    break
            else:
                sheet['B12'] = "\n".join([f"- {s}" for s in reflection_flow.split('\n') if s.strip()])
        else:
            sheet['B12'] = "\n".join([f"- {s}" for s in reflection_flow.split('\n') if s.strip()])


        if 'B9' in sheet.merged_cells:
            for merged_range in sheet.merged_cells:
                if 'B9' in str(merged_range):
                    top_left_cell_ref = str(merged_range).split(':')[0]
                    sheet[top_left_cell_ref] = "\n".join([f"- {s}" for s in points.split('\n') if s.strip()])
                    break
            else:
                sheet['B9'] = "\n".join([f"- {s}" for s in points.split('\n') if s.strip()])
        else:
            sheet['B9'] = "\n".join([f"- {s}" for s in points.split('\n') if s.strip()])


        if 'B14' in sheet.merged_cells:
            for merged_range in sheet.merged_cells:
                if 'B14' in str(merged_range):
                    top_left_cell_ref = str(merged_range).split(':')[0]
                    sheet[top_left_cell_ref] = "\n".join([f"- {s}" for s in materials.split('\n') if s.strip()])
                    break
            else:
                sheet['B14'] = "\n".join([f"- {s}" for s in materials.split('\n') if s.strip()])
        else:
            sheet['B14'] = "\n".join([f"- {s}" for s in materials.split('\n') if s.strip()])


        if 'B22' in sheet.merged_cells:
            for merged_range in sheet.merged_cells:
                if 'B22' in str(merged_range):
                    top_left_cell_ref = str(merged_range).split(':')[0]
                    sheet[top_left_cell_ref] = ", ".join([f"#{t.strip()}" for t in hashtags.split(',') if t.strip()])
                    break
            else:
                sheet['B22'] = ", ".join([f"#{t.strip()}" for t in hashtags.split(',') if t.strip()])
        else:
            sheet['B22'] = ", ".join([f"#{t.strip()}" for t in hashtags.split(',') if t.strip()])


        if 'B20' in sheet.merged_cells:
            for merged_range in sheet.merged_cells:
                if 'B20' in str(merged_range):
                    top_left_cell_ref = str(merged_range).split(':')[0]
                    sheet[top_left_cell_ref] = ict_use
                    break
            else:
                sheet['B20'] = ict_use
        else:
            sheet['B20'] = ict_use


        # URL
        # これらは単独セルであることが多いため、直接書き込みを試みますが、
        # もし結合セルであれば同様の処理が必要になります。
        sheet['B15'] = image # メイン画像URL
        sheet['B16'] = video_link # 参考動画URL
        sheet['B17'] = detail_word_url # 指導案Word
        sheet['B18'] = detail_pdf_url # 指導案PDF
        sheet['B19'] = detail_ppt_url # 授業資料PowerPoint
        sheet['B21'] = detail_excel_url # 評価シートExcel
        
        # ... (セルの結合と中央揃えのコメントはそのまま) ...

        output = io.BytesIO()
        workbook.save(output)
        processed_data = output.getvalue()
        return processed_data
    except FileNotFoundError:
        st.error("エラー: '授業カード.xlsm' テンプレートファイルが見つかりません。アプリと同じ階層に配置してください。")
        return None
    except Exception as e:
        st.error(f"Excelファイルの書き込み中にエラーが発生しました: {e}")
        st.exception(e)
        return None
# ★ここまでが新しい関数 `create_and_fill_excel` の追加箇所

# st.session_stateの初期化 (この部分は変更なし)
if 'current_lesson_id' not in st.session_state:
    st.session_state.current_lesson_id = None
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'selected_hashtags' not in st.session_state:
    st.session_state.selected_hashtags = []
if 'selected_subject' not in st.session_state: # 教科フィルター
    st.session_state.selected_subject = "全て"
if 'selected_unit' not in st.session_state: # 単元フィルターを追加
    st.session_state.selected_unit = "全て"
if 'lesson_data' not in st.session_state:
    st.session_state.lesson_data = lesson_data_raw # アプリ内でデータを更新できるようにセッションステートに保持
if 'show_all_flow' not in st.session_state: # 授業の流れ全体表示フラグ
    st.session_state.show_all_flow = False
if 'show_create_form' not in st.session_state: # ★追加: 新規作成フォーム表示フラグを初期化
    st.session_state.show_create_form = False

# --- Helper Functions ---

def set_detail_page(lesson_id):
    """詳細ページへの遷移をトリガーする関数"""
    st.session_state.current_lesson_id = lesson_id
    st.session_state.show_all_flow = False # 詳細ページに遷移したらフロー表示をリセット

def back_to_list():
    """一覧ページに戻る関数"""
    st.session_state.current_lesson_id = None
    st.session_state.show_all_flow = False # 一覧に戻ったらフロー表示をリセット
    st.session_state.show_create_form = False # 一覧に戻ったらフォームも閉じる

def toggle_all_flow_display():
    """授業の流れ全体の表示を切り替える関数"""
    st.session_state.show_all_flow = not st.session_state.show_all_flow

# ★新しい授業カード作成フォームの表示/非表示を切り替える関数
def toggle_create_form_display():
    st.session_state.show_create_form = not st.session_state.show_create_form

# 授業カードのヘッダーカラム定義
LESSON_CARD_COLUMNS = [
    "id", "unit_name", "catch_copy", "goal", "target_grade", "disability_type", 
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
        workbook  = writer.book
        worksheet = writer.sheets['授業カードテンプレート']
        # ヘッダーにコメントを追加（入力ガイド）
        worksheet.write_comment('B1', '例: 「買い物学習」, 「話し言葉の学習」 (単元名)') 
        worksheet.write_comment('C1', '例: 生活スキルを楽しく学ぶ実践的な買い物学習！')
        worksheet.write_comment('D1', '例: お店での買い物の手順を理解し、お金の計算ができるようになる。')
        worksheet.write_comment('E1', '例: 小学部3年')
        worksheet.write_comment('F1', '例: 知的障害')
        worksheet.write_comment('G1', '例: 45分×3コマ')
        worksheet.write_comment('H1', '例: 財布;お金;買い物リスト  (セミコロン区切り)')
        worksheet.write_comment('I1', '例: 課題の提示;本時の目標共有 (セミコロン区切りで複数行)')
        worksheet.write_comment('J1', '例: 商品選び;お金の支払い練習 (セミコロン区切りで複数行)')
        worksheet.write_comment('K1', '例: できたことの共有;次回の課題 (セミコロン区切りで複数行)')
        worksheet.write_comment('L1', '例: スモールステップで指導;具体物を用意 (セミコロン区切り)')
        worksheet.write_comment('M1', '例: 生活単元,自立活動 (カンマ区切り)')
        worksheet.write_comment('N1', 'メインとなる画像URL (無い場合は空欄でOK)')
        worksheet.write_comment('O1', '教材写真などのURL (セミコロン区切り、無い場合は空欄でOK)')
        worksheet.write_comment('P1', 'YouTubeなどの動画URL (無い場合は空欄でOK)')
        worksheet.write_comment('Q1', '指導案WordファイルのダウンロードURL (無い場合は空欄でOK)')
        worksheet.write_comment('R1', '指導案PDFファイルのダウンロードURL (無い場合は空欄でOK)')
        worksheet.write_comment('S1', '指導案PowerPointファイルのダウンロードURL (無い場合は空欄でOK)')
        worksheet.write_comment('T1', '指導案ExcelファイルのダウンロードURL (無い場合は空欄でOK)')
        worksheet.write_comment('U1', 'TRUEまたはFALSE') # ICT活用
        worksheet.write_comment('V1', '例: 生活単元学習,国語,算数など') # subject
        worksheet.write_comment('W1', '例: 全体,個別,小グループ  (学習集団の単位)') # group_type
        worksheet.write_comment('X1', '例: 「〜しよう」など、単元内での各授業のタイトル (空欄の場合、単元名が使われます)') # unit_lesson_title
    processed_data = output.getvalue()
    return processed_data

# CSVテンプレートダウンロード関数
def get_csv_template():
    template_df = pd.DataFrame(columns=LESSON_CARD_COLUMNS)
    output = BytesIO()
    template_df.to_csv(output, index=False, encoding='utf-8-sig')
    processed_data = output.getvalue()
    return processed_data

# ★ここから新しい関数 `create_and_fill_excel` の追加箇所
# この関数は、ファイルアップロードやフォーム処理の前に定義される必要があります。
def create_and_fill_excel(
    unit_name, lesson_title, catch_copy, goal, target_grade, disability_type, 
    duration, group_type, subject, introduction_flow, activity_flow, 
    reflection_flow, points, materials, hashtags, ict_use, image, video_link,
    detail_word_url, detail_pdf_url, detail_ppt_url, detail_excel_url
):
    try:
        # Excelファイルを読み込む
        workbook = openpyxl.load_workbook("授業カード.xlsm")
        sheet = workbook.active

        # セルに値を書き込む (結合セルを考慮し、結合範囲の左上隅に書き込む)
        # 結合セルに直接書き込むとエラーになるため、結合範囲をチェックして左上隅に書く
        def write_to_cell(sheet, cell_coord, value):
            for merged_cell_range in sheet.merged_cells:
                if cell_coord in merged_cell_range:
                    # 結合セルの左上隅のセルに書き込む
                    min_col, min_row, max_col, max_row = openpyxl.utils.cell.range_boundaries(str(merged_cell_range))
                    top_left_cell_coord = openpyxl.utils.cell.get_column_letter(min_col) + str(min_row)
                    sheet[top_left_cell_coord].value = value
                    return
            # 結合セルでなければ直接書き込む
            sheet[cell_coord].value = value

        write_to_cell(sheet, 'B3', unit_name) # 単元名 (A3-B4 が結合されている場合、A3に書く) -> Excelテンプレートに合わせて B3
        write_to_cell(sheet, 'B7', lesson_title) # 授業タイトル
        write_to_cell(sheet, 'C5', catch_copy) # キャッチコピー (C5-D5 が結合されている場合、C5に書く)
        write_to_cell(sheet, 'B8', goal)       # ねらい (B8-E8 が結合されている場合、B8に書く)
        write_to_cell(sheet, 'A5', target_grade) # 対象学部学年
        write_to_cell(sheet, 'B5', disability_type) # 障害種別
        write_to_cell(sheet, 'E5', duration)   # 授業時間
        write_to_cell(sheet, 'E3', group_type) # 学習形態
        write_to_cell(sheet, 'C3', subject)    # 教科 (C3-D4 が結合されている場合、C3に書く)

        # 流れとポイントは改行区切りで入力されるので、セミコロンに変換して書き込む
        write_to_cell(sheet, 'B10', ";".join([s.strip() for s in introduction_flow.split('\n') if s.strip()]))
        write_to_cell(sheet, 'B11', ";".join([s.strip() for s in activity_flow.split('\n') if s.strip()]))
        write_to_cell(sheet, 'B12', ";".join([s.strip() for s in reflection_flow.split('\n') if s.strip()]))
        write_to_cell(sheet, 'B9', ";".join([s.strip() for s in points.split('\n') if s.strip()]))
        write_to_cell(sheet, 'B14', ";".join([s.strip() for s in materials.split('\n') if s.strip()]))
        
        # ハッシュタグはカンマ区切り
        write_to_cell(sheet, 'B22', hashtags)
        
        # ICT活用
        write_to_cell(sheet, 'B20', ict_use) # ICT活用内容

        # URL
        write_to_cell(sheet, 'B16', image)
        write_to_cell(sheet, 'B17', video_link)
        write_to_cell(sheet, 'B18', detail_word_url)
        write_to_cell(sheet, 'B19', detail_pdf_url)
        write_to_cell(sheet, 'B21', detail_ppt_url) # Excelテンプレートの正しいセルを仮定
        write_to_cell(sheet, 'B23', detail_excel_url) # Excelテンプレートの正しいセルを仮定


        output = BytesIO()
        workbook.save(output)
        processed_data = output.getvalue()
        return processed_data
    except FileNotFoundError:
        st.error("エラー: '授業カード.xlsm' テンプレートファイルが見つかりません。")
        return None
    except Exception as e:
        st.error(f"Excelファイルの書き込み中にエラーが発生しました: {e}")
        st.exception(e)
        return None
# ★ここまでが新しい関数 `create_and_fill_excel` の追加箇所


# --- Sidebar for Data Entry and Filters ---
# !!! サイドバーのコンテンツはここにあり、このブロック全体は変更しません !!!
with st.sidebar:
    st.header("📚 データ登録・管理")
    st.markdown("---")

    st.subheader("① Googleフォーム方式")
    st.info("""
    Googleフォームで入力されたデータは、自動的にGoogleスプレッドシートに蓄積され、このアプリに反映されます。
    以下のボタンからフォームを開き、新しい授業カードを登録してください。
    """)
    google_form_link = "https://forms.gle/YOUR_GOOGLE_FORM_LINK" # ここを実際のGoogleフォームのリンクに置き換えてください
    st.markdown(
        f"""
        <a href="{google_form_link}" target="_blank">
        <button style="
        background-color: #4CAF50; color: white; border: none; padding: 10px 20px;
        border-radius: 25px; cursor: pointer; font-size: 1em; font-weight: bold;
        transition: background-color 0.3s, transform 0.2s;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); width: 100%;
        ">
        📝 Googleフォームを開く
        </button>
        </a>
        """, unsafe_allow_html=True
    )
    if google_form_link == "https://forms.gle/YOUR_GOOGLE_FORM_LINK":
        st.warning("⚠️ Googleフォームのリンクを実際のURLに更新してください。")

    st.markdown("---")

    st.subheader("② ファイルテンプレート方式")
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

    uploaded_file = st.file_uploader("⬆️ ファイルをアップロード", type=["xlsx", "csv"], help="入力済みのExcelまたはCSVファイルをアップロードして、データを追加します。")

    if uploaded_file is not None:
        try:
            # ... (ファイルアップロードのロジックは変更なし。ただし、Excel読み込み時にはopenpyxlを使うことを推奨) ...
            if uploaded_file.name.endswith('.xlsx'):
                # openpyxlで読み込み、データフレームに変換
                workbook = openpyxl.load_workbook(uploaded_file)
                sheet = workbook.active
                data = sheet.values
                cols = next(data)[0:] # ヘッダー行をスキップ
                new_data_df = pd.DataFrame(data, columns=cols)
            elif uploaded_file.name.endswith('.csv'):
                new_data_df = pd.read_csv(uploaded_file)
            else:
                st.error("サポートされていないファイル形式です。Excel (.xlsx) または CSV (.csv) ファイルをアップロードしてください。")
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
                
                def process_string_column(df, col_name, default_value):
                    if col_name in df.columns:
                        return df[col_name].apply(lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else default_value)
                    return [default_value] * len(df)

                if 'unit_order' in new_data_df.columns:
                    new_data_df['unit_order'] = new_data_df['unit_order'].apply(lambda x: int(x) if pd.notna(x) and str(x).strip().isdigit() else 9999)
                else:
                    new_data_df['unit_order'] = 9999
             
                if 'unit_lesson_title' in new_data_df.columns:
                    new_data_df['unit_lesson_title'] = new_data_df['unit_lesson_title'].apply(lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '')
                else:
                    new_data_df['unit_lesson_title'] = new_data_df.get('unit_name', '単元内授業')
                
                new_data_df['introduction_flow'] = process_list_column(new_data_df, 'introduction_flow', ';')
                new_data_df['activity_flow'] = process_list_column(new_data_df, 'activity_flow', ';')
                new_data_df['reflection_flow'] = process_list_column(new_data_df, 'reflection_flow', ';')
                new_data_df['points'] = process_list_column(new_data_df, 'points', ';')
                new_data_df['hashtags'] = process_list_column(new_data_df, 'hashtags', ',')
                new_data_df['material_photos'] = process_list_column(new_data_df, 'material_photos', ';')

                if 'ict_use' in new_data_df.columns:
                    new_data_df['ict_use'] = new_data_df['ict_use'].astype(str).apply(lambda x: x.strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else 'なし')
                else:
                    new_data_df['ict_use'] = 'なし'

                new_data_df['subject'] = process_string_column(new_data_df, 'subject', 'その他')
                new_data_df['unit_name'] = process_string_column(new_data_df, 'unit_name', '単元なし')
                new_data_df['group_type'] = process_string_column(new_data_df, 'group_type', '全体')

                existing_ids = {d['id'] for d in st.session_state.lesson_data}
                max_id = max(existing_ids) if existing_ids else 0

                new_entries = []
                for _, row in new_data_df.iterrows():
                    current_id = row.get('id')
                    if pd.isna(current_id) or current_id in existing_ids:
                        max_id += 1
                        row_id = max_id
                    else:
                        try:
                            row_id = int(current_id)
                            if row_id in existing_ids:
                                max_id += 1
                                row_id = max_id
                        except ValueError:
                            max_id += 1
                            row_id = max_id
                    
                    lesson_dict = {
                        'id': row_id,
                        'unit_name': row.get('unit_name', '単元なし'),
                        'catch_copy': row.get('catch_copy', ''),
                        'goal': row.get('goal', ''),
                        'target_grade': row.get('target_grade', '不明'),
                        'disability_type': row.get('disability_type', '不明'),
                        'duration': row.get('duration', '不明'),
                        'materials': row.get('materials', ''),
                        'introduction_flow': row.get('introduction_flow', []), 
                        'activity_flow': row.get('activity_flow', []),     
                        'reflection_flow': row.get('reflection_flow', []),   
                        'points': row.get('points', []),
                        'hashtags': row.get('hashtags', []),
                        'image': process_string_column(new_data_df.iloc[[_]], 'image', '').iloc[0],
                        'material_photos': row.get('material_photos', []),
                        'video_link': process_string_column(new_data_df.iloc[[_]], 'video_link', '').iloc[0],
                        'detail_word_url': process_string_column(new_data_df.iloc[[_]], 'detail_word_url', '').iloc[0],
                        'detail_pdf_url': process_string_column(new_data_df.iloc[[_]], 'detail_pdf_url', '').iloc[0],   
                        'detail_ppt_url': process_string_column(new_data_df.iloc[[_]], 'detail_ppt_url', '').iloc[0],   
                        'detail_excel_url': process_string_column(new_data_df.iloc[[_]], 'detail_excel_url', '').iloc[0],
                        'ict_use': row.get('ict_use', False),
                        'subject': row.get('subject', 'その他'),
                        'group_type': row.get('group_type', '全体'),
                        'unit_order': row.get('unit_order', 9999),
                        'unit_lesson_title': row.get('unit_lesson_title', row.get('unit_name', '単元内の授業'))
                    }
                    new_entries.append(lesson_dict)
                    existing_ids.add(row_id)

                st.session_state.lesson_data.extend(new_entries)
                st.success(f"{len(new_entries)}件の授業カードをファイルから追加しました！")
                st.experimental_rerun()
        except Exception as e:
            st.error(f"ファイルの読み込みまたは処理中にエラーが発生しました: {e}")
            st.exception(e)

    st.markdown("---") # サイドバーのコンテンツがここで終わる


# --- Main Page Logic ---

if st.session_state.current_lesson_id is None:
    # --- Lesson Card List View ---

    st.markdown("<h1>🃏 授業カードライブラリー</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1em; color: #555;'>先生方の実践授業アイデアを検索し、日々の指導に役立てましょう！</p>", unsafe_allow_html=True)

    # ★★★ ここに「新しい授業カードの作成」セクションを配置 ★★★
    st.markdown("---")
    st.subheader("新しい授業カードの作成")
    # ここに配置されたボタンが、メインページでのみフォームの表示/非表示を切り替えます。
    if st.button("📝 授業カード作成フォームを開く / 閉じる", on_click=toggle_create_form_display, key="toggle_create_form_main_page_button"): 
        pass

    if st.session_state.show_create_form:
        st.info("以下のフォームに授業カードの情報を入力し、「授業カードExcelをダウンロード」ボタンをクリックすると、入力済みのExcelファイルが生成されます。")

        with st.form("new_lesson_card_form_main_page"): # フォームキーもメインページ用にする
            st.subheader("授業カード入力フォーム")

            # 入力項目を定義 (前の回答で提示したフォームの内容をそのままここに記述)
            # 全てのkeyをユニークなものに変更 (例: _main)
            unit_name_input = st.text_input("単元名", help="例: 買い物学習、話し言葉の学習", key="form_unit_name_main")
            lesson_title_input = st.text_input("授業タイトル", help="例: 「買い物学習」〜お店で買ってみよう〜", key="form_lesson_title_main")
            catch_copy_input = st.text_area("キャッチコピー", help="この授業の魅力が伝わる一文を！", key="form_catch_copy_main")
            goal_input = st.text_area("ねらい", help="授業で子どもたちに身につけてほしい力を具体的に記述します。", key="form_goal_main")
            
            col_meta1, col_meta2, col_meta3 = st.columns(3)
            with col_meta1:
                target_grade_input = st.text_input("対象学部学年", help="例: 小学部3年、中学部", key="form_target_grade_main")
            with col_meta2:
                disability_type_input = st.text_input("障害種別", help="例: 知的障害、肢体不自由", key="form_disability_type_main")
            with col_meta3:
                duration_input = st.text_input("授業時間", help="例: 45分×3コマ、90分", key="form_duration_main")
            
            col_meta4, col_meta5 = st.columns(2)
            with col_meta4:
                group_type_input = st.selectbox("学習形態", ["全体", "個別", "小グループ", "その他"], help="授業における学習集団の形態", key="form_group_type_main")
            with col_meta5:
                subject_input = st.text_input("教科", help="例: 生活単元学習、国語、算数", key="form_subject_main")

            introduction_flow_input = st.text_area("導入の流れ", help="各ステップを改行で区切ってください。", key="form_intro_flow_main")
            activity_flow_input = st.text_area("活動の流れ", help="各ステップを改行で区切ってください。", key="form_activity_flow_main")
            reflection_flow_input = st.text_area("振り返り", help="各ステップを改行で区切ってください。", key="form_reflect_flow_main")
            points_input = st.text_area("授業のポイント", help="指導上の工夫や留意点など。各ポイントを改行で区切ってください。", key="form_points_main")
            materials_input = st.text_area("準備物", help="必要な物を改行またはカンマで区切ってください。", key="form_materials_main")
            hashtags_input = st.text_input("ハッシュタグ (カンマ区切り)", help="例: 生活単元,自立活動,SST", key="form_hashtags_main")
            ict_use_input = st.text_area("ICT活用内容", help="使用するICT機器や具体的な活用方法を記述してください。", key="form_ict_use_main")

            image_url_input = st.text_input("メイン画像URL", help="授業のイメージが伝わる画像のURL", key="form_image_url_main")
            video_link_input = st.text_input("参考動画URL", help="YouTubeなどの動画リンク", key="form_video_link_main")
            detail_word_url_input = st.text_input("指導案WordファイルURL", help="詳細な指導案のWordファイルへのリンク", key="form_word_url_main")
            detail_pdf_url_input = st.text_input("指導案PDFファイルURL", help="詳細な指導案のPDFファイルへのリンク", key="form_pdf_url_main")
            detail_ppt_url_input = st.text_input("授業資料PowerPointファイルURL", help="授業で使うPowerPointファイルへのリンク", key="form_ppt_url_main")
            detail_excel_url_input = st.text_input("評価シートExcelファイルURL", help="評価シートなどのExcelファイルへのリンク", key="form_excel_url_main")

            submitted = st.form_submit_button("授業カードExcelをダウンロード")

            if submitted:
                # openpyxlを使ってExcelファイルを操作する関数を呼び出す
                excel_output = create_and_fill_excel(
                    unit_name=unit_name_input,
                    lesson_title=lesson_title_input,
                    catch_copy=catch_copy_input,
                    goal=goal_input,
                    target_grade=target_grade_input,
                    disability_type=disability_type_input,
                    duration=duration_input,
                    group_type=group_type_input,
                    subject=subject_input,
                    introduction_flow=introduction_flow_input,
                    activity_flow=activity_flow_input,
                    reflection_flow=reflection_flow_input,
                    points=points_input,
                    materials=materials_input,
                    hashtags=hashtags_input,
                    ict_use=ict_use_input,
                    image=image_url_input,
                    video_link=video_link_input,
                    detail_word_url=detail_word_url_input,
                    detail_pdf_url=detail_pdf_url_input,
                    detail_ppt_url=detail_ppt_url_input,
                    detail_excel_url=detail_excel_url_input,
                )
                if excel_output:
                    st.download_button(
                        label="⬇️ 授業カード_入力済.xlsm をダウンロード", # labelを修正
                        data=excel_output,
                        file_name="授業カード_入力済.xlsm",
                        mime="application/vnd.ms-excel.sheet.macroEnabled.12",
                        key="download_filled_excel_main", # keyをユニークに
                        help="入力した情報が反映されたExcelファイルをダウンロードします。"
                    )
                    st.success("Excelファイルの準備ができました！ダウンロードボタンをクリックしてください。")
                else:
                    st.error("Excelファイルの作成に失敗しました。テンプレートファイルがあるか確認してください。")
                
        st.markdown("---") # フォームの後に区切り線
    

    
# --- Main Page Logic ---

if st.session_state.current_lesson_id is None:
    # --- Lesson Card List View ---

    st.markdown("<h1>🃏 授業カードライブラリー</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1em; color: #555;'>先生方の実践授業アイデアを検索し、日々の指導に役立てましょう！</p>", unsafe_allow_html=True)

    # Search and Filter Section
    search_col, tag_col = st.columns([0.6, 0.4])
    with search_col:
        # キーワード検索のスタイル修正: label_visibility="visible" を追加
        st.session_state.search_query = st.text_input(
            "キーワードで検索",
            st.session_state.search_query,
            placeholder="例: 買い物、生活単元、小学部",
            key="search_input",
            label_visibility="visible" # これでラベルが常に見えるようになる
        )
    
    all_hashtags = sorted(list(set(tag for lesson in st.session_state.lesson_data for tag in lesson['hashtags'] if tag)))

    with tag_col:
        st.session_state.selected_hashtags = st.multiselect(
            "ハッシュタグで絞り込み",
            options=all_hashtags,
            default=st.session_state.selected_hashtags,
            placeholder="選択してください",
            label_visibility="visible" # これでラベルが常に見えるようになる
        )
        
# カテゴリーで絞り込みのセクション
    st.markdown("---") # 区切り線
    st.subheader("カテゴリーで絞り込み")

    col_subject, col_unit = st.columns(2) # 2カラムに分割して表示

    with col_subject:
        all_subjects_raw = sorted(list(set(lesson['subject'] for lesson in st.session_state.lesson_data if 'subject' in lesson and lesson['subject'])))
        all_subjects = ["全て"] + all_subjects_raw

        # on_changeコールバック関数を定義
        def update_subject_selection():
            st.session_state.selected_subject = st.session_state.main_page_subject_filter_v4 # selectboxのkeyで直接値を取得
            st.session_state.selected_unit = "全て" # 教科が変わったら単元フィルターをリセット

        # selected_subject が有効なオプションに含まれていない場合、"全て"にリセット
        if st.session_state.selected_subject not in all_subjects:
            st.session_state.selected_subject = "全て"

        try:
            default_subject_index = all_subjects.index(st.session_state.selected_subject)
        except ValueError:
            default_subject_index = 0 # 見つからない場合は「全て」に設定

        st.selectbox(
            "教科を選択",
            options=all_subjects,
            index=default_subject_index,
            key="main_page_subject_filter_v4",
            on_change=update_subject_selection, # on_changeイベントハンドラを設定
            label_visibility="visible"
        )
    
    with col_unit:
        # 選択された教科に基づいて単元をフィルタリング
        if st.session_state.selected_subject == "全て":
            available_units_raw = sorted(list(set(lesson['unit_name'] for lesson in st.session_state.lesson_data if 'unit_name' in lesson and lesson['unit_name'] and lesson['unit_name'] != '単元なし')))
        else:
            available_units_raw = sorted(list(set(
                lesson['unit_name'] for lesson in st.session_state.lesson_data
                if 'unit_name' in lesson and lesson['unit_name'] and lesson['unit_name'] != '単元なし' and lesson.get('subject') == st.session_state.selected_subject
            )))

        all_units = ["全て"] + available_units_raw

        def update_unit_selection():
            st.session_state.selected_unit = st.session_state.main_page_unit_filter_v4

        if st.session_state.selected_unit not in all_units:
            st.session_state.selected_unit = "全て"

        try:
            default_unit_index = all_units.index(st.session_state.selected_unit)
        except ValueError:
            default_unit_index = 0

        st.selectbox(
            "単元を選択",
            options=all_units,
            index=default_unit_index,
            key="main_page_unit_filter_v4",
            on_change=update_unit_selection,
            label_visibility="visible"
        )       

        

    st.markdown("---") # 区切り線

  
    filtered_lessons = []
    # search_lower をループの前に初期化するか、
    # 検索クエリがない場合は、検索ロジックを完全にスキップするように変更します。
    # ここでは、よりシンプルにするために、検索クエリがある場合のみ処理するようにします。

    for lesson in st.session_state.lesson_data:
        match_search = True
        match_tags = True
        match_subject = True
        match_unit = True # 単元フィルターを追加

        # Keyword search のロジックを修正
        if st.session_state.search_query: # 検索クエリがある場合のみ検索を実行
            search_lower = st.session_state.search_query.lower()
            if not (
                (search_lower in str(lesson.get('unit_name', '')).lower()) or
                (search_lower in str(lesson.get('subject', '')).lower()) or
                (search_lower in str(lesson.get('catch_copy', '')).lower()) or
                (search_lower in str(lesson.get('goal', '')).lower()) or
                (search_lower in str(lesson.get('target_grade', '')).lower()) or
                (search_lower in str(lesson.get('disability_type', '')).lower()) or
                (search_lower in str(lesson.get('duration', '')).lower()) or # duration も追加しました
                (search_lower in str(lesson.get('materials', '')).lower()) or 
                any(search_lower in str(step).lower() for step in lesson.get('introduction_flow', [])) or
                any(search_lower in str(step).lower() for step in lesson.get('activity_flow', [])) or     
                any(search_lower in str(step).lower() for step in lesson.get('reflection_flow', [])) or   
                any(search_lower in str(point).lower() for point in lesson.get('points', [])) or 
                any(search_lower in str(t).lower() for t in lesson.get('hashtags', [])) or
                (search_lower in str(lesson.get('unit_lesson_title', '')).lower())
            ):
                match_search = False
        # else:
        #     st.session_state.search_query が空の場合、match_search はデフォルトの True のまま
        #     なので、ここでは何もする必要がありません。

        # Hashtag filter
        if st.session_state.selected_hashtags:
            if not all(tag in lesson['hashtags'] for tag in st.session_state.selected_hashtags):
                match_tags = False

        # Subject filter
        if st.session_state.selected_subject != "全て":
            if lesson.get('subject') != st.session_state.selected_subject:
                match_subject = False
        
        # Unit filter (新規追加)
        if st.session_state.selected_unit != "全て":
            if lesson.get('unit_name') != st.session_state.selected_unit:
                match_unit = False

        if match_search and match_tags and match_subject and match_unit:
            filtered_lessons.append(lesson)
    
            
    st.markdown("<div class='lesson-card-grid'>", unsafe_allow_html=True)
    if filtered_lessons:
        for lesson in filtered_lessons:
            # 教科と単元名が空文字列や'単元なし'の場合は表示しない
            display_subject = lesson['subject'] if lesson['subject'] and lesson['subject'] != 'その他' else ''
            display_unit = lesson['unit_name'] if lesson['unit_name'] and lesson['unit_name'] != '単元なし' else ''
            
            # 教科と単元名を組み合わせる
            subject_unit_display = ""
            if display_subject and display_unit:
                subject_unit_display = f"<span class='card-subject-unit'><span class='icon'>📖</span>{display_subject} / {display_unit}</span>"
            elif display_subject:
                subject_unit_display = f"<span class='card-subject-unit'><span class='icon'>📖</span>{display_subject}</span>"
            elif display_unit:
                subject_unit_display = f"<span class='card-subject-unit'><span class='icon'>📖</span>{display_unit}</span>"
            st.markdown(f"""
            <div class="lesson-card">
             <img class="lesson-card-image" src="{lesson['image'] if lesson['image'] else 'https://via.placeholder.com/400x200?text=No+Image'}" alt="{lesson['unit_name']}">
             <div class="lesson-card-content">
                 <div>
                     {subject_unit_display}
                     <div class="lesson-card-title">{lesson['unit_name']}</div> 
                     <div class="lesson-card-catchcopy">{lesson['catch_copy']}</div>
                     <div class="lesson-card-goal">🎯 ねらい: {lesson['goal']}</div>
                     <div class="lesson-card-meta">
                <span><span class="icon">🎓</span>{lesson['target_grade']}</span>
                <span><span class="icon">🧩</span>{lesson['disability_type']}</span>
                         <span><span class="icon">⏱</span>{lesson['duration']}</span>
                     </div>
                 </div>
                 <div class="lesson-card-tags">
                     {''.join(f'<span class=\"tag-badge\">#{tag}</span>' for tag in lesson['hashtags'] if tag)}
                 </div>
                 {st.button("👇この授業の詳細を見る", key=f"detail_btn_{lesson['id']}", on_click=set_detail_page, args=(lesson['id'],))}
             </div>
            </div>
             """, unsafe_allow_html=True)

else:
    # --- Lesson Card Detail View ---

    selected_lesson = next((lesson for lesson in st.session_state.lesson_data if lesson['id'] == st.session_state.current_lesson_id), None)

    if selected_lesson:
        st.button("↩️ 一覧に戻る", on_click=back_to_list, key="back_to_list_btn_top")

        st.markdown(f"<h1 class='detail-header'>{selected_lesson['unit_name']}</h1>", unsafe_allow_html=True) # メインタイトルをに変更
        if selected_lesson['catch_copy']:
            st.markdown(f"<h3 class='detail-header'>{selected_lesson['catch_copy']}</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<br>", unsafe_allow_html=True)

        st.image(selected_lesson['image'] if selected_lesson['image'] else 'https://via.placeholder.com/800x400?text=No+Image', caption=selected_lesson['unit_name'], use_container_width=True) # 画像キャプションも単元名に

        st.markdown("""
            <style>
                .flow-section {
                    background-color: #f9f9f9;
                    border-left: 5px solid #8A2BE2;
                    padding: 15px 20px;
                    margin-bottom: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                }
                .flow-section h4 {
                    color: #8A2BE2;
                    font-weight: 600;
                    margin-bottom: 10px;
                    font-size: 1.2em;
                }
                .flow-list {
                    list-style-type: decimal;
                    margin-left: 20px;
                    padding-left: 0;
                }
                .flow-list li {
                    margin-bottom: 5px;
                    line-height: 1.6;
                }
                .related-lesson-card {
                    display: flex;
                    align-items: center;
                    background-color: #fff;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    margin-bottom: 10px;
                    padding: 10px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                    cursor: pointer;
                    transition: all 0.2s ease-in-out;
                }
                .related-lesson-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 3px 6px rgba(0,0,0,0.1);
                }
                .related-lesson-card img {
                    width: 80px;
                    height: 50px;
                    object-fit: cover;
                    border-radius: 4px;
                    margin-right: 15px;
                }
                .related-lesson-card-content {
                    flex-grow: 1;
                }
                .related-lesson-card-title {
                    font-weight: bold;
                    color: #333;
                    font-size: 1em;
                    margin-bottom: 5px;
                }
                .related-lesson-card-meta {
                    font-size: 0.85em;
                    color: #666;
                }
            </style>
        """, unsafe_allow_html=True)

        # 授業の流れセクション
        st.subheader("授業の流れ")
        # ボタンとコンテンツの間に明確な区切りを入れる
        st.button(f"{'授業の流れを非表示' if st.session_state.show_all_flow else '授業の流れを表示'} 🔃", on_click=toggle_all_flow_display, key=f"toggle_all_flow_{selected_lesson['id']}")
        
        # ここにコンテンツを表示するDivを追加し、CSSで上部の余白を調整
        st.markdown("<div class='flow-content-wrapper'>", unsafe_allow_html=True)

        if st.session_state.show_all_flow:
            if selected_lesson['introduction_flow']:
                
                st.markdown("<h4><span class='icon'>🚀</span>導入</h4>", unsafe_allow_html=True)
                st.markdown("<ol class='flow-list'>", unsafe_allow_html=True)
                for step in selected_lesson['introduction_flow']:
                    st.markdown(f"<li>{step}</li>", unsafe_allow_html=True)
                st.markdown("</ol>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            if selected_lesson['activity_flow']:
                st.markdown("<h4><span class='icon'>💡</span>活動</h4>", unsafe_allow_html=True)
                st.markdown("<ol class='flow-list'>", unsafe_allow_html=True)
                for step in selected_lesson['activity_flow']:
                    st.markdown(f"<li>{step}</li>", unsafe_allow_html=True)
                st.markdown("</ol>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            if selected_lesson['reflection_flow']:
                
                st.markdown("<h4><span class='icon'>💭</span>振り返り</h4>", unsafe_allow_html=True)
                st.markdown("<ol class='flow-list'>", unsafe_allow_html=True)
                for step in selected_lesson['reflection_flow']:
                    st.markdown(f"<li>{step}</li>", unsafe_allow_html=True)
                st.markdown("</ol>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True) # flow-content-wrapper の閉じタグ
        
        st.markdown("---") # ここに区切り線を追加して、新機能との区切りを明確にする
    
    
        # ねらい
       
        st.markdown("<h3><span class='header-icon'>🎯</span>ねらい</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{selected_lesson['goal']}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")
        # 対象・種別・時間・教科・単元・学習集団の単位 (表示カラム追加)
        
        st.markdown("<h3><span class='header-icon'>ℹ️</span>基本情報</h3>", unsafe_allow_html=True)
        # 6カラムに変更
        col1, col2, col3, col4, col5, col6 = st.columns(6) 
        with col1:
            st.markdown(f"**対象学年:** {selected_lesson['target_grade']}")
        with col2:
            st.markdown(f"**障害種別:** {selected_lesson['disability_type']}")
        with col3:
            st.markdown(f"**時間:** {selected_lesson['duration']}")
        with col4:
            st.markdown(f"**ICT活用:** {selected_lesson.get('ict_use', 'なし')}")
        with col5:
            st.markdown(f"**教科:** {selected_lesson.get('subject', 'その他')}")
        with col6: # 新規追加
            st.markdown(f"**学習集団:** {selected_lesson.get('group_type', '全体')}")    
        
        # 単元名は別途表示（関連カードセクションと連動させるため）
        st.markdown(f"<p style='font-size:1.1em; font-weight:bold; margin-top:10px;'>単元名: <span style='color:#8A2BE2;'>{selected_lesson.get('unit_name', '単元なし')}</span></p>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # --- 単元の授業の流れ (新規追加または既存セクションを拡張) ---
        if selected_lesson.get('unit_name') and selected_lesson.get('unit_name') != '単元なし':
            unit_name_to_search = selected_lesson['unit_name']
            all_lessons_in_unit = [
                lesson for lesson in st.session_state.lesson_data
                if lesson.get('unit_name') == unit_name_to_search
            ]

            # 単元内での順番 (unit_order) でソート
            sorted_lessons_in_unit = sorted(all_lessons_in_unit, key=lambda x: x.get('unit_order', 9999))

            if sorted_lessons_in_unit:
             st.markdown(f"<h3><span class='header-icon'>📚</span>「{unit_name_to_search}」の授業の流れ</h3>", unsafe_allow_html=True)
             st.markdown("<ol class='flow-list'>", unsafe_allow_html=True) # 番号付きリスト
            
             for lesson_in_unit in sorted_lessons_in_unit:
                 # unit_lesson_title が存在すればそれを使用、なければ unit_name を使用
                 display_title = lesson_in_unit.get('unit_lesson_title') if lesson_in_unit.get('unit_lesson_title') else lesson_in_unit['unit_name'] 
                 is_current_lesson = (lesson_in_unit['id'] == selected_lesson['id'])
                
                 if is_current_lesson:
                     st.markdown(f"<li style='font-weight: bold; color: #8A2BE2;'>{display_title} 【現在の授業】</li>", unsafe_allow_html=True)
                 else:
                    # 他の授業カードへのリンク（クリックで詳細に飛ぶ）
                    # Streamlitのボタンを直接使って、非表示のボタンで遷移をトリガーする
                     st.markdown(f"""
                         <li>
                             <a href="#" onclick="document.querySelector('button[data-testid=\"stButton_unit_flow_link_direct_{lesson_in_unit['id']}\"]').click(); return false;" style="text-decoration: none; color: inherit;">
                                 {display_title}
                             </a>
                         </li>
                     """, unsafe_allow_html=True)
                     # 実際の遷移を処理する非表示のボタン（display:noneで完全に隠す）
                     st.button(
                         "隠しボタン", # ボタンのテキストは表示されないので何でもOK
                         key=f"unit_flow_link_direct_{lesson_in_unit['id']}",
                         on_click=set_detail_page,
                         args=(lesson_in_unit['id'],),
                         help="この授業の詳細を表示します",
                     )
            
            st.markdown("</ol>", unsafe_allow_html=True)

        st.markdown("---") # 区切り線
        # 既存の「準備物」以下のセクションはそのまま残す

        # 準備物
        if selected_lesson['materials']:
            
            st.markdown("<h3><span class='header-icon'>✂️</span>準備物</h3>", unsafe_allow_html=True)
            st.markdown(f"<p>{selected_lesson['materials']}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # 指導のポイント
        if selected_lesson['points']:
            
            st.markdown("<h3><span class='header-icon'>💡</span>指導のポイント</h3>", unsafe_allow_html=True)
            st.markdown("<ul>", unsafe_allow_html=True)
            for point in selected_lesson['points']:
                st.markdown(f"<li>{point}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # ハッシュタグ
        if selected_lesson['hashtags']:
            
            st.markdown("<h3><span class='header-icon'>#️⃣</span>ハッシュタグ</h3>", unsafe_allow_html=True)
            st.markdown(
                f"<p>{''.join(f'<span class=\"tag-badge\" style=\"margin-right: 5px;\">#{tag}</span>' for tag in selected_lesson['hashtags'])}</p>",
                unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # 教材写真
        if selected_lesson['material_photos']: # リストが空でない場合のみ表示
            
            st.markdown("<h3><span class='header-icon'>📸</span>授業・教材写真</h3>", unsafe_allow_html=True)
            cols = st.columns(3)
            # material_photosリスト内の各URLをst.imageで表示。
            # リストが空でないことは既にif文でチェック済みなので、ここではエラーは出ないはず。
            for i, photo_url in enumerate(selected_lesson['material_photos']):
                with cols[i % 3]:
                    # ここで個別のURLが空文字列でないことを再度チェックするとより安全
                    if photo_url.strip(): 
                        st.image(photo_url, use_container_width=True)
                    else:
                        st.warning("一部の教材写真URLが無効なため表示できませんでした。") # 必要に応じてメッセージ
            st.markdown("</div>", unsafe_allow_html=True)

        # 動画リンク
        if selected_lesson['video_link'].strip(): # video_linkが空文字列でないことを確認 (strip()で空白も考慮)
            
            st.markdown("<h3><span class='header-icon'>▶️</span>参考動画</h3>", unsafe_allow_html=True)
            try:
                st.video(selected_lesson['video_link'])
            except Exception as e:
                st.warning(f"動画の読み込み中に問題が発生しました。リンクを確認してください。エラー: {e}")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            # 動画リンクが空の場合にメッセージを表示
            st.markdown("<h3><span class='header-icon'>▶️</span>参考動画</h3>", unsafe_allow_html=True)
            st.info("参考動画は登録されていません。")
            st.markdown("</div>", unsafe_allow_html=True)


        # 詳細資料ダウンロード
        # 既存のif文の条件を変更
        if selected_lesson['detail_word_url'] or selected_lesson['detail_pdf_url'] or selected_lesson['detail_ppt_url'] or selected_lesson['detail_excel_url']: # ★変更
            st.markdown("<h3><span class='header-icon'>📄</span>詳細資料ダウンロード</h3>", unsafe_allow_html=True)
            if selected_lesson['detail_word_url']:
                st.markdown(f'<a href="{selected_lesson["detail_word_url"]}" target="_blank" style="text-decoration: none;"><button style="background-color: #264A9D; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; margin-right: 10px;">📖 指導案 (Word)</button></a>', unsafe_allow_html=True)
            if selected_lesson['detail_pdf_url']:
                st.markdown(f'<a href="{selected_lesson["detail_pdf_url"]}" target="_blank" style="text-decoration: none;"><button style="background-color: #B40000; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; margin-right: 10px;">📚 指導案 (PDF)</button></a>', unsafe_allow_html=True)
            if selected_lesson['detail_ppt_url']: # ★追加
                st.markdown(f'<a href="{selected_lesson["detail_ppt_url"]}" target="_blank" style="text-decoration: none;"><button style="background-color: #D24726; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; margin-right: 10px;">📊 授業資料 (PowerPoint)</button></a>', unsafe_allow_html=True)
            if selected_lesson['detail_excel_url']: # ★追加
                st.markdown(f'<a href="{selected_lesson["detail_excel_url"]}" target="_blank" style="text-decoration: none;"><button style="background-color: #0E6839; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; margin-right: 10px;">📈 評価シート (Excel)</button></a>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.button("↩️ 一覧に戻る", on_click=back_to_list, key="back_to_list_btn_bottom")

    else:
        st.error("指定された授業カードが見つかりませんでした。")
        st.button("↩️ 一覧に戻る", on_click=back_to_list)

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    /* General body and text */
    body {
        font-family: 'Noto Sans JP', sans-serif;
        color: #333;
        background-color: #f0f2f6;
    }
    .stApp {
        max-width: 1200px;
        margin: auto;
        padding: 20px;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
        font-weight: 700;
    }
    h1 {
        text-align: center;
        color: #8A2BE2; /* 紫 */
        font-size: 2.5em;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
    }
    
    p {
        line-height: 1.6;
        font-size: 1.05em;
    }
    .stButton > button {
        /* ここは詳細ページや一覧ページで使われるボタン全般に適用されます */
        background-color: #4A90E2 !important; /* 明るい青 */
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-size: 1em !important;
        font-weight: bold !important;
        cursor: pointer !important;
        transition: background-color 0.3s ease, transform 0.2s ease !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }
    .stButton > button:hover {
        background-color: #357ABD !important; /* ホバー時の暗めの青 */
        transform: translateY(-2px) !important;
    }
    /* Secondary buttons (e.g., related lessons) */
    /* unit_flow_link_hidden_btn_ の data-testid をターゲットに */
    button[data-testid^="stButton_unit_flow_link_hidden_btn_"] {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
        display: none !important; /* 見えないように */
        height: 0 !important; /* 高さを0にする */
        width: 0 !important; /* 幅を0にする */
        overflow: hidden !important; /* 内容を隠す */
    }

    /* Sidebar specific styles */
    .stSidebar .stSelectbox, .stSidebar .stMultiSelect, .stSidebar .stTextInput {
        margin-bottom: 10px;
    }
    .stSidebar .stButton > button {
        width: 100%;
        margin-top: 5px;
    }
    .stSidebar .stFileUploader {
        margin-top: 15px;
    }
    .stSidebar h2, .stSidebar h3 {
        color: #8A2BE2;
        border-bottom: 2px solid #eee;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }
    .stSidebar .stInfo, .stSidebar .stWarning {
        font-size: 0.9em;
    }

    /* Lesson Card Grid */
    .lesson-card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 30px;
        margin-top: 30px;
    }
    .lesson-card {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        overflow: hidden;
        display: flex;
        flex-direction: column;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        border: 1px solid #e0e0e0;
    }
    .lesson-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    .lesson-card-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-bottom: 1px solid #eee;
    }
    .lesson-card-content {
        padding: 20px;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .lesson-card-title {
        font-size: 1.5em;
        font-weight: bold;
        color: #333;
        margin-bottom: 8px;
        line-height: 1.3;
    }
    .lesson-card-catchcopy {
        font-size: 0.9em;
        color: #777;
        margin-bottom: 10px;
        min-height: 2.5em; /* 複数行対応 */
    }
    .lesson-card-goal {
        font-size: 0.95em;
        color: #555;
        margin-bottom: 15px;
        border-left: 3px solid #FF6347;
        padding-left: 8px;
        min-height: 3em; /* 複数行対応 */
    }
    .lesson-card-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        font-size: 0.9em;
        color: #666;
        margin-bottom: 15px;
    }
    .lesson-card-meta span .icon {
        margin-right: 5px;
        color: #8A2BE2;
    }
    .lesson-card-tags {
        margin-top: 15px;
        margin-bottom: 15px;
        min-height: 3em; /* 複数行対応 */
    }
    .tag-badge {
        display: inline-block;
        background-color: #e6e6fa; /* 薄い紫 */
        color: #8A2BE2;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8em;
        margin-right: 5px;
        margin-bottom: 5px;
        white-space: nowrap;
    }
    .lesson-card .stButton > button {
        width: 100%;
        margin-top: auto; /* ボタンをカードの下部に固定 */
    }

    /* Detail Page Styles */
    .detail-section {
        background-color: white;
        border-radius: 12px;
        padding: 25px 30px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        border: 1px solid #e0e0e0;
    }
    .detail-section h3 {
        color: #8A2BE2;
        font-size: 1.6em;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 2px solid #f0e6fa;
        display: flex;
        align-items: center;
    }
    .detail-section h3 .header-icon {
        margin-right: 10px;
        font-size: 1.2em;
        color: #FF6347; /* 目を引くアイコンカラー */
    }
    .detail-section ul {
        list-style-type: disc;
        margin-left: 25px;
        padding-left: 0;
    }
    .detail-section li {
        margin-bottom: 8px;
        line-height: 1.6;
        font-size: 1.05em;
    }
    .stImage > img {
        border-radius: 12px;
        margin-bottom: 20px;
        /* height: auto;  高さを自動調整し、幅いっぱいに表示されるように */
        /* object-fit: contain; /* 必要に応じて、画像全体が見えるように調整 */
        max-height: 500px; /* 例えば、最大高さを設定して大きくなりすぎないように制御 */
    }

    /* Streamlit specific adjustments */
    .css-1d391kg.e16z5j6o2 { /* main content area */
        padding-top: 30px;
        padding-bottom: 30px;
    }
    .css-1lcbmhc.e16z5j6o3, .css-1lcbmhc.e1fb7f71 { /* sidebar width */
        width: 350px;
    }
</style>
""", unsafe_allow_html=True)