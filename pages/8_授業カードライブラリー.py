import streamlit as st
import pandas as pd
import base64
import re
import io
from io import BytesIO
import xlsxwriter
import hashlib
import os
from pathlib import Path

# ==========================================
# 1. 認証設定
# ==========================================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("snow".encode()).hexdigest()

def check_password(username, password):
    if username == ADMIN_USERNAME:
        return hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH
    return False

# ==========================================
# 2. ページ設定
# ==========================================
st.set_page_config(
    page_title="授業カードライブラリー",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 3. 画像処理 & ロゴ
# ==========================================
def get_img_as_base64(file):
    try:
        script_path = Path(__file__)
        possible_paths = [script_path.parent / file, script_path.parent.parent / file]
        for img_path in possible_paths:
            if img_path.exists():
                with open(img_path, "rb") as f:
                    data = f.read()
                return base64.b64encode(data).decode()
        return None
    except:
        return None

logo_path = "mirairo2.png" 
logo_b64 = get_img_as_base64(logo_path)
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img">' if logo_b64 else '<div class="logo-placeholder">🃏</div>'

# ==========================================
# 4. CSSデザイン (ぬるっと動くカード + ページネーション)
# ==========================================
def load_css():
    st.markdown(r"""
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        /* --- 全体フォント --- */
        html, body, [class*="css"] {
            font-family: 'Noto Sans JP', sans-serif !important;
            color: #333333 !important;
        }

        /* --- 背景 --- */
        [data-testid="stAppViewContainer"] {
            background-color: #f8f9fa; /* 背景を少しグレーにしてカードを際立たせる */
            background-image: linear-gradient(rgba(255,255,255,0.92), rgba(255,255,255,0.92)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-attachment: fixed;
        }

        /* --- ヘッダー --- */
        .header-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-bottom: 40px;
            padding: 40px 0;
        }
        .logo-img { width: 100px; height: auto; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1)); }
        .page-title { font-size: 3rem; font-weight: 900; color: #0f172a !important; margin: 0; line-height: 1.2; }
        .page-subtitle { font-size: 1.2rem; color: #475569 !important; font-weight: bold; margin-top: 5px; }

        /* --- ★重要: カードデザイン (st.container) --- */
        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            background-color: #ffffff;
            border-radius: 20px; /* 角丸を強く */
            border: 2px solid #e5e7eb; /* デフォルトの枠線 */
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            /* ぬるっと動くアニメーション設定 */
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            padding: 0px !important;
            overflow: hidden;
            height: 100%;
            display: flex;
            flex-direction: column;
            position: relative;
        }
        
        /* ホバー時の動き: 浮き上がり + 枠線強調 + 影 */
        div[data-testid="stVerticalBlockBorderWrapper"] > div:hover {
            border-color: #4a90e2;
            transform: translateY(-8px) scale(1.01); /* 少し拡大して浮く */
            box-shadow: 0 20px 40px rgba(74, 144, 226, 0.15);
            background-color: #ffffff;
            z-index: 10;
        }

        /* --- カード内要素 --- */
        .card-img-wrapper {
            width: calc(100% + 32px);
            margin-left: -16px;
            margin-top: -16px;
            height: 180px;
            overflow: hidden;
            border-bottom: 2px solid #f3f4f6;
            position: relative;
        }
        .card-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }
        /* ホバー時に画像を少しズーム */
        div[data-testid="stVerticalBlockBorderWrapper"] > div:hover .card-img {
            transform: scale(1.05);
        }

        .card-content {
            padding: 5px 10px 15px 10px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }
        
        .subject-badge {
            font-size: 0.7em;
            color: #ffffff;
            font-weight: 800;
            background: linear-gradient(135deg, #4a90e2, #00d2ff);
            padding: 4px 12px;
            border-radius: 15px;
            display: inline-block;
            margin-bottom: 8px;
            box-shadow: 0 2px 4px rgba(74, 144, 226, 0.3);
            align-self: flex-start;
        }

        .card-title {
            font-size: 1.25em;
            font-weight: 900;
            color: #1e293b;
            margin-bottom: 8px;
            line-height: 1.4;
        }

        .card-catch {
            font-size: 0.9em;
            color: #64748b;
            font-weight: 600;
            margin-bottom: 12px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            min-height: 2.8em;
        }

        .card-goal {
            font-size: 0.85em;
            color: #334155;
            background-color: #f1f5f9;
            border-left: 4px solid #cbd5e1;
            padding: 10px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 12px;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            min-height: 4.5em;
        }

        .card-badges {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 10px;
        }
        
        .meta-badge {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            color: #64748b;
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 0.75em;
            font-weight: bold;
        }

        .tag-container {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-bottom: 15px;
            min-height: 25px;
        }
        
        .tag {
            color: #0284c7;
            background-color: #e0f2fe;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 0.75em;
            font-weight: bold;
        }

        /* --- ボタンカスタマイズ --- */
        .stButton > button {
            width: 100%;
            border-radius: 12px;
            font-weight: bold;
            border: none;
            background: linear-gradient(to right, #f1f5f9, #e2e8f0);
            color: #475569;
            padding: 10px 0;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .stButton > button:hover {
            background: linear-gradient(to right, #4a90e2, #3b82f6);
            color: white;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        /* Primary Button (詳細ページなど) */
        .stButton > button[kind="primary"] {
            background: #4a90e2;
            color: white;
        }

        /* --- ページネーション --- */
        .pagination-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 5px;
            margin-top: 40px;
            padding: 20px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.03);
            width: fit-content;
            margin-left: auto;
            margin-right: auto;
        }
        /* ページネーションボタンの個別調整 */
        div[data-testid="stHorizontalBlock"] button {
            width: 45px !important;
            height: 45px !important;
            padding: 0 !important;
            border-radius: 12px !important;
            border: 1px solid #e2e8f0 !important;
            background: white !important;
            color: #64748b !important;
        }
        div[data-testid="stHorizontalBlock"] button:hover {
            border-color: #4a90e2 !important;
            color: #4a90e2 !important;
            background: #f8fafc !important;
        }
        /* アクティブなページ */
        div[data-testid="stHorizontalBlock"] button[kind="primary"] {
            background: #4a90e2 !important;
            color: white !important;
            border-color: #4a90e2 !important;
            box-shadow: 0 4px 10px rgba(74, 144, 226, 0.3) !important;
        }

        /* --- 詳細ページのデザイン --- */
        .detail-box {
            background-color: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.03);
            margin-bottom: 30px;
            border: 1px solid #f1f5f9;
        }
        .detail-header-title {
            font-size: 2.5rem;
            font-weight: 900;
            color: #1e293b;
            margin-bottom: 10px;
            line-height: 1.3;
        }
        .detail-label {
            font-size: 0.85em;
            color: #94a3b8;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 5px;
        }
        .detail-value {
            font-size: 1.1em;
            color: #334155;
            font-weight: 500;
            margin-bottom: 20px;
        }
        .flow-step {
            background: #ffffff;
            border-left: 4px solid #4a90e2;
            padding: 15px 20px;
            margin-bottom: 15px;
            border-radius: 0 10px 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        }
        .dl-btn-container {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 15px;
        }
        .custom-dl-btn {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 24px;
            border-radius: 12px;
            color: white;
            text-decoration: none;
            font-weight: bold;
            transition: transform 0.2s;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        .custom-dl-btn:hover {
            transform: translateY(-3px);
            opacity: 0.95;
        }

        /* --- 戻るボタン --- */
        .back-link a {
            display: inline-block;
            padding: 8px 20px;
            background: #ffffff;
            border: 2px solid #e2e8f0;
            border-radius: 25px;
            color: #4a90e2 !important;
            text-decoration: none;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        /* Google Form Link */
        .google-form-link-button {
            display: inline-flex;
            align-items: center;
            padding: 10px 25px;
            background-color: #ffffff;
            color: #4a90e2;
            border: 2px solid #4a90e2;
            border-radius: 30px;
            text-decoration: none;
            font-weight: bold;
            margin: 20px auto;
            display: block;
            width: fit-content;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        .google-form-link-button:hover {
            background-color: #4a90e2;
            color: #ffffff;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ==========================================
# 5. データ処理 & ロジック
# ==========================================

# Googleフォームリンク
google_form_html = """
    <a href="https://leeson-abfy5bxayhavhoznzexj8r.streamlit.app/" target="_blank" class="google-form-link-button">
        <span style="margin-right:10px;">📝</span> 授業カードを作成する (Googleフォーム)
    </a>
"""

# 戻るボタン
st.markdown('<div class="back-link"><a href="https://aspecialeducationapp-6iuvpdfjbflp4wyvykmzey.streamlit.app/" target="_self">« TOPページに戻る</a></div>', unsafe_allow_html=True)

LESSON_CARDS_CSV = "lesson_cards.csv"
LESSON_CARD_COLUMNS = [
    "id", "unit_name", "catch_copy", "goal", "target_grade", "disability_type",
    "developmental_stage", "duration", "materials", "introduction_flow", "activity_flow", 
    "reflection_flow", "points", "hashtags", "image", "material_photos", "video_link", 
    "detail_word_url", "detail_pdf_url", "detail_ppt_url", "detail_excel_url",
    "ict_use", "subject", "group_type", "unit_order", "unit_lesson_title"
]

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
            }
        )
        # 欠損値処理と文字列変換
        str_cols = ['unit_name', 'unit_lesson_title', 'video_link', 'image', 'target_grade', 'ict_use', 
                    'subject', 'group_type', 'catch_copy', 'goal', 'disability_type', 'duration', 
                    'materials', 'developmental_stage', 'detail_word_url', 'detail_pdf_url', 
                    'detail_ppt_url', 'detail_excel_url']
        for col in str_cols:
            if col in lesson_data_df.columns:
                lesson_data_df[col] = lesson_data_df[col].fillna('').astype(str)
        
        # ID生成
        if 'id' not in lesson_data_df.columns:
            lesson_data_df['id'] = range(1, len(lesson_data_df) + 1)
        else:
            lesson_data_df['id'] = lesson_data_df['id'].fillna(0).astype(int)
            
        return lesson_data_df.to_dict(orient='records')
    except FileNotFoundError:
        st.error(f"{LESSON_CARDS_CSV} が見つかりません。")
        return []
    except Exception as e:
        st.error(f"CSV読み込みエラー: {e}")
        return []

if 'lesson_data' not in st.session_state:
    st.session_state.lesson_data = load_lesson_data()

# セッション状態初期化
if 'current_lesson_id' not in st.session_state: st.session_state.current_lesson_id = None
if 'search_query' not in st.session_state: st.session_state.search_query = ""
if 'selected_hashtags' not in st.session_state: st.session_state.selected_hashtags = []
if 'selected_subject' not in st.session_state: st.session_state.selected_subject = "全て"
if 'show_all_flow' not in st.session_state: st.session_state.show_all_flow = True # デフォルトでフロー表示ON
if 'current_page' not in st.session_state: st.session_state.current_page = 1
if 'authenticated' not in st.session_state: st.session_state.authenticated = False

# ページ遷移関数
def set_detail_page(lesson_id):
    st.session_state.current_lesson_id = lesson_id
    st.session_state.show_all_flow = True

def back_to_list():
    st.session_state.current_lesson_id = None
    st.session_state.show_all_flow = True

def toggle_all_flow_display():
    st.session_state.show_all_flow = not st.session_state.show_all_flow

def set_page(page_num):
    st.session_state.current_page = page_num
    # st.rerun() # rerurnは不要な場合が多いが、動作が怪しい場合は有効化

# ==========================================
# 6. サイドバー (管理者機能 - 完全版)
# ==========================================
with st.sidebar:
    st.header("📚 データ登録・管理")
    st.markdown("---")

    if not st.session_state.authenticated:
        st.subheader("管理者ログイン")
        with st.form("login_form"):
            username = st.text_input("ユーザー名")
            password = st.text_input("パスワード", type="password")
            if st.form_submit_button("ログイン"):
                if check_password(username, password):
                    st.session_state.authenticated = True
                    st.success("ログイン成功")
                    st.rerun()
                else:
                    st.error("認証失敗")
    else:
        st.success("ログイン中")
        if st.button("ログアウト"):
            st.session_state.authenticated = False
            st.rerun()
        st.markdown("---")
        
        st.subheader("ファイル操作")
        
        template_df = pd.DataFrame(columns=LESSON_CARD_COLUMNS)
        csv_buffer = io.BytesIO()
        template_df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
        st.download_button("⬇️ CSVテンプレートDL", data=csv_buffer.getvalue(), file_name="template.csv", mime="text/csv")

        uploaded_file = st.file_uploader("⬆️ ファイルアップロード", type=["xlsx", "csv", "xlsm"])
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    new_df = pd.read_csv(uploaded_file)
                else:
                    try:
                        new_df = pd.read_excel(uploaded_file, sheet_name='自動集計')
                    except:
                        new_df = pd.read_excel(uploaded_file)
                
                for col in LESSON_CARD_COLUMNS:
                    if col not in new_df.columns:
                        if col in ['introduction_flow', 'activity_flow', 'reflection_flow', 'points', 'hashtags', 'material_photos']:
                            new_df[col] = [[]] * len(new_df)
                        else:
                            new_df[col] = ''
                
                existing_ids = {d['id'] for d in st.session_state.lesson_data}
                max_id = max(existing_ids) if existing_ids else 0
                
                new_entries = []
                for idx, row in new_df.iterrows():
                    current_id = row.get('id')
                    row_id = int(current_id) if pd.notna(current_id) and str(current_id).isdigit() and int(current_id) > 0 else 0
                    
                    if row_id == 0 or row_id in existing_ids:
                        max_id += 1
                        row_id = max_id
                    
                    lesson_dict = {col: row[col] for col in LESSON_CARD_COLUMNS if col in row}
                    lesson_dict['id'] = row_id
                    new_entries.append(lesson_dict)
                    existing_ids.add(row_id)
                
                st.session_state.lesson_data.extend(new_entries)
                
                df_to_save = pd.DataFrame(st.session_state.lesson_data)
                for col in ['introduction_flow', 'activity_flow', 'reflection_flow', 'points', 'material_photos']:
                    df_to_save[col] = df_to_save[col].apply(lambda x: ';'.join(map(str, x)) if isinstance(x, list) else str(x))
                if 'hashtags' in df_to_save.columns:
                    df_to_save['hashtags'] = df_to_save['hashtags'].apply(lambda x: ','.join(map(str, x)) if isinstance(x, list) else str(x))
                
                df_to_save.to_csv(LESSON_CARDS_CSV, index=False, encoding='utf-8-sig')
                st.success(f"{len(new_entries)}件追加しました！")
                st.rerun()
                
            except Exception as e:
                st.error(f"エラー: {e}")

# ==========================================
# 7. メイン表示切り替え
# ==========================================

if st.session_state.current_lesson_id is None:
    # === 一覧ページ ===
    st.markdown(f"""
        <div class="header-container">
            {logo_html}
            <div class="title-group">
                <h1 class="page-title">授業カードライブラリー</h1>
                <div class="page-subtitle">先生方の実践授業アイデアを共有・検索できるデータベース</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(google_form_html, unsafe_allow_html=True)
    st.markdown("---")

    # 検索フィルター
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.search_query = st.text_input("🔍 キーワード検索", st.session_state.search_query, placeholder="例: 買い物、小学部")
    with c2:
        all_tags = sorted(list(set(t for l in st.session_state.lesson_data for t in l.get('hashtags', []))))
        st.session_state.selected_hashtags = st.multiselect("🏷️ タグ絞り込み", all_tags, default=st.session_state.selected_hashtags)
    
    all_subjects = ["全て"] + sorted(list(set(l.get('subject', '') for l in st.session_state.lesson_data if l.get('subject'))))
    def update_sub(): st.session_state.selected_subject = st.session_state.sub_select
    st.selectbox("📖 教科", all_subjects, index=0 if st.session_state.selected_subject not in all_subjects else all_subjects.index(st.session_state.selected_subject), key="sub_select", on_change=update_sub)

    # フィルタリング
    filtered = []
    for l in st.session_state.lesson_data:
        text = (str(l.get('unit_name','')) + str(l.get('subject','')) + str(l.get('catch_copy','')) + 
                str(l.get('goal','')) + str(l.get('hashtags',''))).lower()
        if st.session_state.search_query.lower() in text:
            if not st.session_state.selected_hashtags or any(t in l.get('hashtags',[]) for t in st.session_state.selected_hashtags):
                if st.session_state.selected_subject == "全て" or l.get('subject') == st.session_state.selected_subject:
                    filtered.append(l)

    # ページネーション設定 (12枚/ページ)
    PER_PAGE = 12 
    total_pages = max(1, (len(filtered) + PER_PAGE - 1) // PER_PAGE)
    st.session_state.current_page = min(max(1, st.session_state.current_page), total_pages)
    
    start = (st.session_state.current_page - 1) * PER_PAGE
    display_items = filtered[start : start + PER_PAGE]

    st.markdown("---")
    
    if not display_items:
        st.info("該当する授業カードはありません。")
    else:
        # ★★★ 3列グリッド (12枚表示) ★★★
        rows = [display_items[i:i + 3] for i in range(0, len(display_items), 3)]

        for row in rows:
            cols = st.columns(3) # 常に3列
            for i, lesson in enumerate(row):
                with cols[i]:
                    # border=Trueで枠線付きコンテナを作成 (CSSでリッチに装飾)
                    with st.container(border=True):
                        
                        # 画像
                        img_url = lesson.get('image') if lesson.get('image') else 'https://via.placeholder.com/400x200?text=No+Image'
                        st.markdown(f"""
                            <div class="card-img-wrapper">
                                <img src="{img_url}" class="card-img">
                            </div>
                        """, unsafe_allow_html=True)

                        # テキスト情報
                        subject = lesson.get('subject', 'その他')
                        unit = lesson.get('unit_name', '名称未設定')
                        catch = lesson.get('catch_copy', '')
                        goal = lesson.get('goal', '')
                        grade = lesson.get('target_grade', '不明')
                        duration = lesson.get('duration', '不明')
                        tags_html = "".join(f'<span class="tag">#{t}</span>' for t in lesson.get('hashtags', []))
                        
                        content_html = f"""
                            <div class="card-content">
                                <span class="subject-badge">📖 {subject}</span>
                                <div class="card-title">{unit}</div>
                                <div class="card-catch">{catch}</div>
                                <div class="card-goal">🎯 {goal}</div>
                                <div class="card-badges">
                                    <span class="meta-badge">🎓 {grade}</span>
                                    <span class="meta-badge">⏱ {duration}</span>
                                </div>
                                <div class="tag-container">{tags_html}</div>
                            </div>
                        """
                        st.markdown(content_html, unsafe_allow_html=True)
                        
                        # 詳細ボタン (カードの下部に配置)
                        st.button("👉 詳細を見る", key=f"btn_{lesson['id']}", on_click=set_detail_page, args=(lesson['id'],), use_container_width=True)

    # ★★★ 拡張ページネーション (数字で指定可能) ★★★
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True) # スペーサー
    
    if total_pages > 1:
        # 中央寄せのためにカラムで調整
        _, center_col, _ = st.columns([1, 6, 1])
        
        with center_col:
            # ページネーションのロジック: 前、1, 2, ... 現在 ... 最後、次
            pagination_cols = st.columns(min(total_pages + 2, 9)) # 最大9個のボタンを表示
            col_idx = 0
            
            # 前へ
            with pagination_cols[col_idx]:
                if st.session_state.current_page > 1:
                    st.button("◀", on_click=set_page, args=(st.session_state.current_page - 1,), key="pg_prev")
            col_idx += 1
            
            # 表示するページ番号の範囲を決定 (現在のページを中心に5つ程度)
            page_range_start = max(1, st.session_state.current_page - 2)
            page_range_end = min(total_pages, page_range_start + 4)
            if page_range_end - page_range_start < 4:
                page_range_start = max(1, page_range_end - 4)
                
            # ページ番号ボタン
            for p in range(page_range_start, page_range_end + 1):
                with pagination_cols[col_idx]:
                    is_current = (p == st.session_state.current_page)
                    st.button(str(p), on_click=set_page, args=(p,), key=f"pg_{p}", type="primary" if is_current else "secondary")
                col_idx += 1
            
            # 次へ
            if col_idx < len(pagination_cols):
                with pagination_cols[col_idx]:
                    if st.session_state.current_page < total_pages:
                        st.button("▶", on_click=set_page, args=(st.session_state.current_page + 1,), key="pg_next")

else:
    # === 詳細ページ (機能完全版 + デザイン強化) ===
    lesson = next((l for l in st.session_state.lesson_data if l['id'] == st.session_state.current_lesson_id), None)
    
    if lesson:
        # トップに戻るボタン
        st.button("↩️ 一覧に戻る", on_click=back_to_list, key="back_top")
        
        # 白背景のボックスで詳細を囲む
        with st.container():
            st.markdown("<div class='detail-box'>", unsafe_allow_html=True)
            
            # タイトルエリア
            st.markdown(f"<div class='detail-header-title'>{lesson.get('unit_name')}</div>", unsafe_allow_html=True)
            if lesson.get('catch_copy'):
                st.markdown(f"<div style='color:#64748b; font-size:1.2rem; font-weight:bold; margin-bottom:20px;'>{lesson['catch_copy']}</div>", unsafe_allow_html=True)
            
            # メイン画像
            if lesson.get('image'):
                st.image(lesson['image'], use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)

            # 3カラムレイアウトで基本情報
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("<div class='detail-label'>対象学年</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='detail-value'>🎓 {lesson.get('target_grade')}</div>", unsafe_allow_html=True)
                st.markdown("<div class='detail-label'>障害種別</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='detail-value'>🧩 {lesson.get('disability_type')}</div>", unsafe_allow_html=True)
            with c2:
                st.markdown("<div class='detail-label'>授業時間</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='detail-value'>⏱ {lesson.get('duration')}</div>", unsafe_allow_html=True)
                st.markdown("<div class='detail-label'>発達段階</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='detail-value'>🌱 {lesson.get('developmental_stage', '不明')}</div>", unsafe_allow_html=True)
            with c3:
                st.markdown("<div class='detail-label'>教科</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='detail-value'>📖 {lesson.get('subject')}</div>", unsafe_allow_html=True)
                st.markdown("<div class='detail-label'>ICT活用</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='detail-value'>💻 {lesson.get('ict_use')}</div>", unsafe_allow_html=True)

            st.markdown("---")
            
            # ねらいと準備物
            col_goal, col_mat = st.columns([1, 1])
            with col_goal:
                st.markdown("### 🎯 ねらい")
                st.info(lesson.get('goal'))
            with col_mat:
                st.markdown("### ✂️ 準備物")
                st.warning(lesson.get('materials') if lesson.get('materials') else "特になし")

            st.markdown("---")

            # 授業の流れ
            st.subheader("⏳ 授業の流れ")
            if st.button("表示 / 非表示 切り替え", key="toggle_flow"): toggle_all_flow_display()
            
            if st.session_state.show_all_flow:
                if lesson.get('introduction_flow'):
                    flow_html = "<div class='flow-step'><h4>🚀 導入</h4><ul style='margin:0; padding-left:20px;'>" + "".join(f"<li>{s}</li>" for s in lesson['introduction_flow']) + "</ul></div>"
                    st.markdown(flow_html, unsafe_allow_html=True)
                if lesson.get('activity_flow'):
                    flow_html = "<div class='flow-step'><h4>💡 展開</h4><ul style='margin:0; padding-left:20px;'>" + "".join(f"<li>{s}</li>" for s in lesson['activity_flow']) + "</ul></div>"
                    st.markdown(flow_html, unsafe_allow_html=True)
                if lesson.get('reflection_flow'):
                    flow_html = "<div class='flow-step'><h4>💭 まとめ</h4><ul style='margin:0; padding-left:20px;'>" + "".join(f"<li>{s}</li>" for s in lesson['reflection_flow']) + "</ul></div>"
                    st.markdown(flow_html, unsafe_allow_html=True)

            # ポイント
            if lesson.get('points'):
                st.markdown("### 💡 指導のポイント")
                for p in lesson['points']:
                    st.markdown(f"- {p}")

            # 単元連携機能 (復活)
            if lesson.get('unit_name') and lesson.get('unit_name') != '単元なし':
                unit_name_to_search = lesson['unit_name']
                target_grade_to_match = lesson['target_grade']
                all_lessons_in_unit = [l for l in st.session_state.lesson_data if l.get('unit_name') == unit_name_to_search and l.get('target_grade') == target_grade_to_match]
                sorted_lessons_in_unit = sorted(all_lessons_in_unit, key=lambda x: x.get('unit_order', 9999))

                if len(sorted_lessons_in_unit) > 1:
                    st.markdown("---")
                    st.markdown(f"### 📚 この単元 ({unit_name_to_search}) の他の授業")
                    cols = st.columns(len(sorted_lessons_in_unit))
                    for idx, l_unit in enumerate(sorted_lessons_in_unit):
                        title = l_unit.get('unit_lesson_title') or l_unit['unit_name']
                        if l_unit['id'] == lesson['id']:
                            st.markdown(f"**{idx+1}. {title} (表示中)**")
                        else:
                            if st.button(f"{idx+1}. {title} へ", key=f"go_unit_{l_unit['id']}"):
                                set_detail_page(l_unit['id'])
                                st.rerun()

            # 教材写真 & 動画
            if lesson.get('material_photos') or lesson.get('video_link'):
                st.markdown("---")
                if lesson.get('material_photos'):
                    st.markdown("### 📸 教材写真")
                    p_cols = st.columns(3)
                    for i, p_url in enumerate(lesson['material_photos']):
                        with p_cols[i % 3]:
                            if p_url.strip(): st.image(p_url, use_container_width=True)
                
                if lesson.get('video_link'):
                    st.markdown("### ▶️ 参考動画")
                    st.video(lesson['video_link'])

            # ダウンロードボタン (リッチデザイン)
            st.markdown("---")
            st.subheader("📄 資料ダウンロード")
            
            dl_html = "<div class='dl-btn-container'>"
            has_dl = False
            if lesson.get('detail_word_url'):
                dl_html += f'<a href="{lesson["detail_word_url"]}" target="_blank" class="custom-dl-btn" style="background-color:#2b579a;"><span>📝</span> 指導案 (Word)</a>'
                has_dl = True
            if lesson.get('detail_pdf_url'):
                dl_html += f'<a href="{lesson["detail_pdf_url"]}" target="_blank" class="custom-dl-btn" style="background-color:#b30b00;"><span>📄</span> 指導案 (PDF)</a>'
                has_dl = True
            if lesson.get('detail_ppt_url'):
                dl_html += f'<a href="{lesson["detail_ppt_url"]}" target="_blank" class="custom-dl-btn" style="background-color:#d24726;"><span>📊</span> 授業スライド (PPT)</a>'
                has_dl = True
            if lesson.get('detail_excel_url'):
                dl_html += f'<a href="{lesson["detail_excel_url"]}" target="_blank" class="custom-dl-btn" style="background-color:#217346;"><span>📈</span> 評価シート (Excel)</a>'
                has_dl = True
            dl_html += "</div>"
            
            if has_dl:
                st.markdown(dl_html, unsafe_allow_html=True)
            else:
                st.info("ダウンロード可能な資料はありません。")

            st.markdown("</div>", unsafe_allow_html=True) # End detail-box

        st.button("↩️ 一覧に戻る", on_click=back_to_list, key="back_btm")
        
    else:
        st.error("データが見つかりません")
        st.button("戻る", on_click=back_to_list)