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
    </style>
    """, unsafe_allow_html=True)

load_css()

# --- Load Data from CSV ---
# 'pages'フォルダと同じ階層に lesson_cards.csv を置いてください。
try:
    lesson_data_df = pd.read_csv(
        "lesson_cards.csv",
        converters={
            'introduction_flow': lambda x: x.split(';') if pd.notna(x) else [], # 導入フロー
            'activity_flow': lambda x: x.split(';') if pd.notna(x) else [],     # 活動フロー
            'reflection_flow': lambda x: x.split(';') if pd.notna(x) else [],   # 振り返りフロー
            'points': lambda x: x.split(';') if pd.notna(x) else [],
            'hashtags': lambda x: x.split(',') if pd.notna(x) else [],
            'material_photos': lambda x: x.split(';') if pd.notna(x) else []
        }
    )
    # ICT活用有無のTRUE/FALSEをbool型に変換
    lesson_data_df['ict_use'] = lesson_data_df['ict_use'].astype(bool)
    lesson_data_raw = lesson_data_df.to_dict(orient='records')
except FileNotFoundError:
    st.error("`lesson_cards.csv` ファイルが見つかりませんでした。`pages` フォルダと同じ階層に配置してください。")
    st.stop()
except Exception as e:
    st.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
    st.stop()


# st.session_stateの初期化
if 'current_lesson_id' not in st.session_state:
    st.session_state.current_lesson_id = None
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'selected_hashtags' not in st.session_state:
    st.session_state.selected_hashtags = []
if 'lesson_data' not in st.session_state:
    st.session_state.lesson_data = lesson_data_raw # アプリ内でデータを更新できるようにセッションステートに保持

# --- Helper Functions ---
def set_detail_page(lesson_id):
    """詳細ページへの遷移をトリガーする関数"""
    st.session_state.current_lesson_id = lesson_id
    # 詳細ページに遷移する際に、フロー表示状態をリセット
    st.session_state.show_introduction_flow = False
    st.session_state.show_activity_flow = False
    st.session_state.show_reflection_flow = False

def back_to_list():
    """一覧ページに戻る関数"""
    st.session_state.current_lesson_id = None
    # リストに戻る際にも、フロー表示状態をリセット
    st.session_state.show_introduction_flow = False
    st.session_state.show_activity_flow = False
    st.session_state.show_reflection_flow = False

# 授業カードのヘッダーカラム定義
LESSON_CARD_COLUMNS = [
    "id", "title", "catch_copy", "goal", "target_grade", "disability_type", 
    "duration", "materials", "introduction_flow", "activity_flow", "reflection_flow", "points", "hashtags", 
    "image", "material_photos", "video_link", "detail_word_url", "detail_pdf_url", "ict_use"
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
        worksheet.write_comment('I1', '例: 課題の提示;本時の目標共有 (セミコロン区切りで複数行)') # 変更
        worksheet.write_comment('J1', '例: 商品選び;お金の支払い練習 (セミコロン区切りで複数行)') # 変更
        worksheet.write_comment('K1', '例: できたことの共有;次回の課題 (セミコロン区切りで複数行)') # 変更
        worksheet.write_comment('L1', '例: スモールステップで指導;具体物を用意 (セミコロン区切り)')
        worksheet.write_comment('M1', '例: 生活単元,自立活動 (カンマ区切り)')
        worksheet.write_comment('N1', 'メインとなる画像URL (無い場合は空欄でOK)')
        worksheet.write_comment('O1', '教材写真などのURL (セミコロン区切り、無い場合は空欄でOK)')
        worksheet.write_comment('P1', 'YouTubeなどの動画URL (無い場合は空欄でOK)')
        worksheet.write_comment('Q1', '指導案WordファイルのダウンロードURL (無い場合は空欄でOK)')
        worksheet.write_comment('R1', '指導案PDFファイルのダウンロードURL (無い場合は空欄でOK)')
        worksheet.write_comment('S1', 'TRUEまたはFALSE')
    processed_data = output.getvalue()
    return processed_data

# CSVテンプレートダウンロード関数
def get_csv_template():
    template_df = pd.DataFrame(columns=LESSON_CARD_COLUMNS)
    output = BytesIO()
    # CSVではコメント機能がないため、データフレームのみを書き出す
    template_df.to_csv(output, index=False, encoding='utf-8-sig') # Excelで開いたときに文字化けしないように'utf-8-sig'
    processed_data = output.getvalue()
    return processed_data

# --- Sidebar for Data Entry ---
with st.sidebar:
    st.header("📚 データ登録・管理")
    st.markdown("---")

    st.subheader("① Googleフォーム方式")
    st.info("""
        Googleフォームで入力されたデータは、自動的にGoogleスプレッドシートに蓄積され、このアプリに反映されます。
        以下のボタンからフォームを開き、新しい授業カードを登録してください。
    """)
    # !!! ここに実際のGoogleフォームのリンクを貼り付けてください !!!
    google_form_link = "https://forms.gle/YOUR_GOOGLE_FORM_LINK" 
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
    excel_data_for_download = get_excel_template() # 関数呼び出し
    st.download_button(
        label="⬇️ Excelテンプレートをダウンロード",
        data=excel_data_for_download,
        file_name="授業カードテンプレート.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        help="テンプレートをダウンロードして、新しい授業カード情報を入力してください。"
    )

    # CSVテンプレートのダウンロード
    csv_data_for_download = get_csv_template() # 関数呼び出し
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
            
            # 必須カラムの存在チェック
            required_cols = ["title", "goal"] # 例としてタイトルとねらいを必須とする
            if not all(col in new_data_df.columns for col in required_cols):
                st.error(f"ファイルに以下の必須項目が含まれていません: {', '.join(required_cols)}")
            else:
                # コンバータと同様の処理をアップロードデータにも適用
                # 存在しないカラムはエラーにならないように.get()を使用
                def process_list_column(df, col_name, separator):
                    if col_name in df.columns:
                        return df[col_name].apply(lambda x: x.split(separator) if pd.notna(x) else [])
                    return [[]] * len(df) # カラムがない場合は空のリストを返す

                new_data_df['introduction_flow'] = process_list_column(new_data_df, 'introduction_flow', ';')
                new_data_df['activity_flow'] = process_list_column(new_data_df, 'activity_flow', ';')
                new_data_df['reflection_flow'] = process_list_column(new_data_df, 'reflection_flow', ';')
                new_data_df['points'] = process_list_column(new_data_df, 'points', ';')
                new_data_df['hashtags'] = process_list_column(new_data_df, 'hashtags', ',')
                new_data_df['material_photos'] = process_list_column(new_data_df, 'material_photos', ';')

                if 'ict_use' in new_data_df.columns:
                    # Excelから読み込むと'TRUE'/'FALSE'文字列になる場合があるので変換
                    new_data_df['ict_use'] = new_data_df['ict_use'].astype(str).str.lower().map({'true': True, 'false': False}).fillna(False)
                else:
                    new_data_df['ict_use'] = False # デフォルト値

                # IDの重複を避けるためのロジック
                existing_ids = {d['id'] for d in st.session_state.lesson_data}
                max_id = max(existing_ids) if existing_ids else 0

                new_entries = []
                for _, row in new_data_df.iterrows():
                    # 既存IDが指定されていればそれを使用、なければ新しいIDを生成
                    current_id = row.get('id')
                    if pd.isna(current_id) or current_id in existing_ids:
                        max_id += 1
                        row_id = max_id
                    else:
                        try:
                            row_id = int(current_id)
                            if row_id in existing_ids: # Excel/CSV内の重複も考慮
                                max_id += 1
                                row_id = max_id
                        except ValueError: # idが数値でない場合
                            max_id += 1
                            row_id = max_id
                    
                    # 辞書に変換する前に、存在しないカラムにデフォルト値を設定
                    # CSVの読み込み時のカラムと整合性を取る
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
                        'ict_use': row.get('ict_use', False)
                    }
                    new_entries.append(lesson_dict)
                    existing_ids.add(row_id) # 新しく追加されたIDも記録

                # 既存データと新しいデータを結合
                st.session_state.lesson_data.extend(new_entries)
                st.success(f"{len(new_entries)}件の授業カードをファイルから追加しました！")
                st.experimental_rerun() # データ更新後に再描画
        except Exception as e:
            st.error(f"ファイルの読み込みまたは処理中にエラーが発生しました: {e}")
            st.exception(e) # 詳細なエラーメッセージを表示
    st.markdown("---")

# --- Main Page Logic ---
if st.session_state.current_lesson_id is None:
    # --- Lesson Card List View ---
    st.markdown("<h1>🃏 授業カードライブラリー</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1em; color: #555;'>先生方の実践授業アイデアを検索し、日々の指導に役立てましょう！</p>", unsafe_allow_html=True)

    # Search and Filter Section
    search_col, tag_col = st.columns([0.6, 0.4])
    with search_col:
        st.session_state.search_query = st.text_input("キーワードで検索", st.session_state.search_query, placeholder="例: 買い物、生活単元、小学部", key="search_input")
    
    # Extract all unique hashtags from current lesson data
    all_hashtags = sorted(list(set(tag for lesson in st.session_state.lesson_data for tag in lesson['hashtags'] if tag)))

    with tag_col:
        st.session_state.selected_hashtags = st.multiselect(
            "ハッシュタグで絞り込み", 
            options=all_hashtags, 
            default=st.session_state.selected_hashtags,
            placeholder="選択してください"
        )
    
    filtered_lessons = []
    for lesson in st.session_state.lesson_data:
        match_search = True
        match_tags = True

        # Keyword search
        if st.session_state.search_query:
            search_lower = st.session_state.search_query.lower()
            # 検索対象カラムを追加: catch_copy, materials, introduction_flow, activity_flow, reflection_flow, points
            if not (search_lower in lesson['title'].lower() or
                    search_lower in lesson['catch_copy'].lower() or
                    search_lower in lesson['goal'].lower() or
                    search_lower in lesson['target_grade'].lower() or
                    search_lower in lesson['disability_type'].lower() or
                    lesson['materials'] and search_lower in lesson['materials'].lower() or 
                    any(search_lower in step.lower() for step in lesson['introduction_flow']) or 
                    any(search_lower in step.lower() for step in lesson['activity_flow']) or     
                    any(search_lower in step.lower() for step in lesson['reflection_flow']) or   
                    any(search_lower in point.lower() for point in lesson['points']) or 
                    any(search_lower in t.lower() for t in lesson['hashtags'])):
                match_search = False
        
        # Hashtag filter
        if st.session_state.selected_hashtags:
            if not all(tag in lesson['hashtags'] for tag in st.session_state.selected_hashtags):
                match_tags = False
        
        if match_search and match_tags:
            filtered_lessons.append(lesson)

    st.markdown("<div class='lesson-card-grid'>", unsafe_allow_html=True)
    if filtered_lessons:
        for lesson in filtered_lessons:
            st.markdown(f"""
                <div class="lesson-card">
                    <img class="lesson-card-image" src="{lesson['image'] if lesson['image'] else 'https://via.placeholder.com/400x200?text=No+Image'}" alt="{lesson['title']}">
                    <div class="lesson-card-content">
                        <div>
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
                            {''.join(f'<span class="tag-badge">#{tag}</span>' for tag in lesson['hashtags'] if tag)}
                        </div>
                        {st.button("詳細を見る ➡", key=f"detail_btn_{lesson['id']}", on_click=set_detail_page, args=(lesson['id'],))}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    else:
        st.info("条件に一致する授業カードは見つかりませんでした。")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- Lesson Card Detail View ---
    selected_lesson = next((lesson for lesson in st.session_state.lesson_data if lesson['id'] == st.session_state.current_lesson_id), None)

    if selected_lesson:
        st.button("↩️ 一覧に戻る", on_click=back_to_list, key="back_to_list_btn_top")

        st.markdown(f"<h1 class='detail-header'>{selected_lesson['title']}</h1>", unsafe_allow_html=True)
        if selected_lesson['catch_copy']:
            st.markdown(f"<h3 class='detail-header'>{selected_lesson['catch_copy']}</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<br>", unsafe_allow_html=True) # レイアウト調整

        # メインイメージ
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
                    list-style-type: decimal; /* 箇条書きを数字に */
                    margin-left: 20px;
                    padding-left: 0;
                }
                .flow-list li {
                    margin-bottom: 5px;
                    line-height: 1.6;
                }
            </style>
        """, unsafe_allow_html=True)

        st.subheader("授業の流れ")
        flow_cols = st.columns(3)

        with flow_cols[0]:
            if st.button("導入を表示", key=f"show_intro_{selected_lesson['id']}"):
                st.session_state.show_introduction_flow = not st.session_state.show_introduction_flow
                st.session_state.show_activity_flow = False
                st.session_state.show_reflection_flow = False
        with flow_cols[1]:
            if st.button("活動を表示", key=f"show_activity_{selected_lesson['id']}"):
                st.session_state.show_activity_flow = not st.session_state.show_activity_flow
                st.session_state.show_introduction_flow = False
                st.session_state.show_reflection_flow = False
        with flow_cols[2]:
            if st.button("振り返りを表示", key=f"show_reflection_{selected_lesson['id']}"):
                st.session_state.show_reflection_flow = not st.session_state.show_reflection_flow
                st.session_state.show_introduction_flow = False
                st.session_state.show_activity_flow = False
        
        # 導入フローの表示
        if st.session_state.show_introduction_flow:
            if selected_lesson['introduction_flow']:
                st.markdown("<div class='flow-section'>", unsafe_allow_html=True)
                st.markdown("<h4><span class='icon'>🚀</span>導入</h4>", unsafe_allow_html=True)
                st.markdown("<ol class='flow-list'>", unsafe_allow_html=True)
                for step in selected_lesson['introduction_flow']:
                    st.markdown(f"<li>{step}</li>", unsafe_allow_html=True)
                st.markdown("</ol>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("導入の記載はありません。")
        
        # 活動フローの表示
        if st.session_state.show_activity_flow:
            if selected_lesson['activity_flow']:
                st.markdown("<div class='flow-section'>", unsafe_allow_html=True)
                st.markdown("<h4><span class='icon'>💡</span>活動</h4>", unsafe_allow_html=True)
                st.markdown("<ol class='flow-list'>", unsafe_allow_html=True)
                for step in selected_lesson['activity_flow']:
                    st.markdown(f"<li>{step}</li>", unsafe_allow_html=True)
                st.markdown("</ol>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("活動の記載はありません。")

        # 振り返りフローの表示
        if st.session_state.show_reflection_flow:
            if selected_lesson['reflection_flow']:
                st.markdown("<div class='flow-section'>", unsafe_allow_html=True)
                st.markdown("<h4><span class='icon'>💭</span>振り返り</h4>", unsafe_allow_html=True)
                st.markdown("<ol class='flow-list'>", unsafe_allow_html=True)
                for step in selected_lesson['reflection_flow']:
                    st.markdown(f"<li>{step}</li>", unsafe_allow_html=True)
                st.markdown("</ol>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("振り返りの記載はありません。")

        st.markdown("---")

        # ねらい
        st.markdown("<div class='detail-section'>", unsafe_allow_html=True)
        st.markdown("<h3><span class='header-icon'>🎯</span>ねらい</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{selected_lesson['goal']}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 対象・種別・時間
        st.markdown("<div class='detail-section'>", unsafe_allow_html=True)
        st.markdown("<h3><span class='header-icon'>ℹ️</span>基本情報</h3>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"**対象学年:** {selected_lesson['target_grade']}")
        with col2:
            st.markdown(f"**障害種別:** {selected_lesson['disability_type']}")
        with col3:
            st.markdown(f"**時間:** {selected_lesson['duration']}")
        with col4:
            st.markdown(f"**ICT活用:** {'あり' if selected_lesson['ict_use'] else 'なし'}")
        st.markdown("</div>", unsafe_allow_html=True)

        # 準備物
        if selected_lesson['materials']:
            st.markdown("<div class='detail-section'>", unsafe_allow_html=True)
            st.markdown("<h3><span class='header-icon'>🎒</span>準備物</h3>", unsafe_allow_html=True)
            st.markdown(f"<p>{selected_lesson['materials']}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # 指導のポイント
        if selected_lesson['points']:
            st.markdown("<div class='detail-section'>", unsafe_allow_html=True)
            st.markdown("<h3><span class='header-icon'>💡</span>指導のポイント</h3>", unsafe_allow_html=True)
            st.markdown("<ul class='flow-list'>", unsafe_allow_html=True)
            for point in selected_lesson['points']:
                st.markdown(f"<li>{point}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # 教材写真ギャラリー
        if selected_lesson['material_photos']:
            st.markdown("<div class='detail-section'>", unsafe_allow_html=True)
            st.markdown("<h3><span class='header-icon'>📸</span>教材写真</h3>", unsafe_allow_html=True)
            st.markdown("<div class='detail-image-gallery'>", unsafe_allow_html=True)
            for photo_url in selected_lesson['material_photos']:
                st.image(photo_url, use_column_width=False, width=280) # 固定幅で表示
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # 参考動画
        if selected_lesson['video_link']:
            st.markdown("<div class='detail-section'>", unsafe_allow_html=True)
            st.markdown("<h3><span class='header-icon'>▶️</span>参考動画</h3>", unsafe_allow_html=True)
            st.video(selected_lesson['video_link'])
            st.markdown("</div>", unsafe_allow_html=True)

        # ハッシュタグ
        if selected_lesson['hashtags']:
            st.markdown("<div class='detail-section detail-tag-container'>", unsafe_allow_html=True)
            st.markdown("<h3><span class='header-icon'>🏷️</span>タグ</h3>", unsafe_allow_html=True)
            st.markdown("<div class='lesson-card-tags'>", unsafe_allow_html=True)
            for tag in selected_lesson['hashtags']:
                st.markdown(f"<span class='tag-badge'>#{tag}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # 指導案ダウンロード
        if selected_lesson['detail_word_url'] or selected_lesson['detail_pdf_url']:
            st.markdown("<div class='download-button-wrapper'>", unsafe_allow_html=True)
            download_cols = st.columns(2)
            if selected_lesson['detail_word_url']:
                with download_cols[0]:
                    st.markdown(
                        f"""
                        <a href="{selected_lesson['detail_word_url']}" target="_blank">
                            <button>
                                <span class="icon">📄</span>Word指導案をダウンロード
                            </button>
                        </a>
                        """, unsafe_allow_html=True
                    )
            if selected_lesson['detail_pdf_url']:
                with download_cols[1]:
                    st.markdown(
                        f"""
                        <a href="{selected_lesson['detail_pdf_url']}" target="_blank">
                            <button>
                                <span class="icon">⬇️</span>PDF指導案をダウンロード
                            </button>
                        </a>
                        """, unsafe_allow_html=True
                    )
            st.markdown("</div>", unsafe_allow_html=True)

        st.button("↩️ 一覧に戻る", on_click=back_to_list, key="back_to_list_btn_bottom")

    else:
        st.error("指定された授業カードが見つかりませんでした。")