import streamlit as st
import pandas as pd
import base64
import re
import io
from io import BytesIO
import xlsxwriter

# ページ設定
st.set_page_config(
    page_title="授業カードライブラリー",
    page_icon="🃏",
    layout="wide",  # レイアウトをwideに設定
    initial_sidebar_state="expanded"
)

# カスタムCSSを読み込む関数
def load_css():
    st.markdown(r"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Poppins:wght@400;600&display=swap');
        
        body {
            font-family: 'Noto Sans JP', sans-serif;
            background-color: #f0f2f6;
            color: #333;
        }

        /* アプリ全体のコンテナの最大幅を広げ、中央寄せを維持 */
        [data-testid="stAppViewContainer"] {
            max-width: 1200px; /* ここを調整してより広く */
            margin: auto; /* 中央寄せ */
            padding-left: 20px;
            padding-right: 20px;
        }

        /* メインコンテンツの背景色とパディング */
        [data-testid="stAppViewContainer"] > .main {
            background-color: #f0f2f6;
            padding-top: 30px;
            padding-bottom: 30px;
            padding-left: 20px;
            padding-right: 20px;
        }

        /* サイドバーのスタイル */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e0e0e0;
            box-shadow: 2px 0 10px rgba(0,0,0,0.05);
            padding-top: 20px;
        }
        [data-testid="stSidebar > div:first-child"] {
            padding-left: 20px;
            padding-right: 20px;
        }

               
        /* 見出しのスタイル */
        h1, h2, h3, h4, h5, h6 { 
            font-family: 'Poppins', 'Noto Sans JP', sans-serif;
            color: #2c3e50; 
            font-weight: 700;
        }
        h1 {
            text-align: center; 
            padding-bottom: 25px;
            font-size: 2.8em;
            color: #4A90E2;
            letter-spacing: -0.5px;
        }
        h2 {
            text-align: left;
            border-left: 6px solid #8A2BE2;
            padding-left: 15px;
            margin-top: 45px;
            font-size: 1.9em;
            color: #34495e;
        }
        h3 {
            text-align: left;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 8px;
            margin-top: 35px;
            font-size: 1.5em;
            color: #34495e;
            display: flex;
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

        /* 戻るボタンのスタイル */
        .back-button-container {
            padding-bottom: 20px;
            margin-bottom: -50px;
        }

        /* Streamlitウィジェットのスタイル */
        .stTextInput>div>div>input, .stMultiSelect>div>div>div, .stSelectbox>div>div {
            border-radius: 12px;
            padding: 10px 15px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            transition: all 0.2s ease-in-out;
            background-color: #ffffff;
        }
        .stTextInput>div>div>input:focus, .stMultiSelect>div>div>div:focus-within, .stSelectbox>div>div:focus-within {
            border-color: #4A90E2;
            box-shadow: 0 0 0 0.2rem rgba(74,144,226,0.15);
        }
        .stMultiSelect div[data-testid="stMultiSelectOptions"] {
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }
        
        /* 授業カードグリッドのスタイル */
        .lesson-card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); /* デフォルトは330px以上で自動調整 */
            gap: 30px;
            padding: 25px 0;
        }

        /* PC (広い画面) では3列 */
        @media (min-width: 500px) {
            .lesson-card-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        /* タブレット (中間の画面) では2列 */
        @media (min-width: 708px) and (max-width: 599px) {
            .lesson-card-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        /* スマートフォン (狭い画面) では1列 */
        @media (max-width: 567px) {
            .lesson-card-grid {
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            }
        }

        /* 個々の授業カードのスタイル */
        .lesson-card {
            background-color: #ffffff;
            border: none;
            border-radius: 18px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        }
        .lesson-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 18px 35px rgba(74, 144, 226, 0.18);
        }
        .lesson-card-image {
            width: 100%;
            height: 200px;
            object-fit: cover; 
            border-bottom: 1px solid #f0f0f0;
        }
        .lesson-card-content {
            padding: 22px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .lesson-card-title {
            font-size: 1.4em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 8px;
            line-height: 1.4;
        }
        .lesson-card-catchcopy {
            font-size: 0.95em;
            color: #6a0dad;
            font-weight: 500;
            margin-bottom: 15px;
            line-height: 1.4;
            font-style: italic;
            min-height: 3em; /* 高さのばらつきを抑える */
            display: -webkit-box;
            -webkit-line-clamp: 2; /* 2行で省略 */
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .lesson-card-goal {
            font-size: 0.9em;
            color: #555;
            margin-bottom: 12px;
            border-left: 4px solid #4a90e2;
            padding-left: 10px;
            line-height: 1.5;
            min-height: 60px; /* 高さのばらつきを抑える */
            display: -webkit-box;
            -webkit-line-clamp: 3; /* 3行で省略 */
            -webkit-box-orient: vertical;
            overflow: hidden;
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
            background-color: #f0f8ff;
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
            background-color: #e3f2fd;
            color: #2196f3;
            border-radius: 15px;
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

        /* アイコンのスタイル */
        .icon {
            margin-right: 8px;
            font-size: 1.2em;
            color: #8A2BE2;
        }

        /* ボタンのスタイル */
        .stButton>button {
            border: 2px solid #4a90e2;
            border-radius: 25px;
            color: #4a90e2;
            background-color: #ffffff;
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.3s ease;
            margin-top: 20px;
            width: 100%;
            box-shadow: 0 4px 10px rgba(74, 144, 226, 0.1);
        }
        .stButton>button:hover {
            border-color: #8A2BE2;
            color: white;
            background-color: #8A2BE2;
            transform: translateY(-3px); 
            box-shadow: 0 8px 15px rgba(138,43,226,0.2);
        }
        
        /* 詳細ページ用スタイル */
        .detail-header {
            text-align: left;
            margin-bottom: 25px;
        }
        [data-testid="stImage"] > img {
            width: 100% !important;
            height: 400px !important;
            object-fit: cover !important;
            border-radius: 15px !important;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1) !important;
            margin-bottom: 30px !important;
            display: block !important;
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
            list-style-position: inside;
        }
        .detail-section li {
            margin-bottom: 8px;
            padding-left: 5px;
        }
        .detail-image-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 25px;
            margin-bottom: 35px;
        }
        
        .detail-image-gallery img {
            max-width: 100%;
            height: 220px;
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
            background-color: #e6f7ff;
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

        /* ダウンロードボタンのスタイル */
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
            color: white;
        }

        .card-subject-unit {
            font-size: 0.9em;
            color: #4A90E2;
            font-weight: 600;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            background-color: #e6f7ff;
            padding: 5px 10px;
            border-radius: 8px;
            width: fit-content;
            border: 1px solid #cceeff;
        }
        .card-subject-unit .icon {
            margin-right: 6px;
            font-size: 1.1em;
            color: #4A90E2;
        }
        .flow-content-wrapper {
            margin-top: 20px;
        }
         
        /* 詳細ページの「この授業の詳細を見る」ボタンのスタイル */
        .lesson-card .stButton > button {
            border: 2px solid #4a90e2 !important;
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
            border-color: #357ABD !important;
            color: white !important;
            background-color: #357ABD !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 15px rgba(74,144,226,0.2) !important;
        }

        /* ページネーションボタンのスタイル調整 (横並び、中央寄せ) */
        .pagination-container {
            display: flex; /* Flexboxを有効にする */
            justify-content: center; /* 中央寄せ */
            align-items: center;
            gap: 8px; /* ボタン間のスペースを調整 */
            margin-top: 25px;
            margin-bottom: 25px;
            flex-wrap: wrap; /* ボタンが多すぎる場合に折り返す */
        }
        .pagination-container .stButton > button {
            min-width: 42px;
            height: 42px;
            padding: 0 12px;
            font-size: 1.0em;
            border-radius: 21px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
            background-color: #ffffff !important;
            color: #555 !important;
            border: 1px solid #ddd !important;
            margin: 0 !important;
            display: inline-flex !important;
            justify-content: center;
            align-items: center;
        }
        .pagination-container .stButton > button:hover {
            background-color: #eef !important;
            border-color: #cce !important;
            transform: translateY(-1px) !important;
        }
        /* アクティブなページ番号ボタンのスタイル */
        .pagination-container .stButton > button[data-testid*="stPageLinkButton-primary"],
        .pagination-container .stButton > button[type="primary"] {
            background-color: #8A2BE2 !important;
            border-color: #8A2BE2 !important;
            color: white !important;
            font-weight: bold !important;
            box-shadow: 0 4px 10px rgba(138,43,226,0.2) !important;
        }
        /* 前後ページボタンのスタイル */
        .pagination-container .stButton > button[key*="prev_page"],
        .pagination-container .stButton > button[key*="next_page"] {
            background-color: #f0f2f6 !important;
            color: #4A90E2 !important;
            border: 1px solid #cceeff !important;
            font-weight: bold !important;
        }
        .pagination-container .stButton > button[key*="prev_page"]:hover,
        .pagination-container .stButton > button[key*="next_page"]:hover {
            background-color: #e3f2fd !important;
            border-color: #99ccff !important;
        }

        /* 省略記号 (st.markdown("<span>...</span>") ) のコンテナをターゲット */
        .pagination-container .stMarkdown > div { 
            display: flex;
            align-items: center;
            height: 42px;
            font-size: 1.2em;
            color: #777;
            padding: 0 5px;
        }

        /* 詳細ページ内の「単元の授業の流れ」のボタンのスタイル */
        .unit-lesson-list li .stButton > button {
            background-color: #f0f2f6 !important;
            color: #333 !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 8px !important;
            padding: 5px 10px !important;
            font-size: 1em !important;
            width: auto !important;
            box-shadow: none !important;
            transition: all 0.2s ease !important;
        }
        .unit-lesson-list li .stButton > button:hover {
            background-color: #e6e6fa !important;
            color: #8A2BE2 !important;
            border-color: #ccacee !important;
            transform: translateY(-1px) !important;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Googleフォームへの外部リンク
google_form_css = r"""
    <style>
        .google-form-link-container {
            text-align: center;
            margin-top: 20px;
            margin-bottom: 40px;
        }
        .google-form-link-button {
            display: inline-flex;
            align-items: center;
            padding: 15px 30px;
            background-color: #4285F4;
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

# 戻るボタン (TOPページへのリンク)
col_back, _ = st.columns([0.15, 0.85])
with col_back:
    st.page_link("tokusi_app.py", label="« TOPページに戻る", icon="🏠")

# lesson_cards.csv の読み込み
try:
    lesson_data_df = pd.read_csv(
        "lesson_cards.csv",
        converters={
            'introduction_flow': lambda x: [item.strip() for item in x.split(';') if item.strip()] if pd.notna(x) else [],
            'activity_flow': lambda x: [item.strip() for item in x.split(';') if item.strip()] if pd.notna(x) else [],
            'reflection_flow': lambda x: [item.strip() for item in x.split(';') if item.strip()] if pd.notna(x) else [],
            'points': lambda x: [item.strip() for item in x.split(';') if item.strip()] if pd.notna(x) else [],
            'hashtags': lambda x: [item.strip() for item in x.split(',') if item.strip()] if pd.notna(x) else [],
            'material_photos': lambda x: [url.strip() for url in x.split(';') if url.strip()] if pd.notna(x) else [],
            'unit_name': lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != '' and str(x).lower() != 'nan' else '単元なし',
            'unit_order': lambda x: int(x) if pd.notna(x) and str(x).isdigit() else 9999,
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
        }
    )

    # 必須カラムの確認とデフォルト値設定
    # unit_lesson_titleのデフォルト値をunit_nameで補完
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
        # 重複するIDがあれば新しいIDを割り振る
        lesson_data_df['id'] = lesson_data_df['id'].apply(lambda x: x if pd.notna(x) and isinstance(x, (int, float)) else 0) # 非数値やNaNを0に
        lesson_data_df['id'] = lesson_data_df['id'].astype(int) # int型に変換
        # idが重複している行を特定
        duplicated_ids = lesson_data_df[lesson_data_df.duplicated('id', keep='first')]['id'].unique()
        
        if len(duplicated_ids) > 0:
            st.warning(f"以下のIDが重複しています: {', '.join(map(str, duplicated_ids))}")
            # 重複するIDを持つ行に新しいユニークなIDを割り振る
            next_id = lesson_data_df['id'].max() + 1
            for dup_id in duplicated_ids:
                # 重複IDのうち、最初に見つかったものを除く全ての行に新しいIDを割り振る
                mask = (lesson_data_df['id'] == dup_id) & (~lesson_data_df.index.isin(lesson_data_df[lesson_data_df['id'] == dup_id].index[:1]))
                lesson_data_df.loc[mask, 'id'] = range(next_id, next_id + mask.sum())
                next_id += mask.sum()
            st.success("重複IDを修正しました。")
    

    lesson_data_raw = lesson_data_df.to_dict(orient='records')
    st.session_state.lesson_data = lesson_data_raw

except FileNotFoundError:
    st.error("lesson_cards.csv ファイルが見つかりませんでした。pages フォルダと同じ階層に配置してください。")
    st.stop()
except Exception as e:
    st.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
    st.exception(e)
    st.stop()

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
        worksheet.write_comment('U1', 'ICT活用有無 (TRUEまたはFALSE)')
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

# サイドバー
with st.sidebar:
    st.header("📚 データ登録・管理")
    st.markdown("---")

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
                st.success(f"{len(new_entries)}件の授業カードをファイルから追加しました！")
                st.experimental_rerun()
        except Exception as e:
            st.error(f"ファイルの読み込みまたは処理中にエラーが発生しました: {e}")
            st.exception(e)

    st.markdown("---")

# メインページ
if st.session_state.current_lesson_id is None:
    st.markdown("<h1>🃏 授業カードライブラリー</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1em; color: #555;'>先生方の実践授業アイデアを検索し、日々の指導に役立てましょう！</p>", unsafe_allow_html=True)

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

    with col_filler:
        st.empty()

    st.markdown("---")

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

    # ページネーション処理
    CARDS_PER_PAGE = 10
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

    st.markdown("<div class='lesson-card-grid'>", unsafe_allow_html=True)
    if displayed_lessons:
        for lesson in displayed_lessons:
            display_subject = lesson['subject'] if lesson['subject'] and lesson['subject'] != 'その他' else ''
            display_unit = lesson['unit_name'] if lesson['unit_name'] and lesson['unit_name'] != '単元なし' else ''

            subject_unit_display_html = ""
            if display_subject and display_unit:
                subject_unit_display_html = '<span class="card-subject-unit"><span class="icon">📖</span>{} / {}</span>'.format(display_subject, display_unit)
            elif display_subject:
                subject_unit_display_html = '<span class="card-subject-unit"><span class="icon">📖</span>{}</span>'.format(display_subject)
            elif display_unit:
                subject_unit_display_html = '<span class="card-subject-unit"><span class="icon">📖</span>{}</span>'.format(display_unit)

            tags_html = "".join('<span class="tag-badge">#{}</span>'.format(tag) for tag in lesson.get('hashtags', []) if tag)
            
            # Catch copyとGoalが複数行になる可能性があるので、最小の高さを設定
            catch_copy_style = "min-height: 2.5em; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;"
            goal_style = "min-height: 3em; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;"

            lesson_card_html = f"""
            <div class="lesson-card">
             <img class="lesson-card-image" src="{lesson['image'] if lesson['image'] else 'https://via.placeholder.com/400x200?text=No+Image'}" alt="{lesson['unit_name']}">
             <div class="lesson-card-content">
                 <div>
                     {subject_unit_display_html}
                     <div class="lesson-card-title">{lesson['unit_name']}</div> 
                     <div class="lesson-card-catchcopy" style="{catch_copy_style}">{lesson['catch_copy']}</div>
                     <div class="lesson-card-goal" style="{goal_style}">🎯 ねらい: {lesson['goal']}</div>
                     <div class="lesson-card-meta">
                <span><span class="icon">🎓</span>{lesson['target_grade']}</span>
                <span><span class="icon">🧩</span>{lesson['disability_type']}</span>
                         <span><span class="icon">⏱</span>{lesson['duration']}</span>
                     </div>
                 </div>
                 <div class="lesson-card-tags">
                     {tags_html}
                 </div>
                 {st.button("👇この授業の詳細を見る", key=f"detail_btn_{lesson['id']}", on_click=set_detail_page, args=(lesson['id'],))}
             </div>
            </div>
             """
            st.markdown(lesson_card_html, unsafe_allow_html=True)

    else:
        st.info("条件に合う授業カードは見つかりませんでした。")
    st.markdown("</div>", unsafe_allow_html=True)

    # ページネーションUI
    st.markdown("---")
    st.markdown("<div class='pagination-container'>", unsafe_allow_html=True)

    if st.session_state.current_page > 1:
        st.button("⏪ 前ページ", key="prev_page_bottom", on_click=set_page, args=(st.session_state.current_page - 1,))
    
    max_pages_to_show = 5
    page_range_start = max(1, st.session_state.current_page - (max_pages_to_show // 2))
    page_range_end = min(total_pages, page_range_start + max_pages_to_show - 1)
    
    if (page_range_end - page_range_start + 1) < max_pages_to_show and total_pages > max_pages_to_show:
        page_range_start = max(1, page_range_end - max_pages_to_show + 1)

    if page_range_start > 1:
        st.button("1", key="page_1", on_click=set_page, args=(1,), type="secondary" if st.session_state.current_page != 1 else "primary")
        if page_range_start > 2:
            st.markdown("<span>...</span>", unsafe_allow_html=True)

    for i in range(page_range_start, page_range_end + 1):
        is_current = (i == st.session_state.current_page)
        st.button(str(i), key=f"page_{i}", on_click=set_page, args=(i,), type="primary" if is_current else "secondary")

    if page_range_end < total_pages:
        if page_range_end < total_pages - 1:
            st.markdown("<span>...</span>", unsafe_allow_html=True)
        st.button(str(total_pages), key=f"page_{total_pages}", on_click=set_page, args=(total_pages,), type="secondary" if st.session_state.current_page != total_pages else "primary")

    if st.session_state.current_page < total_pages:
        st.button("次ページ ⏩", key="next_page_bottom", on_click=set_page, args=(st.session_state.current_page + 1,))

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")

else:  # 詳細ページ
    selected_lesson = next((lesson for lesson in st.session_state.lesson_data if lesson['id'] == st.session_state.current_lesson_id), None)

    if selected_lesson:
        st.button("↩️ 一覧に戻る", on_click=back_to_list, key="back_to_list_btn_top")

        header_html = f"<h1 class='detail-header'>{selected_lesson['unit_name']}</h1>"
        st.markdown(header_html, unsafe_allow_html=True)
        if selected_lesson['catch_copy']:
            catchcopy_html = f"<h3 class='detail-header'>{selected_lesson['catch_copy']}</h3>"
            st.markdown(catchcopy_html, unsafe_allow_html=True)
        else:
            st.markdown("<br>", unsafe_allow_html=True)

        st.image(selected_lesson['image'] if selected_lesson['image'] else 'https://via.placeholder.com/800x400?text=No+Image', caption=selected_lesson['unit_name'], use_container_width=True)

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
                .unit-lesson-list {
                    list-style-type: decimal;
                    padding-left: 20px;
                }
                .unit-lesson-list li {
                    margin-bottom: 8px;
                    font-size: 1.05em;
                }
            </style>
        """
        st.markdown(detail_css, unsafe_allow_html=True)

        st.subheader("授業の流れ")
        st.button('{} 🔃'.format('授業の流れを非表示' if st.session_state.show_all_flow else '授業の流れを表示'), on_click=toggle_all_flow_display, key=f"toggle_all_flow_{selected_lesson['id']}")

        st.markdown("<div class='flow-content-wrapper'>", unsafe_allow_html=True)

        if st.session_state.show_all_flow:
            if selected_lesson['introduction_flow']:
                intro_html = "<div class='flow-section'><h4><span class='icon'>🚀</span>導入</h4><ol class='flow-list'>"
                for step in selected_lesson['introduction_flow']:
                    intro_html += f"<li>{step}</li>"
                intro_html += "</ol></div>"
                st.markdown(intro_html, unsafe_allow_html=True)

            if selected_lesson['activity_flow']:
                activity_html = "<div class='flow-section'><h4><span class='icon'>💡</span>活動</h4><ol class='flow-list'>"
                for step in selected_lesson['activity_flow']:
                    activity_html += f"<li>{step}</li>"
                activity_html += "</ol></div>"
                st.markdown(activity_html, unsafe_allow_html=True)

            if selected_lesson['reflection_flow']:
                reflection_html = "<div class='flow-section'><h4><span class='icon'>💭</span>振り返り</h4><ol class='flow-list'>"
                for step in selected_lesson['reflection_flow']:
                    reflection_html += f"<li>{step}</li>"
                reflection_html += "</ol></div>"
                st.markdown(reflection_html, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("<h3><span class='header-icon'>🎯</span>ねらい</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{selected_lesson['goal']}</p>", unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("<h3><span class='header-icon'>ℹ️</span>基本情報</h3>", unsafe_allow_html=True)
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
        with col6:
            st.markdown(f"**学習集団:** {selected_lesson.get('group_type', '全体')}")

        unit_name_html = f"<p style='font-size:1.1em; font-weight:bold; margin-top:10px;'>単元名: <span style='color:#8A2BE2;'>{selected_lesson.get('unit_name', '単元なし')}</span></p>"
        st.markdown(unit_name_html, unsafe_allow_html=True)

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
                unit_flow_header_html = f"<h3><span class='header-icon'>📚</span>「{unit_name_to_search} ({target_grade_to_match}学年)」の授業の流れ</h3>"
                st.markdown(unit_flow_header_html, unsafe_allow_html=True)
                st.markdown("<ol class='unit-lesson-list'>", unsafe_allow_html=True)

                for lesson_in_unit in sorted_lessons_in_unit:
                    display_title = lesson_in_unit.get('unit_lesson_title') if lesson_in_unit.get('unit_lesson_title') else lesson_in_unit['unit_name']
                    is_current_lesson = (lesson_in_unit['id'] == selected_lesson['id'])

                    if is_current_lesson:
                        list_item_html = f"<li style='font-weight: bold; color: #8A2BE2;'>{display_title} 【現在の授業】</li>"
                        st.markdown(list_item_html, unsafe_allow_html=True)
                    else:
                        st.markdown(f"<li>", unsafe_allow_html=True)
                        st.button(display_title, key=f"unit_flow_link_direct_{lesson_in_unit['id']}", on_click=set_detail_page, args=(lesson_in_unit['id'],), help=f"「{display_title}」の詳細を見る", type="secondary")
                        st.markdown(f"</li>", unsafe_allow_html=True)
                        
                st.markdown("</ol>", unsafe_allow_html=True)

        st.markdown("---")

        if selected_lesson['materials']:
            st.markdown("<h3><span class='header-icon'>✂️</span>準備物</h3>", unsafe_allow_html=True)
            st.markdown(f"<p>{selected_lesson['materials']}</p>", unsafe_allow_html=True)

        if selected_lesson['points']:
            st.markdown("<h3><span classt='header-icon'>💡</span>指導のポイント</h3>", unsafe_allow_html=True)
            st.markdown("<ul>", unsafe_allow_html=True)
            for point in selected_lesson['points']:
                st.markdown(f"<li>{point}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)

        if selected_lesson['hashtags']:
            st.markdown("<h3><span class='header-icon'>#️⃣</span>ハッシュタグ</h3>", unsafe_allow_html=True)
            tags_html_detail = "".join(f'<span class="tag-badge" style="margin-right: 5px;">#{tag}</span>' for tag in selected_lesson.get('hashtags', []) if tag)
            st.markdown(f"<p>{tags_html_detail}</p>", unsafe_allow_html=True)

        if selected_lesson['material_photos']:
            st.markdown("<h3><span class='header-icon'>📸</span>授業・教材写真</h3>", unsafe_allow_html=True)
            cols = st.columns(3)
            for i, photo_url in enumerate(selected_lesson['material_photos']):
                with cols[i % 3]:
                    if photo_url.strip():
                        st.image(photo_url, use_container_width=True)
                    else:
                        st.warning("一部の教材写真URLが無効なため表示できませんでした。")

        if selected_lesson['video_link'].strip():
            st.markdown("<h3><span class='header-icon'>▶️</span>参考動画</h3>", unsafe_allow_html=True)
            try:
                st.video(selected_lesson['video_link'])
            except Exception as e:
                st.warning(f"動画の読み込み中に問題が発生しました。リンクを確認してください。エラー: {e}")
        else:
            st.markdown("<h3><span class='header-icon'>▶️</span>参考動画</h3>", unsafe_allow_html=True)
            st.info("参考動画は登録されていません。")

        if selected_lesson['detail_word_url'] or selected_lesson['detail_pdf_url'] or selected_lesson['detail_ppt_url'] or selected_lesson['detail_excel_url']:
            st.markdown("<h3><span class='header-icon'>📄</span>詳細資料ダウンロード</h3>", unsafe_allow_html=True)
            if selected_lesson['detail_word_url']:
                word_button_html = f'<a href="{selected_lesson["detail_word_url"]}" target="_blank" style="text-decoration: none;"><button style="background-color: #264A9D; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; margin-right: 10px;">📖 指導案 (Word)</button></a>'
                st.markdown(word_button_html, unsafe_allow_html=True)
            if selected_lesson['detail_pdf_url']:
                pdf_button_html = f'<a href="{selected_lesson["detail_pdf_url"]}" target="_blank" style="text-decoration: none;"><button style="background-color: #B40000; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; margin-right: 10px;">📚 指導案 (PDF)</button></a>'
                st.markdown(pdf_button_html, unsafe_allow_html=True)
            if selected_lesson['detail_ppt_url']:
                ppt_button_html = f'<a href="{selected_lesson["detail_ppt_url"]}" target="_blank" style="text-decoration: none;"><button style="background-color: #D24726; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; margin-right: 10px;">📊 授業資料 (PowerPoint)</button></a>'
                st.markdown(ppt_button_html, unsafe_allow_html=True)
            if selected_lesson['detail_excel_url']:
                excel_button_html = f'<a href="{selected_lesson["detail_excel_url"]}" target="_blank" style="text-decoration: none;"><button style="background-color: #0E6839; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; margin-right: 10px;">📈 評価シート (Excel)</button></a>'
                st.markdown(excel_button_html, unsafe_allow_html=True)

        st.markdown("---")
        st.button("↩️ 一覧に戻る", on_click=back_to_list, key="back_to_list_btn_bottom")

    else:
        st.error("指定された授業カードが見つかりませんでした。")
        st.button("↩️ 一覧に戻る", on_on_click=back_to_list)