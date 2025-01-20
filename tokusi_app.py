import streamlit as st
import pandas as pd
import os


#from google.oauth2.credentials import Credentials
#from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError

# 環境変数からGoogle Drive APIの認証情報を取得
#def authenticate_gdrive():
    # 環境変数を設定している場合のみ読み込む
    #creds = Credentials.from_service_account_file(
        #os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        #scopes=["https://www.googleapis.com/auth/drive"]
   # )
    #return build("drive", "v3", credentials=creds)

# Google Driveのファイルリンクを取得する関数
#def get_file_link(file_id):
    #return f"https://drive.google.com/uc?id={file_id}"

# Google Driveの画像を取得して表示
#file_id1 = "1tQMqjPNYvQMwQo1GIXJSeJOs4NtgrBHR"  # 画像1のファイルID
#file_id2 = "14S9vje6JPIkqcUTwW4gD_tmJq2tBTmVt"  # 画像2のファイルID

#image_url1 = get_file_link(file_id1)
#image_url2 = get_file_link(file_id2)

#st.image(image_url1, caption="画像1: 衣服の着脱練習", use_column_width=True)
#st.image(image_url2, caption="画像2: その他の活動", use_column_width=True)



# フィードバック保存用のExcelファイル
feedback_dir = r"C:\Users\taka\OneDrive\デスクトップ\GitHub\special_education_app\feedback.xlsx"
feedback_file = os.path.join(feedback_dir, "feedback.xlsx")

# ディレクトリが存在しない場合、作成する
if not os.path.exists(feedback_file):
    pd.DataFrame(columns=["カテゴリー", "項目", "追加内容"]).to_excel(feedback_file, index=False, engine='openpyxl')
feedback_data = pd.read_excel(feedback_file, engine='openpyxl')

# 初期データの読み込み
if os.path.exists(feedback_file):
    feedback_data = pd.read_excel(feedback_file, engine='openpyxl')
else:
    feedback_data = pd.DataFrame(columns=["カテゴリー", "項目", "追加内容"])


# アプリの基本構造
st.title("🌟 自立活動の参考指導 🌟")

# メニュー選択
menu = st.sidebar.selectbox("メニューを選択してください", ["指導支援内容", "フィードバック追加", "フィードバック集計と削除"])



# メニューによって表示を制御
if menu not in ["フィードバック追加", "フィードバック集計と削除"]:
    # 'フィードバック追加' または 'フィードバック集計と削除' 以外のメニューが選ばれた場合にのみ表示
    
    guidance_data = []  # 指導データの実際の内容
    st.write(guidance_data)
# メニューごとの処理
if menu == "フィードバック追加":
    st.subheader("📝 フィードバック追加")
    
    feedback_category = st.selectbox("カテゴリーを選択:", ["日常生活における実態", "障害の種類"])
    feedback_subcategory = st.selectbox("項目を選択:", ["身辺自立が未熟な生徒","コミュニケーションが苦手な生徒","社会生活スキルが不足している生徒","時間や順序の理解が苦手な生徒","運動能力や感覚に偏りがある生徒","情緒が不安定な生徒","集団活動への参加が難しい生徒", "聴覚障害","視覚障害","ダウン症","自閉スペクトラム症（ASD）","注意・欠如・多動性障害（ADHD）","自閉スペクトラム症（ASD）","学習障害（LD）","発達性協調運動障害（DCD）","四肢・体幹機能障害"])
    feedback_content = st.text_area("追加するフィードバックを入力してください:")

    if st.button("フィードバックを保存"):
        if feedback_content:
            # 新しいフィードバックのデータフレーム
            new_feedback = pd.DataFrame([{
                "カテゴリー": feedback_category,
                "項目": feedback_subcategory,
                "追加内容": feedback_content
            }])
            feedback_data = pd.concat([feedback_data, new_feedback], ignore_index=True)
            try:
                # フィードバックの保存
                feedback_data.to_excel(feedback_file, index=False, engine='openpyxl')
                st.success("フィードバックが保存されました！")
                st.text(f"保存先: {feedback_file}")
            except Exception as e:
                st.error(f"フィードバックの保存中にエラーが発生しました: {e}")
        else:
            st.warning("フィードバック内容を入力してください。")

if menu == "指導支援内容":
    st.subheader("📚 指導支援内容の参照")
    st.text("1から順番に選択して下さい")



elif menu == "フィードバック集計と削除":
    st.subheader("📊 フィードバック集計と削除")
    if feedback_data.empty:
        st.info("現在、保存されているフィードバックはありません。")
    else:
        for i, row in feedback_data.iterrows():
            st.write(f"{i + 1}. 【カテゴリー】{row['カテゴリー']} / 【項目】{row['項目']} / 【内容】{row['追加内容']}")
            if st.checkbox(f"削除: {i + 1}", key=f"delete_{i}"):
                feedback_data.drop(index=i, inplace=True)
        
        if st.button("選択したフィードバックを削除"):
            feedback_data = feedback_data[~feedback_data.index.isin([i for i, row in feedback_data.iterrows() if st.checkbox(f"削除: {i + 1}", key=f"delete_{i}")])]
            feedback_data.reset_index(drop=True, inplace=True)
            feedback_data.to_excel(feedback_file, index=False, engine='openpyxl')  # 保存
            st.success("選択したフィードバックを削除しました！")

# ディレクトリが存在しない場合、作成する
if not os.path.exists(feedback_dir):
    os.makedirs(feedback_dir)  # この行で保存先ディレクトリを作成



    
# 指導データ
guidance_data = {
    "日常生活における実態": {
        "身辺自立が未熟な生徒": {
            "衣服の着脱練習": [
                         "ボタンやファスナーを練習するための専用教材を使用。"#,st.image(image_url1, caption="画像1: 衣服の着脱練習", use_column_width=True),
              ],
            "食事の練習": [
                          "スプーンやフォークの使い方、食器を片付ける練習。"
              ],
            "感覚統合活動": [ 
                         "異なる素材の布や玩具を触る活動を取り入れ、感覚過敏を軽減。"
              ],
        },
        "コミュニケーションが苦手な生徒": {
            "ピクトグラムや絵カードの活用": [
                         "自分の意思や要望をカードで表現する練習。"
              ],
            "リトミック": [
                         " 音楽に合わせて動き、教師や仲間と簡単なやり取りを行う。"
              ],
            "ジェスチャー練習": [
                         "「ありがとう」「おいしい」など簡単な表現を学ぶ活動。"
              ],
        },
        "社会生活スキルが不足している生徒": {
            "買い物の練習": [
                        "模擬店舗でお金を払う練習や、お釣りを受け取る活動。"
              ],
            "交通機関の利用練習": [
                        "学校近隣のバスや電車を利用し、切符購入や乗り降りを学ぶ。"
              ],
            "挨拶や簡単な会話の練習": [
                        "「こんにちは」「これをください」といった基本的なやり取りを身につける。"
              ],
        },
        "時間や順序の理解が苦手な生徒": {
            "時計の読み方練習": [ 
                        "アナログ時計を用いて「○時○分」を理解する活動。"
              ],
            "視覚的スケジュール": [  
                        "ピクトグラムや写真を用いた1日の流れを確認する練習。"
              ],
            "タイマーの活用": [ 
                        "「この活動は5分」「次は10分後」といった時間感覚を養うための練習。"
              ],
        },
        "運動能力や感覚に偏りがある生徒": {
            "感覚統合運動": [ 
                        "平均台を使ったバランス練習や、ボール遊びを通じた体幹の強化。"
              ],
            "リトミック": [
                        "音楽に合わせて手足を動かし、動作のリズム感や協調性を高める。"
              ],
            "簡単な体操": [
                         "短時間でできるストレッチや全身運動で体力をつける。"
              ],
        },
        "情緒が不安定な生徒": {
            "リラクゼーション活動": [
                         "静かな音楽を聴きながらの深呼吸や簡単なストレッチ。"
              ],
            "自己表現活動": [
                         "絵や音楽を使い、自分の感情を自由に表現する練習。"
              ],
            "感情コントロール練習": [
                         "「怒ったら深呼吸を3回」「悲しいときは絵で表す」などの具体的な方法を教える。"
              ],
        },
         "集団活動への参加が難しい生徒": {
            "簡単なゲーム活動": [
                         "ルールが明確で、短時間で終わる集団ゲーム（例: ボール渡し、手遊び歌）。"
               ],
            "役割分担の練習": [
                         "「今日はあなたが○○をする役」と明確に役割を設定した活動。"
               ],
            "少人数からの集団練習": [
                         "2～3人の小グループから始め、徐々に大人数に移行。"
               ],
         },
   },    
    "障害の種類": {
        "聴覚障害": {
            "コミュニケーション支援": [
                "手話の練習: 手話を使って、自己紹介や日常会話を学ぶ。",
                "ジェスチャー活用: 視覚的な動きで意思を伝える練習（例: 「飲みたい」「行きたい」など）。",
                "指文字練習: 手話に加え、指文字を活用する場面を設定。",
                "タブレットでのコミュニケーション: 音声入力から文字表示を活用したアプリでの意思疎通。",
            ],
            "視覚的支援": [
                "ピクトグラムや文字カードの活用: 1日の流れや指示内容を視覚的に表示。",
                "サインカード作成: 「待つ」「見る」「静かに」などの指示を表すカードを使う。",
                "ICTを活用: 図や表、動画、アニメーションなどをより多く提示する。",
            ],
            "集団活動への参加": [
                "音ではなく光を使った指示: ランプやフラッシュライトを使い、スタートや終了を知らせる。",
                "ペアでの活動: 聞こえる生徒とペアを組み、互いに補い合う練習。",
            ],
        },
        "視覚障害": {
            "空間認識の訓練": [
                "白杖の使い方練習: 安全に歩行するための基本操作を学ぶ。",
                "誘導ロープの使用: ロープを手に持ちながら教室や廊下を移動する練習。",
                "点字ブロックの理解: 点字ブロックの種類や意味を実際に歩いて確認。",
            ],
            "感覚を活用した学習": [
                "点字の練習: 自分の名前や簡単な単語を点字で学ぶ。",
                "触覚教材の利用: 凸凹で文字や図形を感じ取れる教材を使った学習。",
                "音声教材の活用: 録音教材や音声ガイドを利用して学ぶ。",
            ],
            "生活スキルの向上":[
                          "身辺自立活動: ボタンやファスナーを触覚で確認しながら衣服を着脱。"
                          "台所の基本操作: 安全に調理器具を使う練習（例: 包丁の持ち方や火加減の確認）。"
            ],
             "ICTを活用した支援":[
                          "音声読み上げソフト: タブレットやパソコンの音声機能を使って学習。"
                          "拡大読書器の利用: 弱視の場合は文字や画像を拡大して見る訓練。"
             ],
        },
         "ダウン症": {
            "コミュニケーションスキルの向上": [
                "ゆっくりした発話練習: 正確に言葉を発する練習（例: 音読や短い歌）。",
                "簡単な会話の練習: 「こんにちは」「これをください」など、日常生活で使うフレーズの練習。",
                "非言語的な表現練習: 表情やジェスチャーを使ったコミュニケーション。",
                            ],
            "運動機能の向上": [
                "基礎体力づくり: ストレッチや簡単な体操で筋力と柔軟性を向上。",
                "手先の器用さを鍛える活動: 紐通し、ブロック遊び、ボタンつけなどの指先運動。",
                "歩行やジャンプの練習: 障害物を乗り越える練習でバランス感覚を育てる。",
            ],
            "日常生活スキルの訓練": [
                "買い物練習: 模擬店舗を使い、お金の支払いとお釣りの確認を練習。",
                "時間管理の練習: ピクトグラムや時計を使い、スケジュールを守る練習。",
                "衣服の着脱練習: マジックテープやゴム付き衣類で簡単な着替えから始める。",
            ],
            "社会参加の促進": [
                "グループ活動の練習: 少人数での簡単な役割分担から始め、集団活動に参加。",
                "公共マナーの練習: 電車やバスの使い方、待つ姿勢を学ぶ。",
                "挨拶やお礼の練習: 人と接する際の基本動作を反復する。",
            ],
        },
        "自閉スペクトラム症（ASD）": {
            "スケジュール管理の練習": [
                "視覚的な見通しの提供: 写真や絵カードで1日の流れを示す。",
                "タイマーの活用: 活動時間や休憩時間を視覚化し、予測可能な環境を作る。",
            ],
            "社会性を高める活動": [
                "	ソーシャルスキルトレーニング（SST）: 挨拶や順番待ちなど、具体的な場面のロールプレイを行う。",
                "	感情表現の練習: 表情カードを使って感情の名前や適切な反応を学ぶ。",
           ],
            "感覚への配慮と調整": [
                "感覚統合遊び: ブランコやタッチプールで安心感を育む。",
                "静かな環境での活動: 感覚過敏が強い場合、刺激の少ない部屋での作業を行う。",
            ],
        },
        "注意・欠如・多動性障害（ADHD）": {
            "注意力を育てる活動": [
                "視覚的手がかりの活用: やるべきことをリスト化し、順序立てて行う。",
                "短い課題から始める: 5分程度の簡単な作業から集中力を育てる。",
            ],
            "衝動性の調整": [
                "リラックス法の導入: 深呼吸やヨガなどを行い、衝動をコントロールする練習。",
                "「待つ」練習: ゲームを通じて、指示が出るまで待つ訓練を行う。",
            ],
            "余分なエネルギーの発散": [
                "運動活動: ジャンプやランニングで身体を動かし、多動性を和らげる。",
                "活動と休憩のバランス: 15分作業→5分休憩など、適切なスケジュールを設定。",
            ],
        },
        "自閉スペクトラム症（ASD）": {
            "スケジュール管理の練習": [
                "視覚的な見通しの提供: 写真や絵カードで1日の流れを示す。",
                "タイマーの活用: 活動時間や休憩時間を視覚化し、予測可能な環境を作る。",
            ],
            "社会性を高める活動": [
                "ソーシャルスキルトレーニング（SST）: 挨拶や順番待ちなど、具体的な場面のロールプレイを行う。",
                "感情表現の練習: 表情カードを使って感情の名前や適切な反応を学ぶ。",
           ],
            "感覚への配慮と調整": [
                "感覚統合遊び: ブランコやタッチプールで安心感を育む。",
                "静かな環境での活動: 感覚過敏が強い場合、刺激の少ない部屋での作業を行う。",
            ],
        },
        "学習障害（LD）": {
            "読み書きのサポート": [
                "拡大文字や音声教材の活用: 読むことが苦手な生徒に文字を大きくしたり、音声で補助。",
                "段階的な書字練習: 文字や単語から始め、徐々に文章を書けるようにする。",
            ],
            " 計算のサポート": [
                "具体物を用いた計算: お金やブロックを使って目に見える形で数量を学ぶ。",
                "計算補助機器の利用: 電卓やタブレットを活用し、スムーズな計算を促す。",
            ],
            "学習の成功体験": [
                "興味を引き出す教材選び: 生徒が関心を持つ内容（好きなキャラクターや趣味）を教材に反映する。",
                "達成感を感じやすい課題: 簡単な成功体験を積み重ねることで自己肯定感を高める。",
            ],
        },
        "発達性協調運動障害（DCD）": {
            "動作訓練": [
                "基礎運動の反復: 投げる、捕る、歩くといった基本動作を繰り返し練習。",
                "バランス運動: 平均台を使ったバランス訓練やケンケン遊び。",
            ],
            "手先の巧緻性を高める活動": [
                "運筆練習: 簡単な線や形を描く練習から始める。",
                "手先を使う遊び: 紐通しやビーズ遊びで指先を鍛える。",
           ],
            "自信を育てる活動": [
                "成功体験を重視: 苦手な運動ではなく得意なこと（絵を描く、音楽など）を活かして自信を持たせる。",
                "目標設定の工夫: 小さな達成目標を設定し、達成感を感じさせる。",
            ],
        },
        "四肢・体幹機能障害": {
            "身体的支援と訓練": [
                "基本動作の練習: 寝返り、座る、立つなどの基本動作を繰り返し練習。",
                "リハビリ機器の活用: スタンディングフレームや車椅子での姿勢保持練習。",
            ],
            "コミュニケーションの工夫": [
                "AAC（補助代替コミュニケーション）機器の利用: ボタンを押すことで意思を伝えるスイッチ教材や音声出力デバイス、ジョイスティックマウスや視線入力装置の活用。",
                "ェスチャーや表情の認識練習: 簡単なサインを繰り返し学習する。",
            ],
            "環境への配慮": [
                "感覚刺激の提供: 光や音、触覚遊びで刺激を与え、環境への興味を引き出す。",
                "安全な環境作り: 移動や行動に制限がある場合、安全で快適な空間を確保する。",
                "呼吸器系の健康維持： 呼吸器疾患の予防や痰の粘度の低下、ウイルスの拡散抑制から部屋をよく加湿する必要がある"
            ],
        },
    },
}


# メインメニュー
#menu = st.selectbox("メニューを選択してください", ["指導支援内容"])

# 指導支援内容表示
if menu == "指導支援内容":
    # カテゴリー選択
    selected_category = st.selectbox("1.カテゴリーを選択してください:", list(guidance_data.keys()))
    # 項目選択
    selected_subcategory = st.selectbox(
        "2.該当する項目を選択してください:",
        list(guidance_data[selected_category].keys())
    )
    
    # 辞書かリストかを確認して処理
    if isinstance(guidance_data[selected_category][selected_subcategory], dict):
        selected_detail = st.selectbox(
            "3.具体的な支援内容を選択してください:",
            list(guidance_data[selected_category][selected_subcategory].keys())
        )
    elif isinstance(guidance_data[selected_category][selected_subcategory], list):
        selected_detail = st.selectbox(
            "3.具体的な支援内容を選択してください:",
            guidance_data[selected_category][selected_subcategory]
        )
    else:
        st.error("不明なデータ形式です。")
        selected_detail = None

    # 内容表示
    if selected_detail and st.button("適した指導・支援を表示"):
        st.subheader("📌 適した指導・支援")
        # 結果の整形
        if isinstance(guidance_data[selected_category][selected_subcategory], dict):
            detail = guidance_data[selected_category][selected_subcategory][selected_detail]
        else:
            detail = selected_detail
        
        # リスト形式であれば改行して表示
        if isinstance(detail, list):
            formatted_detail = "\n".join([f"- {item}" for item in detail])
        else:
            formatted_detail = detail
        
        # 直接表示
        st.markdown(f"**{selected_detail}**:  \n{formatted_detail}")



   