import streamlit as st
import io
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
import os

# --- ▼ 共通CSSの読み込み ▼ ---
# (変更ないため、コードは前のものをそのままお使いください)
def load_css():
    """カスタムCSSを読み込む関数"""
    css = """
    <style>
        /* --- 背景画像の設定 --- */
        [data-testid="stAppViewContainer"] > .main {
            background-image: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), url("https://i.imgur.com/CTSCBYi.png");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        /* サイドバーの背景を少し透過 */
        [data-testid="stSidebar"] {
            background-color: rgba(240, 242, 246, 0.9);
        }
        
            
        /* --- ▼ サイドバーの閉じるボタンをカスタマイズ（最終版）▼ --- */
        [data-testid="stSidebarNavCollapseButton"] {
            position: relative !important;
            width: 2rem !important;
            height: 2rem !important;
        }
        /* 元のアイコンを完全に非表示にする */
        [data-testid="stSidebarNavCollapseButton"] * {
            display: none !important;
            visibility: hidden !important;
        }
        /* カスタムアイコン「«」を疑似要素として追加 */
        [data-testid="stSidebarNavCollapseButton"]::before {
            content: '«' !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            position: absolute !important;
            width: 100% !important;
            height: 100% !important;
            top: 0 !important;
            left: 0 !important;
            font-size: 24px !important;
            font-weight: bold !important;
            color: #31333F !important;
            transition: background-color 0.2s, color 0.2s !important;
            border-radius: 0.5rem;
        }
        [data-testid="stSidebarNavCollapseButton"]:hover::before {
            background-color: #F0F2F6 !important;
            color: #8A2BE2 !important;
        }
        /* --- ▲ サイドバーのカスタマイズここまで ▲ --- */

  

        /* --- 全体のフォント (修正版) --- */
        /* アプリのコンテナに基本フォントを適用し、アイコンフォントの上書きを防ぐ */
        [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
        }

        /* --- 見出しのスタイル --- */
        h1 {
            color: #2c3e50;
            text-align: center;
            padding-bottom: 20px;
            font-weight: bold;
        }
        h2 {
            color: #34495e;
            border-left: 6px solid #8A2BE2;
            padding-left: 12px;
            margin-top: 40px;
        }
        h3 {
            color: #34495e;
            border-bottom: 2px solid #4a90e2;
            padding-bottom: 8px;
            margin-top: 30px;
        }

        /* --- カードデザイン (st.container(border=True)のスタイル) --- */
        div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] div.st-emotion-cache-1r6slb0 {
            background-color: rgba(255, 255, 255, 0.95);
            border: 1px solid #e0e0e0;
            border-radius: 15px;
            padding: 1.5em 1.5em;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
            transition: box-shadow 0.3s ease-in-out, transform 0.3s ease-in-out;
            margin-bottom: 20px;
        }
        div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] div.st-emotion-cache-1r6slb0:hover {
            box-shadow: 0 10px 20px rgba(74, 144, 226, 0.2);
            transform: translateY(-5px);
        }
        
        /* --- ボタンのスタイル --- */
        .stButton>button {
            border: 2px solid #4a90e2;
            border-radius: 25px;
            color: #4a90e2;
            background-color: #ffffff;
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            border-color: #8A2BE2;
            color: white;
            background-color: #8A2BE2;
            transform: scale(1.05);
        }
        .stButton>button[kind="primary"] {
            background-color: #4a90e2;
            color: white;
            border: none;
        }
        .stButton>button[kind="primary"]:hover {
            background-color: #357ABD;
            border-color: #357ABD;
            transform: scale(1.05);
        }

                /* --- st.infoのカスタムスタイル --- */
        .st-emotion-cache-1wivap1 {
             background-color: rgba(232, 245, 253, 0.7);
             border-left: 5px solid #4a90e2;
             border-radius: 8px;
        }
        
        /* --- ▼▼▼ この部分を新しいコードに置き換える ▼▼▼ --- */
        /* st.expanderのデフォルトアイコン（文字化けしているもの）を非表示にする */
        [data-testid="stExpanderToggleIcon"] {
            display: none;
        }
        /* --- ▲▲▲ ここまで ▲▲▲ --- */

        /* --- フッターの区切り線 --- */
        .footer-hr {
            border: none;
            height: 3px;
            background: linear-gradient(to right, #4a90e2, #8A2BE2);
            margin-top: 40px;
            margin-bottom: 20px;
        }
        /* --- 戻るボタンのスタイル (位置調整) --- */
        .back-button-container {
            position: relative; /* relativeにして通常のフローで配置 */
            padding-bottom: 20px; /* 下に余白 */
            margin-bottom: -50px; /* 上の要素との重なりを調整 */
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
# --- ▲ 共通CSSの読み込み ▲ ---

st.set_page_config(
    page_title="発達チャート作成", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSSを適用
load_css()

# --- ★★★ここからが大きな変更点★★★ ---
# --- ▼ 戻るボタンの配置 (メインコンテンツの左上) ▼ ---
# st.columnsを使って、左端に配置する
col_back, _ = st.columns([0.15, 0.85]) # ボタン用に狭いカラムを確保
with col_back:
    # `st.page_link` を使用すると、直接ページに遷移できてより確実です。
    st.page_link("tokusi_app.py", label="« TOPページに戻る", icon="🏠")
# --- ▲ 戻るボタンの配置 ▲ ---

# データをキャッシュする関数
@st.cache_data(ttl=600) # 10分間データをキャッシュしてAPIの負荷を減らす
def load_guidance_data(_sheets_service, spreadsheet_id):
    try:
        sheet_data = _sheets_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range="シート2!A1:V"
        ).execute().get('values', [])
        
        headers = [h.strip() for h in sheet_data[0]]
        data_map = {key: {} for key in headers}
        for row in sheet_data[1:]:
            if len(row) > 21 and row[21].isdigit():
                age_step = int(row[21])
                for j, key in enumerate(headers):
                    if j < len(row):
                        data_map[key][age_step] = row[j]
        return data_map
    except Exception as e:
        st.error(f"発達段階表データの読み込み中にエラーが発生しました: {e}")
        return None
# --- Google API関連のセットアップ ---
try:
    # RenderのSecret Filesからサービスアカウントキーをファイルとして読み込む
    # Secret Filesは通常 /etc/secrets/ ディレクトリにマウントされる
    secret_file_path = "/etc/secrets/GOOGLE_SHEETS_CREDENTIALS"

    # ▼ ここからが、変更（追加）する部分です ▼
    if not os.path.exists(secret_file_path):
        # ファイルが見つからない場合に、エラーメッセージをStreamlitアプリ上に表示し、処理を停止します。
        st.error(f"エラー: Secret file not found at {secret_file_path}. RenderのSecret Files設定を確認してください。")
        raise FileNotFoundError(f"Secret file not found at {secret_file_path}. Please check Render Secret Files configuration.")
    
    with open(secret_file_path, "r") as f:
        file_content = f.read() # JSON文字列として読み込む
        # 読み込んだファイルの先頭100文字をStreamlitアプリ上に表示します。
        st.info(f"Secret file '{secret_file_path}' を読み込みました。内容の先頭100文字: {file_content[:100]}...") 
        
        try:
            google_credentials_info = json.loads(file_content) # JSON文字列をパース
            # JSONとして正常にパースできたことをStreamlitアプリ上に表示します。
            st.info("Secret fileの内容をJSONとして正常にパースできました。")
        except json.JSONDecodeError as json_e:
            # JSONパースエラーが発生した場合、エラーメッセージをStreamlitアプリ上に表示し、処理を停止します。
            st.error(f"エラー: Secret fileの内容が不正なJSONです: {json_e}")
            raise json_e # 例外を再発生させて、外側のtry-exceptで捕捉させます

    # JSONからGoogle認証情報を構築します。
    credentials = Credentials.from_service_account_info(
        google_credentials_info,
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    # 認証情報構築を試みていることをStreamlitアプリ上に表示します。
    st.info("Google認証情報の構築を試みています...") 
    
    sheets_service = build('sheets', 'v4', credentials=credentials)
    drive_service = build('drive', 'v3', credentials=credentials)
    
    # スプレッドシートIDは変更なし
    SPREADSHEET_ID = "1yXSXSjYBaV2jt2BNO638Y2YZ6U7rdOCv5ScozlFq_EE"
    
    # 発達段階の目安データを読み込む
    guidance_map = load_guidance_data(sheets_service, SPREADSHEET_ID)
    # 全ての処理が成功した場合に、成功メッセージをStreamlitアプリ上に表示します。
    st.success("Google API認証およびデータ読み込みに成功しました。") 

# ▲ ここまでが、変更（追加）する部分です ▲

except HttpError as e:
    # Google API呼び出し中にHTTPエラーが発生した場合
    st.error(f"Google API呼び出し中にHTTPエラーが発生しました: {e.content.decode()}")
    st.stop()
except Exception as e:
    # その他の予期せぬエラーが発生した場合
    st.error(f"Google APIの認証またはデータ読み込みでエラーが発生しました: {e}")
    st.stop()



st.title("📊 発達チャート作成")
st.write("お子さんの発達段階を選択し、現在の状態と次のステップをまとめたチャートを作成・保存します。")

# --- UIの定義 ---
st.header("発達段階の入力")
st.info("各項目の**「▼ 目安を見る」**を開いて内容を確認しながら、現在の発達段階を選択してください。")

categories = ["認知力・操作", "認知力・注意力", "集団参加", "生活動作", "言語理解", "表出言語", "記憶", "読字", "書字", "粗大運動", "微細運動","数の概念"]
options = ["0〜3ヶ月", "3〜6ヶ月", "6〜9ヶ月", "9〜12ヶ月", "12～18ヶ月", "18～24ヶ月", "2～3歳", "3～4歳", "4～5歳", "5～6歳", "6～7歳", "7歳以上"]
age_categories_map = {text: i + 1 for i, text in enumerate(options)}

with st.form("chart_form"):
    selected_options = {}
    cols = st.columns(3)
    for i, category in enumerate(categories):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"**{category}**")
                selected_options[category] = st.radio(
                    f"{category}の選択肢:", options, key=f"radio_{category}", label_visibility="collapsed"
                )

                # ★★★ここが新しい機能！★★★
                with st.expander("▼ 目安を見る"):
                    if guidance_map and category in guidance_map:
                        for age_text, age_step in age_categories_map.items():
                            description = guidance_map[category].get(age_step, "（記載なし）")
                            st.markdown(f"**{age_text}:** {description}")
                    else:
                        st.write("このカテゴリの目安データはありません。")
    
    submitted = st.form_submit_button("📊 チャートを作成して書き込む", use_container_width=True, type="primary")

# --- 処理と結果表示 ---
if submitted:
    with st.spinner('スプレッドシートにデータを書き込み、チャートを更新しています... しばらくお待ちください。'):
        try:
            # (書き込みロジックは元のコードと同じでOK)
            sheet_name = "シート1"
            # 1. 各カテゴリと選択肢をスプレッドシートに書き込む
            values_to_write = [[cat, '', opt] for cat, opt in selected_options.items()]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID, range=f"{sheet_name}!A3:C14",
                valueInputOption="RAW", body={"values": values_to_write}
            ).execute()

            # 2. 年齢カテゴリを数値にマッピングし、B列を更新
            age_categories = { "0〜3ヶ月": 1, "3〜6ヶ月": 2, "6〜9ヶ月": 3, "9〜12ヶ月": 4, "12～18ヶ月": 5, "18～24ヶ月": 6, "2～3歳": 7, "3～4歳": 8, "4～5歳": 9, "5～6歳": 10, "6～7歳": 11, "7歳以上": 12 }
            converted_values = [[age_categories.get(opt, "")] for opt in selected_options.values()]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID, range=f"{sheet_name}!B3:B14",
                valueInputOption="RAW", body={"values": converted_values}
            ).execute()

            # 3. A3:C14の内容をA19:C30にコピー
            sheet1_data = sheets_service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID, range=f"{sheet_name}!A3:C14"
            ).execute().get('values', [])
            sheets_service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID, range=f"{sheet_name}!A19:C30",
                valueInputOption="RAW", body={"values": sheet1_data}
            ).execute()
            
            # 4. B19:B30の段階を+1（最大12）
            updated_b_values = [[min(12, int(row[1]) + 1) if len(row) > 1 and row[1].isdigit() else ""] for row in sheet1_data]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID, range=f"{sheet_name}!B19:B30",
                valueInputOption="RAW", body={"values": updated_b_values}
            ).execute()

            # 5. C19:C30を更新
            b_to_c_mapping = {v: k for k, v in age_categories.items()}
            updated_c_values = [[b_to_c_mapping.get(b[0], "該当なし")] for b in updated_b_values]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID, range=f"{sheet_name}!C19:C30",
                valueInputOption="RAW", body={"values": updated_c_values}
            ).execute()

            # 7. D3:D14とD19:D30を更新 (guidance_mapを再利用)
            category_names = [row[0].strip() for row in sheet1_data]
            results_d3 = [[guidance_map.get(cat, {}).get(int(age[0]), "該当なし")] for cat, age in zip(category_names, converted_values) if age and age[0]]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID, range=f"{sheet_name}!D3:D14",
                valueInputOption="RAW", body={"values": results_d3}
            ).execute()

            results_d19 = [[guidance_map.get(cat, {}).get(b[0], "該当なし")] for cat, b in zip(category_names, updated_b_values) if b and b[0]]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID, range=f"{sheet_name}!D19:D30",
                valueInputOption="RAW", body={"values": results_d19}
            ).execute()
            # ...元のロジックここまで...

            st.success("✅ スプレッドシートへの書き込みとチャートの更新が完了しました！")
            st.session_state.chart_created = True # 結果表示用のフラグ

        except HttpError as e:
            st.error(f"スプレッドシートへのアクセス中にエラーが発生しました: {e.content.decode()}")
            st.session_state.chart_created = False
        except Exception as e:
            st.error(f"書き込み中に予期せぬエラーが発生しました: {e}")
            st.session_state.chart_created = False

# チャート作成が成功した場合のみ結果表示エリアを表示
if st.session_state.get('chart_created', False):
    st.markdown('<hr class="footer-hr">', unsafe_allow_html=True)
    st.header("作成したチャートの確認と保存")

    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            sheet_gid = "0"
            spreadsheet_url_chart = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid={sheet_gid}"
            st.link_button("🌐 スプレッドシートでチャートを確認", spreadsheet_url_chart, use_container_width=True)
        with col2:
            if st.button("💾 Excel形式でダウンロード", use_container_width=True):
                try:
                    with st.spinner("Excelファイルを生成しています..."):
                        request = drive_service.files().export_media(fileId=SPREADSHEET_ID, mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                        file_data = io.BytesIO()
                        downloader = MediaIoBaseDownload(file_data, request)
                        done = False
                        while not done: status, done = downloader.next_chunk()
                        file_data.seek(0)
                        st.session_state.excel_data = file_data.getvalue()
                except Exception as e:
                    st.error(f"Excelエクスポート中にエラーが発生しました: {e}")

        if 'excel_data' in st.session_state and st.session_state.excel_data:
            st.download_button(
                label="🔽 ダウンロード準備完了 (クリックして保存)",
                data=st.session_state.excel_data,
                file_name="hattatsu_chart.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary"
            )

st.markdown('<hr class="footer-hr">', unsafe_allow_html=True)
st.header("📈 成長傾向の分析")
with st.container(border=True):
    st.markdown("これまでの発達チャートデータから成長グラフを作成したい場合は、以下のツールをご利用ください。")
    st.page_link("https://bunnsekiexcel-edeeuzkkntxmhdptk54v2t.streamlit.app/", label="発達段階の成長傾向分析ツールへ", icon="🔗")