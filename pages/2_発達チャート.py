import streamlit as st
import io
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
import os

# --- ▼ ページ設定 ▼ ---
st.set_page_config(
    page_title="Mirairo - 発達チャート", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ▼ デザイン定義 (Mirairo共通デザイン) ▼ ---
def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = """
    <style>
        /* --- 全体フォント --- */
        html, body, [class*="css"] {
            font-family: 'Noto Sans JP', sans-serif !important;
        }

        /* --- 背景 (黒ベース + 画像) --- */
        [data-testid="stAppViewContainer"] {
            background-color: #000000;
            background-image: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-attachment: fixed;
        }

        /* --- 文字色 (白・影付き) --- */
        h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown, .stRadio label {
            color: #ffffff !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.9) !important;
        }

        /* --- サイドバー (半透明) --- */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* --- サイドバー開閉ボタン --- */
        [data-testid="stSidebarNavCollapseButton"] {
            color: #fff !important;
        }

        /* 
           ================================================================
           ★ 機能カードのデザイン (白枠・アニメーション) ★
           ================================================================
        */
        
        /* アニメーション定義 */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        [data-testid="stBorderContainer"] {
            background-color: #151515 !important;
            border: 2px solid #ffffff !important;
            border-radius: 16px !important;
            padding: 20px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.8) !important;
            
            /* アニメーション適用 */
            animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        }

        /* ホバー時の動き */
        [data-testid="stBorderContainer"]:hover {
            border-color: #4a90e2 !important;
            transform: translateY(-5px);
            background-color: #000000 !important;
            box-shadow: 0 0 20px rgba(74, 144, 226, 0.4) !important;
            transition: all 0.3s ease;
        }

        /* --- ボタンのデザイン --- */
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
        
        /* Primaryボタン (実行ボタンなど) */
        .stButton > button[kind="primary"] {
            background-color: #4a90e2 !important;
            color: #ffffff !important;
            border: 2px solid #4a90e2 !important;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #ffffff !important;
            color: #4a90e2 !important;
        }

        /* --- ラジオボタンのスタイル調整 --- */
        div[role="radiogroup"] label {
            background-color: rgba(255,255,255,0.05);
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 5px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.2s;
        }
        div[role="radiogroup"] label:hover {
            background-color: rgba(74, 144, 226, 0.2);
            border-color: #4a90e2;
        }

        /* --- エキスパンダー (目安を見る) --- */
        .streamlit-expanderHeader {
            background-color: rgba(255,255,255,0.1) !important;
            color: #fff !important;
            border-radius: 8px !important;
        }
        .streamlit-expanderContent {
            background-color: rgba(0,0,0,0.5) !important;
            color: #ddd !important;
            border: 1px solid #444;
            border-top: none;
            border-radius: 0 0 8px 8px;
        }

        /* --- infoボックス --- */
        [data-testid="stAlert"] {
            background-color: rgba(74, 144, 226, 0.1) !important;
            border: 1px solid #4a90e2 !important;
            color: #fff !important;
        }

        /* --- 戻るボタンコンテナ --- */
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
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# CSS適用
load_css()

# --- ▼ 戻るボタン ▼ ---
st.markdown('<div class="back-link"><a href="Home" target="_self">« TOPページに戻る</a></div>', unsafe_allow_html=True)


# --- ▼ データ処理関数 (キャッシュ) ▼ ---
@st.cache_data(ttl=600)
def load_guidance_data(_sheets_service, spreadsheet_id, sheet_name):
    try:
        sheet_data = _sheets_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=f"{sheet_name}!A1:V"
        ).execute().get('values', [])
        
        if not sheet_data:
            st.warning(f"シート '{sheet_name}' にデータがありません。")
            return None

        headers = [h.strip() for h in sheet_data[0]]
        data_map = {key: {} for key in headers}
        for row in sheet_data[1:]:
            # Age Step列 (V列, インデックス21) が存在し、数値であるか確認
            if len(row) > 21 and row[21].isdigit():
                age_step = int(row[21])
                for j, key in enumerate(headers):
                    if j < len(row):
                        data_map[key][age_step] = row[j]
            elif len(row) > 21:
                 # データはあるがAge Stepが不正な場合（警告は省略）
                 pass
            
        return data_map
    except Exception as e:
        st.error(f"データ読み込みエラー: {e}")
        return None

# --- ▼ Google API セットアップ ▼ ---
sheets_service = None
drive_service = None
SPREADSHEET_ID_UNDER7 = "1yXSXSjYBaV2jt2BNO638Y2YZ6U7rdOCv5ScozlFq_EE"
SPREADSHEET_ID_OVER7 = "13M6lz6CFmGdZ1skJRp44TLm1DR1A4FvxdZdwaJjPJnQ"

try:
    secret_file_path = "/etc/secrets/GOOGLE_SHEETS_CREDENTIALS"

    if not os.path.exists(secret_file_path):
        # ローカル開発用フォールバック (必要なければ削除可)
        # st.warning("Secret file not found. Checking local secrets.")
        pass
    
    with open(secret_file_path, "r") as f:
        file_content = f.read() 
        google_credentials_info = json.loads(file_content) 

    credentials = Credentials.from_service_account_info(
        google_credentials_info,
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    
    sheets_service = build('sheets', 'v4', credentials=credentials)
    drive_service = build('drive', 'v3', credentials=credentials)
    
    guidance_map_under7 = load_guidance_data(sheets_service, SPREADSHEET_ID_UNDER7, "シート2")
    guidance_map_over7 = load_guidance_data(sheets_service, SPREADSHEET_ID_OVER7, "シート3")

except Exception as e:
    st.error(f"API接続エラー: {e}")
    st.stop()


# --- ▼ メインコンテンツ ▼ ---

st.title("📊 発達チャート作成")
st.markdown("""
<div style="background: rgba(255,255,255,0.05); border: 1px solid #fff; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
    お子さんの現在の発達段階を選択し、状態と次のステップをまとめたチャートを作成・保存します。
</div>
""", unsafe_allow_html=True)

# --- 発達段階表の切り替え ---
st.subheader("表示する発達段階表の選択")
col_under7, col_over7 = st.columns(2)

if 'display_mode' not in st.session_state:
    st.session_state.display_mode = "under7"

with col_under7:
    if st.button("発達年齢 7歳以下用", use_container_width=True, type="primary" if st.session_state.display_mode == "under7" else "secondary"):
        st.session_state.display_mode = "under7"
with col_over7:
    if st.button("発達年齢 8歳以上用", use_container_width=True, type="primary" if st.session_state.display_mode == "over7" else "secondary"):
        st.session_state.display_mode = "over7"

st.info(f"現在、**{'7歳以下用' if st.session_state.display_mode == 'under7' else '8歳以上用'}**の発達段階表が表示されています。")

# --- 入力フォーム ---
st.markdown("### 発達段階の入力")
st.caption("各項目の「▼ 目安を見る」を開いて内容を確認し、選択してください。")

if st.session_state.display_mode == "under7":
    current_spreadsheet_id = SPREADSHEET_ID_UNDER7
    current_guidance_map = guidance_map_under7
    categories = ["認知力・操作", "認知力・注意力", "集団参加", "生活動作", "言語理解", "表出言語", "記憶", "読字", "書字", "粗大運動", "微細運動","数の概念"]
    options = ["0〜3ヶ月", "3〜6ヶ月", "6〜9ヶ月", "9〜12ヶ月", "12～18ヶ月", "18～24ヶ月", "2～3歳", "3～4歳", "4～5歳", "5～6歳", "6～7歳"]
    age_categories_map = {text: i + 1 for i, text in enumerate(options)}
    sheet_to_write_data = "シート1"
else: 
    current_spreadsheet_id = SPREADSHEET_ID_OVER7
    current_guidance_map = guidance_map_over7
    categories = ["自己管理スキル", "行動調整スキル", "社会的コミュニケーション", "協働スキル", "実用リテラシー", "実用数学", "健康・安全スキル", "情報活用スキル", "地域利用・社会参加スキル", "進路・職業スキル"]
    options = ["8〜10歳", "10〜12歳", "12～14歳", "14〜16歳", "16歳以上"]
    age_categories_map = {text: i + 1 for i, text in enumerate(options)}
    sheet_to_write_data = "シート1"

with st.form("chart_form"):
    selected_options = {}
    # 3カラムレイアウト (各コンテナにCSSで白枠・アニメーションが適用される)
    cols = st.columns(3)
    for i, category in enumerate(categories):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"#### {category}")
                default_index = options.index(st.session_state.get(f"radio_{category}_{st.session_state.display_mode}", options[0]))
                
                selected_options[category] = st.radio(
                    f"{category}", 
                    options, 
                    key=f"radio_{category}_{st.session_state.display_mode}", 
                    label_visibility="collapsed", 
                    index=default_index
                )

                with st.expander("▼ 目安を見る"):
                    if current_guidance_map and category in current_guidance_map:
                        for age_text, age_step in age_categories_map.items():
                            description = current_guidance_map[category].get(age_step, "（記載なし）")
                            st.markdown(f"**{age_text}:** {description}")
                    else:
                        st.write("データなし")
    
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("📊 チャートを作成して書き込む", use_container_width=True, type="primary")

# --- 処理実行 ---
if submitted:
    with st.spinner('処理中... しばらくお待ちください。'):
        try:
            # 1. 書き込みデータ準備
            values_to_write = [[cat, '', opt] for cat, opt in selected_options.items()]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=current_spreadsheet_id, range=f"{sheet_to_write_data}!A3:C14",
                valueInputOption="RAW", body={"values": values_to_write}
            ).execute()

            # 2. 数値変換
            converted_values = [[age_categories_map.get(opt, "")] for opt in selected_options.values()]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=current_spreadsheet_id, range=f"{sheet_to_write_data}!B3:B14",
                valueInputOption="RAW", body={"values": converted_values}
            ).execute()

            # 3. データコピー (A3:C14 -> A19:C30)
            sheet_data_current = sheets_service.spreadsheets().values().get(
                spreadsheetId=current_spreadsheet_id, range=f"{sheet_to_write_data}!A3:C14"
            ).execute().get('values', [])
            sheets_service.spreadsheets().values().update(
                spreadsheetId=current_spreadsheet_id, range=f"{sheet_to_write_data}!A19:C30",
                valueInputOption="RAW", body={"values": sheet_data_current}
            ).execute()
            
            # 4. 次のステップ (+1) 計算
            max_age_step = len(options)
            updated_b_values = [[min(max_age_step, int(row[1]) + 1) if len(row) > 1 and str(row[1]).isdigit() else ""] for row in sheet_data_current]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=current_spreadsheet_id, range=f"{sheet_to_write_data}!B19:B30",
                valueInputOption="RAW", body={"values": updated_b_values}
            ).execute()

            # 5. テキスト逆変換
            b_to_c_mapping = {v: k for k, v in age_categories_map.items()}
            updated_c_values = [[b_to_c_mapping.get(b[0], "該当なし")] for b in updated_b_values]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=current_spreadsheet_id, range=f"{sheet_to_write_data}!C19:C30",
                valueInputOption="RAW", body={"values": updated_c_values}
            ).execute()

            # 6. 詳細記述の更新 (D列)
            category_names = [row[0].strip() for row in sheet_data_current if row]
            
            results_d3 = []
            for i, cat in enumerate(category_names):
                if i < len(converted_values) and converted_values[i] and str(converted_values[i][0]).isdigit():
                    results_d3.append([current_guidance_map.get(cat, {}).get(int(converted_values[i][0]), "該当なし")])
                else:
                    results_d3.append(["該当なし"])

            sheets_service.spreadsheets().values().update(
                spreadsheetId=current_spreadsheet_id, range=f"{sheet_to_write_data}!D3:D14",
                valueInputOption="RAW", body={"values": results_d3}
            ).execute()

            results_d19 = []
            for i, cat in enumerate(category_names):
                if i < len(updated_b_values) and updated_b_values[i] and str(updated_b_values[i][0]).isdigit():
                    results_d19.append([current_guidance_map.get(cat, {}).get(updated_b_values[i][0], "該当なし")])
                else:
                    results_d19.append(["該当なし"])

            sheets_service.spreadsheets().values().update(
                spreadsheetId=current_spreadsheet_id, range=f"{sheet_to_write_data}!D19:D30",
                valueInputOption="RAW", body={"values": results_d19}
            ).execute()

            st.success("✅ 作成完了！ 下のボタンから確認・ダウンロードしてください。")
            st.session_state.chart_created = True

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            st.session_state.chart_created = False

# --- 結果表示 ---
if st.session_state.get('chart_created', False):
    st.markdown("---")
    st.subheader("結果の確認と保存")

    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            sheet_gid = "0"
            spreadsheet_url_chart = f"https://docs.google.com/spreadsheets/d/{current_spreadsheet_id}/edit#gid={sheet_gid}"
            st.link_button("🌐 スプレッドシートで確認", spreadsheet_url_chart, use_container_width=True)
        with c2:
            if st.button("💾 Excel形式でダウンロード", use_container_width=True):
                try:
                    request = drive_service.files().export_media(fileId=current_spreadsheet_id, mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    file_data = io.BytesIO()
                    downloader = MediaIoBaseDownload(file_data, request)
                    done = False
                    while not done: status, done = downloader.next_chunk()
                    file_data.seek(0)
                    st.download_button(
                        label="🔽 ダウンロード開始",
                        data=file_data.getvalue(),
                        file_name=f"hattatsu_chart_{st.session_state.display_mode}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        type="primary"
                    )
                except Exception as e:
                    st.error(f"ダウンロードエラー: {e}")

st.markdown("---")
st.markdown("### 📈 成長傾向の分析")
with st.container(border=True):
    st.markdown("これまでのデータから成長グラフを作成します。")
    st.page_link("https://bunnsekiexcel-edeeuzkkntxmhdptk54v2t.streamlit.app/", label="成長傾向分析ツールへ 🔗", icon="📈")