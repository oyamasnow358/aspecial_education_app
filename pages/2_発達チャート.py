import streamlit as st
import io
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
import os
import base64
from pathlib import Path

# ==========================================
# 0. ページ設定
# ==========================================
st.set_page_config(
    page_title="MieeL - 発達チャート", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. 画像処理 (ロゴ読み込み)
# ==========================================
def get_img_as_base64(file):
    try:
        # 画像パスを絶対パスで解決
        script_path = Path(__file__)
        app_root = script_path.parent.parent
        img_path = app_root / file
        
        if img_path.exists():
            with open(img_path, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode()
        else:
            return None
    except:
        return None

logo_path = "MieeL2.png" 
logo_b64 = get_img_as_base64(logo_path)
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img">' if logo_b64 else '<div class="logo-placeholder">📊</div>'


# ==========================================
# 2. デザイン定義 (白ベース・視認性特化・アニメーション)
# ==========================================
def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = f"""
    <style>
        /* --- 全体フォント --- */
        html, body, [class*="css"] {{
            font-family: 'Noto Sans JP', sans-serif !important;
            color: #1a1a1a !important;
            line-height: 1.6 !important;
        }}

        /* --- 背景 --- */
        [data-testid="stAppViewContainer"] {{
            background-color: #ffffff;
            background-image: linear-gradient(rgba(255,255,255,0.92), rgba(255,255,255,0.92)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-attachment: fixed;
            padding-left: 20px;
            padding-right: 20px;
        }}

        /* --- 見出し --- */
        h1, h2, h3, h4, h5, h6 {{
            color: #0f172a !important;
            font-weight: 700 !important;
        }}
        
        p, span, div, label, .stMarkdown {{
            color: #333333 !important;
        }}

        /* --- サイドバー --- */
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid #e2e8f0 !important;
        }}
        [data-testid="stSidebar"] * {{
            color: #333333 !important;
        }}

        /* --- アニメーション --- */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}

        /* --- 機能カード --- */
        [data-testid="stBorderContainer"] {{
            background-color: #ffffff !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 15px !important;
            padding: 25px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
            opacity: 0;
            animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        }}
        
        div[data-testid="column"]:nth-of-type(1) [data-testid="stBorderContainer"] {{ animation-delay: 0.1s; }}
        div[data-testid="column"]:nth-of-type(2) [data-testid="stBorderContainer"] {{ animation-delay: 0.2s; }}
        div[data-testid="column"]:nth-of-type(3) [data-testid="stBorderContainer"] {{ animation-delay: 0.3s; }}

        [data-testid="stBorderContainer"]:hover {{
            border-color: #4a90e2 !important;
            background-color: #f8fafc !important;
            box-shadow: 0 10px 25px rgba(74, 144, 226, 0.15) !important;
            transform: translateY(-3px);
            transition: all 0.3s ease;
        }}

        /* --- ボタン --- */
        .stButton > button {{
            width: 100%;
            background-color: #ffffff !important;
            border: 2px solid #e2e8f0 !important;
            color: #4a90e2 !important;
            font-weight: bold !important;
            border-radius: 30px !important;
            padding: 0.6em 1em !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        }}
        .stButton > button:hover {{
            background-color: #4a90e2 !important;
            color: #ffffff !important;
            border-color: #4a90e2 !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(74, 144, 226, 0.2) !important;
        }}
        
        .stButton > button[kind="primary"] {{
            background-color: #4a90e2 !important;
            color: #ffffff !important;
            border: 2px solid #4a90e2 !important;
            box-shadow: 0 4px 6px rgba(74, 144, 226, 0.2);
        }}
        .stButton > button[kind="primary"]:hover {{
            background-color: #2563eb !important;
            border-color: #2563eb !important;
        }}

        /* --- ラジオボタン --- */
        div[role="radiogroup"] label {{
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            color: #334155 !important;
            padding: 12px !important;
            border-radius: 10px;
            margin-bottom: 8px;
            transition: all 0.2s;
        }}
        div[role="radiogroup"] label:hover {{
            background-color: #e0f2fe !important;
            border-color: #4a90e2 !important;
            color: #0284c7 !important;
        }}

        /* --- エキスパンダー --- */
        .streamlit-expanderHeader {{
            background-color: #f8fafc !important;
            color: #0f172a !important;
            font-weight: 600 !important;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
        }}
        .streamlit-expanderContent {{
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0;
            border-top: none;
            padding: 15px !important;
        }}

        /* --- 説明文ボックス --- */
        .info-box {{
            background-color: #f0f9ff;
            border: 2px solid #4a90e2;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(74,144,226,0.1);
            margin-bottom: 25px;
            color: #0c4a6e;
            animation: fadeInUp 0.8s ease-out forwards;
        }}

        /* --- infoアラート --- */
        [data-testid="stAlert"] {{
            background-color: #f0f9ff !important;
            border: 1px solid #bae6fd !important;
            color: #0369a1 !important;
            border-radius: 10px !important;
        }}

        /* --- 戻るボタン --- */
        .back-link {{
            margin-bottom: 20px;
        }}
        .back-link a {{
            display: inline-block;
            padding: 10px 20px;
            background: #ffffff;
            border: 2px solid #e2e8f0;
            border-radius: 25px;
            color: #4a90e2 !important;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        .back-link a:hover {{
            background: #4a90e2;
            color: #ffffff !important;
            border-color: #4a90e2;
            box-shadow: 0 4px 10px rgba(74, 144, 226, 0.2);
        }}
        
        /* --- ヘッダーレイアウト --- */
        .header-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-bottom: 40px;
            padding: 40px 0;
            border-bottom: 2px solid #f1f5f9;
            animation: float 6s ease-in-out infinite;
        }}
        .logo-img {{
            width: 100px;
            height: auto;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
        }}
        .page-title {{
            font-size: 3rem;
            font-weight: 900;
            color: #0f172a;
            margin: 0;
            line-height: 1.2;
        }}
        hr {{ border-color: #cbd5e1; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# CSS適用
load_css()

# ==========================================
# 3. メインコンテンツ開始
# ==========================================

# 戻るボタン
st.markdown('<div class="back-link"><a href="https://aspecial-education-app.onrender.com/" target="_self">« TOPページに戻る</a></div>', unsafe_allow_html=True)

# ヘッダー
st.markdown(f"""
    <div class="header-container">
        {logo_html}
        <h1 class="page-title">発達チャート作成</h1>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 4. データ処理関数
# ==========================================
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
            if len(row) > 21 and row[21].isdigit():
                age_step = int(row[21])
                for j, key in enumerate(headers):
                    if j < len(row):
                        data_map[key][age_step] = row[j]
            elif len(row) > 21:
                 pass
            
        return data_map
    except Exception as e:
        st.error(f"データ読み込みエラー: {e}")
        return None

# ==========================================
# 5. Google API セットアップ (修正版)
# ==========================================
sheets_service = None
drive_service = None
SPREADSHEET_ID_UNDER7 = "1yXSXSjYBaV2jt2BNO638Y2YZ6U7rdOCv5ScozlFq_EE"
SPREADSHEET_ID_OVER7 = "13M6lz6CFmGdZ1skJRp44TLm1DR1A4FvxdZdwaJjPJnQ"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

try:
    # 認証情報を取得 (優先順位: st.secrets -> ファイル)
    credentials = None
    
    # 1. Renderなどのファイルパス ("/etc/secrets/...") を確認
    secret_file_path = "/etc/secrets/GOOGLE_SHEETS_CREDENTIALS"
    
    if os.path.exists(secret_file_path):
        with open(secret_file_path, "r") as f:
            google_credentials_info = json.load(f)
            credentials = Credentials.from_service_account_info(google_credentials_info, scopes=SCOPES)
            
    # 2. ファイルがない場合、st.secrets (ローカルやStreamlit Cloud) を確認
    elif "gcp_service_account" in st.secrets:
        google_credentials_info = dict(st.secrets["gcp_service_account"])
        credentials = Credentials.from_service_account_info(google_credentials_info, scopes=SCOPES)

    # 3. どちらも見つからない場合はエラー
    else:
        st.error("認証ファイル (/etc/secrets/GOOGLE_SHEETS_CREDENTIALS) が見つかりません。")
        st.stop()
    
    # サービス構築
    sheets_service = build('sheets', 'v4', credentials=credentials)
    drive_service = build('drive', 'v3', credentials=credentials)
    
    # データ読み込み
    guidance_map_under7 = load_guidance_data(sheets_service, SPREADSHEET_ID_UNDER7, "シート2")
    guidance_map_over7 = load_guidance_data(sheets_service, SPREADSHEET_ID_OVER7, "シート3")

except Exception as e:
    st.error(f"API接続エラー: {e}")
    st.stop()


# ==========================================
# 6. アプリケーション本体
# ==========================================

# 説明文
st.markdown("""
<div class="info-box">
    <strong>🎯 使い方：</strong><br>
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
st.markdown("### 📝 発達段階の入力")
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
    st.subheader("📥 結果の確認と保存")

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