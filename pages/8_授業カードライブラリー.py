import streamlit as st
import pandas as pd
import base64
import re # ハッシュタグ抽出用
import io # Wordファイルダウンロード用

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
        /* General styling from main app (adjust as needed for consistency) */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&display=swap');
        body {
            font-family: 'Noto Sans JP', sans-serif;
        }
        [data-testid="stAppViewContainer"] > .main {
            background-image: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        [data-testid="stSidebar"] {
            background-color: rgba(240, 242, 246, 0.95);
        }
        h1, h2, h3, h4, h5, h6 { 
            color: #2c3e50; 
            font-weight: 700;
        }
        h1 {
            text-align: center; 
            padding-bottom: 20px;
            font-size: 2.5em;
            color: #4a90e2; /* メインカラーを使用 */
        }
        h2 {
            text-align: left;
            border-left: 6px solid #8A2BE2; /* 紫のアクセント */
            padding-left: 15px;
            margin-top: 40px;
            font-size: 1.8em;
        }
        h3 {
            text-align: left;
            border-bottom: 2px solid #8A2BE2; /* 青のアクセントを紫に変更 */
            padding-bottom: 8px;
            margin-top: 30px;
            font-size: 1.4em;
            color: #34495e;
        }

        /* Streamlit widget styling */
        .stTextInput>div>div>input {
            border-radius: 25px;
            padding: 10px 18px;
            border: 1px solid #ddd;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            transition: all 0.2s ease-in-out;
        }
        .stTextInput>div>div>input:focus {
            border-color: #8A2BE2;
            box-shadow: 0 0 0 0.2rem rgba(138,43,226,0.25);
        }
        .stMultiSelect>div>div>div { /* multiselect container */
            border-radius: 25px;
            border: 1px solid #ddd;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            transition: all 0.2s ease-in-out;
        }
        .stMultiSelect>div>div>div:focus-within { /* when multiselect is active */
            border-color: #8A2BE2;
            box-shadow: 0 0 0 0.2rem rgba(138,43,226,0.25);
        }
        .stMultiSelect div[data-testid="stMultiSelectOptions"] {
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        /* Card grid specific styles */
        .lesson-card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); /* カードサイズを微調整 */
            gap: 25px; /* カード間の余白を広げる */
            padding: 20px 0;
        }
        .lesson-card {
            background-color: #ffffff;
            border: none; /* ボーダーを削除 */
            border-radius: 15px; /* 角丸を大きく */
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1); /* 影を強調 */
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        }
        .lesson-card:hover {
            transform: translateY(-8px); /* ホバー時の浮き上がりを強調 */
            box-shadow: 0 15px 30px rgba(74, 144, 226, 0.2); /* ホバー時の影をアクセントカラーに */
        }
        .lesson-card-image {
            width: 100%;
            height: 180px; 
            object-fit: cover; 
            border-bottom: 1px solid #f0f0f0;
        }
        .lesson-card-content {
            padding: 20px; /* パディングを増やす */
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .lesson-card-title {
            font-size: 1.3em; /* フォントサイズを大きく */
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 10px;
            line-height: 1.4;
        }
        .lesson-card-catchcopy { /* キャッチコピーを追加 */
            font-size: 0.9em;
            color: #6a0dad; /* 紫色 */
            font-weight: 500;
            margin-bottom: 12px;
            line-height: 1.3;
            font-style: italic;
        }
        .lesson-card-goal {
            font-size: 0.95em;
            color: #555;
            margin-bottom: 12px;
            border-left: 4px solid #4a90e2; /* アクセントカラー */
            padding-left: 10px;
            line-height: 1.5;
        }
        .lesson-card-meta {
            font-size: 0.85em;
            color: #777;
            display: flex;
            flex-wrap: wrap; /* 小さな画面で折り返す */
            gap: 10px; /* アイテム間の隙間 */
            align-items: center;
            margin-top: 10px;
        }
        .lesson-card-meta span {
            display: flex;
            align-items: center;
            background-color: #f7f9fc; /* 少し明るい背景 */
            padding: 5px 10px;
            border-radius: 8px;
        }
        .lesson-card-tags {
            font-size: 0.8em;
            color: #4a90e2;
            margin-top: 15px;
            min-height: 30px; 
            display: flex; /* Flexboxでタグをきれいに配置 */
            flex-wrap: wrap;
            gap: 5px;
        }
        .tag-badge {
            display: inline-block;
            background-color: #e3f2fd; /* 明るい青 */
            color: #2196f3;
            border-radius: 12px; /* 角丸を大きく */
            padding: 5px 10px;
            font-size: 0.75em;
            white-space: nowrap;
            transition: background-color 0.2s;
            cursor: pointer;
        }
        .tag-badge:hover {
            background-color: #bbdefb;
            color: #1976d2;
        }

        /* Icons */
        .icon {
            margin-right: 8px;
            font-size: 1.1em; /* アイコンサイズを少し大きく */
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
            margin-top: 15px; /* ボタンとコンテンツの間の余白 */
            width: 100%; /* カード幅いっぱいに */
        }
        .stButton>button:hover {
            border-color: #8A2BE2;
            color: white;
            background-color: #8A2BE2;
            transform: scale(1.02); 
        }

        /* Detail page specific styles */
        .detail-header {
            text-align: left;
            margin-bottom: 20px;
        }
        .detail-section h3 {
            border-bottom: 2px solid #8A2BE2;
            padding-bottom: 5px;
            margin-top: 35px;
            margin-bottom: 15px;
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
        }
        .detail-section li {
            margin-bottom: 8px;
        }
        .detail-image-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
            margin-bottom: 30px;
        }
        .detail-image-gallery img {
            max-width: 100%;
            height: 200px; /* 固定の高さ */
            object-fit: cover;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s ease-in-out;
        }
        .detail-image-gallery img:hover {
            transform: scale(1.03);
        }
        .stVideo {
            border-radius: 10px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.15);
            margin-top: 20px;
            margin-bottom: 30px;
        }
        .detail-tag-container {
            margin-top: 25px;
            margin-bottom: 25px;
        }
        .stAlert {
            border-radius: 10px;
            font-size: 0.95em;
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
            'flow': lambda x: x.split(';') if pd.notna(x) else [],
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


# --- Helper Functions ---
def set_detail_page(lesson_id):
    """詳細ページへの遷移をトリガーする関数"""
    st.session_state.current_lesson_id = lesson_id

def back_to_list():
    """一覧ページに戻る関数"""
    st.session_state.current_lesson_id = None

# --- Main Page Logic ---
if st.session_state.current_lesson_id is None:
    # --- Lesson Card List View ---
    st.markdown("<h1>🃏 授業カードライブラリー</h1>", unsafe_allow_html=True)
    st.write("先生方の実践授業アイデアを検索し、日々の指導に役立てましょう！")

    # Search and Filter Section
    search_col, tag_col = st.columns([0.6, 0.4]) # レイアウト調整
    with search_col:
        st.session_state.search_query = st.text_input("キーワードで検索", st.session_state.search_query, placeholder="例: 買い物、生活単元、小学部", key="search_input")
    
    # Extract all unique hashtags
    all_hashtags = sorted(list(set(tag for lesson in lesson_data_raw for tag in lesson['hashtags'] if tag))) # 空のタグを除外

    with tag_col:
        st.session_state.selected_hashtags = st.multiselect(
            "ハッシュタグで絞り込み", 
            options=all_hashtags, 
            default=st.session_state.selected_hashtags,
            placeholder="選択してください"
        )
    
    filtered_lessons = []
    for lesson in lesson_data_raw:
        match_search = True
        match_tags = True

        # Keyword search
        if st.session_state.search_query:
            search_lower = st.session_state.search_query.lower()
            if not (search_lower in lesson['title'].lower() or
                    search_lower in lesson['catch_copy'].lower() or
                    search_lower in lesson['goal'].lower() or
                    search_lower in lesson['target_grade'].lower() or
                    search_lower in lesson['disability_type'].lower() or
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
            # 各カードをHTMLとStreamlitボタンの組み合わせで表示
            # Streamlitのbuttonは、その親がHTML要素であっても機能します。
            st.markdown(f"""
                <div class="lesson-card">
                    <img class="lesson-card-image" src="{lesson['image']}" alt="{lesson['title']}">
                    <div class="lesson-card-content">
                        <div>
                            <div class="lesson-card-title">{lesson['title']}</div>
                            <div class="lesson-card-catchcopy">{lesson['catch_copy']}</div>
                            <div class="lesson-card-goal">🎯 ねらい: {lesson['goal']}</div>
                            <div class="lesson-card-meta">
                                <span><span class="icon">🎓</span>{lesson['target_grade']}・{lesson['disability_type']}</span>
                                <span><span class="icon">⏱</span>{lesson['duration']}</span>
                            </div>
                        </div>
                        <div class="lesson-card-tags">
                            {''.join(f'<span class="tag-badge">#{tag}</span>' for tag in lesson['hashtags'])}
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
    selected_lesson = next((lesson for lesson in lesson_data_raw if lesson['id'] == st.session_state.current_lesson_id), None)

    if selected_lesson:
        st.button("↩️ 一覧に戻る", on_click=back_to_list)

        st.markdown(f"<h1 class='detail-header'>{selected_lesson['title']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 class='detail-header'>{selected_lesson['catch_copy']}</h3>", unsafe_allow_html=True)

        # メインイメージ
        st.image(selected_lesson['image'], caption=selected_lesson['title'], use_container_width=True)

        st.markdown("---")
        
        # 基本情報と活動の流れを横並びに
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.subheader("🎯 ねらい")
            st.markdown(f"<p>{selected_lesson['goal']}</p>", unsafe_allow_html=True)
            st.subheader("👥 対象学年・障害特性")
            st.markdown(f"<p>{selected_lesson['target_grade']}・{selected_lesson['disability_type']}</p>", unsafe_allow_html=True)
            st.subheader("⏱ 所要時間・準備物")
            st.markdown(f"<p>所要時間: **{selected_lesson['duration']}**</p>", unsafe_allow_html=True)
            st.markdown(f"<p>準備物: **{selected_lesson['materials']}**</p>", unsafe_allow_html=True)
            st.subheader("💻 ICT活用有無")
            st.markdown(f"<p>{'あり' if selected_lesson['ict_use'] else 'なし'}</p>", unsafe_allow_html=True)

        with col_info2:
            st.subheader("📖 活動の流れ")
            st.markdown("<ol>" + "".join(f"<li>{step}</li>" for step in selected_lesson['flow']) + "</ol>", unsafe_allow_html=True)

            st.subheader("💡 ポイント・工夫")
            st.markdown("<ul>" + "".join(f"<li>{point}</li>" for point in selected_lesson['points']) + "</ul>", unsafe_allow_html=True)
        
        st.markdown("<div class='detail-tag-container'>", unsafe_allow_html=True)
        st.subheader("🔖 ハッシュタグ")
        st.markdown(''.join(f'<span class="tag-badge">#{tag}</span>' for tag in selected_lesson['hashtags']), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")

        st.header("詳細資料")

        # 指導案 (Wordファイルダウンロード)
        if selected_lesson['detail_word_url']:
            st.subheader("📄 指導略案 (Wordファイル)")
            # Wordファイルは直接Streamlitで表示できないため、ダウンロードリンクを提供
            st.markdown(f"""
            <a href="{selected_lesson['detail_word_url']}" download="{selected_lesson['title']}_指導案.docx" target="_blank">
                <button style="
                    background-color: #4a90e2; color: white; border: none; padding: 10px 20px;
                    border-radius: 25px; cursor: pointer; font-size: 1em; font-weight: bold;
                    transition: background-color 0.3s, transform 0.2s;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                " onmouseover="this.style.backgroundColor='#357ABD'; this.style.transform='scale(1.03)';" onmouseout="this.style.backgroundColor='#4a90e2'; this.style.transform='scale(1.0)';">
                    Wordファイルをダウンロード ⬇️
                </button>
            </a>
            """, unsafe_allow_html=True)
            st.info("※Wordファイルは直接プレビューできません。ダウンロードして内容をご確認ください。")
        elif selected_lesson['detail_pdf_url']:
            st.subheader("📄 指導略案 (PDFファイル)")
            st.markdown(f"[指導略案PDFをダウンロード]({selected_lesson['detail_pdf_url']})", unsafe_allow_html=True)
            st.info("※PDFファイルはブラウザで開くかダウンロードしてご確認ください。")
        else:
            st.warning("この授業カードには指導略案が登録されていません。")

        # 配布資料・教材写真
        if selected_lesson['material_photos']:
            st.subheader("🖼️ 配布資料・教材写真")
            st.markdown("<div class='detail-image-gallery'>", unsafe_allow_html=True)
            for photo_url in selected_lesson['material_photos']:
                # Streamlitのimageで直接ギャラリーを構築
                st.image(photo_url, use_column_width="always") 
            st.markdown("</div>", unsafe_allow_html=True)
            # Streamlitのグリッド機能で画像を並べる方が綺麗かもしれません
            # cols_photos = st.columns(min(3, len(selected_lesson['material_photos'])))
            # for i, photo_url in enumerate(selected_lesson['material_photos']):
            #     with cols_photos[i % 3]:
            #         st.image(photo_url, use_container_width=True)
        else:
            st.info("この授業カードには配布資料・教材写真が登録されていません。")

        # 動画リンク
        if selected_lesson['video_link']:
            st.subheader("▶️ 活動の様子 (動画)")
            youtube_match = re.match(r"(?:https?://)?(?:www\.)?(?:m\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=|embed/|v/)?([a-zA-Z0-9_-]{11})", selected_lesson['video_link'])
            if youtube_match:
                video_id = youtube_match.group(1)
                st.video(f"https://www.youtube.com/watch?v={video_id}")
            else:
                st.warning("動画URLの形式が正しくないか、YouTube以外の動画です。")
                st.video(selected_lesson['video_link']) # その他の動画URLをそのまま埋め込み試行
        else:
            st.warning("この授業カードには活動の様子の動画が登録されていません。")

    else:
        st.error("指定された授業カードが見つかりませんでした。")
        st.button("↩️ 一覧に戻る", on_click=back_to_list)