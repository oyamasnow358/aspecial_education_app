import streamlit as st
import pandas as pd
import os

# フィードバック保存用のExcelファイル
feedback_dir = r"C:\Users\taka\OneDrive\デスクトップ\GitHub\special_education_app"
feedback_file = os.path.join(feedback_dir, "feedback.xlsx")

# ディレクトリが存在しない場合、作成する
if not os.path.exists(feedback_dir):  # feedback_dir を確認する
    os.makedirs(feedback_dir)

# Excelファイルが存在しない場合、作成する
if not os.path.exists(feedback_file):
    pd.DataFrame(columns=["カテゴリー", "項目", "追加内容"]).to_excel(feedback_file, index=False, engine='openpyxl')

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
                "具体的教材の導入: 実際のボタン付きシャツやファスナーを取り付けたパネル教材を使い、繰り返し練習する。",
                "段階的指導: まずは「袖に手を通す」「ボタンをつまむ」など簡単なステップに分け、一つずつ練習を進める。",
                "視覚支援の活用: 着替えの順序をイラストや写真で示し、見通しを持たせる。",
                "実践的練習: 毎朝の登校後や体育の後など、実際の生活場面での練習を取り入れる。",
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
                "成功体験を重視: 生徒が触れられる素材や温度に合わせて成功しやすい体験を積ませ、自信を持たせる。 異なる素材の布や玩具を触る活動を取り入れ、感覚過敏を軽減。"
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
                        "家族との連携: 家庭でも手話を使えるよう、保護者向けのワークショップを実施し、共通の表現方法を増やす。",
                    ],
                },
                 {
                    "title": "ジェスチャー活用: 視覚的な動きで意思を伝える練習（例: 「飲みたい」「行きたい」など）。",
                    "details": [
                        "生活場面に応じた練習: 「飲みたい」→水を指差す、「行きたい」→ドアを指差す、など具体的な場面での練習。",
                        "絵カードとの併用: ジェスチャーと同時にピクトグラムを使い、視覚的に補助する。ジェスチャーの意味を明確に伝えやすくなる。",
                        "家族との連携: 家庭でも手話を使えるよう、保護者向けのワークショップを実施し、共通の表現方法を増やす。",
                    ],
                },
                {
                    "title": "指文字練習: 手話に加え、指文字を活用する場面を設定。",
                    "details": [
                        "名前や身近な単語から練習: 生徒自身の名前や友達の名前を指文字で表現するところからスタート。",
                        "指文字を使ったスピードゲーム: 生徒に単語を出題し、指文字で早く表現できるか競争することで楽しみながら習得。",
                        "日記での活用: 1日の出来事を指文字で表現する練習を取り入れる。",
                    ],
                },
            ],
            "視覚的支援": [
                {
                    "title": "タイムラインやカードの提示",
                    "details": [
                        "1日の流れを図示: 朝、昼、放課後など、具体的な時間帯ごとの活動を絵や写真で示すタイムラインを作成。",
                        "カラーカードの使用: 指示の優先順位を「赤＝すぐに」「青＝後で」と色分けして伝える。",
                        ": 生徒自身で作成する活動: 例えば「静かにする」カードを自分でデザインし、ルールを覚えながら製作。学校全体での活用: そのカードをクラス全員で使い、共通の視覚的ルールを浸透させる。",
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
                        "点字ブロックを使ったミニゲーム: ゴール地点を設定し、点字ブロックに沿って歩き目的地にたどり着く練習を行う。",
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
    "ダウン症のある生徒": {
            "コミュニケーションスキルの向上": [
                 {
                    "title": "ゆっくりした発話練習",
                    "details": [
                        "短いフレーズの反復練習: 「おはようございます」など、3～5文字程度の短いフレーズをカードや音声教材を使って反復。",
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
                        "身振りの活用場面を設定: 例：「静かに」を示す指一本のジェスチャー、「こっちに来て」を示す手招きなど。",
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
                        "部分的な練習から始める: 例：靴を脱ぐ→履くの順番から、徐々に衣服全体の着脱に移行。",
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
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                    ],
                },
                 {
                    "title": "",
                    "details": [
                        "",
                        "",
                    ],
                },
                
                   
            ],
        },
    },
}



# 指導支援内容表示
if menu == "指導支援内容":
    
    # カテゴリー選択
    selected_category = st.selectbox("1. カテゴリーを選択してください:", list(guidance_data.keys()))
    # サブカテゴリー選択
    selected_subcategory = st.selectbox(
        "2. 該当する項目を選択してください:", list(guidance_data[selected_category].keys())
    )

    # 辞書かリストかを確認して処理
    subcategory_data = guidance_data[selected_category][selected_subcategory]

    if isinstance(subcategory_data, dict):
        selected_detail = st.selectbox(
            "3. 具体的な支援内容を選択してください:",
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
        st.subheader("📌 適した指導・支援")

        # リストの場合、要素の内容を整形して表示
        if isinstance(detail_data, list):
            for item in detail_data:
                if isinstance(item, dict):  # 辞書の場合
                    st.markdown(f"**{item.get('title', 'タイトルなし')}**")
                    details = item.get("details", [])
                    for detail in details:
                        # 各詳細をエクスパンダーで表示
                        with st.expander(detail.split(":")[0]):  # 冒頭をタイトルに
                            st.write(detail)
                else:  # 文字列の場合
                    st.write(f"- {item}")
        else:
            st.write(detail_data)
