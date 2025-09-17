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
        /* General styling from main app */
        [data-testid="stAppViewContainer"] > .main {
            background-image: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        [data-testid="stSidebar"] {
            background-color: rgba(240, 242, 246, 0.9);
        }
        h1, h2, h3 { 
            color: #2c3e50; 
            text-align: center; /* ページタイトルを中央揃えに */
            padding-bottom: 10px;
            font-weight: bold;
        }
        h2 {
            text-align: left;
            border-left: 6px solid #8A2BE2; /* 紫のアクセント */
            padding-left: 12px;
            margin-top: 40px;
        }
        h3 {
            text-align: left;
            border-bottom: 2px solid #4a90e2; /* 青のアクセント */
            padding-bottom: 8px;
            margin-top: 30px;
        }

        /* Card grid specific styles */
        .lesson-card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            padding: 20px 0;
        }
        .lesson-card {
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        }
        .lesson-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        }
        .lesson-card-image {
            width: 100%;
            height: 180px; /* 固定の高さ */
            object-fit: cover; /* 画像がカードに収まるようにトリミング */
            border-bottom: 1px solid #f0f0f0;
        }
        .lesson-card-content {
            padding: 15px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .lesson-card-title {
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 8px;
            line-height: 1.4;
        }
        .lesson-card-goal {
            font-size: 0.9em;
            color: #555;
            margin-bottom: 10px;
            border-left: 3px solid #8A2BE2;
            padding-left: 8px;
        }
        .lesson-card-meta {
            font-size: 0.8em;
            color: #777;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
        }
        .lesson-card-tags {
            font-size: 0.8em;
            color: #4a90e2;
            margin-top: 10px;
            word-break: break-word; /* ハッシュタグが長い場合に改行 */
            min-height: 30px; /* タグがないカードとの高さのズレを緩和 */
        }
        .tag-badge {
            display: inline-block;
            background-color: #e3f2fd;
            color: #2196f3;
            border-radius: 5px;
            padding: 3px 8px;
            margin-right: 5px;
            margin-bottom: 5px;
            font-size: 0.75em;
            white-space: nowrap;
            cursor: pointer; /* タグをクリック可能にする */
        }
        .tag-badge:hover {
            background-color: #bbdefb;
        }

        /* Icons */
        .icon {
            margin-right: 5px;
            vertical-align: middle;
        }

        /* Detail Button Styling */
        .stButton>button {
            border: 2px solid #4a90e2;
            border-radius: 25px;
            color: #4a90e2;
            background-color: #ffffff;
            padding: 8px 20px; /* ボタンのパディングを調整 */
            font-weight: bold;
            transition: all 0.3s ease;
            margin-top: 10px;
        }
        .stButton>button:hover {
            border-color: #8A2BE2;
            color: white;
            background-color: #8A2BE2;
            transform: scale(1.03); /* ホバー時の拡大を少し控えめに */
        }

        /* Detail page specific styles */
        .detail-header {
            text-align: left;
            margin-bottom: 20px;
        }
        .detail-section h3 {
            border-bottom: 2px solid #8A2BE2;
            padding-bottom: 5px;
            margin-top: 25px;
            margin-bottom: 15px;
        }
        .detail-section p, .detail-section ul {
            font-size: 1.05em;
            line-height: 1.6;
            color: #333;
        }
        .detail-section ul {
            list-style-type: disc;
            margin-left: 20px;
        }
        .detail-section li {
            margin-bottom: 5px;
        }
        .detail-image {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }
        .stVideo { /* Streamlit video player */
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .detail-tag-container {
            margin-top: 20px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# --- Sample Data (Replace with your actual data source) ---
# Wordファイルはbase64でエンコードしてダミーコンテンツとして保持
# 実際には、サーバーサイドでファイルを管理し、URLとして提供するのが一般的です。
# ここではデモのため、最小限のWordファイル内容をPythonで生成しています。
def create_dummy_word_file(title="指導案", content="ここに指導案の具体的な内容が入ります。"):
    # docxライブラリがないため、ここではテキストファイルを.docxとして偽装します。
    # 実際のWordファイルを作成するには `python-docx` ライブラリが必要です。
    # pip install python-docx
    # import docx
    # doc = docx.Document()
    # doc.add_heading(title, level=1)
    # doc.add_paragraph(content)
    # bio = io.BytesIO()
    # doc.save(bio)
    # return bio.getvalue()

    # 簡単なテキストをWordファイルのように見せかけるダミー
    dummy_content = f"--- {title} ---\n\n{content}\n\nこのファイルは指導案のサンプルです。\n\n"
    return dummy_content.encode('utf-8')


lesson_data_raw = [
    {
        "id": 1,
        "image": "https://i.imgur.com/example_shopping.jpg", # 生徒がレジで支払いをしている写真
        "title": "高等部 生活単元学習「買い物体験」",
        "catch_copy": "失敗しても笑って学べる買い物授業！",
        "goal": "自分でお金を支払う",
        "target_grade": "高等部",
        "disability_type": "知的中度",
        "duration": "45分",
        "materials": "値段カード, 財布・模擬硬貨, 実店舗（スーパー）",
        "flow": [
            "値段カードで事前練習（いくら払うか、おつりはいくつか）",
            "実店舗で商品を選び、カゴに入れる",
            "レジでお金を支払う（店員さんとのやりとり練習を含む）"
        ],
        "points": [
            "視覚支援（値段カード、支払いステップシート）で「支払う」流れを事前確認",
            "失敗しても先生が適切にフォローし、成功体験につなげる",
            "少人数グループでの実施で個別のサポートを充実"
        ],
        "ict_use": True, # タブレットの計算アプリ活用などを想定
        "hashtags": ["高等部", "生活単元", "お金", "自立活動", "買い物", "社会生活"],
        "detail_pdf_url": "https://example.com/shopping_lesson_plan.pdf", # 指導略案PDF
        "detail_word_data": create_dummy_word_file(
            title="高等部 買い物体験 指導案",
            content="【単元名】生活単元学習「買い物体験を通じて、お金の使い方と社会参加を学ぶ」\n【ねらい】金銭の支払いを通して、買い物の手順を理解し、社会生活に必要な態度や習慣を身に付ける。\n【評価規準】〇〇できる。\n【本時の目標】レジで店員に「お願いします」「ありがとうございました」と伝え、自分の順番でお金を支払うことができる。\n【指導の流れ】\n1. 導入：今日の買い物テーマを確認。値段カードの復習。\n2. 展開：実店舗へ移動。買い物リストに基づき商品を選ぶ。レジでの支払い練習。\n3. まとめ：購入品の確認。振り返り。\n"
        ),
        "material_photos": [
            "https://i.imgur.com/example_price_card.jpg", # 値段カードの写真
            "https://i.imgur.com/example_payment_sheet.jpg" # 支払いステップシートの写真
        ],
        "video_link": "https://www.youtube.com/watch?v=example_shopping_video" # 活動中の動画
    },
    {
        "id": 2,
        "image": "https://i.imgur.com/example_cooking.jpg", # 生徒が調理している写真
        "title": "中学部 生活単元学習「自分でお弁当を作ろう」",
        "catch_copy": "得意なことを見つけて、自立へ一歩！",
        "goal": "手順に沿って調理し、お弁当を完成させる",
        "target_grade": "中学部",
        "disability_type": "知的中度",
        "duration": "90分",
        "materials": "食材一式, 調理器具, レシピカード",
        "flow": [
            "今日のメニューと役割分担の確認",
            "レシピカードを見ながら調理（計量、切る、炒めるなど）",
            "お弁当箱に盛り付け、片付け"
        ],
        "points": [
            "写真付きレシピカードで視覚的に手順を支援",
            "包丁や火の扱いなど、安全指導を徹底",
            "役割分担を明確にし、協力して作業する経験を積む"
        ],
        "ict_use": False,
        "hashtags": ["中学部", "生活単元", "調理", "自立活動", "食育", "家庭科"],
        "detail_pdf_url": "https://example.com/cooking_lesson_plan.pdf",
        "detail_word_data": create_dummy_word_file(
            title="中学部 お弁当作り 指導案",
            content="【単元名】生活単元学習「栄養満点！オリジナル弁当を作ろう」\n【ねらい】調理を通して、食に関する知識を深め、食生活を豊かにしようとする態度を養う。\n【評価規準】〇〇できる。\n【本時の目標】レシピカードを見て、安全に配慮しながら一品を調理することができる。\n"
        ),
        "material_photos": [
            "https://i.imgur.com/example_recipe_card.jpg" # レシピカードの写真
        ],
        "video_link": None
    },
    {
        "id": 3,
        "image": "https://i.imgur.com/example_art.jpg", # 生徒が絵を描いている写真
        "title": "小学部 図画工作「季節を感じるちぎり絵」",
        "catch_copy": "指先の感触で、豊かな表現力を育む",
        "goal": "様々な色の紙を使って、季節の風景をちぎり絵で表現する",
        "target_grade": "小学部",
        "disability_type": "知的軽度",
        "duration": "45分",
        "materials": "色紙, 台紙, のり",
        "flow": [
            "季節の風景（紅葉、雪景色など）の絵本を見る",
            "好きな色の紙を選び、手でちぎる",
            "台紙に貼って風景を完成させる"
        ],
        "points": [
            "色の組み合わせの楽しさを伝え、自由に表現できる雰囲気を作る",
            "指先を使うことで、微細運動能力の発達を促す",
            "完成した作品は教室に飾り、達成感を味わわせる"
        ],
        "ict_use": False,
        "hashtags": ["小学部", "図画工作", "表現", "季節", "アート"],
        "detail_pdf_url": None,
        "detail_word_data": create_dummy_word_file(
            title="小学部 ちぎり絵 指導案",
            content="【単元名】図画工作「指で表現！秋のちぎり絵」\n【ねらい】季節の変化に気づき、色紙の持つ特性を生かして、ちぎり絵で表現することを楽しむ。\n【評価規準】〇〇できる。\n【本時の目標】秋の風景をイメージし、色紙をちぎって台紙に貼り、作品を完成させることができる。\n"
        ),
        "material_photos": [],
        "video_link": None
    }
]

# st.session_stateの初期化
if 'current_lesson_id' not in st.session_state:
    st.session_state.current_lesson_id = None
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'selected_hashtags' not in st.session_state:
    st.session_state.selected_hashtags = []


# --- Helper Functions ---
def display_lesson_card(lesson):
    """個別の授業カードを表示する関数"""
    with st.container():
        st.markdown(f"""
        <div class="lesson-card">
            <img class="lesson-card-image" src="{lesson['image']}" alt="{lesson['title']}">
            <div class="lesson-card-content">
                <div>
                    <div class="lesson-card-title">{lesson['title']}</div>
                    <div class="lesson-card-goal">🎯 {lesson['goal']}</div>
                    <div class="lesson-card-meta">
                        <span><span class="icon">🎓</span>{lesson['target_grade']}・{lesson['disability_type']}</span>
                        <span><span class="icon">⏱</span>{lesson['duration']}</span>
                    </div>
                </div>
                <div class="lesson-card-tags">
                    {''.join(f'<span class="tag-badge" onclick="Streamlit.setComponentValue(\'selected_tag_{tag}\', true)">#{tag}</span>' for tag in lesson['hashtags'])}
                </div>
                {st.button("詳細を見る ➡", key=f"detail_btn_{lesson['id']}", on_click=set_detail_page, args=(lesson['id'],))}
            </div>
        </div>
        """, unsafe_allow_html=True)
        # 上記の onclick イベントは、Streamlitのカスタムコンポーネントを使わないと直接動作しません。
        # 代わりに Streamlitのbuttonを使用します。HTML内のタグは表示用とします。


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
    search_col, tag_col = st.columns([0.7, 0.3])
    with search_col:
        st.session_state.search_query = st.text_input("キーワードで検索", st.session_state.search_query, placeholder="例: 買い物、生活単元、小学部", key="search_input")
    
    # Extract all unique hashtags
    all_hashtags = sorted(list(set(tag for lesson in lesson_data_raw for tag in lesson['hashtags'])))

    with tag_col:
        # st.multiselectでハッシュタグを選択できるようにする
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
                    search_lower in lesson['goal'].lower() or
                    search_lower in lesson['target_grade'].lower() or
                    search_lower in lesson['disability_type'].lower() or
                    any(search_lower in tag.lower() for tag in lesson['hashtags'])):
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
            # st.columnを使って各カードを囲むと、gridレイアウトが崩れる可能性があるため
            # HTMLとCSSで直接gridを構築します。st.button は grid item の中に配置します。
            # st.markdownを使って各カードをHTMLとしてレンダリングし、その中にStreamlitボタンを埋め込む
            st.markdown(f"""
                <div class="lesson-card">
                    <img class="lesson-card-image" src="{lesson['image']}" alt="{lesson['title']}">
                    <div class="lesson-card-content">
                        <div>
                            <div class="lesson-card-title">{lesson['title']}</div>
                            <div class="lesson-card-goal">🎯 {lesson['goal']}</div>
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

        st.image(selected_lesson['image'], caption=selected_lesson['title'], use_container_width=True, class_name="detail-image")

        st.markdown("---")
        
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.subheader("🎯 ねらい")
            st.write(f"**{selected_lesson['goal']}**")
            st.subheader("👥 対象学年・障害特性")
            st.write(f"**{selected_lesson['target_grade']}**・**{selected_lesson['disability_type']}**")
            st.subheader("⏱ 所要時間・準備物")
            st.write(f"**所要時間**: {selected_lesson['duration']}")
            st.write(f"**準備物**: {selected_lesson['materials']}")
            st.subheader("💻 ICT活用有無")
            st.write("あり" if selected_lesson['ict_use'] else "なし")

        with col_info2:
            st.subheader("📖 活動の流れ")
            st.markdown("<ul>" + "".join(f"<li>{step}</li>" for step in selected_lesson['flow']) + "</ul>", unsafe_allow_html=True)

            st.subheader("💡 ポイント・工夫")
            st.markdown("<ul>" + "".join(f"<li>{point}</li>" for point in selected_lesson['points']) + "</ul>", unsafe_allow_html=True)
        
        st.markdown("<div class='detail-tag-container'>", unsafe_allow_html=True)
        st.subheader("🔖 ハッシュタグ")
        st.markdown(''.join(f'<span class="tag-badge">#{tag}</span>' for tag in selected_lesson['hashtags']), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")

        st.header("詳細資料")

        # 指導案 (Wordファイルダウンロード)
        if selected_lesson['detail_word_data']:
            st.subheader("📄 指導略案 (Word)")
            st.download_button(
                label="Wordファイルをダウンロード",
                data=selected_lesson['detail_word_data'],
                file_name=f"{selected_lesson['title']}_指導案.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="download_word_btn"
            )
            st.info("※Wordファイルは直接プレビューできません。ダウンロードしてご確認ください。")
        elif selected_lesson['detail_pdf_url']:
            st.subheader("📄 指導略案 (PDF)")
            st.markdown(f"[指導略案PDFをダウンロード]({selected_lesson['detail_pdf_url']})", unsafe_allow_html=True)
        else:
            st.info("この授業カードには指導略案がありません。")

        # 配布資料・教材写真
        if selected_lesson['material_photos']:
            st.subheader("🖼️ 配布資料・教材写真")
            cols_photos = st.columns(len(selected_lesson['material_photos']))
            for i, photo_url in enumerate(selected_lesson['material_photos']):
                with cols_photos[i]:
                    st.image(photo_url, use_container_width=True, class_name="detail-image")
        else:
            st.info("この授業カードには配布資料・教材写真がありません。")

        # 動画リンク
        if selected_lesson['video_link']:
            st.subheader("▶️ 活動の様子 (動画)")
            # YouTube動画埋め込み対応 (要URLフォーマット確認)
            youtube_match = re.match(r"(?:https?://)?(?:www\.)?(?:m\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=|embed/|v/)?([a-zA-Z0-9_-]{11})", selected_lesson['video_link'])
            if youtube_match:
                video_id = youtube_match.group(1)
                st.video(f"https://www.youtube.com/watch?v={video_id}")
            else:
                st.video(selected_lesson['video_link']) # その他の動画URLをそのまま埋め込み試行
        else:
            st.info("この授業カードには活動の様子の動画がありません。")

    else:
        st.error("指定された授業カードが見つかりませんでした。")
        st.button("↩️ 一覧に戻る", on_click=back_to_list)