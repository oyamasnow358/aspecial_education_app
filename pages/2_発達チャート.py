import streamlit as st
import io
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
import os

# --- ▼ 共通CSSの読み込み ▼ ---
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

# --- ▼ 戻るボタンの配置 (メインコンテンツの左上) ▼ ---
col_back, _ = st.columns([0.15, 0.85]) 
with col_back:
    st.page_link("tokusi_app.py", label="« TOPページに戻る", icon="🏠")
# --- ▲ 戻るボタンの配置 ▲ ---

# データをキャッシュする関数
@st.cache_data(ttl=600) # 10分間データをキャッシュしてAPIの負荷を減らす
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
            elif len(row) > 21: # データはあるがAge Stepが不正な場合
                 st.warning(f"シート '{sheet_name}' の行 {sheet_data.index(row) + 2} に無効なAge Stepデータが検出されました。スキップします。")
            
        return data_map
    except Exception as e:
        st.error(f"発達段階表データ (シート: {sheet_name}) の読み込み中にエラーが発生しました: {e}")
        return None

# --- Google API関連のセットアップ ---
sheets_service = None
drive_service = None
SPREADSHEET_ID_UNDER7 = "1yXSXSjYBaV2jt2BNO638Y2YZ6U7rdOCv5ScozlFq_EE" # 既存の7歳未満用スプレッドシートID
# ★★★ ここに8歳以上用の新しいスプレッドシートIDを入力してください ★★★
SPREADSHEET_ID_OVER7 = "13M6lz6CFmGdZ1skJRp44TLm1DR1A4FvxdZdwaJjPJnQ" # 例: "1abcdefghijklmnopqrstuvwxyzABCDEFG"

try:
    secret_file_path = "/etc/secrets/GOOGLE_SHEETS_CREDENTIALS"

    if not os.path.exists(secret_file_path):
        st.error(f"エラー: Secret file not found at {secret_file_path}. RenderのSecret Files設定を確認してください。")
        raise FileNotFoundError(f"Secret file not found at {secret_file_path}. Please check Render Secret Files configuration.")
    
    with open(secret_file_path, "r") as f:
        file_content = f.read() 
        try:
            google_credentials_info = json.loads(file_content) 
        except json.JSONDecodeError as json_e:
            st.error(f"エラー: Secret fileの内容が不正なJSONです: {json_e}")
            raise json_e 

    credentials = Credentials.from_service_account_info(
        google_credentials_info,
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    
    sheets_service = build('sheets', 'v4', credentials=credentials)
    drive_service = build('drive', 'v3', credentials=credentials)
    
    # 7歳未満用と7歳以上用の発達段階の目安データをそれぞれ読み込む
    # 7歳未満用は「シート2」を参照
    guidance_map_under7 = load_guidance_data(sheets_service, SPREADSHEET_ID_UNDER7, "シート2")
    # 7歳以上用は「シート3」を参照 (新規作成)
    guidance_map_over7 = load_guidance_data(sheets_service, SPREADSHEET_ID_OVER7, "シート3")

    st.success("プログラムは正常に認証情報を構築、Google API認証およびデータ読み込みに成功しました。") 

except HttpError as e:
    st.error(f"Google API呼び出し中にHTTPエラーが発生しました: {e.content.decode()}")
    st.stop()
except Exception as e:
    st.error(f"Google APIの認証またはデータ読み込みでエラーが発生しました: {e}")
    st.stop()


st.title("📊 発達チャート作成")
st.write("お子さんの発達段階を選択し、現在の状態と次のステップをまとめたチャートを作成・保存します。")

# --- 発達段階表の切り替えボタン ---
st.header("表示する発達段階表の選択")
col_under7, col_over7 = st.columns(2)

if 'display_mode' not in st.session_state:
    st.session_state.display_mode = "under7" # デフォルトは7歳未満用

with col_under7:
    if st.button("発達年齢 7歳以下用を表示", use_container_width=True, type="primary" if st.session_state.display_mode == "under7" else "secondary"):
        st.session_state.display_mode = "under7"
with col_over7:
    if st.button("発達年齢 8歳以上用を表示", use_container_width=True, type="primary" if st.session_state.display_mode == "over7" else "secondary"):
        st.session_state.display_mode = "over7"

st.info(f"現在、**{'7歳以下用' if st.session_state.display_mode == 'under7' else '8歳以上用'}**の発達段階表が表示されています。")

# --- UIの定義 ---
st.header("発達段階の入力")
st.info("各項目の**「▼ 目安を見る」**を開いて内容を確認しながら、現在の発達段階を選択してください。")

if st.session_state.display_mode == "under7":
    current_spreadsheet_id = SPREADSHEET_ID_UNDER7
    current_guidance_map = guidance_map_under7
    categories = ["認知力・操作", "認知力・注意力", "集団参加", "生活動作", "言語理解", "表出言語", "記憶", "読字", "書字", "粗大運動", "微細運動","数の概念"]
    options = ["0〜3ヶ月", "3〜6ヶ月", "6〜9ヶ月", "9〜12ヶ月", "12～18ヶ月", "18～24ヶ月", "2～3歳", "3～4歳", "4～5歳", "5～6歳", "6～7歳"]
    # 7歳未満用の age_categories_map は 7歳以上 が含まれない
    age_categories_map = {text: i + 1 for i, text in enumerate(options)}
    sheet_to_write_data = "シート1" # 7歳未満用の書き込み先シート
    sheet_to_read_guidance = "シート2" # 7歳未満用の目安データシート
else: # "over7"
    current_spreadsheet_id = SPREADSHEET_ID_OVER7
    current_guidance_map = guidance_map_over7
    # 7歳以上用のカテゴリとオプション (例として仮で設定。実際はスプレッドシートに合わせて変更)
    categories = ["自己管理スキル", "行動調整スキル", "社会的コミュニケーション", "協働スキル", "実用リテラシー", "実用数学", "健康・安全スキル", "情報活用スキル", "地域利用・社会参加スキル", "進路・職業スキル"]
    options = ["8〜10歳", "10〜12歳", "12～14歳", "14〜16歳", "16歳以上"]
    age_categories_map = {text: i + 1 for i, text in enumerate(options)}
    sheet_to_write_data = "シート1" # 7歳以上用の書き込み先シート (こちらも「シート1」を使用)
    sheet_to_read_guidance = "シート3" # 7歳以上用の目安データシート

with st.form("chart_form"):
    selected_options = {}
    cols = st.columns(3)
    for i, category in enumerate(categories):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"**{category}**")
                # セッションステートから前回の選択値を取得（異なるカテゴリセットではリセットされる）
                default_index = options.index(st.session_state.get(f"radio_{category}_{st.session_state.display_mode}", options[0]))
                selected_options[category] = st.radio(
                    f"{category}の選択肢:", options, key=f"radio_{category}_{st.session_state.display_mode}", 
                    label_visibility="collapsed", index=default_index
                )

                with st.expander("▼ 目安を見る"):
                    if current_guidance_map and category in current_guidance_map:
                        for age_text, age_step in age_categories_map.items():
                            description = current_guidance_map[category].get(age_step, "（記載なし）")
                            st.markdown(f"**{age_text}:** {description}")
                    else:
                        st.write("このカテゴリの目安データはありません。")
    
    submitted = st.form_submit_button("📊 チャートを作成して書き込む", use_container_width=True, type="primary")

# --- 処理と結果表示 ---
if submitted:
    with st.spinner('スプレッドシートにデータを書き込み、チャートを更新しています... しばらくお待ちください。'):
        try:
            # 選択されたスプレッドシートIDとシート名を使用
            # 既存のシート1に書き込むのは変わらない
            
            # 1. 各カテゴリと選択肢をスプレッドシートに書き込む
            values_to_write = [[cat, '', opt] for cat, opt in selected_options.items()]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=current_spreadsheet_id, range=f"{sheet_to_write_data}!A3:C14",
                valueInputOption="RAW", body={"values": values_to_write}
            ).execute()

            # 2. 年齢カテゴリを数値にマッピングし、B列を更新
            # age_categories_map を現在のオプションに対応したものに置き換える
            converted_values = [[age_categories_map.get(opt, "")] for opt in selected_options.values()]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=current_spreadsheet_id, range=f"{sheet_to_write_data}!B3:B14",
                valueInputOption="RAW", body={"values": converted_values}
            ).execute()

            # 3. A3:C14の内容をA19:C30にコピー
            sheet_data_current = sheets_service.spreadsheets().values().get(
                spreadsheetId=current_spreadsheet_id, range=f"{sheet_to_write_data}!A3:C14"
            ).execute().get('values', [])
            sheets_service.spreadsheets().values().update(
                spreadsheetId=current_spreadsheet_id, range=f"{sheet_to_write_data}!A19:C30",
                valueInputOption="RAW", body={"values": sheet_data_current}
            ).execute()
            
            # 4. B19:B30の段階を+1（最大値はage_categories_mapのサイズ）
            max_age_step = len(options)
            updated_b_values = [[min(max_age_step, int(row[1]) + 1) if len(row) > 1 and str(row[1]).isdigit() else ""] for row in sheet_data_current]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=current_spreadsheet_id, range=f"{sheet_to_write_data}!B19:B30",
                valueInputOption="RAW", body={"values": updated_b_values}
            ).execute()

            # 5. C19:C30を更新 (数値からテキストに戻す)
            # 逆マッピングを作成 (age_stepからage_textへ)
            b_to_c_mapping = {v: k for k, v in age_categories_map.items()}
            updated_c_values = [[b_to_c_mapping.get(b[0], "該当なし")] for b in updated_b_values]
            sheets_service.spreadsheets().values().update(
                spreadsheetId=current_spreadsheet_id, range=f"{sheet_to_write_data}!C19:C30",
                valueInputOption="RAW", body={"values": updated_c_values}
            ).execute()

            # 7. D3:D14とD19:D30を更新 (current_guidance_mapを再利用)
            category_names = [row[0].strip() for row in sheet_data_current if row] # 空行対策
            
            results_d3 = []
            for i, cat in enumerate(category_names):
                if i < len(converted_values) and converted_values[i] and str(converted_values[i][0]).isdigit():
                    results_d3.append([current_guidance_map.get(cat, {}).get(int(converted_values[i][0]), "該当なし")])
                else:
                    results_d3.append(["該当なし"]) # データが不正な場合

            sheets_service.spreadsheets().values().update(
                spreadsheetId=current_spreadsheet_id, range=f"{sheet_to_write_data}!D3:D14",
                valueInputOption="RAW", body={"values": results_d3}
            ).execute()

            results_d19 = []
            for i, cat in enumerate(category_names):
                if i < len(updated_b_values) and updated_b_values[i] and str(updated_b_values[i][0]).isdigit():
                    results_d19.append([current_guidance_map.get(cat, {}).get(updated_b_values[i][0], "該当なし")])
                else:
                    results_d19.append(["該当なし"]) # データが不正な場合

            sheets_service.spreadsheets().values().update(
                spreadsheetId=current_spreadsheet_id, range=f"{sheet_to_write_data}!D19:D30",
                valueInputOption="RAW", body={"values": results_d19}
            ).execute()

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
            # 現在選択されているスプレッドシートのURLを生成
            sheet_gid = "0" # 通常、シート1のGIDは0
            spreadsheet_url_chart = f"https://docs.google.com/spreadsheets/d/{current_spreadsheet_id}/edit#gid={sheet_gid}"
            st.link_button("🌐 スプレッドシートでチャートを確認", spreadsheet_url_chart, use_container_width=True)
        with col2:
            if st.button("💾 Excel形式でダウンロード", use_container_width=True):
                try:
                    with st.spinner("Excelファイルを生成しています..."):
                        request = drive_service.files().export_media(fileId=current_spreadsheet_id, mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
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
                file_name=f"hattatsu_chart_{st.session_state.display_mode}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary"
            )

st.markdown('<hr class="footer-hr">', unsafe_allow_html=True)
st.header("📈 成長傾向の分析")
with st.container(border=True):
    st.markdown("これまでの発達チャートデータから成長グラフを作成したい場合は、以下のツールをご利用ください。")
    # こちらの分析ツールも、7歳以下/7歳以上でスプレッドシートを切り替えられるようにする必要があるかもしれません。
    # 現時点ではリンク先は固定ですが、もし必要であればここも拡張可能です。
    st.page_link("https://bunnsekiexcel-edeeuzkkntxmhdptk54v2t.streamlit.app/", label="発達段階の成長傾向分析ツールへ", icon="🔗")




    