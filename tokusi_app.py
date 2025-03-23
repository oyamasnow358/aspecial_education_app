import streamlit as st
import pandas as pd
import io
import os  # osをインポート
import requests
from PIL import Image
import requests
import json

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from google.cloud import storage
from googleapiclient.http import MediaIoBaseDownload

# 画像のURLを貼る（手動でコピーしたもの）
# 画像のURLを手動で設定（Imgur にアップロードした画像のリンクを使う）
img_dressing = "https://i.imgur.com/t4RLTeG.jpeg"  # 着脱練習の画像
img_eating = "https://i.imgur.com/xyz123.jpg"  # 食事練習の画像
img_sensory = "https://i.imgur.com/789lmn.jpg"  # 感覚統合活動の画像
# 画像データ（指文字）
img_sign_language = "https://i.imgur.com/gqmXyNT.png"  # 画像のファイル名を指定（事前にアップロード）
img_hasizo = "https://imgur.com/FW4CF0E.jpeg"  # 箸ぞー画像のファイル名を指定






# CSVのファイル名
CSV_FILE = "feedback_data.csv"

# CSVからデータを読み込む関数
def load_feedback():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["カテゴリー", "項目", "追加内容"])

# CSVにデータを保存する関数
def save_feedback(data):
    data.to_csv(CSV_FILE, index=False)

# フィードバックデータの読み込み
if "feedback_data" not in st.session_state:
    st.session_state.feedback_data = load_feedback()

# 🔐 ログイン状態を管理する
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False  # 初期状態はログアウト

# アプリの基本構造
st.title("🌟 自立活動の参考指導 🌟")

# メニュー選択
#menu = st.sidebar.selectbox("メニューを選択してください", ["指導支援内容", "フィードバック追加", "フィードバック集計と削除"])
# タブを作成
# ドロップダウンメニューの作成
menu_options = ["指導支援内容", "フィードバック", "発達チャート作成", "特別支援分析法"]
selected_menu = st.selectbox("メニューを選択", menu_options)

if selected_menu == "指導支援内容":
    st.subheader("📚 指導支援内容の参照")
    st.text("１から順番に選択して下さい")

# メニューによって表示を制御
elif selected_menu == "フィードバック追加":
    st.subheader("📝 フィードバック追加(2つの方法から1つを選んで入力)")
    st.markdown("あなたの自立活動、生活指導を教えてください♪")
      # Microsoft Forms の埋め込み
    st.info("方法１   Microsoft foam")
    form_url = "https://forms.office.com/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAMAANa6zUxUQjRFQ1NRUFhJODhKVFMzUkdVVzVCR0JEVS4u&embed=true"
    st.components.v1.iframe(form_url, width=700, height=900)
    st.info("方法２   Google foam")
    google_form_url = "https://docs.google.com/forms/d/1xXzq0vJ9E5FX16CFNoTzg5VAyX6eWsuN8Xl5qEwJFTc/preview"

    st.components.v1.iframe(google_form_url, width=700, height=900)

elif selected_menu == "発達チャート作成":
    st.subheader("📊 発達チャート作成")
    st.text("ここに発達チャート作成アプリのコードを挿入してください。")
    # 別アプリのコードをここにコピー＆ペースト
    # Secrets から認証情報を取得
    credentials = Credentials.from_service_account_info(
        st.secrets["google_credentials"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
    ]
    )
    
    
    # Google Sheets API クライアントを作成
    service = build('sheets', 'v4', credentials=credentials)
    
    # Google Drive API クライアントを作成（ダウンロード時に使用）
    drive_service = build('drive', 'v3', credentials=credentials)
    
    # Google Cloud Storage クライアントを作成（必要なら使用）
    client = storage.Client(credentials=credentials)
    
    # **スプレッドシートのIDをグローバル変数として定義**
    spreadsheet_id = "1yXSXSjYBaV2jt2BNO638Y2YZ6U7rdOCv5ScozlFq_EE"
    
    def write_to_sheets(sheet_name, cell, value):
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!{cell}",
            valueInputOption="RAW",
            body={"values": [[value]]}
        ).execute()
    
    def main():
        st.title("📉発達段階能力チャート作成📈")
        st.info("児童・生徒の発達段階が分からない場合は下の「現在の発達段階を表から確認する」⇒「発達段階表」を順に押して下さい。")
    
    
    
    
    
        if st.button("現在の発達段階を表から確認する"):
         try:
            # 指定したシートのID（例: "0" は通常、最初のシート）
            sheet_gid = "643912489"  # 必要に応じて変更
            
            # スプレッドシートのURLを生成してブラウザで開けるようにする
            spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={sheet_gid}"
            st.markdown(f"[発達段階表]({spreadsheet_url})", unsafe_allow_html=True)
            
         except Exception as e:
            st.error(f"スプレッドシートのリンク生成中にエラーが発生しました: {e}")
    
    
        sheet_name = "シート1"
    
        categories = ["認知力・操作", "認知力・注意力", "集団参加", "生活動作", "言語理解", "表出言語", "記憶", "読字", "書字", "粗大運動", "微細運動","数の概念"]
        options = ["0〜3ヶ月", "3〜6ヶ月", "6〜9ヶ月", "9〜12ヶ月", "12～18ヶ月", "18～24ヶ月", "2～3歳", "3～4歳", "4～5歳", "5～6歳", "6～7歳", "7歳以上"]
        #変更
        selected_options = {}
    
        for index, category in enumerate(categories, start=1):
            st.subheader(category)
            selected_options[category] = st.radio(f"{category}の選択肢を選んでください:", options, key=f"radio_{index}")
    
        st.markdown("""1.各項目の選択が終わりましたら、まず「スプレッドシートに書き込む」を押してください。  
                    2.続いて「スプレッドシートを開く」を押して内容を確認してくだい。  
                    3.Excelでデータを保存したい方は「EXCELを保存」を押してくだい。""")
    
        if st.button("スプレッドシートに書き込む"):
         try:
              # 各カテゴリと選択肢をスプレッドシートに書き込む
              for index, (category, selected_option) in enumerate(selected_options.items(), start=1):
                  write_to_sheets(sheet_name, f"A{index + 2}", category)
                  write_to_sheets(sheet_name, f"C{index + 2}", selected_option)  # C列に発達年齢を記入
          
              # 年齢カテゴリのマッピング
              age_categories = {
                  "0〜3ヶ月": 1, "3〜6ヶ月": 2, "6〜9ヶ月": 3, "9〜12ヶ月": 4,
                  "12～18ヶ月": 5, "18～24ヶ月": 6, "2～3歳": 7, "3～4歳": 8,
                  "4～5歳": 9, "5～6歳": 10, "6～7歳": 11, "7歳以上": 12
              }
          
              # シート1のデータを取得
              sheet1_data = service.spreadsheets().values().get(
                  spreadsheetId=spreadsheet_id,
                  range="シート1!A3:C14"
              ).execute().get('values', [])
          
              # A列（カテゴリ名）とC列（発達年齢）を取得
              category_names = [row[0].strip() for row in sheet1_data]
              age_range = [row[2].strip() for row in sheet1_data]  # C列に発達年齢がある
          
              # 年齢を数値化
              converted_values = [[age_categories.get(age, "")] for age in age_range]
          
              # B3:B14に数値（段階）を設定
              service.spreadsheets().values().update(
                  spreadsheetId=spreadsheet_id,
                  range="シート1!B3:B14",
                  valueInputOption="RAW",
                  body={"values": converted_values}
              ).execute()
          
              # A3:C13をA18:C28にコピー
              sheet1_copy_data = service.spreadsheets().values().get(
                  spreadsheetId=spreadsheet_id,
                  range="シート1!A3:C14"
              ).execute().get('values', [])
              
              # シートの範囲を一度に更新
              service.spreadsheets().values().update(
                  spreadsheetId=spreadsheet_id,
                  range="シート1!A19:C30",
                  valueInputOption="RAW",
                  body={"values": sheet1_copy_data}
              ).execute()
          
              # B19:B30の段階を+1（最大値12を超えない）
              updated_b_values = [[min(12, int(row[1]) + 1) if row[1].isdigit() else ""] for row in sheet1_copy_data]
              service.spreadsheets().values().update(
                  spreadsheetId=spreadsheet_id,
                  range="シート1!B19:B30",
                  valueInputOption="RAW",
                  body={"values": updated_b_values}
              ).execute()
          
              # **🟢 B19:B30の段階データを取得**
              b19_b30_values = service.spreadsheets().values().get(
                  spreadsheetId=spreadsheet_id,
                  range="シート1!B19:B30"
              ).execute().get('values', [])
          
              # **🔵 B列の値（段階）を整数に変換**
              b19_b30_values = [int(row[0]) if row and row[0].isdigit() else None for row in b19_b30_values]
          
              # **🔵 段階に対応する発達年齢を取得**
              b_to_c_mapping = {  # B列の段階をC列の発達年齢に変換
                  1: "0〜3ヶ月", 2: "3〜6ヶ月", 3: "6〜9ヶ月", 4: "9〜12ヶ月",
                  5: "12～18ヶ月", 6: "18～24ヶ月", 7: "2～3歳", 8: "3～4歳",
                  9: "4～5歳", 10: "5～6歳", 11: "6～7歳", 12: "7歳以上"
              }
          
              # **C19:C30に対応する発達年齢をセット**
              updated_c_values = [[b_to_c_mapping.get(b, "該当なし")] for b in b19_b30_values]
          
              # **Google SheetsにC19:C30のデータを更新**
              service.spreadsheets().values().update(
                  spreadsheetId=spreadsheet_id,
                  range="シート1!C19:C30",
                  valueInputOption="RAW",
                  body={"values": updated_c_values}
              ).execute()
          
              # **🟢 シート2のデータを取得**
              sheet2_data = service.spreadsheets().values().get(
                  spreadsheetId=spreadsheet_id,
                  range="シート2!A1:V"
              ).execute().get('values', [])
          
              # **データマッピングを作成**
              headers = [h.strip() for h in sheet2_data[0]]
              data_map = {}  # 🔵 ここで `data_map` を適切に定義
              for row in sheet2_data[1:]:
                  age_step = row[21] if len(row) > 21 else ""
                  if not age_step.isdigit():
                      continue
                  for j, key in enumerate(headers):
                      if key not in data_map:
                          data_map[key] = {}
                      data_map[key][int(age_step)] = row[j]
          
              # **D3:D14にシート2の対応データを設定**
              results = [[data_map.get(category, {}).get(age[0], "該当なし")]
                         for category, age in zip(category_names, converted_values)]
              service.spreadsheets().values().update(
                  spreadsheetId=spreadsheet_id,
                  range="シート1!D3:D14",
                  valueInputOption="RAW",
                  body={"values": results}
              ).execute()
              
    
              # 🟢 **B19:B30の値を取得**
              b19_b30_values = service.spreadsheets().values().get(
                  spreadsheetId=spreadsheet_id,
                  range="シート1!B19:B30"
              ).execute().get('values', [])
              
              # 🟢 **A19:A30のカテゴリを取得**
              a19_a30_values = service.spreadsheets().values().get(
                  spreadsheetId=spreadsheet_id,
                  range="シート1!A19:A30"
              ).execute().get('values', [])
    
    
          
                        # 🔵 **カテゴリと対応する段階（B19:B30）を使ってD19:D30の値を決定**
              new_results = []
              for category_row, stage_row in zip(a19_a30_values, b19_b30_values):
                  category = category_row[0] if category_row else ""  # A列のカテゴリ
                  stage = int(stage_row[0]) if stage_row and stage_row[0].isdigit() else None  # B列の段階
              
                  if stage is not None:
                      result_value = data_map.get(category, {}).get(stage, "該当なし")  # シート2のデータを参照
                  else:
                      result_value = "該当なし"
              
                  new_results.append([result_value])
              
              # **D19:D30に対応する値を更新**
              service.spreadsheets().values().update(
                  spreadsheetId=spreadsheet_id,
                  range="シート1!D19:D30",
                  valueInputOption="RAW",
                  body={"values": new_results}
              ).execute()
          
         except Exception as e:
              st.error(f"エラーが発生しました: {e}")
    
      # ダウンロード機能
        if st.button("スプレッドシートを開く"):
         try:
            # 指定したシートのID（例: "0" は通常、最初のシート）
            sheet_gid = "0"  # 必要に応じて変更
            
            # スプレッドシートのURLを生成してブラウザで開けるようにする
            spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={sheet_gid}"
            st.markdown(f"[スプレッドシートを開く]({spreadsheet_url})", unsafe_allow_html=True)
    
            st.info("スプレッドシートを開いた後に、Excelとして保存できます。")
         except Exception as e:
            st.error(f"スプレッドシートのリンク生成中にエラーが発生しました: {e}")
    
        
    # Excelダウンロード機能
        if st.button("EXCELを保存"):
         try:
            # Google Drive API を使用してスプレッドシートをエクスポート
            request = drive_service.files().export_media(
                fileId=spreadsheet_id,
                mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            file_data = io.BytesIO()
            downloader = MediaIoBaseDownload(file_data, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
    
            file_data.seek(0)
            st.download_button(
                label="PCに結果を保存",
                data=file_data,
                file_name="spreadsheet.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.info("保存EXCELのレーダーチャートは仕様が少し異なります。")
         except Exception as e:
            st.error(f"Excel保存中にエラーが発生しました: {e}")
    
        
         st.subheader("今までの発達チャートから成長グラフを作成する")
         st.markdown("[発達段階の成長傾向分析](https://bunnsekiexcel-edeeuzkkntxmhdptk54v2t.streamlit.app/)")
    
elif selected_menu == "特別支援分析法":
    st.subheader("📈 特別支援分析法")
    st.text("ここに特別支援分析法アプリのコードを挿入してください。")
        # 別アプリのコードをここにコピー＆ペースト
    # 画像のURLを貼る（手動でコピーしたもの）
# 画像のURLを手動で設定（Imgur にアップロードした画像のリンクを使う）
img1 = "https://i.imgur.com/SwjfDft.png"  # 動作法１画像
img2 = "https://i.imgur.com/LqbE9Nf.png"  # 動作法２画像
img3 = "https://i.imgur.com/XLwjXFE.png"  # 動作法３の画像
img4 = "https://i.imgur.com/2MfaBxc.png"  # 動作法４
img5 = "https://i.imgur.com/zheqhdv.png"  #
img6 = "https://i.imgur.com/Hw4PIKo.jpeg"#
img7 = "https://i.imgur.com/vnMHFNE.png"#

# 画像を読み込む（PIL を使用）
#image1 = Image.open("images/生徒1.png")
#image2 = Image.open("images/生徒2.png")
#image3 = Image.open("images/生徒3.png")
#image4 = Image.open("images/生徒4.png")

# タイトル
st.title("特別支援教育サポートアプリ")

# 療法・分析法の一覧
methods = {
    "ABA（応用行動分析）": "pages/aba.md",
    "FBA/PBS（機能的アセスメント/ポジティブ行動支援）": "pages/fba_pbs.md",
    "CBT（認知行動療法）": "pages/cbt.md",
    "ソーシャルスキルトレーニング": "pages/sst.md",
    "感覚統合療法": "pages/sensory_integration.md",
    "PECS（絵カード交換式コミュニケーション）": "pages/pecs.md",
    "動作法": "pages/dousahou.md",
    "TEACCH": "pages/teacch.md",
    "SEL（社会情動的学習）": "pages/sel.md",
    "マインドフルネス": "pages/mindfulness.md",
    "プレイセラピー": "pages/play_therapy.md",
    "アートセラピー": "pages/art_therapy.md",
    "ミュージックセラピー": "pages/music_therapy.md",
    "セルフモニタリング":"pages/self_monitar.md",
    "統計学的分析方法":"pages/toukei.md",
}

# セッションステートを使用して、選択された療法を記憶
if "selected_method" not in st.session_state:
    st.session_state.selected_method = None  # 初期状態はNone

# サイドバーに療法・分析法の一覧
st.sidebar.title("療法・分析法一覧")
selected_method = st.sidebar.radio("選択してください", list(methods.keys()), index=None)

# サイドバーで選択があれば、セッションステートを更新
if selected_method:
    st.session_state.selected_method = selected_method

# メイン画面に実態選択フォーム
st.subheader("児童・生徒の実態を選択してください")

# 実態リスト
student_conditions = {
    "言葉で気持ちを伝えるのが難しい": ["プレイセラピー", "アートセラピー", "PECS（絵カード交換式コミュニケーション）"],
    "感情のコントロールが苦手": ["CBT（認知行動療法）", "SEL（社会情動的学習）", "マインドフルネス"],
    "対人関係が苦手": ["ソーシャルスキルトレーニング", "TEACCH"],
    "学習の集中が続かない": ["ABA（応用行動分析）", "感覚統合療法", "セルフモニタリング"],
    "行動の問題がある": ["FBA/PBS（機能的アセスメント/ポジティブ行動支援）", "ABA（応用行動分析）"],
    "身体に課題がある": ["動作法"],
}

# 実態を選択
condition = st.selectbox("実態を選んでください", list(student_conditions.keys()))

# 適した療法を表示
st.write("この実態に適した療法・分析法:")

# 選択肢ごとにボタンを作成
for method in student_conditions[condition]:
    if method in methods:  # methods に存在するかチェック
        if st.button(method):  # ボタンを押したらサイドバーで選択したのと同じ状態にする
            st.session_state.selected_method = method
            st.rerun()  # ✅ 最新のStreamlitではこちらを使う
    else:
        st.error(f"{method} のページが見つかりません")

# 説明ページの表示
if st.session_state.selected_method:
    st.markdown(f"### {st.session_state.selected_method}")
    file_path = methods.get(st.session_state.selected_method)

    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                st.markdown(file.read(), unsafe_allow_html=True)
        except FileNotFoundError:
            st.error(f"{st.session_state.selected_method} の説明ページが見つかりません（ファイルが存在しません）")
    else:
        st.error(f"{st.session_state.selected_method} の説明ページが見つかりません（辞書に登録されていません）")

    # **CBT（認知行動療法）なら画像を表示**
    if st.session_state.selected_method == "CBT（認知行動療法）":
        #st.image("images/cbt_diagram.png", caption="認知行動療法", use_container_width=True)
        st.image(img7, caption="認知行動療法", use_container_width=True) 

    elif st.session_state.selected_method == "PECS（絵カード交換式コミュニケーション）":
          st.image(img6, caption="PECS（絵カード交換式コミュニケーション）", use_container_width=True) 

    elif st.session_state.selected_method == "動作法":
          # 📌 画像1と画像2を横並び
     col1, col2 = st.columns(2)
     with col1:
       #st.image(image1, caption="生徒1", use_container_width=True)
       st.image(img1, caption="生徒1", use_container_width=True)
     with col2:
       #st.image(image2, caption="生徒2", use_container_width=True)
       st.image(img2, caption="生徒2", use_container_width=True)

          # 📌 画像3と画像4を横並び（下段）
     col3, col4 = st.columns(2)
     with col3:
        #st.image(image3, caption="生徒3", use_container_width=True)
        st.image(img3, caption="生徒3", use_container_width=True)
     with col4:
        #st.image(image4, caption="生徒4", use_container_width=True)
        st.image(img4, caption="生徒4", use_container_width=True)
    
    elif st.session_state.selected_method == "マインドフルネス":
          #st.image("images/マインドフルネス1.png", caption="マインドフルネス", use_container_width=True)
          st.image(img5, caption="マインドフルネス", use_container_width=True)
          

     # **FBA/PBS（機能的行動評価/ポジティブ行動支援）の場合、Word・Excelダウンロードを追加**
    elif st.session_state.selected_method == "FBA/PBS（機能的アセスメント/ポジティブ行動支援）":
        st.markdown("---")  # 区切り線
        st.subheader("📂 参考データのダウンロード")

        # Wordファイルのダウンロード
        word_file_path = "data/機能的アセスメントについて.docx"
        with open(word_file_path, "rb") as f:
            st.download_button(
                label="📄 ①機能的アセスメントについてをダウンロード",
                data=f,
                file_name="機能的アセスメントについて.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        # Wordファイルのダウンロード
        word_file_path = "data/ワークシート１　基礎情報.doc"
        with open(word_file_path, "rb") as f:
            st.download_button(
                label="📄 ②ワークシート１　基礎情報をダウンロード",
                data=f,
                file_name="ワークシート１　基礎情報.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        # Excelファイルのダウンロード
        excel_file_path = "data/ワークシート２　MAS機能分析.xls"
        with open(excel_file_path, "rb") as f:
            st.download_button(
                label="📊 ③ワークシート２　MAS機能分析.xlsをダウンロード",
                data=f,
                file_name="ワークシート２　MAS機能分析.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        # Wordファイルのダウンロード
        word_file_path = "data/ワークシート３　行動問題の特徴.doc"
        with open(word_file_path, "rb") as f:
            st.download_button(
                label="📄 ④ワークシート３　行動問題の特徴をダウンロード",
                data=f,
                file_name="ワークシート３　行動問題の特徴.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ) 
        # Wordファイルのダウンロード
        word_file_path = "data/ワークシート４　ライフスタイルの特徴.doc"
        with open(word_file_path, "rb") as f:
            st.download_button(
                label="📄 ⑤ワークシート４　ライフスタイルの特徴をダウンロード",
                data=f,
                file_name="ワークシート４　ライフスタイルの特徴.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        # Wordファイルのダウンロード
        word_file_path = "data/ワークシート５　行動の記録スキャッターブロット.doc"
        with open(word_file_path, "rb") as f:
            st.download_button(
                label="📄 ⑥ワークシート５　行動の記録スキャッターブロットをダウンロード",
                data=f,
                file_name="ワークシート５　行動の記録スキャッターブロット.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        # Wordファイルのダウンロード
        word_file_path = "data/ワークシート６　１日の記録.doc"
        with open(word_file_path, "rb") as f:
            st.download_button(
                label="📄 ⑦ワークシート６　１日の記録をダウンロード",
                data=f,
                file_name="ワークシート６　１日の記録.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        # Wordファイルのダウンロード
        word_file_path = "data/ワークシート７　頭の中のアセスメント.doc"
        with open(word_file_path, "rb") as f:
            st.download_button(
                label="📄 ⑧ワークシート７　頭の中のアセスメント.docをダウンロード",
                data=f,
                file_name="ワークシート７　頭の中のアセスメント.doc.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        # Wordファイルのダウンロード
        word_file_path = "data/ワークシート８　ＡＢＣ分析.doc"
        with open(word_file_path, "rb") as f:
            st.download_button(
                label="📄 ⑨ワークシート８　ＡＢＣ分析をダウンロード",
                data=f,
                file_name="ワークシート８　ＡＢＣ分析.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

        # **出典情報を追加**
        st.subheader("📖 出典情報")
        st.markdown("""
        - **参考文献:** Durand, V. M. (1990). Severe behavior problems: A functional communication training approach. Guilford Press..
        - **Webサイト:** [機能的アセスメント](http://www.kei-ogasawara.com/support/assessment/)
        """)

        st.markdown("---")  # 区切り線
        st.subheader("📂 機能的アセスメント分析")
        st.markdown("""
        [機能的行動評価分析ツール](https://kinoukoudou-ptfpnkq3uqgaorabcyzgf2.streamlit.app/)
        """)

         # **応用行動分析ツール**
    elif st.session_state.selected_method == "ABA（応用行動分析）":
        st.markdown("---")  # 区切り線
        st.subheader("📂 簡単分析ツール")
        st.markdown("""
        [応用行動分析ツール](https://abaapppy-k7um2qki5kggexf8qkfxjc.streamlit.app/)
        """)
         # **統計学的分析方法ツール**
    elif st.session_state.selected_method == "統計学的分析方法":
        st.write("""※以下の分析ツールを気軽に試してみて下さい。初心者でも簡単に使えるようにはしましたが、説明が難しい箇所はあると思います。フォームで意見を入力して頂くか、直接小山にお声かけ下さい。""")
        st.markdown("---")  # 区切り線
        st.subheader("📂 統計学 分析ツール一覧")
        st.markdown("""
        [相関分析](https://soukan-jlhkdhkradbnxssy29aqte.streamlit.app/)
        """)
        st.markdown("""
        [多変量回帰分析](https://kaikiapp-tjtcczfvlg2pyhd9bjxwom.streamlit.app/)
        """)
        st.markdown("""
        [t検定](https://tkentei-flhmnqnq6dti6oyy9xnktr.streamlit.app/)""")
        st.markdown("""
        [ロジスティック回帰分析](https://rojisthik-buklkg5zeh6oj2gno746ix.streamlit.app/)
        """)
        st.markdown("""
        [ノンパラメトリック統計分析](https://nonparametoric-nkk2awu6yv9xutzrjmrsxv.streamlit.app/)
        """)


    #feedback_category = st.selectbox("カテゴリーを選択:", ["日常生活における実態", "障害の種類"])
    #feedback_subcategory = st.selectbox("項目を選択:", ["身辺自立が未熟な生徒","コミュニケーションが苦手な生徒","社会生活スキルが不足している生徒","時間や順序の理解が苦手な生徒","運動能力や感覚に偏りがある生徒","情緒が不安定な生徒","集団活動への参加が難しい生徒", "聴覚障害","視覚障害","ダウン症","自閉スペクトラム症（ASD）","注意・欠如・多動性障害（ADHD）","自閉スペクトラム症（ASD）","学習障害（LD）","発達性協調運動障害（DCD）","四肢・体幹機能障害"])
    #feedback_content = st.text_area("追加するフィードバックを入力してください:")

    #if st.button("フィードバックを保存"):
     #   if feedback_content:
      #      new_feedback = pd.DataFrame([{
       #         "カテゴリー": feedback_category,
        #        "項目": feedback_subcategory,
         #       "追加内容": feedback_content
          #  }])
           # st.session_state.feedback_data = pd.concat([st.session_state.feedback_data, new_feedback], ignore_index=True)
            #save_feedback(st.session_state.feedback_data)  # CSVに保存
            #st.success("フィードバックが保存されました！")
        #else:
         #   st.warning("フィードバック内容を入力してください。")

#elif menu == "フィードバック集計と削除":
    # 🔐 ログイン機能
 #   if not st.session_state.logged_in:
  #      st.subheader("🔑 パスワード認証（管理者専用）")
   #     password_input = st.text_input("パスワードを入力してください", type="password")
    #    correct_password = st.secrets.get("admin_password", "default_password")
#
 #       if st.button("ログイン"):
  #          if password_input == correct_password:
   #             st.session_state.logged_in = True  # ログイン成功！
    #            st.success("認証成功！")
     #           st.experimental_rerun()  # 画面を更新
      #      else:
       #         st.error("パスワードが違います。")
    #else:
     #   st.subheader("📊 フィードバック集計と削除")
        
      #  if st.session_state.feedback_data.empty:
           # st.info("現在、保存されているフィードバックはありません。")
       # else:
        #    st.dataframe(st.session_state.feedback_data)

             # **削除機能**
         #   delete_index = st.number_input("削除する行の番号を入力（1から）", min_value=1, max_value=len(st.session_state.feedback_data), step=1) - 1

          #  if st.button("選択した行を削除"):
           #  st.session_state.feedback_data = st.session_state.feedback_data.drop(delete_index).reset_index(drop=True)
            # save_feedback(st.session_state.feedback_data)
             #st.rerun()  # 最新の状態に更新 # 最新のデータを反映

            # データをCSVとしてダウンロード
        #    st.subheader("📥 フィードバックのダウンロード")
         #   csv = st.session_state.feedback_data.to_csv(index=False, encoding="utf-8-sig") 
          #  st.download_button(
            #    label="CSVファイルをダウンロード",
             #   data=csv.encode("utf-8-sig"),
              #  file_name="feedback.csv",
               # mime="text/csv"
            #)

        # 🔓 ログアウトボタン
      #  if st.button("ログアウト"):
       #     st.session_state.logged_in = False
        #    st.experimental_rerun()

# 指導データ
guidance_data = {
    "日常生活における実態": {
        "身辺自立が未熟な生徒": {
            "衣服の着脱練習": [
                "具体的教材の導入: 実際のボタン付きシャツやファスナーを取り付けたパネル教材を使い、繰り返し練習する。",
                "段階的指導: まずは「袖に手を通す」「ボタンをつまむ」など簡単なステップに分け、一つずつ練習を進める。",
                "視覚支援の活用: 着替えの順序をイラストや写真で示し、見通しを持たせる。",
                "実践的練習: 毎朝の登校後や体育の後など、実際の生活場面での練習を取り入れる。"
            ],
            "食事の練習": [
                "器具選び: 太めで握りやすいスプーンやフォークを使い、持ち方や使い方を教える。",
                "模倣の練習: 教員がゆっくりと動作を見せ、生徒が真似をする形でスプーンの持ち方や口への運び方を学ぶ。",
                "具体的課題設定: 小さな一口サイズの食べ物から始め、達成しやすい目標を設定する。",
                "片付けの練習: 食事後にお皿を所定の場所に運ぶ練習を取り入れる。開始時は手を添えてサポートし、徐々に自立を促す。"
            ],
            "感覚統合活動": [
                "感覚に配慮した布選び: 初めは柔らかく生徒が触りやすい素材を使い、徐々に異なる感触の素材に慣れさせる。",
                "遊びを取り入れた活動: 感触遊び（触覚用スライム、ビーズのプール）や、冷たい・温かい感覚を体験するゲームを実施する。",
                "成功体験を重視: 生徒が触れられる素材や温度に合わせて成功しやすい体験を積ませ、自信を持たせる。 異なる素材の布や玩具を触る活動を取り入れ、感覚過敏を軽減。",
                "トランポリン: トランポリンに立ったり飛んだりすることで、感覚刺激を調整。"
              ],
        },
        
        "コミュニケーションが苦手な生徒": {
            "ピクトグラムや絵カードの活用 (自分の意思や要望をカードで表現する練習。)": [
                "個別にカスタマイズしたカード作成: 生徒の日常生活や好きな物に基づいて、実際の写真や絵を用意。",
                "ルールの反復練習: 例えば、「飲み物が欲しいときは飲み物のカードを見せる」といった場面ごとのルールを繰り返し指導。",
                "応用的な使い方: カードを複数使って「ジュースが欲しい」「トイレに行きたい」など具体的なフレーズを伝えられるようにする。また、依頼する教員の写真カードと要求の絵・写真カードを同時に使って伝えられるようにする。（PECS、コミュニケーションボード）"
              ],
            "リトミック (音楽に合わせて動き、教師や仲間と簡単なやり取りを行う。)": [
                         "個人から集団へ: 初めは教員と1対1で音楽に合わせた動きを練習し、慣れたら徐々に他の生徒と関わる活動を増やす。","簡単な役割設定: 「先生の動きを真似する」「次に自分が音を鳴らす」など、小さな役割を与え、成功体験を積ませる。","感情表現の促進: 音楽のテンポやリズムに合わせ、「嬉しい」「悲しい」など感情を表す動きを取り入れる。"
              ],
            "ジェスチャー練習 (「ありがとう」「おいしい」など簡単な表現を学ぶ活動。)": [
                         "日常生活での活用: 実際の場面（給食時に「ありがとう」や、おかわりの際に「もっと」など）でジェスチャーを自然に使う練習を行う。","視覚教材を活用: ジェスチャーの動きを示すイラストを用意し、動き方を理解しやすくする。","ゲーム形式で学習: 「これ何のジェスチャー？」とクイズ形式で楽しく取り組む。"
              ],
        },

        "社会生活スキルが不足している生徒": {
            "買い物の練習 (模擬店舗でお金を払う練習や、お釣りを受け取る活動。)": [
                        "模擬店舗の設定: 実際にレジや商品棚を模した教室内環境を作り、お金の支払い方や商品選びを練習。",
                        "具体的な役割分担: 生徒が「お客さん役」「店員役」を交互に体験し、それぞれの立場のやり取りを学ぶ。",
                        "数の理解を強化: 商品価格がわかりやすいよう、価格シールに大きな数字を記載。「リンゴ2つで100円」といった足し算の練習も含める。"
              ],
            "交通機関の利用練習": [
                        "ステップ練習: (1) 切符を買う→(2) 改札を通る→(3) バス停やホームで待つ、など行動を分けて練習。",
                        "実際の利用体験: 教員が付き添い、学校周辺でバスや電車を実際に使う。降車のタイミングを知らせる練習も行う。",
                        "シミュレーション教材の活用: 動画や写真で「バスに乗る流れ」を事前に学び、実際の場面に活かす。"
              ],
            "挨拶や簡単な会話の練習": [
                        "場面設定型練習: 「先生に挨拶」「友達にお願いする」など、状況を再現して練習。",
                        "具体的なフレーズ練習: 例として「これをください」「ありがとう」「すみません」など基本的な表現を繰り返し指導。",
                        "視覚的サポート: 挨拶や会話の場面を示す絵カードを見せ、次に行う動作をイメージさせる。"
              ],
        },
        "時間や順序の理解が苦手な生徒": {
            "時計の読み方練習 (アナログ時計を用いて「○時○分」を理解する活動。)": [ 
                        "視覚と触覚を活用した時計教材: 時計の針を動かせる教材を用意し、「短い針が3、長い針が12だから3時」といった具体的な説明を繰り返す。",
                        "デジタル時計とアナログ時計の一致練習: 同時にデジタル時計を見せて、対応関係を確認。例えば、「3:30と時計の針はこうなる」と視覚的に理解させる。",
                        "ゲーム形式で練習: 「10時に針を合わせてみて」といった指示で実際に針を動かすゲームを取り入れる。正解したら褒めることで動機づけする。"
              ],
            "視覚的スケジュール(ピクトグラムや写真を用いた1日の流れを確認する練習。)": [  
                        "個別化したスケジュール表の作成: 生徒の活動に応じたピクトグラムや写真を並べ、「朝の会」「休憩」「掃除」など活動ごとに分かりやすく整理。",
                        "実物の確認とリンク: 活動前に実際の物（掃除道具や給食トレーなど）を見せ、スケジュール上の画像と結びつける。",
                        "完成表での達成感を促進: 終わった活動のピクトグラムを「完了」ボックスに移動することで進行状況を可視化。"
              ],
            "タイマーの活用 (「この活動は5分」「次は10分後」といった時間感覚を養うための練習。)": [ 
                        "視覚タイマーを使用: 時間が減る様子が視覚的にわかるタイマー（例: Time Timer）を使い、「赤い部分がなくなったら次の活動」と説明。",
                        "切り替え練習の導入: タイマーが鳴った後にすぐ切り替える練習を小さなタスク（「ボールを箱に入れる」「机に座る」など）で繰り返す。",
                        "活動前の見通し提示: 「この活動は3分間だけ」など時間を事前に伝えることで、安心感と集中力を高める。"
              ],
        },
        "運動能力や感覚に偏りがある生徒": {
            "感覚統合運動 (平均台を使ったバランス練習や、ボール遊びを通じた体幹の強化。)": [ 
                        "簡易なバランス練習: 平均台の幅を調整し、初めは広めに設定。バランスを取りやすい状態で練習を始める。",
                        "複合的な活動: ボールを渡す→次に平均台を渡る、といった複数の動きを組み合わせることで運動能力を向上。",
                        "成功の楽しさを強調: 小さな成功を積み重ねることで運動への抵抗感を軽減する。"
              ],
            "リトミック (音楽に合わせて手足を動かし、動作のリズム感や協調性を高める)": [
                        "動作の選択肢を広げる: 簡単な手拍子からジャンプや回転といった動作へ徐々に難易度を上げる。",
                        "音楽の多様化: 生徒が興味を持つ曲を使い、音楽との親和性を高める。",
                        "褒める機会を増やす: できた動作に対し、すぐに「素晴らしい！」といったフィードバックを行い自信を促す。"
              ],
            "簡単な体操( 短時間でできるストレッチや全身運動で体力をつける。)": [
                         "遊びを取り入れる: 体操の動作を「動物ごっこ（うさぎ跳び、クマ歩き）」として楽しめる形で導入。",
                         "短時間のサイクル: 最初は1分程度の体操から始め、徐々に時間を延ばす。","反復学習: 毎日同じ体操を繰り返し行い、動作のパターンを身につけさせる。"
              ],
        },
        "情緒が不安定な生徒 (静かな音楽を聴きながらの深呼吸や簡単なストレッチ。)": {
            "リラクゼーション活動": [
                         "段階的深呼吸練習: 「鼻から4秒吸って、口から6秒吐く」といったカウント付きの深呼吸を繰り返し指導。タイマーやメトロノームを使うとリズムをつかみやすい。",
                         "環境調整: リラクゼーションの場は光を弱め、柔らかいクッションやブランケットを用意して安心感を与える。",
                         "五感を使ったリラックス: 柔らかいボールを握る、香り付きのオイルやハンドクリームを使うなど、触覚や嗅覚を取り入れた活動を組み込む。"
              ],
            "自己表現活動:  絵や音楽を使い、自分の感情を自由に表現する練習。": [
                         "絵画や造形活動: 「好きな色で今日の気分を描いてみよう」など自由なテーマを与える。興味を広げるために粘土やクラフト素材も用意。",
                         "音楽を用いた表現: 太鼓やカスタネットなどの楽器を使い、強い音や静かな音で感情を表現する練習を行う。",
                         "感情カードの活用: 表情や気分を示したカード（例: 怒り、悲しみ、喜び）を使い、どのカードが自分の気持ちに近いか選ばせる。"
              ],
            "感情コントロール練習:  「怒ったら深呼吸を3回」「悲しいときは絵で表す」などの具体的な方法を教える。": [
                         "具体的な手順の提示: 「怒ったときは手をグーにして3秒間握る→パッと開く」を繰り返す。緊張をほぐすための身体的な動作を教える。",
                         "感情日記の導入: 簡単な絵やシールを使い、1日の中で気持ちがどう変化したか記録する習慣をつける。",
                         "モデルロールプレイ: 教員が感情をコントロールする場面を演じ、生徒がそれを真似る練習を行う。"
              ],
        },
         "集団活動への参加が難しい生徒 (ルールが明確で、短時間で終わる集団ゲーム（例: ボール渡し、手遊び歌）。": {
            "簡単なゲーム活動": [
                         "ルールの視覚化: ゲームの手順やルールをピクトグラムや簡単な文章で示す。「まず手を挙げる→次にボールを渡す」など具体的に説明。",
                         "短時間で終わるゲーム: ボールを隣に渡すだけの「リレー遊び」や「手を叩いて次の人に合図を送る」など、単純な動作で完結するゲームを選ぶ。",
                         "成功体験を積ませる: できたことを即座に褒める。「○○さんが次の人にボールを渡せたね！」と具体的に声をかける。"
               ],
            "役割分担の練習 (「今日はあなたが○○をする役」と明確に役割を設定した活動。)": [
                         "簡単で明確な役割設定: 「ボールを渡す役」「時間を測る役」など、個々の役割が明確な活動を選ぶ。",
                         "役割を変更する練習: 同じ活動内で役割を交代させる。「次は○○さんがタイマーを押すね」と練習を通して柔軟性を高める。",
                         "役割カードの利用: 役割をイラストや写真で提示し、視覚的にわかりやすく伝える。"
               ],
            "少人数からの集団練習 (2～3人の小グループから始め、徐々に大人数に移行。)": [
                         "特定の友達とのペア活動: 信頼関係がある生徒とペアを組み、少人数での活動に慣れる。",
                         "「待つ」練習: 少人数グループ内で順番を待つ練習を取り入れ、焦らず参加できる環境を作る。",
                         "グループの人数を段階的に増やす: 2人→3人→5人と徐々に人数を増やし、活動のスケールに慣れさせる。"
               ],
        }
    },
    "障害の種類": {
        "聴覚障害": {
            "コミュニケーション支援": [
                {
                    "title": "手話の練習: 手話を使って、自己紹介や日常会話を学ぶ。",
                    "details": [
                        "場面設定を重視した練習: 食事の場面で「ごはん」「おかわり」などの手話を学ぶ。学校や家で頻繁に使うフレーズから始める。",
                        "ゲーム形式の練習: 手話でしりとりや「〇〇はどこ？」のようなクイズを行い、楽しく習得できる環境を提供する。",
                        "家族との連携: 家庭でも手話を使えるよう、保護者向けのワークショップを実施し、共通の表現方法を増やす。"
                    ],
                },
                 {
                    "title": "ジェスチャー活用: 視覚的な動きで意思を伝える練習（例: 「飲みたい」「行きたい」など）。",
                    "details": [
                        "生活場面に応じた練習: 「飲みたい」→水を指差す、「行きたい」→ドアを指差す、など具体的な場面での練習。",
                        "絵カードとの併用: ジェスチャーと同時にピクトグラムを使い、視覚的に補助する。ジェスチャーの意味を明確に伝えやすくなる。",
                        "家族との連携: 家庭でも手話を使えるよう、保護者向けのワークショップを実施し、共通の表現方法を増やす。"
                    ],
                },
                {
                    "title": "指文字練習: 手話に加え、指文字を活用する場面を設定。",
                    "details": [
                        "名前や身近な単語から練習: 生徒自身の名前や友達の名前を指文字で表現するところからスタート。",
                        "指文字を使ったスピードゲーム: 生徒に単語を出題し、指文字で早く表現できるか競争することで楽しみながら習得。",
                        "日記での活用: 1日の出来事を指文字で表現する練習を取り入れる。"
                    ],
                },
            ],
            "視覚的支援": [
                {
                    "title": "タイムラインやカードの提示",
                    "details": [
                        "1日の流れを図示: 朝、昼、放課後など、具体的な時間帯ごとの活動を絵や写真で示すタイムラインを作成。",
                        "カラーカードの使用: 指示の優先順位を「赤＝すぐに」「青＝後で」と色分けして伝える。",
                        "生徒自身で作成する活動: 例えば「静かにする」カードを自分でデザインし、ルールを覚えながら製作。学校全体での活用: そのカードをクラス全員で使い、共通の視覚的ルールを浸透させる。",
                    ],
                },
                 {
                    "title": "サインカード作成",
                    "details": [
                        "生徒自身で作成する活動: 例えば「静かにする」カードを自分でデザインし、ルールを覚えながら製作。",
                        "サインカード作成: 学校全体での活用: そのカードをクラス全員で使い、共通の視覚的ルールを浸透させる。",
                    ],
                },
            ],
            "集団活動への参加": [
                 {
                    "title": "音ではなく光を使った指示",
                    "details": [
                        "LEDライトやスマートランプの活用: スタート時は「緑」、終了時は「赤」を点灯させるなど、シンプルで直感的な方法を採用。",
                        "プロジェクターを活用した合図: 教室の壁やホワイトボードに視覚的な合図を映し出し、参加者全員が確認できるようにする。",                                          
                    ],
                },
                 {
                    "title": "ペアでの活動",
                    "details": [
                       "ローテーションでのペア変更: 聞こえる生徒とのペアを毎回変え、協力の幅を広げる。",
                       "ルールを視覚化した活動: 「次は○○さんが発表します」と紙やホワイトボードで順番を表示。ペア活動の進行がわかりやすくなる。",
                                           ],
                },
            ],
            "補聴器やICTの活用": [
                 {
                    "title": "補聴器や人工内耳の操作練習",
                    "details": [
                        "実物を使った練習: 模擬的な補聴器を用意し、着脱や音量調整のシミュレーションを繰り返し行う。",
                        "点検の手順を学ぶ: 電池交換や機器の状態チェックを生徒自身でできるよう、点検リストを作成。",
                        "トラブル対応のシナリオ練習: 補聴器が壊れた場合や音が聞こえにくい場合の対応方法を事前にロールプレイで学ぶ。",
                    ],
                },
                 {
                    "title": "タブレットでのコミュニケーション",
                    "details": [
                        "音声認識アプリの練習: 音声を文字に変換するアプリ（例: Google Live Transcribe）を使い、聞き取りの補助として活用。",
                        "絵文字やスタンプの活用: タブレットでの会話において、スタンプや絵文字を選ぶことで感情を伝える練習。",
                        "ビデオメッセージの利用: 手話を録画して送る練習を行い、ICTを使った非同期コミュニケーションのスキルを習得。",
                    ],
                },
            ],
        },
                
    "視覚障害": {
            "空間認識の訓練": [
                 {
                    "title": "白杖の使い方練習",
                    "details": [
                        "安全な練習環境の設定: 体育館や特別室など広くて安全な場所で、白杖を持って歩く基本操作を練習。障害物を配置して回避練習も行う。",
                        "屋外での実地練習: 点字ブロックのある道や交差点で、歩行練習を行いながら信号音や周囲の音を活用して移動する方法を学ぶ。",
                        "シナリオ学習: 「学校の入り口から教室まで行く」など具体的な移動シナリオを設定し、実践的な練習を繰り返す。",
                    ],
                },
                 {
                    "title": "誘導ロープの使用",
                    "details": [
                        "移動ルートの確認: 教室内や廊下にロープを設置し、そのルートを使って安全に目的地に到達する練習を実施。",
                        "ロープの質感の違いを活用: 例えば、行き先ごとにロープの素材や太さを変え、触感で区別する方法を教える。",
                    ],
                },
                 {
                    "title": "点字ブロックの理解",
                    "details": [
                        "種類別の歩行練習: 点字ブロック（誘導用・警告用）の違いを足裏で感じながら、それぞれの役割を説明。",
                        "点字ブロックを使ったミニゲーム: ゴール地点を設定し、点字ブロックに沿って歩き目的地にたどり着く練習を行う。"
                    ],
                },
            ],
            "感覚を活用した学習": [
                 {
                    "title": "点字の練習",
                    "details": [
                        "日常生活で使う単語から練習: 「学校」「名前」「ありがとう」など身近な単語を中心に、実用的な語彙を点字で学ぶ。",
                        "ゲームを取り入れる: 点字で書かれた単語を触覚で読み取って当てるクイズ形式の活動を実施。",
                    ],
                },
                 {
                    "title": "触覚教材の利用",
                    "details": [
                        "テーマ別教材: 季節やイベントごとに触覚教材を用意し、興味を引き出す（例: 凸凹で紅葉の葉を感じる教材）。",
                        "複雑な形状の認識練習: 凸凹の地図や図形教材を使い、触覚を使った情報収集のスキルを高める。",
                    ],
                },
                 {
                    "title": "音声教材の活用",
                    "details": [
                        "音声ガイド付きの読書: 好きな絵本や物語を音声ガイドで楽しむ活動を取り入れ、聴覚を活用した読解力を育てる。",
                        "録音教材の自作: 生徒自身が録音した音声メモを教材として活用し、情報の整理力を養う。",
                    ],
                },
            ],
             "生活スキルの向上": [
                 {
                    "title": "身辺自立活動",
                    "details": [
                        "着脱練習キットの使用: ボタンやファスナー、マジックテープが付いた特製の練習用パネルを活用。",
                        "触覚での確認ポイントを教える: ボタンの位置やファスナーの始点など、触覚で確認できるポイントを具体的に指導。",
                    ],
                },
                 {
                    "title": "台所の基本操作",
                    "details": [
                        "専用の調理補助具の活用: 包丁ガイドや視覚障害者向けの火加減センサーを使って安全性を確保。",
                        "工程ごとの分割練習: 野菜を洗う→切る→鍋に入れる、など一つの作業を分解し、それぞれを順番に習得。",
                        "香りや音の活用: 例えば、お湯が沸騰する音や、炒め物の香りをヒントに料理の進行状況を把握する練習を行う。",
                    ],
                },
                 {
                    "title": "音声読み上げソフト",
                    "details": [
                        "簡単な操作方法から指導: 文字を選択して読み上げさせる基本操作を学ぶ。アプリの操作をシンプルに説明したマニュアルを用意。",
                        "学習アプリの活用: 「Seeing AI」や「Be My Eyes」など視覚障害者向けのアプリを使い、日常生活での情報収集をサポート。",
                    ],
                },
                 {
                    "title": "拡大読書器の利用",
                    "details": [
                        "文字の拡大度合いを個別調整: 生徒の視力に合わせて最適な拡大倍率を設定し、無理のない範囲で利用。",
                        "学校教材への応用: 拡大読書器で教科書やプリントを読み、課題を進める練習を行う。",
                        "視覚疲労への配慮: 長時間の使用を避け、短時間での練習を積み重ねて負担を軽減。",
                    ],
                },
             ],
    },
    "ダウン症": {
            "コミュニケーションスキルの向上": [
                 {
                    "title": "ゆっくりした発話練習",
                    "details": [
                        "短いフレーズの反復練習: 「おはようございます」など、短いフレーズをカードや音声教材を使って反復。",
                        "リズムを取り入れる: リズムに合わせて言葉を発する練習（例: 音楽に合わせて「いち、に、さん」と声を出す）。",
                        "ビデオ録画での自己確認: 生徒自身が話す様子を録画し、映像を確認しながら改善点を一緒に見つける。",
                    ],
                },
                 {
                    "title": "簡単な会話の練習",
                    "details": [
                        "場面を設定したロールプレイ: 「お店で買い物」「バスで挨拶」など、具体的な場面を設定して対話を練習。",
                        "指導者との1対1練習からスタート: 初めは安心できる環境で指導者と練習し、慣れてきたら他の生徒と練習。",
                        "視覚補助の使用: ピクトグラムやフラッシュカードを使って、会話の流れを視覚的に理解させる。",
                    ],
                },
                 {
                    "title": "非言語的な表現練習",
                    "details": [
                        "ジェスチャーゲーム: お題に合わせて表情や動作で意思を伝えるゲームを行い、楽しみながらスキルを習得。",
                        "鏡を使った表情練習: 鏡を見ながら笑顔や怒りなどの表情を練習し、感情表現の幅を広げる。",
                        "手話やジェスチャーを使用する場面の設定: 例：「静かに」を示す指一本のジェスチャー、「こっちに来て」を示す手招きなど。",
                    ],
                },
            ],
             "運動機能の向上": [
                 {
                    "title": "基礎体力づくり",
                    "details": [
                        "音楽に合わせた体操: 好きな曲に合わせてストレッチや軽いダンスを取り入れ、楽しく体力を向上。",
                        "動作を分割して指導: ストレッチや体操を一つひとつの動作に分解し、わかりやすく説明。",
                        "運動日記の活用: 毎日取り組む運動を記録し、達成感を感じられるようにする。",
                    ],
                },
                 {
                    "title": "手先の器用さを鍛える活動",
                    "details": [
                        "操作の幅を広げる道具の活用: 紐通しやブロック遊びだけでなく、パズルやマグネットブロックを使う。",
                        "実生活に関連づける練習: ボタンつけ練習から実際の衣服を使った着脱練習に発展させる。",
                        "タイムチャレンジ: 紐通しやボタンかけを時間内にできるか挑戦し、集中力を高める。",
                    ],
                },
                 {
                    "title": "歩行やジャンプの練習",
                    "details": [
                        "障害物コースの設定: 簡単な障害物を配置したコースを歩き、乗り越える練習を行う。",
                        "音楽とジャンプを組み合わせる: 音楽に合わせてステップやジャンプを行い、タイミング感覚を鍛える。",
                        "バランスボールの利用: ボールに座りながらバランスを取る練習で、体幹を強化。",
                    ],
                },
             ],
             "日常生活スキルの訓練": [
                 {
                    "title": "買い物練習",
                    "details": [
                        "実際の道具を使用: 模擬店舗で本物のお金や品物を使い、現実的な体験を提供。",
                        "買い物リストの活用: 「リンゴ1個」など視覚的なリストを使い、自分で確認しながら買い物を進める練習。",
                        "段階的な目標設定: 最初は一つの商品だけを購入する練習から始め、徐々に複数の商品に挑戦。",
                    ],
                },
                 {
                    "title": "時間管理の練習",
                    "details": [
                        "タイマーでの視覚と音の活用: 「残り5分」を視覚的（砂時計やデジタルタイマー）と聴覚的に知らせる。",
                        "スケジュールボードの使用: 朝の準備や授業ごとにチェックマークをつけられるスケジュールボードを作成。",
                        "時間をテーマにした遊び: 時計の針を合わせるゲームや「今何時？」クイズを行う。",
                    ],
                },
                 {
                    "title": "衣服の着脱練習",
                    "details": [
                        "部分的な練習から始める: 例)靴を脱ぐ→履くの順番から、徐々に衣服全体の着脱に移行。",
                        "着脱に便利な服の準備: ゴムパンツやベルクロ付き衣服を使い、最初は簡単な操作に集中。",
                        "タイムトライアルを実施: 時間内に着替えを完了させる遊び感覚の練習を取り入れる。",
                    ],
                },
                ],
             "社会参加の促進": [
                 {
                    "title": "グループ活動の練習",
                    "details": [
                        "役割を明確にする: 「リーダー」「道具を渡す人」など簡単な役割を設定し、達成感を与える。",
                        "少人数から始める: 2～3人での活動に慣れたら、徐々に大人数のグループに移行。",
                        "成功体験の共有: 活動後に良かった点を全員で話し合い、褒め合う場を作る。",
                    ],
                },
                 {
                    "title": "公共マナーの練習",
                    "details": [
                        "簡単なルールから指導: 例：「バスでは座って待つ」「電車では静かにする」など基本的な行動を具体的に示す。",
                        "現場での体験学習: 実際にバスや電車を利用し、指導者が横でサポートしながら学ぶ。",
                        "繰り返し練習: 学校近くのバス停や駅で、同じ行動を繰り返し練習して習慣化する。",
                    ],
                },
                 {
                    "title": "挨拶やお礼の練習",
                    "details": [
                        "カードを活用: 「こんにちは」「ありがとう」と書かれたカードを見ながら挨拶練習。",
                        "褒める文化の導入: 挨拶ができた際には周囲が褒め、行動を強化。",
                        "日常生活に組み込む: 朝の挨拶や帰りの挨拶を自然な流れで行う習慣を作る。",
                    ],
                },
             ],
    },

    "自閉スペクトラム症（ASD）": {
            "スケジュール管理の練習": [
                 {
                    "title": "視覚的な見通しの提供",
                    "details": [
                        "時間ごとのカード: 時計とリンクさせたカードを準備し、「9:00 勉強」「10:00 休憩」などを示す。",
                        "完了ボード: 終わったタスクを「完了エリア」に移動することで達成感を感じさせる。",
                        "デジタルアプリの活用: タブレットアプリを使用し、スケジュールをデジタルで視覚化する。",
                    ],
                },
                 {
                    "title": "タイマーの活用",
                    "details": [
                        "カウントダウン式のタイマー: 残り時間が視覚的に分かるタイマーを使い、時間感覚を育てる。",
                        "音と光での終了通知: 活動終了時に音や光で知らせるタイマーを用いて、次の行動への切り替えをスムーズにする。",
                    ],
                },
            ],
             "社会性を高める活動": [
                 {
                    "title": "ソーシャルスキルトレーニング（SST）",
                    "details": [
                        "写真や動画を使った分析: 生徒の普段の行動を撮影し、何が良かったか一緒に振り返る。",
                        "グループでの練習: 少人数で「順番待ち」や「頼む・断る」の練習をし、実際の場面に応用する。",
                        "「ちくちく言葉」と「あったか言葉」:  \n  〇ちくちく言葉とあったか言葉を分類するクイズ形式  \n   〇日常の場面をイラストや動画で見せて、どちらの言葉か選ばせる  \n  〇あったか言葉を増やす目標を設定し、カウントする。",
                    ],
                },
                 {
                    "title": "感情表現の練習",
                    "details": [
                        "感情サイコロ: 6面のサイコロに「嬉しい」「悲しい」などの表情や言葉を書き、サイコロを振って状況を演じる。",
                        "色や音を使った練習: 「青は悲しい、赤は怒り」など、色や音で感情を表現する方法を学ぶ。",
                    ],
                },
             ],
             "感覚への配慮と調整": [
                 {
                    "title": "感覚統合遊び",
                    "details": [
                        "トランポリン: トランポリンに立ったり飛んだりすることで、感覚刺激を調整。",
                        "触覚: スライムなど様々な物に触れる活動を設定。",
                        "障害物コース: ミニハードルやトンネルなど、適度な感覚刺激を取り入れたコースを用意。",
                    ],
                },
             ],
    },
    "自閉症（孤立型）": {
            "関わる機会を増やす（他者とのやりとりの第一歩）": [
                 {
                    "title": "指差しや選択カードの使用",
                    "details": [
                        "教師が「〇〇が欲しい？」と尋ね、指差しやカードで答えられるようにする。",
                        "絵カードを使用して気持ちを伝えられるようにする。",
                    ],
                },
                 {
                    "title": "ペアでの作業時間を短く設定",
                    "details": [
                        "「1分だけ隣の人と同じ色の積み木を並べよう」→徐々に時間を延ばす。",
                    ],
                },
                {
                    "title": "バトン渡しゲーム",
                    "details": [
                        "「バトンを〇〇さんに渡そう」など、簡単なやりとりから始める。。",
                    ],
                },
            ],
             "他者との活動を意識させる": [
                 {
                    "title": "共同作業（役割を分ける）",
                    "details": [
                        "「一人が色を塗り、もう一人が切る」など、自然に協力できるようにする。",                        
                    ],
                },
                 {
                    "title": "視線の誘導",
                    "details": [
                        "「先生が今何を持っているでしょう？」→視線を向けることを促す。",
                    ],
                },
             ],
             "表情や感情を理解する練習": [
                 {
                    "title": "感情カードのマッチング",
                    "details": [
                        "「この顔はどんな気持ちかな？」→嬉しい・悲しいの基本感情を理解する。",                        
                    ],
                },
                {
                    "title": "表情を当てるゲーム",
                    "details": [
                        "「先生は今どんな顔をしている？」→笑顔や驚いた顔などを真似する。",                        
                    ],
                },
             ],
    },
    "自閉症（ 受動型）": {
            "自発的な発話を促す": [
                 {
                    "title": "選択肢を作る",
                    "details": [
                        "「今日は〇〇と〇〇のどっちをやりたい？」→自分の意見を言う練習。",
                    ],
                },
                 {
                    "title": "ジェスチャーで伝える練習",
                    "details": [
                        "「先生の好きな動物を当ててみよう」→ジェスチャーを使うと表現の幅が広がる。",
                    ],
                },
            ],
             "簡単な役割を与える": [
                 {
                    "title": "授業での発表機会を増やす",
                    "details": [
                        "「今日の天気をみんなに教えて」→短い発表から始める。",
                    ],
                },
                 {
                    "title": "当番活動を取り入れる",
                    "details": [
                        "「今日は〇〇さんが黒板を消す係ね」→役割を持たせることで積極性を引き出す。",
                    ],
                },
             ],
             "社会的な関わりを広げる": [
                 {
                    "title": "「ありがとう」や「どうぞ」を言う練習",
                    "details": [
                        "物を受け取る際に必ず「ありがとう」と言う習慣をつける。",
                    ],
                },
                {
                    "title": "簡単なゲームで自然な会話を促す",
                    "details": [
                        "「お互いの好きな食べ物を5つずつ言い合おう」→自然なやりとりを増やす。",
                    ],
                },
             ],
    },
    "自閉症（積極奇異型）": {
            "会話の順番を意識する練習": [
                 {
                    "title": "ターン制の会話ゲーム",
                    "details": [
                        "「1回話したら、相手に質問をする」→質問する習慣をつける。",
                        "「〇〇くんの番！次は△△くんの番！」と順番を明確に→視覚的に分かるカードを用意する。",
                    ],
                },
            ],
             "話す内容を整理する": [
                 {
                    "title": "時間を区切る練習",
                    "details": [
                        "「1分以内に好きな電車のことを話そう」→時間を意識させる。",
                    ],
                },
                 {
                    "title": "3つのポイントで話すルール",
                    "details": [
                        "「好きなもの・理由・面白いところの3つにまとめる」→話を短く整理する習慣をつける。",
                    ],
                },
             ],
             "相手の気持ちを考える": [
                 {
                    "title": "話を聞いてもらうにはどうしたらいいか考えるワーク",
                    "details": [
                        "「〇〇くんが興味のある話題は何かな？」→相手の立場を意識する練習。",
                    ],
                },
                {
                    "title": "表情の読み取り練習",
                    "details": [
                        "「この顔はどんな気持ち？」→相手の反応を見て、話すペースを調整する習慣をつける。",
                    ],
                },
             ],
    },
    "自閉症（尊大型）": {
            " 柔軟な考え方を身につける": [
                 {
                    "title": "いろいろな意見があることを学ぶ練習",
                    "details": [
                        "「この問題にはいくつ答えがあるかな？」→一つの答えにこだわらない練習。",
                    ],
                },
                 {
                    "title": "「違う意見を聞くことも大切」ルールを作る",
                    "details": [
                        "「間違いを指摘する前に、まず相手の意見を聞こう」→話す前に考える習慣をつける。",
                    ],
                },
            ],
             "相手を尊重する練習": [
                 {
                    "title": "ロールプレイで練習",
                    "details": [
                        "「相手が間違えたとき、どんな言い方をすればいい？」→攻撃的な言い方を避ける練習。",
                        " ちくちく言葉とあったか言葉を分類するクイズ形式。",
                    ],
                },
                 {
                    "title": "他の人の良いところを見つける活動",
                    "details": [
                        "「〇〇さんの得意なことを1つ言おう」→他者への関心を持たせる。",
                    ],
                },
             ],
             "知識を活かした活動を用意する": [
                 {
                    "title": "「先生役」を経験させる",
                    "details": [
                        "「みんなに〇〇のことを教えてあげよう！」→知識を適切に伝える場を作る。",
                    ],
                },
                {
                    "title": "「知識をクイズ形式にする",
                    "details": [
                        "「先生とクイズを作ってみよう！」→話しすぎず、相手とやりとりをしながら進める習慣をつける。",
                    ],
                },
             ],
    },


    "ADHD（注意欠如・多動症）": {
        "注意力を育てる活動": [
                 {
                    "title": "視覚的手がかりの活用",
                    "details": [
                        "チェックリスト: 1つ作業が終わるたびにチェックを入れるリストで達成感を与える。",
                        "カラフルなタスクリスト: 作業ごとに色分けしたカードを使い、視覚的に分かりやすく提示する。",
                   ],
                },
                 {
                    "title": "短い課題から始める",
                    "details": [
                        "分割された課題: 長い作業は小さなステップに分け、1つずつ達成する練習を行う。",
                        "即時フィードバック: 短い課題が完了した際、すぐに具体的な褒め言葉で達成感を強化する。",
                    ],
                },
                 {
                    "title": "衝動性の調整",
                    "details": [
                        "簡単な深呼吸練習: 鼻から息を吸い、口からゆっくり吐く練習をゲーム感覚で導入。",
                        "ストレスボールの使用: 衝動的になりそうなときにストレスボールを握ることでエネルギーを発散。",
                    ],
                },
                 {
                    "title": "「待つ」練習",
                    "details": [
                        "信号ゲーム: 「赤→止まる、青→進む」といったゲームで、衝動を抑える練習。",
                        "タイミングを計るゲーム: 指導者が「今！」と合図を出すまで静止する遊びを行う。",
                    ],
                },
        ],
        "余分なエネルギーの発散": [
                 {
                    "title": "運動活動",
                    "details": [
                        "トランポリンやボール遊び: 座っていられない生徒には、まず適度な運動でエネルギーを発散させる。",
                        "リレー形式のゲーム: 集中を要する活動の前に体を動かし、気持ちを切り替える。",
                    ],
                },
                 {
                    "title": "活動と休憩のバランス",
                    "details": [
                        "タイマーの利用: 作業時間と休憩時間をタイマーで視覚的に示し、リズムを作る。",
                        "休憩に特定の活動を設定: 休憩時間に簡単なぬり絵やリラクゼーション活動を行う。",
                    ],
                },
                 ],
    },
    
    "発達性協調運動障害（DCD）": {
        "動作訓練": [
                 {
                    "title": "基礎運動の反復",
                    "details": [
                        "段階的練習: 投げる動作を「1. ボールを持つ→2. 腕を振る→3. 投げる」というように分解し、一つずつ確認。",
                        "目標を設定: ボールをカゴに入れるなど簡単な目標を設定し、成功体験を増やす。",
                        "リズム運動: リズムに合わせてジャンプや歩行を行い、動きに流れを持たせる練習。",
                    ],
                },
                 {
                    "title": "バランス運動",
                    "details": [
                        "柔らかい素材の平均台: 低いスポンジ素材の平均台を使い、恐怖心を軽減しながらバランスを鍛える。",
                        "ボール遊びを活用: バランスボールに座りながら小さなボールを渡す練習で、体幹を意識させる。",
                        "ケンケン練習: 短い距離で足場を色分けしたマットを使い、遊び感覚でケンケンを練習する。",
                    ],
                },
        ],
        "手先の巧緻性を高める活動": [
                 {
                    "title": "運筆練習",
                    "details": [
                        "太いクレヨンやマーカー: 持ちやすい太さの筆記具を使用し、握力を鍛えると同時に書きやすさを確保。",
                        "テンプレートの活用: 線や形が描かれたテンプレートを使用し、なぞることで成功体験を増やす。",
                        "指の体操を取り入れる: 書く前に指をほぐす体操（例: 指を開閉する、指で数字を表現する）を行う。",
                    ],
                },
                 {
                    "title": "手先を使う遊び",
                    "details": [
                        "大きめのビーズ通し: 紐を通しやすい大きなビーズを使い、成功しやすい環境を整える。",
                        "粘土遊び: 手を使った細かい動作を促すために、粘土で簡単な形を作る練習。",
                        "ファスナーやボタンの練習: 小さい道具ではなく、大きめの衣類を使用し、段階的に練習を進める。",
                    ],
                },
                 ],
        "自信を育てる活動": [
                 {
                    "title": "成功体験を重視",
                    "details": [
                        "個別目標の設定: 生徒ごとの得意分野（絵、歌など）を活かした活動を中心に取り入れる。",
                        "結果を視覚化: 上達の記録を写真や作品として保存し、振り返りで達成感を共有する。",
                    ],
                },
                 {
                    "title": "目標設定の工夫",
                    "details": [
                        "短期間で達成できる目標: 例えば「1回キャッチできたら成功」などの小さな目標を設定。",
                        "賞賛の強化: 努力や成功を具体的に褒める（例:「しっかり両手でキャッチできたね！」）。",
                    ],
                },
                 ],
    },
    
    "重度重複障害": {
        "身体的支援と訓練": [
                 {
                    "title": "基本動作の練習",
                    "details": [
                        "動作法: 緊張を緩める方法や力の入れ方を学ぶ。詳細は「特別支援教育サポート分析法・心療法」"
                        "段階的リハビリ: 「寝返り→起き上がる→座る」のように、一つの動作を段階ごとに支援。",
                        "音と触覚での誘導: 手を持ちながら体を動かし、「動くと音が鳴る」などフィードバックを取り入れる。",
                    ],
                },
                 {
                    "title": "リハビリ機器の活用",
                    "details": [
                        "スタンディングフレーム: 立つ練習を行う際、転倒の不安を軽減しながら姿勢保持を促進。",
                        "簡易エクササイズ: 車椅子を使った軽い足の動きや腕の運動を日常に取り入れる。",
                    ],
                },
        ],
        "コミュニケーションの工夫": [
                 {
                    "title": "AAC（補助代替コミュニケーション）機器の利用",
                    "details": [
                        "簡易スイッチ: 大きくて押しやすいスイッチを使用し、好きな音や言葉を再生。",
                        "意思選択カード: 2～3枚のカード（「はい」「いいえ」「もう一度」など）を提示し、選ばせる練習。",
                    ],
                },
                 {
                    "title": "ジェスチャーや表情の認識練習",
                    "details": [
                        "ミラー練習: 鏡を使い、指導者と一緒に表情を確認しながら練習。",
                        "シンプルな手話やサイン: 日常でよく使うサイン（例:「食べる」「飲む」など）を繰り返し導入。",
                    ],
                },
                 ],
    },
    "学習障害（LD）": {
            "読み書きのサポート": [
                 {
                    "title": "拡大文字や音声教材の活用",
                    "details": [
                        "電子書籍やアプリ: 文字サイズを調整できるアプリや音声読み上げ機能付きの電子書籍を使用。",
                        "視覚サポートの追加: 単語や文章に絵やアイコンを付け加え、内容理解を助ける。",
                        "音声録音練習: 生徒が自分の声を録音し、聞き返すことで読みの練習を促進する。",
                    ],
                },
                 {
                    "title": "段階的な書字練習",
                    "details": [
                        "ひらがな・カタカナマットの使用: 書き順や形を学ぶために、指でなぞるマットを活用。",
                        "テンプレートの提供: 行間が広いノートや、文字を書く場所を区切ったガイドシートを使用する。",
                        "タイピングの練習: 書字に困難がある場合は、パソコンやタブレットでタイピング練習を取り入れる。",
                    ],
                },
            ],
            "計算のサポート": [
                {
                    "title": "具体物を用いた計算",
                    "details": [
                        "学用品の活用: 算数ブロック、数え棒、100玉そろばんなどを使用し、数量や計算の概念を視覚化する。",
                        "日常生活のシミュレーション: お買い物ごっこでお金のやり取りを練習し、実生活との関連性を持たせる。",
                        "視覚的な支援: 足し算や引き算で、色分けしたカードや図を使い、数量の変化を視覚化。",
                    ],
                },
                {
                    "title": "計算補助機器の利用",
                    "details": [
                        "計算アプリ: 自動で計算の結果を提示するだけでなく、計算過程を示すアプリを活用。",
                        "電卓の段階的導入: 基本的な操作方法から始め、少しずつ複雑な機能を使えるように練習。",
                        "学習支援カード: 繰り上がりや繰り下がりの計算を視覚的に説明するカードを活用する。",
                    ],
                },
                ],
            "学習の成功体験": [
                {
                    "title": " 興味を引き出す教材選び",
                    "details": [
                        "個別に合わせた教材: 生徒の好きなキャラクターや趣味（スポーツ、音楽、アニメなど）をテーマにした教材を作成。",
                        "マルチメディア教材: 動画、音声、イラストを取り入れた教材で学習意欲を向上。",
                    ],
                },
                {
                    "title": "達成感を感じやすい課題",
                    "details": [
                        "ステップを分けた課題: 1つの目標をさらに細かく分割し、簡単なタスクを順番にクリアする形式を採用。",
                        "ポートフォリオ作成: 自分が達成した課題や作品を記録し、見返すことで成長を実感させる。",
                        "報酬システム: 短期目標達成ごとに、小さなご褒美（シールやメダルなど）を提供。",
                    ],
                },
            ],
           "まとめ": [  
           {
                    "title": "具体的な活動例",
                    "details": [
                        "読み: 好きなキャラクターの絵本を音読し、正しい発音や抑揚を確認。音声ガイド付きの教材も活用。",
                        "書き: 絵とセットになった単語カードを見て、関連する簡単な文章を作成。",
                        "計算: 実際にお金を使った「模擬お店」活動で、足し算や引き算を練習。",
                        "学習意欲向上: 成果を壁に飾ったり、ミニ発表会で家族や友達に見てもらう機会を作る。",
                    ],
                },                
           ],
         },
        },
    }






# 指導支援内容表示
if selected_menu == "指導支援内容":
    
    # カテゴリー選択
    selected_category = st.selectbox("１. カテゴリーを選択してください:", list(guidance_data.keys()))
    # サブカテゴリー選択
    selected_subcategory = st.selectbox(
        "２. 該当する項目を選択してください:", list(guidance_data[selected_category].keys())
    )

    # 辞書かリストかを確認して処理
    subcategory_data = guidance_data[selected_category][selected_subcategory]

    if isinstance(subcategory_data, dict):
        selected_detail = st.selectbox(
            "３. 具体的な支援内容を選択してください:",
            list(subcategory_data.keys())
        )
        detail_data = subcategory_data[selected_detail]
    elif isinstance(subcategory_data, list):
        detail_data = subcategory_data
    else:
        st.error("不明なデータ形式です。")
        detail_data = None

    # 内容表示
    if detail_data and st.button("適した指導・支援を表示"):
        

        # リストの場合、要素の内容を整形して表示
        if isinstance(detail_data, list):
           formatted_detail = "\n".join([
           f"- {item}" if isinstance(item, str) else f"- **{item.get('title', 'タイトルなし')}**: {', '.join(item.get('details', []))}"
           for item in detail_data
        ])
        else:
           formatted_detail = detail_data

# 直接表示する部分を削除し、エクスパンダー内だけで表示
        if detail_data:
           st.subheader("📌 適した指導・支援")

    # 詳細データをエクスパンダーで表示
        for item in detail_data:
            if isinstance(item, dict):
               with st.expander(item.get('title', 'タイトルなし')):
                for detail in item.get('details', []):
                    st.write(f"- {detail}")
            else:
              st.write(f"- {item}")  # 文字列データのリストならそのまま表示
          
        if "衣服の着脱練習" in selected_detail:
              st.image(img_dressing, caption="衣服の着脱練習の教材", use_container_width=True)
        # 「手話の練習: 手話を使って、自己紹介や日常会話を学ぶ。」の場合、画像を表示
        # 指文字の画像を表示（辞書かどうかを確認）
        if isinstance(item, dict) and item.get('title') == "指文字練習: 手話に加え、指文字を活用する場面を設定。":
         st.image(img_sign_language, caption="指文字", width=200)

        if "食事の練習" in selected_detail:
              st.image(img_hasizo, caption="箸ゾーくん（箸の練習に最適）", use_container_width=True)


 # **区切り線**
    st.markdown("---")

    # **別のWebアプリへのリンク**
    st.markdown("🌎関連Webアプリに移動する")
    st.markdown("[発達段階能力チャート作成](https://specialexcel2apppy-bo6jrng9gyqw5dmfcgwbl5.streamlit.app/)")
    st.markdown("[特別支援教育サポート分析法・心療法](https://bunnsekiapppy-6zctfql94fk2x3ghmu5pmx.streamlit.app/)")
    st.markdown("---")  # 区切り線  
    st.markdown("📁教育・心理分析ツール") 
    st.markdown("[応用行動分析](https://abaapppy-k7um2qki5kggexf8qkfxjc.streamlit.app/)")
    st.markdown("[機能的行動評価分析](https://kinoukoudou-ptfpnkq3uqgaorabcyzgf2.streamlit.app/)") 
    st.markdown("---")  # 区切り線
    st.markdown("📁統計学分析ツール") 
    st.markdown("[相関分析ツール](https://soukan-jlhkdhkradbnxssy29aqte.streamlit.app/)")
    st.markdown("[多変量回帰分析](https://kaikiapp-tjtcczfvlg2pyhd9bjxwom.streamlit.app/)")
    st.markdown("[t検定](https://tkentei-flhmnqnq6dti6oyy9xnktr.streamlit.app/)")
    st.markdown("[ロジスティック回帰分析ツール](https://rojisthik-buklkg5zeh6oj2gno746ix.streamlit.app/)")
    st.markdown("[ノンパラメトリック統計分析ツール](https://nonparametoric-nkk2awu6yv9xutzrjmrsxv.streamlit.app/)")


    st.markdown("---")  # 区切り線  
    st.markdown("🗨️自立活動の参考指導、各分析ツールにご意見がある方は以下のフォームから送ってください") 
    st.markdown("    ※埼玉県の学校教育関係者のみＳＴアカウントで回答できます。") 
    st.markdown("[アンケート](https://docs.google.com/forms/d/1dKzh90OkxMoWDZXV31FgPvXG5EvNlMFOrvSPGvYTSC8/preview)")
    st.markdown("---")  # 区切り線
    st.write("""※ それぞれのアプリに記載してある内容、分析ツールのデータや図、表を外部に出す物（研究など）に使用する場合は小山までご相談ください（上記フォームからでも可）。無断での転記・利用を禁じます。""")
   
