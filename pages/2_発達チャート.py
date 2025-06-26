import streamlit as st
import io
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
# --- ▼ 共通CSSの読み込み ▼ ---
def load_css():
    """カスタムCSSを読み込む関数"""
    css = """
    <style>
        /* --- 背景画像の設定 --- */
        /* ご用意された画像のURLを下の 'url(...)' 内に貼り付けてください */
        /* 例: url("https://i.imgur.com/your_image.jpg"); */
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

        /* --- 全体のフォント --- */
        html, body, [class*="st-"] {
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
        }

        /* --- 見出しのスタイル --- */
        h1 {
            color: #2c3e50; /* ダークブルー */
            text-align: center;
            padding-bottom: 20px;
            font-weight: bold;
        }
        h2 {
            color: #34495e; /* 少し明るいダークブルー */
            border-left: 6px solid #8A2BE2; /* 紫のアクセント */
            padding-left: 12px;
            margin-top: 40px;
        }
        h3 {
            color: #34495e;
            border-bottom: 2px solid #4a90e2; /* 青のアクセント */
            padding-bottom: 8px;
            margin-top: 30px;
        }

        /* --- カードデザイン (st.container(border=True)のスタイル) --- */
        div[data-testid="stVerticalBlock"] div.st-emotion-cache-1r6slb0 {
            background-color: rgba(255, 255, 255, 0.95);
            border: 1px solid #e0e0e0;
            border-radius: 15px;
            padding: 1.5em 1.5em;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
            transition: box-shadow 0.3s ease-in-out, transform 0.3s ease-in-out;
            margin-bottom: 20px; /* カード間の余白 */
        }
        div[data-testid="stVerticalBlock"] div.st-emotion-cache-1r6slb0:hover {
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
        /* Primaryボタン */
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
        .st-emotion-cache-1wivap1 { /* st.infoのコンテナ */
             background-color: rgba(232, 245, 253, 0.7); /* 淡い青 */
             border-left: 5px solid #4a90e2;
             border-radius: 8px;
        }

        /* --- フッターの区切り線 --- */
        .footer-hr {
            border: none;
            height: 3px;
            background: linear-gradient(to right, #4a90e2, #8A2BE2);
            margin-top: 40px;
            margin-bottom: 20px;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
# --- ▲ 共通CSSの読み込み ▲ ---
st.set_page_config(page_title="発達チャート作成", page_icon="📊", layout="wide")

st.title("📊 発達チャート作成")
st.write("お子さんの発達段階を選択し、現在の状態と次のステップをまとめたチャートを作成・保存します。")

# --- Google API関連のセットアップ ---
try:
    credentials = Credentials.from_service_account_info(
        st.secrets["google_credentials"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )
    sheets_service = build('sheets', 'v4', credentials=credentials)
    drive_service = build('drive', 'v3', credentials=credentials)
    SPREADSHEET_ID = "1yXSXSjYBaV2jt2BNO638Y2YZ6U7rdOCv5ScozlFq_EE"
except (KeyError, FileNotFoundError):
    st.error("GCPの認証情報が設定されていません。`st.secrets`に`google_credentials`を設定してください。")
    st.stop()
except Exception as e:
    st.error(f"Google APIの認証中に予期せぬエラーが発生しました: {e}")
    st.stop()

# --- ここからUIの定義 ---
st.info("まず、各項目の現在の発達段階を下の選択肢から選んでください。")

# カテゴリと選択肢
categories = ["認知力・操作", "認知力・注意力", "集団参加", "生活動作", "言語理解", "表出言語", "記憶", "読字", "書字", "粗大運動", "微細運動","数の概念"]
options = ["0〜3ヶ月", "3〜6ヶ月", "6〜9ヶ月", "9〜12ヶ月", "12～18ヶ月", "18～24ヶ月", "2～3歳", "3～4歳", "4～5歳", "5～6歳", "6～7歳", "7歳以上"]

# フォームを使って入力をグループ化
with st.form("chart_form"):
    selected_options = {}
    # 3列に分けてラジオボタンを配置
    cols = st.columns(3)
    for i, category in enumerate(categories):
        with cols[i % 3]:
            st.subheader(category)
            selected_options[category] = st.radio(
                f"{category}の選択肢:", options, key=f"radio_{category}", label_visibility="collapsed"
            )

    submitted = st.form_submit_button("📊 チャートを作成して書き込む", use_container_width=True, type="primary")

if submitted:
    with st.spinner('スプレッドシートにデータを書き込み、チャートを更新しています... しばらくお待ちください。'):
        try:
            # --- 元のコードの書き込みロジックをここに移植 ---
            # (長いですが、元のコードのロジックをそのまま関数化せずに持ってきています)
            sheet_name = "シート1"
            
            # 1. 各カテゴリと選択肢をスプレッドシートに書き込む
            values_to_write = []
            for cat, opt in selected_options.items():
                values_to_write.append([cat, '', opt]) # B列は後で更新

            sheets_service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=f"{sheet_name}!A3:C14",
                valueInputOption="RAW",
                body={"values": values_to_write}
            ).execute()

            # 2. 年齢カテゴリを数値にマッピングし、B列を更新
            age_categories = {
                "0〜3ヶ月": 1, "3〜6ヶ月": 2, "6〜9ヶ月": 3, "9〜12ヶ月": 4,
                "12～18ヶ月": 5, "18～24ヶ月": 6, "2～3歳": 7, "3～4歳": 8,
                "4～5歳": 9, "5～6歳": 10, "6～7歳": 11, "7歳以上": 12
            }
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

            # 6. シート2のデータを取得してマッピングを作成
            sheet2_data = sheets_service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID, range="シート2!A1:V"
            ).execute().get('values', [])
            headers = [h.strip() for h in sheet2_data[0]]
            data_map = {key: {} for key in headers}
            for row in sheet2_data[1:]:
                if len(row) > 21 and row[21].isdigit():
                    age_step = int(row[21])
                    for j, key in enumerate(headers):
                        if j < len(row):
                            data_map[key][age_step] = row[j]
            
            # 7. D3:D14とD19:D30を更新
            category_names = [row[0].strip() for row in sheet1_data]
            
            # D3:D14
            results_d3 = [[data_map.get(cat, {}).get(int(age[0]), "該当なし")] for cat, age in zip(category_names, converted_values) if age and age[0]]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID, range=f"{sheet_name}!D3:D14",
                valueInputOption="RAW", body={"values": results_d3}
            ).execute()

            # D19:D30
            results_d19 = [[data_map.get(cat, {}).get(b[0], "該当なし")] for cat, b in zip(category_names, updated_b_values) if b and b[0]]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID, range=f"{sheet_name}!D19:D30",
                valueInputOption="RAW", body={"values": results_d19}
            ).execute()

            st.success("✅ スプレッドシートへの書き込みとチャートの更新が完了しました！")
            st.info("下のボタンから結果の確認とダウンロードができます。")

        except HttpError as e:
            st.error(f"スプレッドシートへのアクセス中にエラーが発生しました: {e.content.decode()}")
        except Exception as e:
            st.error(f"書き込み中に予期せぬエラーが発生しました: {e}")

st.markdown("---")
st.subheader("作成したチャートの確認と保存")

col1, col2, col3 = st.columns([1,1,2])

with col1:
    # スプレッドシートへのリンク
    sheet_gid = "0"
    spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid={sheet_gid}"
    st.link_button("🌐 スプレッドシートで確認", spreadsheet_url, use_container_width=True)

with col2:
    # Excelダウンロード機能
    if st.button("💾 Excel形式でダウンロード", use_container_width=True):
        try:
            with st.spinner("Excelファイルを生成しています..."):
                request = drive_service.files().export_media(
                    fileId=SPREADSHEET_ID,
                    mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                file_data = io.BytesIO()
                downloader = MediaIoBaseDownload(file_data, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                file_data.seek(0)
                st.session_state.excel_data = file_data.getvalue()

        except HttpError as e:
            st.error(f"Excelのエクスポート中にエラーが発生しました: {e.content.decode()}")
        except Exception as e:
            st.error(f"Excelダウンロード準備中に予期せぬエラーが発生しました: {e}")

if 'excel_data' in st.session_state and st.session_state.excel_data:
    st.download_button(
        label="🔽 ダウンロード準備完了",
        data=st.session_state.excel_data,
        file_name="hattatsu_chart.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        key="download_excel_final"
    )

with col3:
    st.markdown("[発達段階表](https://docs.google.com/spreadsheets/d/1yXSXSjYBaV2jt2BNO638Y2YZ6U7rdOCv5ScozlFq_EE/edit#gid=643912489)で基準を確認できます。")


st.markdown("---")
st.subheader("📈 成長傾向の分析")
st.markdown("これまでの発達チャートデータから成長グラフを作成したい場合は、以下のツールをご利用ください。")
st.page_link("https://bunnsekiexcel-edeeuzkkntxmhdptk54v2t.streamlit.app/", label="発達段階の成長傾向分析ツール", icon="🔗")