import streamlit as st
import pandas as pd
import base64
import re  # ハッシュタグ抽出用
import io  # Word/Excelファイルダウンロード・アップロード用
from io import BytesIO  # Excelアップロード用
import xlsxwriter  # エラー解決のためにインポートを追加

st.set_page_config(
    page_title="授業カードライブラリー",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_css():
    """カスタムCSSを読み込む関数"""
    css = r"""
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

        /* --- ページネーションボタンのスタイル調整 --- */
        /* Streamlitの内部コンテナのdata-testidを利用してセンタリングとギャップ調整 */
        .pagination-container {
            display: flex; /* Flexboxを有効にする */
            justify-content: center; /* 中央寄せ */
            align-items: center;
            gap: 10px; /* ボタン間のスペースを調整 */
            margin-top: 20px;
            margin-bottom: 20px;
            flex-wrap: wrap; /* ボタンが多すぎる場合に折り返す */
        }
        .pagination-container .stButton > button {
            min-width: 40px; /* ページ番号ボタンの最小幅 */
            height: 40px; /* ページ番号ボタンの高さ */
            padding: 0 10px;
            font-size: 1.0em; /* ページ番号ボタンのフォントサイズ */
            border-radius: 20px !important; /* 全てのボタンを角丸に */
            box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
            background-color: #f0f2f6 !important; /* 通常のページ番号ボタンの背景色 */
            color: #555 !important; /* 通常のページ番号ボタンのテキスト色 */
            border: 1px solid #ddd !important;
            margin: 0 !important; /* ボタンが個別に持つmarginをリセット */
        }
        .pagination-container .stButton > button:hover {
            background-color: #e0e0e0 !important;
            border-color: #bbb !important;
            transform: translateY(-1px) !important;
        }
        /* アクティブなページ番号ボタンのスタイル */
        .pagination-container .stButton > button[data-testid="stPageLinkButton-primary"] {
            background-color: #8A2BE2 !important; /* アクティブなページ番号の色 */
            border-color: #8A2BE2 !important;
            color: white !important;
            font-weight: bold !important;
        }
        .pagination-info {
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
            margin: 0 10px;
            white-space: nowrap; /* 折り返しを防ぐ */
        }
        .pagination-container .stMarkdown > div { /* 省略記号 (st.markdown("<span>...</span>") ) のコンテナをターゲット */
            display: flex; /* flexアイテムとして扱われるようにする */
            align-items: center; /* 垂直方向中央揃え */
            height: 40px; /* ボタンの高さに合わせる */
            font-size: 1.2em; /* フォントサイズ調整 */
            color: #777;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


load_css()

# --- Googleフォームへの外部リンク (ここに追加) ---
google_form_css = r"""
    <style>
        .google-form-link-container {
            text-align: center;
            margin-top: 20px;
            margin-bottom: 40px; /* 他のコンテンツとの間にスペースを設ける */
        }
        .google-form-link-button {
            display: inline-flex;
            align-items: center;
            padding: 15px 30px;
            background-color: #4285F4; /* Googleのブランドカラー */
            color: white;
            border-radius: 30px;
            text-decoration: none;
            font-size: 1.3em;
            font-weight: bold;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            letter-spacing: 0.5px;
        }
        .google-form-link-button:hover {
            background-color: #357ae8;
            transform: translateY(-3px);
            box-shadow: 0 9px 20px rgba(0, 0, 0, 0.3);
        }
        .google-form-link-button .icon {
            margin-right: 12px;
            font-size: 1.5em;
            color: white;
        }
    </style>
"""
google_form_html = """
    <div class="google-form-link-container">
        <a href="https://leeson-abfy5bxayhavhoznzexj8r.streamlit.app/" target="_blank" class="google-form-link-button">
            <span class="icon">📝</span> Googleフォームで授業カードを作成！
        </a>
    </div>
"""
st.markdown(google_form_css + google_form_html, unsafe_allow_html=True)
# --- ここまで ---
# --- CSS for Card Layout and General Styling ---
# --- ▼ 戻るボタンの配置 (メインコンテンツの左上) ▼ ---
# st.columnsを使って、左端に配置する
col_back, _ = st.columns([0.15, 0.85])  # ボタン用に狭いカラムを確保
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
            'image': lambda x: str(x) if pd.notna(x) else '',  # メイン画像も空文字列処理を追加
            'detail_word_url': lambda x: str(x) if pd.notna(x) else '',
            'detail_pdf_url': lambda x: str(x) if pd.notna(x) else '',
            'detail_ppt_url': lambda x: str(x) if pd.notna(x) else '',
            'detail_excel_url': lambda x: str(x) if pd.notna(x) else '',
            'target_grade': lambda x: str(x) if pd.notna(x) else '', # target_gradeをstringとして読み込む
        }
    )

    # 新規カラムのデフォルト値設定（もしCSVにカラムがない場合）
    if 'unit_order' not in lesson_data_df.columns:
        lesson_data_df['unit_order'] = 9999
    if 'target_grade' not in lesson_data_df.columns: # target_gradeのデフォルト値設定
        lesson_data_df['target_grade'] = '不明'


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
        lesson_data_df['ict_use'] = 'なし'  # カラムがない場合はデフォルトで「なし」

    # 'subject', 'unit_name', 'group_type' カラムが存在しない場合、デフォルト値で作成
    if 'subject' not in lesson_data_df.columns:
        lesson_data_df['subject'] = 'その他'
    if 'unit_name' not in lesson_data_df.columns:
        lesson_data_df['unit_name'] = '単元なし'
    # !!! 既存のデータが空文字列の場合に '単元なし' に変換する処理を追加 !!!
    lesson_data_df['unit_name'] = lesson_data_df['unit_name'].apply(lambda x: '単元なし' if str(x).strip() == '' or str(x).lower() == 'nan' else str(x).strip())

    if 'group_type' not in lesson_data_df.columns:
        lesson_data_df['group_type'] = '全体'  # 例: 全体, 小グループ, 個別 など

    # 各要素 (辞書) に対して unit_lesson_title キーが存在しない場合は追加し、空文字列で埋める
    lesson_data = lesson_data_df.to_dict(orient='records')
    for lesson in lesson_data:  # FIX: KeyError対策としてsetdefaultを追加
        lesson.setdefault('unit_lesson_title', "")  # FIX: KeyError対策としてsetdefaultを追加
        lesson.setdefault('target_grade', '不明') # target_gradeのsetdefault

    st.session_state.lesson_data = lesson_data  # FIX: st.session_state.lesson_dataをここで初期化

    lesson_data_raw = lesson_data_df.to_dict(orient='records')  # FIX: lesson_data_rawの定義を移動

except FileNotFoundError:
    st.error("lesson_cards.csv ファイルが見つかりませんでした。pages フォルダと同じ階層に配置してください。")
    st.stop()
except Exception as e:
    st.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
    st.exception(e)  # デバッグのために例外の詳細を表示
    st.stop()

# st.session_stateの初期化 (★ここを修正/追加)
if 'current_lesson_id' not in st.session_state:
    st.session_state.current_lesson_id = None
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'selected_hashtags' not in st.session_state:
    st.session_state.selected_hashtags = []
if 'selected_subject' not in st.session_state:  # 教科フィルター
    st.session_state.selected_subject = "全て"
# 単元フィルターを削除
# if 'selected_unit' not in st.session_state:  # 単元フィルターを追加
#     st.session_state.selected_unit = "全て"
if 'lesson_data' not in st.session_state:
    st.session_state.lesson_data = lesson_data_raw  # アプリ内でデータを更新できるようにセッションステートに保持
if 'show_all_flow' not in st.session_state:  # 授業の流れ全体表示フラグ
    st.session_state.show_all_flow = False
if 'current_page' not in st.session_state:  # ページネーション用
    st.session_state.current_page = 1
# --- Helper Functions ---

def set_detail_page(lesson_id):
    """詳細ページへの遷移をトリガーする関数"""
    st.session_state.current_lesson_id = lesson_id
    st.session_state.show_all_flow = False  # 詳細ページに遷移したらフロー表示をリセット

def back_to_list():
    """一覧ページに戻る関数"""
    st.session_state.current_lesson_id = None
    st.session_state.show_all_flow = False  # 一覧に戻ったらフロー表示をリセット

def toggle_all_flow_display():
    """授業の流れ全体の表示を切り替える関数"""
    st.session_state.show_all_flow = not st.session_state.show_all_flow

# ページをセットする関数
def set_page(page_num):
    st.session_state.current_page = page_num
    st.rerun()

# 授業カードのヘッダーカラム定義 (★ここを修正/追加)
LESSON_CARD_COLUMNS = [
    "id", "unit_name", "catch_copy", "goal", "target_grade", "disability_type",
    "duration", "materials", "introduction_flow", "activity_flow", "reflection_flow", "points", "hashtags",
    "image", "material_photos", "video_link", "detail_word_url", "detail_pdf_url",
    "detail_ppt_url", "detail_excel_url",  # ★追加: PowerPointとExcelのURLカラム
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
        # ヘッダーにコメントを追加（入力ガイド） (★ここを追加)
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
        worksheet.write_comment('S1', '指導案PowerPointファイルのダウンロードURL (無い場合は空欄でOK)')  # ★追加
        worksheet.write_comment('T1', '指導案ExcelファイルのダウンロードURL (無い場合は空欄でOK)')  # ★追加
        worksheet.write_comment('U1', 'ICT活用有無 (TRUEまたはFALSE)')  # インデックスがずれるため注意
        worksheet.write_comment('V1', '例: 生活単元学習,国語,算数など (教科)')
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

with st.sidebar:
    st.header("📚 データ登録・管理")
    st.markdown("---")

    st.subheader("ファイルテンプレート")
    st.info("""
    ExcelまたはCSVテンプレートをダウンロードし、入力後にアップロードしてデータを追加できます。
    """)

    # Excelマクロありのサンプルファイルダウンロード (ここから変更箇所)
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

            required_cols = ["unit_name", "goal"]
            if not all(col in new_data_df.columns for col in required_cols):
                st.error(f"ファイルに以下の必須項目が含まれていません: {', '.join(required_cols)}")
                # どのカラムが不足しているか具体的に示す
                missing_cols = [col for col in required_cols if col not in new_data_df.columns]
                st.info(f"不足しているカラム: {', '.join(missing_cols)}")
            else:
                def process_list_column(df, col_name, separator):
                    if col_name in df.columns:
                        # ★変更: リストカラムの処理を強化。空文字列を除外する。
                        return df[col_name].apply(lambda x: [item.strip() for item in str(x).split(separator) if item.strip()] if pd.notna(x) and str(x).strip() != '' else [])
                    return [[]] * len(df)

                # 単一文字列カラムのNaN/空文字列処理も同様に強化 (★ここを追加)
                def process_string_column(df, col_name, default_value):
                    if col_name in df.columns:
                        # NaN, 空文字列, 'nan'文字列をデフォルト値に変換
                        return df[col_name].apply(lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else default_value)
                    return [default_value] * len(df)

                # 新規追加：unit_order, unit_lesson_title の処理 (変更箇所のみ)
                if 'unit_order' in new_data_df.columns:
                    new_data_df['unit_order'] = new_data_df['unit_order'].apply(lambda x: int(x) if pd.notna(x) and str(x).strip().isdigit() else 9999)
                else:
                    new_data_df['unit_order'] = 9999  # カラムがない場合はデフォルト値

                if 'unit_lesson_title' in new_data_df.columns:
                    # NaNや空文字列を適切に処理
                    new_data_df['unit_lesson_title'] = new_data_df['unit_lesson_title'].apply(lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '')
                else:
                    # 'unit_lesson_title' カラムがない場合、'unit_name' から設定
                    new_data_df['unit_lesson_title'] = new_data_df.get('unit_name', '単元内授業')  # デフォルトでunit_nameを使用
                
                # target_gradeの処理
                if 'target_grade' in new_data_df.columns:
                    new_data_df['target_grade'] = process_string_column(new_data_df, 'target_grade', '不明')
                else:
                    new_data_df['target_grade'] = '不明'


                # lesson_dict の構築部分で新しいカラムを追加 (★ここを削除/修正)
                # この部分はループの外に出すべきではないため、後続のループ内で処理されるようにする。
                # 元のコードにあった不要な lesson_dict の定義を削除
                # lesson_dict = {
                #    'unit_name': row.get('unit_name', '単元なし'),
                #     'group_type': row.get('group_type', '全体'),
                #     'unit_order': row.get('unit_order', 9999), # ここもデフォルト値取得ロジックを強化
                #     'unit_lesson_title': row.get('unit_lesson_title', row.get('title', '単元内の授業')) # デフォルトでtitleを使用
                # }

                new_data_df['introduction_flow'] = process_list_column(new_data_df, 'introduction_flow', ';')
                new_data_df['activity_flow'] = process_list_column(new_data_df, 'activity_flow', ';')
                new_data_df['reflection_flow'] = process_list_column(new_data_df, 'reflection_flow', ';')
                new_data_df['points'] = process_list_column(new_data_df, 'points', ';')
                new_data_df['hashtags'] = process_list_column(new_data_df, 'hashtags', ',')
                # ★変更: material_photosも上記で定義したprocess_list_columnを使用する
                new_data_df['material_photos'] = process_list_column(new_data_df, 'material_photos', ';')

                # ICT活用有無の処理 (★ここを修正)
                if 'ict_use' in new_data_df.columns:
                    # ICT使用の値をそのまま文字列として保持し、NaNや空文字列は「なし」に
                    new_data_df['ict_use'] = new_data_df['ict_use'].astype(str).apply(lambda x: x.strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else 'なし')
                else:
                    new_data_df['ict_use'] = 'なし'

                # !!! 新規追加：subject, unit_name, group_type も同様に処理 !!! (★ここを追加)
                new_data_df['subject'] = process_string_column(new_data_df, 'subject', 'その他')
                new_data_df['unit_name'] = process_string_column(new_data_df, 'unit_name', '単元なし')
                new_data_df['group_type'] = process_string_column(new_data_df, 'group_type', '全体')

                existing_ids = {d['id'] for d in st.session_state.lesson_data}
                max_id = max(existing_ids) if existing_ids else 0

                new_entries = []
                for idx, row in new_data_df.iterrows():  # ループ変数にidxを追加
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
                        except ValueError:  # idが数値でない場合
                            max_id += 1
                            row_id = max_id

                    # lesson_dict の構築部分で新しいカラムを追加 (★ここを修正/追加)
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
                        'image': process_string_column(new_data_df.iloc[[idx]], 'image', '').iloc[0],  # idxを渡す
                        'material_photos': row.get('material_photos', []),
                        'video_link': process_string_column(new_data_df.iloc[[idx]], 'video_link', '').iloc[0],  # idxを渡す
                        'detail_word_url': process_string_column(new_data_df.iloc[[idx]], 'detail_word_url', '').iloc[0],  # idxを渡す
                        'detail_pdf_url': process_string_column(new_data_df.iloc[[idx]], 'detail_pdf_url', '').iloc[0],  # idxを渡す
                        'detail_ppt_url': process_string_column(new_data_df.iloc[[idx]], 'detail_ppt_url', '').iloc[0],  # idxを渡す
                        'detail_excel_url': process_string_column(new_data_df.iloc[[idx]], 'detail_excel_url', '').iloc[0],  # idxを渡す
                        'ict_use': row.get('ict_use', 'なし'),  # ここもデフォルト値取得ロジックを強化 (Falseから'なし'に変更)
                        'subject': row.get('subject', 'その他'),
                        'group_type': row.get('group_type', '全体'),
                        'unit_order': row.get('unit_order', 9999),  # ここもデフォルト値取得ロジックを強化
                        'unit_lesson_title': row.get('unit_lesson_title', row.get('unit_name', '単元内の授業'))  # デフォルトでtitleを使用 (★変更)
                    }
                    new_entries.append(lesson_dict)
                    existing_ids.add(row_id)  # 新しく生成されたIDも既存IDに加える

                st.session_state.lesson_data.extend(new_entries)
                st.success(f"{len(new_entries)}件の授業カードをファイルから追加しました！")
                st.experimental_rerun()
        except Exception as e:
            st.error(f"ファイルの読み込みまたは処理中にエラーが発生しました: {e}")
            st.exception(e)  # デバッグのために例外の詳細を表示


    st.markdown("---")


# --- Main Page Logic ---

if st.session_state.current_lesson_id is None:
    # --- Lesson Card List View ---

    st.markdown("<h1>🃏 授業カードライブラリー</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1em; color: #555;'>先生方の実践授業アイデアを検索し、日々の指導に役立てましょう！</p>", unsafe_allow_html=True)

    # カテゴリーで絞り込みのセクション
    st.markdown("---")  # 区切り線
    st.subheader("カテゴリーで絞り込み")

    # キーワード検索とハッシュタグ検索を同じ行に配置
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

    col_subject, col_filler = st.columns([0.5, 0.5])  # 2カラムに分割して表示し、右側は空白に

    with col_subject:
        all_subjects_raw = sorted(list(set(lesson['subject'] for lesson in st.session_state.lesson_data if 'subject' in lesson and lesson['subject'])))
        all_subjects = ["全て"] + all_subjects_raw

        # on_changeコールバック関数を定義
        def update_subject_selection():
            st.session_state.selected_subject = st.session_state.main_page_subject_filter_v4  # selectboxのkeyで直接値を取得
            # 単元フィルターを削除したため、リセット処理は不要

        # selected_subject が有効なオプションに含まれていない場合、"全て"にリセット
        if st.session_state.selected_subject not in all_subjects:
            st.session_state.selected_subject = "全て"

        try:
            default_subject_index = all_subjects.index(st.session_state.selected_subject)
        except ValueError:
            default_subject_index = 0  # 見つからない場合は「全て」に設定

        st.selectbox(
            "教科を選択",
            options=all_subjects,
            index=default_subject_index,
            key="main_page_subject_filter_v4",
            on_change=update_subject_selection,  # on_changeイベントハンドラを設定
            label_visibility="visible"
        )

    with col_filler:
        # 単元選択フィルターは削除されたため、ここには何も表示しないか、空のst.empty()を置く
        st.empty()


    st.markdown("---")  # 区切り線


    filtered_lessons = []
    # search_lower をループの前に初期化するか、
    # 検索クエリがない場合は、検索ロジックを完全にスキップするように変更します。
    # ここでは、よりシンプルにするために、検索クエリがある場合のみ処理するようにします。

    for lesson in st.session_state.lesson_data:
        match_search = True
        match_tags = True
        match_subject = True

        # Keyword search のロジックを修正
        if st.session_state.search_query:  # 検索クエリがある場合のみ検索を実行
            search_lower = st.session_state.search_query.lower()
            if not (
                (search_lower in str(lesson.get('unit_name', '')).lower()) or
                (search_lower in str(lesson.get('subject', '')).lower()) or
                (search_lower in str(lesson.get('catch_copy', '')).lower()) or
                (search_lower in str(lesson.get('goal', '')).lower()) or
                (search_lower in str(lesson.get('target_grade', '')).lower()) or
                (search_lower in str(lesson.get('disability_type', '')).lower()) or
                (search_lower in str(lesson.get('duration', '')).lower()) or  # duration も追加しました
                (search_lower in str(lesson.get('materials', '')).lower()) or
                any(search_lower in str(step).lower() for step in lesson.get('introduction_flow', [])) or
                any(search_lower in str(step).lower() for step in lesson.get('activity_flow', [])) or
                any(search_lower in str(step).lower() for step in lesson.get('reflection_flow', [])) or
                any(search_lower in str(point).lower() for point in lesson.get('points', [])) or
                any(search_lower in str(t).lower() for t in lesson.get('hashtags', [])) or
                (search_lower in str(lesson.get('unit_lesson_title', '')).lower())  # ★ここを追加
            ):
                match_search = False
        # else:
        #     st.session_state.search_query が空の場合、match_search はデフォルトの True のまま
        #     なので、ここでは何もする必要がありません。

        # Hashtag filter
        if st.session_state.selected_hashtags:
            if not all(tag in lesson['hashtags'] for tag in st.session_state.selected_hashtags):
                match_tags = False

        # Subject filter (★ここを追加)
        if st.session_state.selected_subject != "全て":
            if lesson.get('subject') != st.session_state.selected_subject:
                match_subject = False

        # 単元フィルターを削除
        # if st.session_state.selected_unit != "全て":
        #     if lesson.get('unit_name') != st.session_state.selected_unit:
        #         match_unit = False

        if match_search and match_tags and match_subject:  # ★ここを修正
            filtered_lessons.append(lesson)

    # --- ★ここからページネーション処理の追加★ --- (★ここから追加)
    CARDS_PER_PAGE = 10  # 1ページあたりの表示件数

    # 総ページ数を計算
    total_pages = (len(filtered_lessons) + CARDS_PER_PAGE - 1) // CARDS_PER_PAGE
    if total_pages == 0:  # カードが0枚の場合の特殊処理
        total_pages = 1

    # 現在のページが総ページ数を超えないように調整
    if st.session_state.current_page > total_pages:
        st.session_state.current_page = total_pages
    if st.session_state.current_page < 1:
        st.session_state.current_page = 1

    # 表示する授業カードの範囲を計算
    start_index = (st.session_state.current_page - 1) * CARDS_PER_PAGE
    end_index = start_index + CARDS_PER_PAGE
    displayed_lessons = filtered_lessons[start_index:end_index]

    # --- ▲ここまでページネーション処理の追加▲ ---

    st.markdown("<div class='lesson-card-grid'>", unsafe_allow_html=True)
    if displayed_lessons:  # filtered_lessons ではなく displayed_lessons をループする (★ここを修正)
        for lesson in displayed_lessons:  # ここを `displayed_lessons` に変更 (★ここを修正)
            # 教科と単元名が空文字列や'単元なし'の場合は表示しない
            display_subject = lesson['subject'] if lesson['subject'] and lesson['subject'] != 'その他' else ''
            display_unit = lesson['unit_name'] if lesson['unit_name'] and lesson['unit_name'] != '単元なし' else ''

            # 教科と単元名を組み合わせるHTMLを事前に作成
            subject_unit_display_html = ""
            if display_subject and display_unit:
                subject_unit_display_html = '<span class="card-subject-unit"><span class="icon">📖</span>{} / {}</span>'.format(display_subject, display_unit)
            elif display_subject:
                subject_unit_display_html = '<span class="card-subject-unit"><span class="icon">📖</span>{}</span>'.format(display_subject)
            elif display_unit:
                subject_unit_display_html = '<span class="card-subject-unit"><span class="icon">📖</span>{}</span>'.format(display_unit)

            # タグHTMLを事前に作成しておき、f文字列内の複雑なネストを避ける
            tags_html = "".join('<span class="tag-badge">#{}</span>'.format(tag) for tag in lesson.get('hashtags', []) if tag)

            # f-stringの内部にHTMLエスケープやバックフラッシュが含まれないように修正
            lesson_card_html = """
            <div class="lesson-card">
             <img class="lesson-card-image" src="{}" alt="{}">
             <div class="lesson-card-content">
                 <div>
                     {}
                     <div class="lesson-card-title">{}</div> 
                     <div class="lesson-card-catchcopy">{}</div>
                     <div class="lesson-card-goal">🎯 ねらい: {}</div>
                     <div class="lesson-card-meta">
                <span><span class="icon">🎓</span>{}</span>
                <span><span class="icon">🧩</span>{}</span>
                         <span><span class="icon">⏱</span>{}</span>
                     </div>
                 </div>
                 <div class="lesson-card-tags">
                     {}
                 </div>
                 {}
             </div>
            </div>
             """.format(
                lesson['image'] if lesson['image'] else 'https://via.placeholder.com/400x200?text=No+Image',
                lesson['unit_name'],
                subject_unit_display_html,
                lesson['unit_name'],
                lesson['catch_copy'],
                lesson['goal'],
                lesson['target_grade'],
                lesson['disability_type'],
                lesson['duration'],
                tags_html,
                st.button("👇この授業の詳細を見る", key="detail_btn_{}".format(lesson['id']), on_click=set_detail_page, args=(lesson['id'],))
            )
            st.markdown(lesson_card_html, unsafe_allow_html=True)
# ... (既存の授業カード表示コードここまで) ...

    else:
        st.info("条件に合う授業カードは見つかりませんでした。")
    st.markdown("</div>", unsafe_allow_html=True)  # lesson-card-grid の閉じタグ

    # --- ★ここからページネーションUIの追加（修正版）★ ---
    st.markdown("---")
    st.markdown("<div class='pagination-container'>", unsafe_allow_html=True)

    # 前ページボタン
    if st.session_state.current_page > 1:
        st.button("⏪ 前ページ", key="prev_page_bottom", on_click=set_page, args=(st.session_state.current_page - 1,))
    
    # ページ番号ボタン
    # 常に表示するページ数の範囲を調整（例: 現在のページを中心に前後2ページずつ、最大5ページ）
    max_pages_to_show = 5
    page_range_start = max(1, st.session_state.current_page - (max_pages_to_show // 2))
    page_range_end = min(total_pages, page_range_start + max_pages_to_show - 1)
    
    # page_range_end が max_pages_to_show より少ない場合、page_range_start を再調整
    if (page_range_end - page_range_start + 1) < max_pages_to_show and total_pages > max_pages_to_show:
        page_range_start = max(1, page_range_end - max_pages_to_show + 1)

    # 最初のページへのジャンプボタン（1ページ目が表示範囲外の場合）
    if page_range_start > 1:
        st.button("1", key="page_1", on_click=set_page, args=(1,), type="secondary" if st.session_state.current_page != 1 else "primary")
        if page_range_start > 2:
            st.markdown("<span>...</span>", unsafe_allow_html=True) # 省略記号

    for i in range(page_range_start, page_range_end + 1):
        # 現在のページをハイライト
        is_current = (i == st.session_state.current_page)
        st.button(str(i), key=f"page_{i}", on_click=set_page, args=(i,), type="primary" if is_current else "secondary")

    # 最後のページへのジャンプボタン（最後のページが表示範囲外の場合）
    if page_range_end < total_pages:
        if page_range_end < total_pages - 1:
            st.markdown("<span>...</span>", unsafe_allow_html=True) # 省略記号
        st.button(str(total_pages), key=f"page_{total_pages}", on_click=set_page, args=(total_pages,), type="secondary" if st.session_state.current_page != total_pages else "primary")

    # 次ページボタン
    if st.session_state.current_page < total_pages:
        st.button("次ページ ⏩", key="next_page_bottom", on_click=set_page, args=(st.session_state.current_page + 1,))

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    # --- ▲ここまでページネーションUIの追加（修正版）▲ ---


else:  # 詳細ページ
    # st.info("条件に合う授業カードは見つかりませんでした。") # この行は詳細ページ表示時には不要なので削除またはコメントアウト
    # --- Lesson Card Detail View ---

    selected_lesson = next((lesson for lesson in st.session_state.lesson_data if lesson['id'] == st.session_state.current_lesson_id), None)

    if selected_lesson:
        st.button("↩️ 一覧に戻る", on_click=back_to_list, key="back_to_list_btn_top")

        # HTMLをf-stringの外で組み立てる
        header_html = "<h1 class='detail-header'>{}</h1>".format(selected_lesson['unit_name'])
        st.markdown(header_html, unsafe_allow_html=True)
        if selected_lesson['catch_copy']:
            catchcopy_html = "<h3 class='detail-header'>{}</h3>".format(selected_lesson['catch_copy'])
            st.markdown(catchcopy_html, unsafe_allow_html=True)
        else:
            st.markdown("<br>", unsafe_allow_html=True)

        st.image(selected_lesson['image'] if selected_lesson['image'] else 'https://via.placeholder.com/800x400?text=No+Image', caption=selected_lesson['unit_name'], use_container_width=True)  # 画像キャプションも単元名に

        detail_css = r"""
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
                .unit-lesson-list {
                    list-style-type: decimal;
                    padding-left: 20px;
                }
                .unit-lesson-list li {
                    margin-bottom: 8px;
                    font-size: 1.05em;
                }
                /* Streamlitボタンをリストアイテム内で自然に見せるための調整 */
                .unit-lesson-list li .stButton > button {
                    background-color: #f0f2f6 !important; /* 背景色を控えめに */
                    color: #333 !important; /* テキスト色を標準に */
                    border: 1px solid #e0e0e0 !important; /* 軽いボーダー */
                    border-radius: 8px !important;
                    padding: 5px 10px !important;
                    font-size: 1em !important;
                    width: auto !important; /* 幅をコンテンツに合わせる */
                    box-shadow: none !important; /* 影をなくす */
                    transition: all 0.2s ease !important;
                }
                .unit-lesson-list li .stButton > button:hover {
                    background-color: #e6e6fa !important; /* ホバーで少し紫色に */
                    color: #8A2BE2 !important; /* ホバーで紫のテキスト */
                    border-color: #ccacee !important;
                    transform: translateY(-1px) !important;
                }
            </style>
        """
        st.markdown(detail_css, unsafe_allow_html=True)

        # 授業の流れセクション
        st.subheader("授業の流れ")
        # ボタンとコンテンツの間に明確な区切りを入れる
        st.button('{} 🔃'.format('授業の流れを非表示' if st.session_state.show_all_flow else '授業の流れを表示'), on_click=toggle_all_flow_display, key="toggle_all_flow_{}".format(selected_lesson['id']))

        # ここにコンテンツを表示するDivを追加し、CSSで上部の余白を調整
        st.markdown("<div class='flow-content-wrapper'>", unsafe_allow_html=True)

        if st.session_state.show_all_flow:
            if selected_lesson['introduction_flow']:
                intro_html = "<div class='flow-section'><h4><span class='icon'>🚀</span>導入</h4><ol class='flow-list'>"
                for step in selected_lesson['introduction_flow']:
                    intro_html += "<li>{}</li>".format(step)
                intro_html += "</ol></div>"
                st.markdown(intro_html, unsafe_allow_html=True)

            if selected_lesson['activity_flow']:
                activity_html = "<div class='flow-section'><h4><span class='icon'>💡</span>活動</h4><ol class='flow-list'>"
                for step in selected_lesson['activity_flow']:
                    activity_html += "<li>{}</li>".format(step)
                activity_html += "</ol></div>"
                st.markdown(activity_html, unsafe_allow_html=True)

            if selected_lesson['reflection_flow']:
                reflection_html = "<div class='flow-section'><h4><span class='icon'>💭</span>振り返り</h4><ol class='flow-list'>"
                for step in selected_lesson['reflection_flow']:
                    reflection_html += "<li>{}</li>".format(step)
                reflection_html += "</ol></div>"
                st.markdown(reflection_html, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)  # flow-content-wrapper の閉じタグ

        st.markdown("---")

        # ねらい

        st.markdown("<h3><span class='header-icon'>🎯</span>ねらい</h3>", unsafe_allow_html=True)
        st.markdown("<p>{}</p>".format(selected_lesson['goal']), unsafe_allow_html=True)
        st.markdown("---")
        # 対象・種別・時間・教科・単元・学習集団の単位 (表示カラム追加)

        st.markdown("<h3><span class='header-icon'>ℹ️</span>基本情報</h3>", unsafe_allow_html=True)
        # 6カラムに変更
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.markdown("**対象学年:** {}".format(selected_lesson['target_grade']))
        with col2:
            st.markdown("**障害種別:** {}".format(selected_lesson['disability_type']))
        with col3:
            st.markdown("**時間:** {}".format(selected_lesson['duration']))
        with col4:
            st.markdown("**ICT活用:** {}".format(selected_lesson.get('ict_use', 'なし')))
        with col5:
            st.markdown("**教科:** {}".format(selected_lesson.get('subject', 'その他')))
        with col6:  # 新規追加
            st.markdown("**学習集団:** {}".format(selected_lesson.get('group_type', '全体')))

        # 単元名は別途表示（関連カードセクションと連動させるため）
        unit_name_html = "<p style='font-size:1.1em; font-weight:bold; margin-top:10px;'>単元名: <span style='color:#8A2BE2;'>{}</span></p>".format(selected_lesson.get('unit_name', '単元なし'))
        st.markdown(unit_name_html, unsafe_allow_html=True)


        # --- 単元の授業の流れ (新規追加または既存セクションを拡張) ---
        if selected_lesson.get('unit_name') and selected_lesson.get('unit_name') != '単元なし':
            unit_name_to_search = selected_lesson['unit_name']
            target_grade_to_match = selected_lesson['target_grade'] # 学年も一致させる

            all_lessons_in_unit = [
                lesson for lesson in st.session_state.lesson_data
                if lesson.get('unit_name') == unit_name_to_search and
                   lesson.get('target_grade') == target_grade_to_match # 学年も一致
            ]

            # 単元内での順番 (unit_order) でソート
            sorted_lessons_in_unit = sorted(all_lessons_in_unit, key=lambda x: x.get('unit_order', 9999))

            if sorted_lessons_in_unit:
                unit_flow_header_html = "<h3><span class='header-icon'>📚</span>「{} ({}学年)」の授業の流れ</h3>".format(unit_name_to_search, target_grade_to_match)
                st.markdown(unit_flow_header_html, unsafe_allow_html=True)
                st.markdown("<ol class='unit-lesson-list'>", unsafe_allow_html=True)  # 番号付きリストにクラスを追加

                for lesson_in_unit in sorted_lessons_in_unit:
                    # unit_lesson_title が存在すればそれを使用、なければ unit_name を使用
                    display_title = lesson_in_unit.get('unit_lesson_title') if lesson_in_unit.get('unit_lesson_title') else lesson_in_unit['unit_name']
                    is_current_lesson = (lesson_in_unit['id'] == selected_lesson['id'])

                    if is_current_lesson:
                        list_item_html = "<li style='font-weight: bold; color: #8A2BE2;'>{} 【現在の授業】</li>".format(display_title)
                        st.markdown(list_item_html, unsafe_allow_html=True)
                    else:
                        # Streamlitのボタンを直接使って、遷移をトリガーする
                        # CSSでスタイルを適用するため、liタグで囲む
                        st.markdown(f"<li>", unsafe_allow_html=True)
                        st.button(display_title, key=f"unit_flow_link_direct_{lesson_in_unit['id']}", on_click=set_detail_page, args=(lesson_in_unit['id'],), help=f"「{display_title}」の詳細を見る", type="secondary")
                        st.markdown(f"</li>", unsafe_allow_html=True)
                        

                st.markdown("</ol>", unsafe_allow_html=True)

        st.markdown("---")  # 区切り線
        # 既存の「準備物」以下のセクションはそのまま残す

        # 準備物
        if selected_lesson['materials']:

            st.markdown("<h3><span class='header-icon'>✂️</span>準備物</h3>", unsafe_allow_html=True)
            st.markdown("<p>{}</p>".format(selected_lesson['materials']), unsafe_allow_html=True)

        # 指導のポイント
        if selected_lesson['points']:

            st.markdown("<h3><span classt='header-icon'>💡</span>指導のポイント</h3>", unsafe_allow_html=True)
            st.markdown("<ul>", unsafe_allow_html=True)
            for point in selected_lesson['points']:
                st.markdown("<li>{}</li>".format(point), unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)

        # ハッシュタグ
        if selected_lesson['hashtags']:

            st.markdown("<h3><span class='header-icon'>#️⃣</span>ハッシュタグ</h3>", unsafe_allow_html=True)
            tags_html_detail = "".join('<span class="tag-badge" style="margin-right: 5px;">#{}</span>'.format(tag) for tag in selected_lesson.get('hashtags', []) if tag)
            st.markdown(
                "<p>{}</p>".format(tags_html_detail),
                unsafe_allow_html=True
            )

        # 教材写真
        if selected_lesson['material_photos']:  # リストが空でない場合のみ表示

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
                        st.warning("一部の教材写真URLが無効なため表示できませんでした。")  # 必要に応じてメッセージ

        # 動画リンク (★ここを修正/追加)
        if selected_lesson['video_link'].strip():  # video_linkが空文字列でないことを確認 (strip()で空白も考慮)

            st.markdown("<h3><span class='header-icon'>▶️</span>参考動画</h3>", unsafe_allow_html=True)
            try:
                st.video(selected_lesson['video_link'])
            except Exception as e:
                st.warning("動画の読み込み中に問題が発生しました。リンクを確認してください。エラー: {}".format(e))
        else:
            # 動画リンクが空の場合にメッセージを表示
            st.markdown("<h3><span class='header-icon'>▶️</span>参考動画</h3>", unsafe_allow_html=True)
            st.info("参考動画は登録されていません。")


        # 詳細資料ダウンロード (★ここを修正/追加)
        # 既存のif文の条件を変更
        if selected_lesson['detail_word_url'] or selected_lesson['detail_pdf_url'] or selected_lesson['detail_ppt_url'] or selected_lesson['detail_excel_url']:  # ★変更
            st.markdown("<h3><span class='header-icon'>📄</span>詳細資料ダウンロード</h3>", unsafe_allow_html=True)
            if selected_lesson['detail_word_url']:
                word_button_html = '<a href="{}" target="_blank" style="text-decoration: none;"><button style="background-color: #264A9D; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; margin-right: 10px;">📖 指導案 (Word)</button></a>'.format(selected_lesson["detail_word_url"])
                st.markdown(word_button_html, unsafe_allow_html=True)
            if selected_lesson['detail_pdf_url']:
                pdf_button_html = '<a href="{}" target="_blank" style="text-decoration: none;"><button style="background-color: #B40000; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; margin-right: 10px;">📚 指導案 (PDF)</button></a>'.format(selected_lesson["detail_pdf_url"])
                st.markdown(pdf_button_html, unsafe_allow_html=True)
            if selected_lesson['detail_ppt_url']:  # ★追加
                ppt_button_html = '<a href="{}" target="_blank" style="text-decoration: none;"><button style="background-color: #D24726; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; margin-right: 10px;">📊 授業資料 (PowerPoint)</button></a>'.format(selected_lesson["detail_ppt_url"])
                st.markdown(ppt_button_html, unsafe_allow_html=True)
            if selected_lesson['detail_excel_url']:  # ★追加
                excel_button_html = '<a href="{}" target="_blank" style="text-decoration: none;"><button style="background-color: #0E6839; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; margin-right: 10px;">📈 評価シート (Excel)</button></a>'.format(selected_lesson["detail_excel_url"])
                st.markdown(excel_button_html, unsafe_allow_html=True)

        st.markdown("---")
        st.button("↩️ 一覧に戻る", on_click=back_to_list, key="back_to_list_btn_bottom")

    else:
        st.error("指定された授業カードが見つかりませんでした。")
        st.button("↩️ 一覧に戻る", on_click=back_to_list)

# --- Custom CSS for Styling ---
global_css = r"""
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
    /* 詳細ページ内の「同じ単元の授業」の個々の授業タイトルボタンのスタイル */
    .unit-lesson-list li .stButton > button {
        background: #f0f0f0 !important; /* 目立たない背景色 */
        color: #333 !important;
        border: 1px solid #ccc !important;
        border-radius: 15px !important;
        padding: 8px 15px !important;
        font-size: 0.95em !important;
        font-weight: normal !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
        transition: all 0.2s ease !important;
        width: auto !important; /* 幅を自動調整 */
        margin-right: 10px; /* ボタン間の余白 */
        margin-bottom: 10px; /* 下方向の余白 */
        display: inline-block; /* リストアイテム内で横並びにするため */
    }
    .unit-lesson-list li .stButton > button:hover {
        background-color: #e0e0e0 !important;
        border-color: #999 !important;
        color: #000 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 3px 8px rgba(0,0,0,0.1) !important;
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
</style>
"""
st.markdown(global_css, unsafe_allow_html=True)