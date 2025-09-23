import streamlit as st
import pandas as pd
import base64
import re # ハッシュタグ抽出用
import io # Word/Excelファイルダウンロード・アップロード用
from io import BytesIO # Excelアップロード用
import xlsxwriter # エラー解決のためにインポートを追加

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
            text-align: left;
            margin-bottom: 25px;
        }
        .detail-main-image {
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
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
                /* Detail Button Styling (上書きまたは追加) */
        .lesson-card .stButton > button { /* .lesson-card 内のボタンにスタイルを適用 */
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
        .lesson-card .stButton > button:hover {
            border-color: #8A2BE2;
            color: white;
            background-color: #8A2BE2;
            transform: translateY(-3px);
            box-shadow: 0 8px 15px rgba(138,43,226,0.2);
        }
    </style>
    """, unsafe_allow_html=True)

load_css()


# 'pages'フォルダと同じ階層に lesson_cards.csv を置いてください。
try:
    lesson_data_df = pd.read_csv(
        "lesson_cards.csv",
        converters={
            'introduction_flow': lambda x: x.split(';') if pd.notna(x) else [],  # 導入フロー
            'activity_flow': lambda x: x.split(';') if pd.notna(x) else [],      # 活動フロー
            'reflection_flow': lambda x: x.split(';') if pd.notna(x) else [],    # 振り返りフロー
            'points': lambda x: x.split(';') if pd.notna(x) else [],
            'hashtags': lambda x: x.split(',') if pd.notna(x) else [],
            'material_photos': lambda x: x.split(';') if pd.notna(x) else []
            # !!! ここに unit_name のコンバーターを追加/修正 !!!
            # unit_name は通常単一の文字列なので、リスト変換は不要。
            # ただし、NaN値は空文字列として扱うと良い。
            ,'unit_name': lambda x: str(x) if pd.notna(x) else '',
             'unit_order': lambda x: int(x) if pd.notna(x) and str(x).isdigit() else 9999, # 数値に変換、ない場合は大きい値
             'unit_lesson_title': lambda x: str(x) if pd.notna(x) else '' # 新規追加
        }
    )
    # 新規カラムのデフォルト値設定（もしCSVにカラムがない場合）
    if 'unit_order' not in lesson_data_df.columns:
        lesson_data_df['unit_order'] = 9999
    if 'unit_lesson_title' not in lesson_data_df.columns:
        lesson_data_df['unit_lesson_title'] = lesson_data_df['title'] # デフォルトでtitleを使用     
    # ICT活用有無のTRUE/FALSEをbool型に変換
    if 'ict_use' in lesson_data_df.columns:
        lesson_data_df['ict_use'] = lesson_data_df['ict_use'].astype(bool)
    else:
        lesson_data_df['ict_use'] = False # カラムがない場合はデフォルトでFalse

    # 'subject', 'unit_name', 'group_type' カラムが存在しない場合、デフォルト値で作成
    if 'subject' not in lesson_data_df.columns:
        lesson_data_df['subject'] = 'その他'
    if 'unit_name' not in lesson_data_df.columns: # ここを修正
        lesson_data_df['unit_name'] = '単元なし' # カラムがない場合はデフォルト値
    # !!! 既存のデータが空文字列の場合に '単元なし' に変換する処理を追加 !!!
    lesson_data_df['unit_name'] = lesson_data_df['unit_name'].apply(lambda x: '単元なし' if str(x).strip() == '' or str(x).lower() == 'nan' else str(x).strip())


    if 'group_type' not in lesson_data_df.columns: # 新規追加
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
    "id", "title", "catch_copy", "goal", "target_grade", "disability_type",
    "duration", "materials", "introduction_flow", "activity_flow", "reflection_flow", "points", "hashtags",
    "image", "material_photos", "video_link", "detail_word_url", "detail_pdf_url", "ict_use", "subject",
    "unit_name", "group_type", "unit_order", "unit_lesson_title" # 新規追加
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
        worksheet.write_comment('B1', '例: 「買い物名人になろう！」')
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
        worksheet.write_comment('S1', 'TRUEまたはFALSE')
        worksheet.write_comment('T1', '例: 生活単元学習,国語,算数など')
        worksheet.write_comment('U1', '例: お金の学習,お店屋さんごっこ  (単元名)') # 新規追加コメント
        worksheet.write_comment('V1', '例: 全体,個別,小グループ  (学習集団の単位)') # 新規追加コメント
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

with st.sidebar:
    st.header("📚 データ登録・管理")
    st.markdown("---")

    st.subheader("① Googleフォーム方式")
    st.info("""
    Googleフォームで入力されたデータは、自動的にGoogleスプレッドシートに蓄積され、このアプリに反映されます。
    以下のボタンからフォームを開き、新しい授業カードを登録してください。
    """)
    #!!! ここに実際のGoogleフォームのリンクを貼り付けてください !!!
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
    # Excelテンプレートのダウンロード
    excel_data_for_download = get_excel_template()
    st.download_button(
        label="⬇️ Excelテンプレートをダウンロード",
        data=excel_data_for_download,
        file_name="授業カードテンプレート.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        help="テンプレートをダウンロードして、新しい授業カード情報を入力してください。"
    )
    # CSVテンプレートのダウンロード
    csv_data_for_download = get_csv_template()
    st.download_button(
        label="⬇️ CSVテンプレートをダウンロード",
        data=csv_data_for_download,
        file_name="授業カードテンプレート.csv",
        mime="text/csv",
        help="テンプレートをダウンロードして、新しい授業カード情報を入力してください。"
    )

    # ファイルのアップロード
    uploaded_file = st.file_uploader("⬆️ ファイルをアップロード", type=["xlsx", "csv"], help="入力済みのExcelまたはCSVファイルをアップロードして、データを追加します。")

        
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.xlsx'):
                new_data_df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.csv'):
                new_data_df = pd.read_csv(uploaded_file)
            else:
                st.error("サポートされていないファイル形式です。Excel (.xlsx) または CSV (.csv) ファイルをアップロードしてください。")
                st.stop()

            required_cols = ["title", "goal"]
            if not all(col in new_data_df.columns for col in required_cols):
                st.error(f"ファイルに以下の必須項目が含まれていません: {', '.join(required_cols)}")
                # どのカラムが不足しているか具体的に示す
                missing_cols = [col for col in required_cols if col not in new_data_df.columns]
                st.info(f"不足しているカラム: {', '.join(missing_cols)}")
            else:
                def process_list_column(df, col_name, separator):
                    if col_name in df.columns:
                        return df[col_name].apply(lambda x: x.split(separator) if pd.notna(x) and str(x).strip() != '' else [])
                    return [[]] * len(df)
                
                # 単一文字列カラムのNaN/空文字列処理も同様に強化
                def process_string_column(df, col_name, default_value):
                    if col_name in df.columns:
                        return df[col_name].apply(lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else default_value)
                    return [default_value] * len(df)
                # 新規追加：unit_order, unit_lesson_title の処理
                # unit_order は数値として扱う。NaNや空欄はデフォルトで高い値（例: 9999）に
                if 'unit_order' in new_data_df.columns:
                    new_data_df['unit_order'] = new_data_df['unit_order'].apply(lambda x: int(x) if pd.notna(x) and str(x).strip().isdigit() else 9999)
                else:
                    new_data_df['unit_order'] = 9999 # カラムがない場合はデフォルト値
             
                if 'unit_lesson_title' in new_data_df.columns:
                    new_data_df['unit_lesson_title'] = new_data_df['unit_lesson_title'].apply(lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '')
                else:
                   new_data_df['unit_lesson_title'] = new_data_df.get('title', '単元内の授業') # カラムがない場合はデフォルトでtitleを使用
               
                # ... 既存の lesson_dict の構築部分で新しいカラムを追加 ...
                lesson_dict = {
                    # ... 既存の項目 ...
                   'unit_name': row.get('unit_name', '単元なし'),
                    'group_type': row.get('group_type', '全体'),
                    'unit_order': row.get('unit_order', 9999), # ここもデフォルト値取得ロジックを強化
                    'unit_lesson_title': row.get('unit_lesson_title', row.get('title', '単元内の授業')) # デフォルトでtitleを使用
               }
                new_data_df['introduction_flow'] = process_list_column(new_data_df, 'introduction_flow', ';')
                new_data_df['activity_flow'] = process_list_column(new_data_df, 'activity_flow', ';')
                new_data_df['reflection_flow'] = process_list_column(new_data_df, 'reflection_flow', ';')
                new_data_df['points'] = process_list_column(new_data_df, 'points', ';')
                new_data_df['hashtags'] = process_list_column(new_data_df, 'hashtags', ',')
                new_data_df['material_photos'] = process_list_column(new_data_df, 'material_photos', ';')

                if 'ict_use' in new_data_df.columns:
                    # 'true', 'True', 'TRUE' などに対応し、NaNはFalseに
                    new_data_df['ict_use'] = new_data_df['ict_use'].astype(str).str.lower().apply(lambda x: True if x == 'true' else False)
                else:
                    new_data_df['ict_use'] = False

                # !!! 新規追加：subject, unit_name, group_type も同様に処理 !!!
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
                            # アップロードされたIDが既存の場合も新しいIDを振る
                            if row_id in existing_ids:
                                max_id += 1
                                row_id = max_id
                        except ValueError: # idが数値でない場合
                            max_id += 1
                            row_id = max_id
                    
                    lesson_dict = {
                        'id': row_id,
                        'title': row.get('title', '無題の授業カード'),
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
                        'image': row.get('image', ''),
                        'material_photos': row.get('material_photos', []),
                        'video_link': row.get('video_link', ''),
                        'detail_word_url': row.get('detail_word_url', ''),
                        'detail_pdf_url': row.get('detail_pdf_url', ''),
                        'ict_use': row.get('ict_use', False),
                        'subject': row.get('subject', 'その他'),
                        'unit_name': row.get('unit_name', '単元なし'), # ここもデフォルト値取得ロジックを強化
                        'group_type': row.get('group_type', '全体') 
                    }
                    new_entries.append(lesson_dict)
                    existing_ids.add(row_id) # 新しく生成されたIDも既存IDに加える

                st.session_state.lesson_data.extend(new_entries)
                st.success(f"{len(new_entries)}件の授業カードをファイルから追加しました！")
                st.experimental_rerun()
        except Exception as e:
            st.error(f"ファイルの読み込みまたは処理中にエラーが発生しました: {e}")
            st.exception(e) # デバッグのために例外の詳細を表示

  

        st.markdown("---")
    

    
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
    for lesson in st.session_state.lesson_data:
        match_search = True
        match_tags = True
        match_subject = True
        match_unit = True # 単元フィルターを追加

        # Keyword search
        if st.session_state.search_query:
            search_lower = st.session_state.search_query.lower()
            if not (search_lower in lesson['title'].lower() or
                    search_lower in lesson['subject'].lower() or
                    search_lower in lesson['catch_copy'].lower() or
                    search_lower in lesson['goal'].lower() or
                    search_lower in lesson['target_grade'].lower() or
                    search_lower in lesson['disability_type'].lower() or
                    (lesson['materials'] and search_lower in lesson['materials'].lower()) or 
                    any(search_lower in step.lower() for step in lesson['introduction_flow']) or 
                    any(search_lower in step.lower() for step in lesson['activity_flow']) or     
                    any(search_lower in step.lower() for step in lesson['reflection_flow']) or   
                    any(search_lower in point.lower() for point in lesson['points']) or 
                    any(search_lower in t.lower() for t in lesson['hashtags']) or
                    (lesson.get('unit_name') and search_lower in lesson['unit_name'].lower()) # 単元名も検索対象
                    ):
                match_search = False

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

        if match_search and match_tags and match_subject and match_unit: # フィルター条件に追加
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
                <img class="lesson-card-image" src="{lesson['image'] if lesson['image'] else 'https://via.placeholder.com/400x200?text=No+Image'}" alt="{lesson['title']}">
                <div class="lesson-card-content">
                    <div>
                        {subject_unit_display}
                        <div class="lesson-card-title">{lesson['title']}</div>
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

        st.markdown(f"<h1 class='detail-header'>{selected_lesson['title']}</h1>", unsafe_allow_html=True)
        if selected_lesson['catch_copy']:
            st.markdown(f"<h3 class='detail-header'>{selected_lesson['catch_copy']}</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<br>", unsafe_allow_html=True)

        st.image(selected_lesson['image'] if selected_lesson['image'] else 'https://via.placeholder.com/800x400?text=No+Image', caption=selected_lesson['title'], use_container_width=True)

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
        
        st.markdown("---")

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
            st.markdown(f"**ICT活用:** {'あり' if selected_lesson['ict_use'] else 'なし'}")
        with col5:
            st.markdown(f"**教科:** {selected_lesson.get('subject', 'その他')}")
        with col6: # 新規追加
            st.markdown(f"**学習集団:** {selected_lesson.get('group_type', '全体')}")
        
        # 単元名は別途表示（関連カードセクションと連動させるため）
        st.markdown(f"<p style='font-size:1.1em; font-weight:bold; margin-top:10px;'>単元名: <span style='color:#8A2BE2;'>{selected_lesson.get('unit_name', '単元なし')}</span></p>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # --- この単元の他の授業カード --- (新規追加)
        # --- 単元の授業の流れ (新規追加または既存セクションを拡張) ---
        if selected_lesson.get('unit_name') and selected_lesson.get('unit_name') != '単元なし':
            unit_name_to_search = selected_lesson['unit_name']
            all_lessons_in_unit = [
                lesson for lesson in st.session_state.lesson_data
                if lesson.get('unit_name') == unit_name_to_search
            ]
        
            # 単元内での順番 (unit_order) でソート
            # unit_order が存在しないか不正な場合は最後に表示されるように大きい値にする
            sorted_lessons_in_unit = sorted(all_lessons_in_unit, key=lambda x: x.get('unit_order', 9999))
        
            if sorted_lessons_in_unit:
                
                st.markdown(f"<h3><span class='header-icon'>📚</span>「{unit_name_to_search}」の授業の流れ</h3>", unsafe_allow_html=True)
                st.markdown("<ol class='flow-list'>", unsafe_allow_html=True) # 番号付きリスト

                for lesson_in_unit in sorted_lessons_in_unit:
                    display_title = lesson_in_unit.get('unit_lesson_title') or lesson_in_unit['title']
                    is_current_lesson = (lesson_in_unit['id'] == selected_lesson['id'])
        
                    if is_current_lesson:
                        st.markdown(f"<li style='font-weight: bold; color: #8A2BE2;'>{display_title} 【現在の授業】</li>", unsafe_allow_html=True)
                    else:
                        # 他の授業カードへのリンク（クリックで詳細に飛ぶ）
                        st.markdown(f"""
                            <li>
                                <a href="#" onclick="document.getElementById('unit_flow_link_{lesson_in_unit['id']}').click(); return false;" style="text-decoration: none; color: inherit;">
                                    {display_title}
                                </a>
                                <button id="unit_flow_link_{lesson_in_unit['id']}" style="display:none;" onclick="document.querySelector('[data-testid=\"stButton_{lesson_in_unit['id']}\"]').click()"></button>
                            </li>
                        """, unsafe_allow_html=True)
                        # 実際の遷移を処理する非表示のボタン
                        st.button("", key=f"unit_flow_link_hidden_btn_{lesson_in_unit['id']}", on_click=set_detail_page, args=(lesson_in_unit['id'],), type="secondary")
        
                st.markdown("</ol>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

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
        if selected_lesson['material_photos']:
            
            st.markdown("<h3><span class='header-icon'>📸</span>授業・教材写真</h3>", unsafe_allow_html=True)
            cols = st.columns(3)
            for i, photo_url in enumerate(selected_lesson['material_photos']):
                with cols[i % 3]:
                    st.image(photo_url, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

         # 動画リンク
        if selected_lesson['video_link']: # video_linkが空文字列でないことを確認
            
            st.markdown("<h3><span class='header-icon'>▶️</span>参考動画</h3>", unsafe_allow_html=True)
            try:
                st.video(selected_lesson['video_link'])
            except Exception as e:
                st.warning(f"動画の読み込み中に問題が発生しました。リンクを確認してください。エラー: {e}")
            st.markdown("</div>", unsafe_allow_html=True)

        # 詳細資料ダウンロード
        if selected_lesson['detail_word_url'] or selected_lesson['detail_pdf_url']:
            st.markdown("<div class='detail-section'>", unsafe_allow_html=True)
            st.markdown("<h3><span class='header-icon'>📄</span>詳細資料ダウンロード</h3>", unsafe_allow_html=True)
            if selected_lesson['detail_word_url']:
                st.markdown(f'<a href="{selected_lesson["detail_word_url"]}" target="_blank" style="text-decoration: none;"><button style="background-color: #264A9D; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; margin-right: 10px;">📖 指導案 (Word)</button></a>', unsafe_allow_html=True)
            if selected_lesson['detail_pdf_url']:
                st.markdown(f'<a href="{selected_lesson["detail_pdf_url"]}" target="_blank" style="text-decoration: none;"><button style="background-color: #B40000; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em;">📚 指導案 (PDF)</button></a>', unsafe_allow_html=True)
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
    .detail-header {
        text-align: center;
        color: #8A2BE2;
        margin-bottom: 15px;
    }
    p {
        line-height: 1.6;
        font-size: 1.05em;
    }
    .stButton > button {
        background-color: #8A2BE2; /* ボタンの背景色 */
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-size: 1em;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background-color: #6A1EB2; /* ホバー時の色 */
        transform: translateY(-2px);
    }
    /* Secondary buttons (e.g., related lessons) */
    button[aria-label="クリックで詳細を表示"] {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
        display: none !important; /* 見えないように */
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