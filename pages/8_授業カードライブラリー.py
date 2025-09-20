import streamlit as st
import pandas as pd
from io import BytesIO

# --- Load Data from CSV ---
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
        }
    )
    # ICT活用有無のTRUE/FALSEをbool型に変換
    lesson_data_df['ict_use'] = lesson_data_df['ict_use'].astype(bool)
    
    # 'subject', 'unit_name', 'group_type' カラムが存在しない場合、デフォルト値で作成
    if 'subject' not in lesson_data_df.columns:
        lesson_data_df['subject'] = 'その他'
    if 'unit_name' not in lesson_data_df.columns: # 新規追加
        lesson_data_df['unit_name'] = '単元なし'
    if 'group_type' not in lesson_data_df.columns: # 新規追加
        lesson_data_df['group_type'] = '全体' # 例: 全体, 小グループ, 個別 など

    lesson_data_raw = lesson_data_df.to_dict(orient='records')
except FileNotFoundError:
    st.error("lesson_cards.csv ファイルが見つかりませんでした。pages フォルダと同じ階層に配置してください。")
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
    "unit_name", "group_type" # 新規追加
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
            else:
                def process_list_column(df, col_name, separator):
                    if col_name in df.columns:
                        return df[col_name].apply(lambda x: x.split(separator) if pd.notna(x) else [])
                    return [[]] * len(df)

                new_data_df['introduction_flow'] = process_list_column(new_data_df, 'introduction_flow', ';')
                new_data_df['activity_flow'] = process_list_column(new_data_df, 'activity_flow', ';')
                new_data_df['reflection_flow'] = process_list_column(new_data_df, 'reflection_flow', ';')
                new_data_df['points'] = process_list_column(new_data_df, 'points', ';')
                new_data_df['hashtags'] = process_list_column(new_data_df, 'hashtags', ',')
                new_data_df['material_photos'] = process_list_column(new_data_df, 'material_photos', ';')

                if 'ict_use' in new_data_df.columns:
                    new_data_df['ict_use'] = new_data_df['ict_use'].astype(str).str.lower().map({'true': True, 'false': False}).fillna(False)
                else:
                    new_data_df['ict_use'] = False

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
                        'unit_name': row.get('unit_name', '単元なし'), # 新規追加
                        'group_type': row.get('group_type', '全体') # 新規追加
                    }
                    new_entries.append(lesson_dict)
                    existing_ids.add(row_id)

                st.session_state.lesson_data.extend(new_entries)
                st.success(f"{len(new_entries)}件の授業カードをファイルから追加しました！")
                st.experimental_rerun()
        except Exception as e:
            st.error(f"ファイルの読み込みまたは処理中にエラーが発生しました: {e}")
            st.exception(e)

    st.markdown("---")
    # 教科カテゴリーフィルター
    st.subheader("カテゴリーで絞り込み")
    all_subjects = sorted(list(set(lesson['subject'] for lesson in st.session_state.lesson_data if 'subject' in lesson)))
    if not all_subjects:
        all_subjects.append("その他")
    all_subjects.insert(0, "全て")

    if st.session_state.selected_subject not in all_subjects:
        st.session_state.selected_subject = "全て"
    try:
        default_subject_index = all_subjects.index(st.session_state.selected_subject)
    except ValueError:
        default_subject_index = 0

    st.session_state.selected_subject = st.selectbox(
        "教科を選択",
        options=all_subjects,
        index=default_subject_index,
        key="subject_filter"
    )

    # --- 単元名フィルターの追加 ---
    all_units = sorted(list(set(lesson['unit_name'] for lesson in st.session_state.lesson_data if 'unit_name' in lesson)))
    if not all_units:
        all_units.append("単元なし")
    all_units.insert(0, "全て")

    if st.session_state.selected_unit not in all_units:
        st.session_state.selected_unit = "全て"
    try:
        default_unit_index = all_units.index(st.session_state.selected_unit)
    except ValueError:
        default_unit_index = 0

    st.session_state.selected_unit = st.selectbox(
        "単元を選択",
        options=all_units,
        index=default_unit_index,
        key="unit_filter"
    )
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
        match_subject = True
        match_unit = True # 単元フィルターを追加

        # Keyword search
        if st.session_state.search_query:
            search_lower = st.session_state.search_query.lower()
            if not (search_lower in lesson['title'].lower() or
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

        st.subheader("授業の流れ")
        st.button(f"{'授業の流れを非表示' if st.session_state.show_all_flow else '授業の流れを表示'} 🔃", on_click=toggle_all_flow_display, key=f"toggle_all_flow_{selected_lesson['id']}")

        if st.session_state.show_all_flow:
            if selected_lesson['introduction_flow']:
                st.markdown("<div class='flow-section'>", unsafe_allow_html=True)
                st.markdown("<h4><span class='icon'>🚀</span>導入</h4>", unsafe_allow_html=True)
                st.markdown("<ol class='flow-list'>", unsafe_allow_html=True)
                for step in selected_lesson['introduction_flow']:
                    st.markdown(f"<li>{step}</li>", unsafe_allow_html=True)
                st.markdown("</ol>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            if selected_lesson['activity_flow']:
                st.markdown("<div class='flow-section'>", unsafe_allow_html=True)
                st.markdown("<h4><span class='icon'>💡</span>活動</h4>", unsafe_allow_html=True)
                st.markdown("<ol class='flow-list'>", unsafe_allow_html=True)
                for step in selected_lesson['activity_flow']:
                    st.markdown(f"<li>{step}</li>", unsafe_allow_html=True)
                st.markdown("</ol>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            if selected_lesson['reflection_flow']:
                st.markdown("<div class='flow-section'>", unsafe_allow_html=True)
                st.markdown("<h4><span class='icon'>💭</span>振り返り</h4>", unsafe_allow_html=True)
                st.markdown("<ol class='flow-list'>", unsafe_allow_html=True)
                for step in selected_lesson['reflection_flow']:
                    st.markdown(f"<li>{step}</li>", unsafe_allow_html=True)
                st.markdown("</ol>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # ねらい
        st.markdown("<div class='detail-section'>", unsafe_allow_html=True)
        st.markdown("<h3><span class='header-icon'>🎯</span>ねらい</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{selected_lesson['goal']}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 対象・種別・時間・教科・単元・学習集団の単位 (表示カラム追加)
        st.markdown("<div class='detail-section'>", unsafe_allow_html=True)
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
        if selected_lesson.get('unit_name') and selected_lesson.get('unit_name') != '単元なし':
            unit_name_to_search = selected_lesson['unit_name']
            related_lessons_raw = [
                lesson for lesson in st.session_state.lesson_data 
                if lesson.get('unit_name') == unit_name_to_search and lesson['id'] != selected_lesson['id']
            ]
            
            # durationを数値としてソートするために整形（例: "45分×3コマ" -> 3）
            def extract_duration_order(duration_str):
                import re
                match = re.search(r'(\d+)\s*コマ', duration_str)
                if match:
                    return int(match.group(1))
                return 9999 # マッチしない場合は最後に表示されるように大きい値を返す
            
            # ソート
            related_lessons_sorted = sorted(
                related_lessons_raw,
                key=lambda x: extract_duration_order(x.get('duration', '0コマ'))
            )

            if related_lessons_sorted:
                st.markdown("<div class='detail-section'>", unsafe_allow_html=True)
                st.markdown(f"<h3><span class='header-icon'>🔗</span>同じ単元の他の授業カード（{unit_name_to_search}）</h3>", unsafe_allow_html=True)
                st.info("単元での系統性を考慮し、授業時間順に並べています。")
                for related_card in related_lessons_sorted:
                    # 関連カードの表示を簡略化し、ボタンで詳細へ遷移
                                    col1, col2 = st.columns([0.7, 0.3])
                with col1:
                    st.markdown(f"""
                        <div class="related-lesson-card">
                            <img src="{related_card['image'] if related_card['image'] else 'https://via.placeholder.com/80x50?text=No+Image'}" alt="{related_card['title']}">
                            <div class="related-lesson-card-content">
                                <div class="related-lesson-card-title">{related_card['title']}</div>
                                <div class="related-lesson-card-meta">
                                    <span>{related_card['target_grade']} | </span>
                                    <span>{related_card['disability_type']} | </span>
                                    <span>{related_card['duration']}</span>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.button("詳細へ", key=f"related_detail_btn_{related_card['id']}", on_click=set_detail_page, args=(related_card['id'],))
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info(f"この単元（{unit_name_to_search}）の他の授業カードはまだ登録されていません。")
    
        st.markdown("---")

        # 指導のポイント
        if selected_lesson['points']:
            st.markdown("<div class='detail-section'>", unsafe_allow_html=True)
            st.markdown("<h3><span class='header-icon'>💡</span>指導のポイント</h3>", unsafe_allow_html=True)
            st.markdown("<ul>", unsafe_allow_html=True)
            for point in selected_lesson['points']:
                st.markdown(f"<li>{point}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # 準備物
        if selected_lesson['materials']:
            st.markdown("<div class='detail-section'>", unsafe_allow_html=True)
            st.markdown("<h3><span class='header-icon'>📦</span>準備物</h3>", unsafe_allow_html=True)
            st.markdown(f"<p>{selected_lesson['materials']}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # ハッシュタグ
        if selected_lesson['hashtags']:
            st.markdown("<div class='detail-section'>", unsafe_allow_html=True)
            st.markdown("<h3><span class='header-icon'>#️⃣</span>ハッシュタグ</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='lesson-card-tags'>{''.join(f'<span class='tag-badge'>#{tag}</span>' for tag in selected_lesson['hashtags'] if tag)}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # 関連資料
        st.markdown("<div class='detail-section'>", unsafe_allow_html=True)
        st.markdown("<h3><span class='header-icon'>📎</span>関連資料</h3>", unsafe_allow_html=True)
        
        # 教材写真
        if selected_lesson['material_photos']:
            st.subheader("教材写真")
            # 2カラムで表示
            cols_photos = st.columns(2)
            for i, photo_url in enumerate(selected_lesson['material_photos']):
                if photo_url: # URLが空でない場合のみ表示
                    with cols_photos[i % 2]:
                        try:
                            st.image(photo_url, caption=f"教材写真 {i+1}", use_container_width=True)
                        except Exception:
                            st.warning(f"教材写真の表示に失敗しました。URLを確認してください: {photo_url}")
        else:
            st.info("教材写真はありません。")

        # 動画リンク
        if selected_lesson['video_link']:
            st.subheader("動画")
            try:
                st.video(selected_lesson['video_link'])
            except Exception:
                st.warning(f"動画の表示に失敗しました。URLを確認してください: {selected_lesson['video_link']}")
        else:
            st.info("関連動画はありません。")

        # 詳細資料ダウンロード
        if selected_lesson['detail_word_url'] or selected_lesson['detail_pdf_url']:
            st.subheader("詳細資料ダウンロード")
            if selected_lesson['detail_word_url']:
                st.markdown(f"""
                <a href="{selected_lesson['detail_word_url']}" target="_blank">
                <button style="
                background-color: #286090; color: white; border: none; padding: 10px 20px;
                border-radius: 25px; cursor: pointer; font-size: 1em; font-weight: bold;
                transition: background-color 0.3s, transform 0.2s;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-right: 10px; margin-bottom: 10px;
                ">
                📄 指導案 (Word) をダウンロード
                </button>
                </a>
                """, unsafe_allow_html=True)
            if selected_lesson['detail_pdf_url']:
                st.markdown(f"""
                <a href="{selected_lesson['detail_pdf_url']}" target="_blank">
                <button style="
                background-color: #D32F2F; color: white; border: none; padding: 10px 20px;
                border-radius: 25px; cursor: pointer; font-size: 1em; font-weight: bold;
                transition: background-color 0.3s, transform 0.2s;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 10px;
                ">
                📄 指導案 (PDF) をダウンロード
                </button>
                </a>
                """, unsafe_allow_html=True)
        else:
            st.info("ダウンロード可能な指導案はありません。")
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")
        st.button("↩️ 一覧に戻る", on_click=back_to_list, key="back_to_list_btn_bottom")

    else:
        st.error("指定された授業カードが見つかりません。")
        st.button("↩️ 一覧に戻る", on_click=back_to_list, key="back_to_list_btn_error")

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    /* General Body Styles */
    body {
        font-family: 'Noto Sans JP', sans-serif;
        color: #333;
        background-color: #f0f2f6;
    }

    /* Header Styles */
    h1 {
        color: #8A2BE2; /* 紫色 */
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
    }
    h2 {
        color: #6A1B9A;
        font-size: 1.8em;
        border-bottom: 2px solid #EEE;
        padding-bottom: 10px;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    h3 {
        color: #4A148C;
        font-size: 1.5em;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    .detail-header {
        text-align: center;
        color: #8A2BE2;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .header-icon {
        margin-right: 8px;
        color: #8A2BE2;
    }

    /* Sidebar Styles */
    .css-1d391kg, .css-vk3252 { /* Sidebar wrapper */
        background-color: #ffffff;
        padding: 20px;
        border-right: 1px solid #e0e0e0;
        box-shadow: 2px 0 5px rgba(0,0,0,0.05);
    }
    .css-1d391kg h2, .css-vk3252 h2 { /* Sidebar headers */
        color: #6A1B9A;
        font-size: 1.5em;
        border-bottom: 1px solid #EEE;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }

    /* Lesson Card Grid */
    .lesson-card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 25px;
        padding: 20px 0;
    }

    /* Individual Lesson Card */
    .lesson-card {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        overflow: hidden;
        transition: transform 0.2s, box-shadow 0.2s;
        display: flex;
        flex-direction: column;
    }
    .lesson-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    .lesson-card-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-bottom: 1px solid #eee;
    }
    .lesson-card-content {
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        flex-grow: 1;
    }
    .lesson-card-title {
        font-size: 1.3em;
        font-weight: bold;
        color: #4A148C;
        margin-bottom: 8px;
        line-height: 1.4;
    }
    .lesson-card-catchcopy {
        font-size: 0.95em;
        color: #555;
        margin-bottom: 12px;
        line-height: 1.5;
    }
    .lesson-card-goal {
        font-size: 0.9em;
        color: #666;
        margin-bottom: 10px;
        border-top: 1px dashed #eee;
        padding-top: 10px;
    }
    .lesson-card-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        font-size: 0.85em;
        color: #777;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .lesson-card-meta span .icon {
        margin-right: 5px;
        color: #8A2BE2;
    }
    .lesson-card-tags {
        margin-top: 15px;
        margin-bottom: 20px;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        min-height: 30px; /* タグがないときもレイアウトが崩れないように */
    }
    .tag-badge {
        background-color: #E0BBE4; /* 薄い紫色 */
        color: #4A148C; /* 濃い紫色 */
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8em;
        font-weight: 500;
        white-space: nowrap;
    }

    /* Streamlit Button Styling (general) */
    .stButton>button {
        width: 100%;
        background-color: #8A2BE2; /* 紫色 */
        color: white;
        border-radius: 25px;
        padding: 10px 20px;
        font-size: 1em;
        font-weight: bold;
        border: none;
        transition: background-color 0.3s, transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #6A1B9A; /* 濃い紫色 */
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Detail Page Specifics */
    .detail-section {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        padding: 25px 30px;
        margin-bottom: 30px;
        line-height: 1.7;
    }
    .detail-section h3 {
        color: #8A2BE2;
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 10px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
    }
    .detail-section p {
        margin-bottom: 10px;
    }
    .detail-section ul {
        list-style-type: disc;
        margin-left: 20px;
        padding-left: 0;
    }
    .detail-section li {
        margin-bottom: 8px;
    }
    .stVideo {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-top: 15px;
        margin-bottom: 20px;
    }
    .stImage > img {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* Info/Warning Messages */
    .stAlert {
        border-radius: 8px;
        padding: 15px;
    }
    .stAlert p {
        margin-bottom: 0;
    }

    /* Streamlit widgets */
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stMultiSelect>div>div>div {
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 8px 12px;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
    }
    .stTextInput label, .stSelectbox label, .stMultiSelect label {
        font-weight: bold;
        color: #4A148C;
    }

</style>
""", unsafe_allow_html=True)