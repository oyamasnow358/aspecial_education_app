import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from io import BytesIO

# --- ▼ 共通CSSの読み込み ▼ ---
def load_css():
    """カスタムCSSを読み込む関数"""
    css = """
    <style>
        /* --- 背景画像の設定 --- */
        [data-testid="stAppViewContainer"] > .main {
            background-image: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        /* --- 戻るボタンのスタイル (位置調整) --- */
        .back-button-container {
            position: relative; /* relativeにして通常のフローで配置 */
            padding-bottom: 20px; /* 下に余白 */
            margin-bottom: -50px; /* 上の要素との重なりを調整 */
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
            transition: box-shadow 0.3s ease-in-out, transform 0 0.3s ease-in-out;
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
        .st-emotion-cache-1wivap1 {
             background-color: rgba(232, 245, 253, 0.7);
             border-left: 5px solid #4a90e2;
             border-radius: 8px;
        }
        
        /* --- ▼▼▼ st.expanderのデフォルトアイコンをカスタマイズ ▼▼▼ --- */
        [data-testid="stExpanderToggleIcon"] {
            display: none; /* デフォルトアイコンを非表示 */
        }
        .st-emotion-cache-p2n28p button { /* st.expanderのボタン全体 */
            background-color: #4a90e2; /* 青色の背景 */
            color: white; /* 白い文字 */
            font-weight: bold;
            border-radius: 10px; /* 角を丸くする */
            padding: 15px 20px; /* パディングを増やす */
            width: 100%; /* 幅をいっぱいに */
            text-align: left; /* テキストを左寄せ */
            transition: background-color 0.3s, transform 0.3s;
            margin-bottom: 10px; /* 下に余白 */
            border: none; /* ボーダーを削除 */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 影を追加 */
            font-size: 1.2em; /* フォントサイズを大きく */
        }

        .st-emotion-cache-p2n28p button:hover {
            background-color: #8A2BE2; /* ホバーで紫色 */
            transform: translateY(-3px); /* 少し上に浮き上がる */
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* 影を濃くする */
        }
        /* 展開時のボタンのスタイル */
        .st-emotion-cache-p2n28p[aria-expanded="true"] button {
             background-color: #8A2BE2; /* 展開時は紫色 */
             color: white;
        }

        /* 展開アイコン（右矢印）を追加 */
        .st-emotion-cache-p2n28p button::after {
            content: '▼'; /* 閉じた状態のアイコン */
            float: right;
            font-size: 1em;
            margin-left: 10px;
            transition: transform 0.3s;
        }
        .st-emotion-cache-p2n28p[aria-expanded="true"] button::after {
            content: '▲'; /* 開いた状態のアイコン */
            transform: rotate(0deg); /* 展開時は上向き */
        }
        
        /* st.expanderのコンテンツ部分のパディング */
        div[data-testid="stExpander"] div[data-testid="stVerticalBlock"] {
            padding-top: 10px;
            padding-bottom: 10px;
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
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
# --- ▲ 共通CSSの読み込み ▲ ---

# CSSを適用
load_css()

# --- ▼ 戻るボタンの配置 (メインコンテンツの左上) ▼ ---
# st.columnsを使って、左端に配置する
col_back, _ = st.columns([0.15, 0.85]) # ボタン用に狭いカラムを確保
with col_back:
    # `st.page_link` を使用すると、直接ページに遷移できてより確実です。
    st.page_link("tokusi_app.py", label="« TOPページに戻る", icon="🏠")
# --- ▲ 戻るボタンの配置 ▲ ---

st.title("🤖 個別の支援計画・指導計画作成サポート")

st.info(
    """
    ここでは、個別の支援計画・指導計画に関する文章を作成するためのプロンプト（AIへの命令文）を簡単に作成できます。
    下の各セクションをボタンで展開し、必要な項目を入力してプロンプトを生成してください。
    """
)

# --- ▼▼▼ AIチャットへのリンク ▼▼▼ ---
with st.container(border=True):
    st.markdown("""
    <div style="background-color: #e9f5ff; padding: 15px 20px; border: 2px solid #4a90e2; border-radius: 10px;">
        <h2 style="margin-top: 0; color: #2c3e50; border-left: none; text-align: center;">
            🚀 プロンプトをコピーしたら、AIチャットへ！
        </h2>
        <p style="text-align: center; font-size: 1.1em; margin-bottom: 15px;">
            下のボタンを押すと各AIチャットが開きます。コピーしたプロンプトを貼り付けて、文章作成を始めましょう。
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ボタンを中央に配置するための列
    b_col1, b_col2, b_col3 = st.columns([1, 1.5, 1])
    with b_col2:
        st.link_button("ChatGPT を開いて文章作成を始める ↗", "https://chat.openai.com/", type="primary", use_container_width=True)

    # Geminiへのリンクを追加（type="primary"に変更）
    st.markdown("<br>", unsafe_allow_html=True) # 少し余白を追加
    b_col_g1, b_col_g2, b_col_g3 = st.columns([1, 1.5, 1])
    with b_col_g2:
        st.link_button("Gemini を開いて文章作成を始める ↗", "https://gemini.google.com/", type="primary", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True) # 少し余白を追加

# --- 「岩槻はるかぜ特別支援学校の人」ボタンと機能追加 ---
st.header("✨ 特別支援学校向け機能")
if st.button("岩槻はるかぜ特別支援学校の人", use_container_width=True, type="secondary"):
    st.session_state["show_iwatsuki_features"] = not st.session_state.get("show_iwatsuki_features", False)

if st.session_state.get("show_iwatsuki_features", False):
    st.subheader("AIの出力をExcelに貼り付け")
    st.info("AIの出力内容を以下のテキストエリアに貼り付け、対応するシートとセルを指定してExcelファイルをダウンロードしてください。")

    # Excelシートとセル情報の定義
    excel_mappings = {
        "プランA": {
            "特別な教育的ニーズ": "D12",
            "合理的配慮の実施内容": "D15",
            "目標・機関名": "D18",
            "支援内容": "E18"
        },
        "プランB": {
            "指導方針": "C5",
            "1健康の保持": "D8",
            "2心理的な安定": "D10",
            "3人間関係の形成": "D12",
            "4環境の把握": "D14",
            "5身体の動き": "D16",
            "6コミュニケーション": "D18",
            "7その他": "D20",
        }
    }

    # 各項目と対応するテキストエリア、シート、セル
    ai_output_inputs = {}
    for sheet_name, cells in excel_mappings.items():
        st.markdown(f"#### シート: {sheet_name}")
        for label, cell_address in cells.items():
            key = f"{sheet_name}_{label}"
            ai_output_inputs[key] = st.text_area(f"「{label}」の内容をここに貼り付け（セル: {cell_address}）", key=key, height=150)

    if st.button("Excelに書き出してダウンロード", type="primary", use_container_width=True):
        try:
            # プロジェクトと同じ階層にあるプラン.xlsxを読み込む
            # st.cache_dataやst.cache_resourceはファイル読み込みには適さないため、直接読み込む
            workbook = load_workbook("プラン.xlsx")
            
            # 各シートにデータを書き込む
            for sheet_name, cells in excel_mappings.items():
                if sheet_name in workbook.sheetnames:
                    sheet = workbook[sheet_name]
                    for label, cell_address in cells.items():
                        key = f"{sheet_name}_{label}"
                        content = ai_output_inputs.get(key, "")
                        
                        # セルに内容を書き込み
                        sheet[cell_address] = content
                        
                        # 結合セルに対応（D12~H12など）
                        if sheet_name == "プランＡ":
                            if label == "特別な教育的ニーズ":
                                sheet.merge_cells('D12:H12')
                                sheet['D12'].alignment = Alignment(wrap_text=True, vertical='top')
                            elif label == "合理的配慮の実施内容":
                                sheet.merge_cells('D15:H15')
                                sheet['D15'].alignment = Alignment(wrap_text=True, vertical='top')
                            elif label == "支援内容": # E18はF18と結合
                                sheet.merge_cells('E18:F18')
                                sheet['E18'].alignment = Alignment(wrap_text=True, vertical='top')
                        elif sheet_name == "プランＢ(実態)":
                            if label == "指導方針":
                                sheet.merge_cells('C5:F5')
                                sheet['C5'].alignment = Alignment(wrap_text=True, vertical='top')
                            elif label.startswith("1") or label.startswith("2") or label.startswith("3") or \
                                 label.startswith("4") or label.startswith("5") or label.startswith("6") or \
                                 label.startswith("7"):
                                # 指導に結びつく実態のD列はF列まで結合
                                # 例: "1健康の保持": "D8" -> D8:F8
                                col_start = cell_address[0] # D
                                row_num = cell_address[1:] # 8
                                sheet.merge_cells(f'{col_start}{row_num}:F{row_num}')
                                sheet[cell_address].alignment = Alignment(wrap_text=True, vertical='top')

                        # テキストの折り返しと上部揃えを設定 (結合セルも考慮)
                        sheet[cell_address].alignment = Alignment(wrap_text=True, vertical='top')
                else:
                    st.warning(f"Excelファイルにシート「{sheet_name}」が見つかりませんでした。")

            # 変更をBytesIOに保存してダウンロード可能にする
            excel_file = BytesIO()
            workbook.save(excel_file)
            excel_file.seek(0) # ファイルの先頭に戻る

            st.download_button(
                label="ダウンロード「プラン.xlsx」",
                data=excel_file,
                file_name="プラン_更新版.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary"
            )
            st.success("Excelファイルが正常に更新され、ダウンロード準備ができました！")

        except FileNotFoundError:
            st.error("エラー: 'プラン.xlsx' ファイルが見つかりませんでした。WEBアプリと同じ階層に配置されていることを確認してください。")
        except Exception as e:
            st.error(f"Excelファイルの書き込み中にエラーが発生しました: {e}")

st.markdown("---") # 区切り線

# --- プロンプト① ---
with st.expander("プロンプト①【プランA：特別な教育的ニーズ／合理的配慮】"):
    with st.container(border=True):
        st.subheader("プロンプト①【プランA：特別な教育的ニーズ／合理的配慮】") # expanderの中ではsubheaderにする
        jittai_1 = st.text_area("✅ お子さんの実態や課題を入力", value="視力が弱い、落ち着きがない、疲れやすい、音に敏感、話しかけられると混乱する、同じ行動を繰り返す", height=100, key="jittai_1")
        if st.button("プロンプト① を生成", key="btn_1", use_container_width=True):
            st.code(f"""以下の実態や課題をもとに、特別支援教育に関する「プランA」の以下の項目を作成してください。

【入力】実態や課題：
{jittai_1}

【出力項目】：
1.特別な教育的ニーズ

・入力から共通性を見出し、2～3つの抽象的カテゴリーに分類する（表記は①～③の形【※必ずしも③まで必要としない入力内容や添付資料により臨機応変に】）。
・各ニーズは20〜100字程度で、児童・生徒の実態を柔らかく教育的にまとめる。
・具体的な出力の形【出力フォーマット】
対象児童（生徒）は現在、以下の状況である。【←必ずこの文言で始める】
① （入力内容を整理してまとめた課題、困難さ、特徴）
② （入力内容を整理してまとめた課題、困難さ、特徴）
③ （入力内容を整理してまとめた課題、困難さ、特徴）
※ 内容は「日常生活・学習・コミュニケーション・行動・身体・感覚・心理」などから、入力内容に応じて適切に選んでまとめること。

従って、以下の支援が必要である。【←必ずこの文言で始める】
① （①の状況に対応した支援目標や方法）
② （②の状況に対応した支援目標や方法）
③ （③の状況に対応した支援目標や方法）

支援に当たっては、以下の配慮が必要である。【←必ずこの文言で始める】
① （①の状況に対応した配慮）
② （②の状況に対応した配慮）
③ （③の状況に対応した配慮）

2.合理的配慮の実施内容
・上記①のニーズに対応した合理的配慮を少なくとも2つ以上提案する。
・シンプルに2つ以上箇条書きで示す。（例：「具体物を示し、視覚的な支援を行う。」、「落ち着ける環境設定にする。」、「生徒が好きな感触の本や音の出る玩具等を教室内に用意し、心理的安定を図る。」など）。

【条件】：
- 添付資料がある場合（「プランA」や「個別の教育支援計画」）にある書き方を参考にしてください。
- この後、この「特別な教育的ニーズ」を「特別な教育的ニーズ」⇒「所属校の支援目標」及び「各目標に連動した支援内容」⇒「指導方針」（プランBや個別の指導計画）の順で具体化していくのでそのつもりで抽象的に表現する。
- 「～です。～ます。」調ではなく、「～である。」調で文章を作成してください。
- 各項目の文量は200〜300文字程度で、柔らかく教育的な表現で整えてください。""", language="text")

# --- プロンプト② ---
with st.expander("プロンプト②【プランA：所属校の支援】"):
    with st.container(border=True):
        st.subheader("プロンプト②【プランA：所属校の支援】")
        needs_2 = st.text_area("✅ プロンプト①でAIが生成した「特別な教育的ニーズ」を貼り付け", value="① 感覚過敏があり、環境刺激に影響を受けやすい\n② 注意の持続が難しく、集中が途切れやすい\n③ コミュニケーションに混乱が見られ、一斉指示に反応しづらい", height=150, key="needs_2")
        if st.button("プロンプト② を生成", key="btn_2", use_container_width=True):
            st.code(f"""以下の「特別な教育的ニーズ」に基づいて、「所属校による支援計画（プランA）」の項目を作成してください。

【参考】特別な教育的ニーズ：
{needs_2}

【出力項目】：
・1所属校の支援目標・機関名、2支援内容のプロンプトを生成　※機関名はそういう表記がされているだけで、意味は無視して良いタイトルはそのままで。
1.所属校の支援目標・機関名  
（特別な教育的ニーズの①～③に対応して作成。②までしかない場合は②まででよい。）

①目標：（30字以内程度・短くてもよい）  
②目標：（30字以内程度・短くてもよい）    
③目標：（30字以内程度・短くてもよい）  

2.支援内容  
（上記の①～③の目標それぞれに対応して作成。）

①（50字以内程度で、学校現場で実践可能な支援内容を記載）  
②（50字以内程度で、学校現場で実践可能な支援内容を記載）  
③（50字以内程度で、学校現場で実践可能な支援内容を記載）

・具体的な出力の形【出力フォーマット】 
このような抽象的な表現でよい（次のプロンプトでより具体化するため）。  


【条件】：
- 「特別な教育的ニーズ」と対応が分かるように①～③の番号を揃えること。  
- 各文は短くてもよいが、教育的で柔らかい表現にすること。  
- 「～です。～ます。」調ではなく、「～である。」調で統一すること。  
- 添付資料（「プランA」や「個別の教育支援計画」）の書き方を参考にしてよい。  
- ここでは抽象的にまとめ、**次の段階（プランBなど）で具体化していくための基礎**として作成すること。""", language="text")

# --- プロンプト③ ---
with st.expander("プロンプト③【プランB：指導方針・7項目の実態】"):
    with st.container(border=True):
        st.subheader("プロンプト③【プランB：指導方針・7項目の実態】")
        jittai_3 = st.text_area("✅ お子さんの実態や課題を入力（プロンプト①と同じでOK）", value="視力が弱い、落ち着きがない、疲れやすい、音に敏感、話しかけられると混乱する、同じ行動を繰り返す", height=100, key="jittai_3")
        if st.button("プロンプト③ を生成", key="btn_3", use_container_width=True):
            st.code(f"""以下の実態・課題をもとに、特別支援計画「プランB」の項目を作成してください。

【入力】実態・課題：
{jittai_3}

【出力項目】

1.指導方針
・「特別な教育的ニーズ①～③」と「所属校の支援目標①～③」を踏まえ、より具体的な指導の方向性を示す。
・児童生徒の実態を冒頭で丁寧に描写し、その後に必要な指導内容を①～③に整理する。
・全体を通して300〜500字程度とし、教育的で柔らかい表現を用いる。
・文章が長くなる場合は複数回に分けて出力してよい。

2.実態（特別支援における7区分〔箇条書きで、例：【着替え】・～の形〕）
・以下の区分ごとに項目をもうけて（内容によって項目の数に偏りがあってもよい）記述する。各区分に例を設けるので参考にしてください
① 健康の保持（日常生活面、健康面など）【着替え】【食事】【排泄】【健康上の配慮】
（この区分は多めに項目を設ける【例：【着替え】・ズボンにはワッペンをつけると前後がわかって履くことができる。・言葉かけを受けて脱いだ服の裏返しを直すことができる。・登校時はオムツを着用している。登校後に布パンツに履き替えている。・下校時は布パンツを使用する。デイサービスにより帰り際にトイレに行かせる。【食事】・食事は少量ずつ別皿に入れて提供している。また、左手をお椀に添えて、右手でスプーンや補助具付きの箸を使用して食べることができる。【排泄】・立ち便器を使うことができる。【健康上の配慮】・春は花粉症の薬を服用している。など】）
② 心理的な安定（情緒面、状況の理解など）【苦手な状況】
【例：【苦手な状況】・急な音や大きな音は苦手で、驚いて不安定になることがある。・気持ちが不安定な時は、首に掴みかかろうとしたり、噛もうとしたりすることがある。・暑い季節は苦手で、夏場は気持ちが不安定になることが多い。汗を拭くことにより気持ちが落ち着くことがある。・気持ちが不安定な時に、イヤーマフを着用している。・気持ちが不安定なときに深呼吸を促したり、教員が胸や背中をトントン叩いたりすると落ち着くことがある。（感覚統合、副交感神経）【その他】・歩いたり、身体を動かしたりすることが好きで、散歩をすることで気持ちを切り替えられることがある。・見通しの持ちやすい課題には３０分程度離席せずに取り組むことができる。・見通しの持ちにくい場面や、気持ちが向かない活動の時にはトイレに行こうとすることがある。・怒ると近くにある物を噛む癖がある。(かなり減ってきた)】
③ 人間関係の形成（人とのかかわり、集団への参加など）【大人や友達との関わり】【集団参加】
【例：【大人や友達との関わり】・教員からの呼びかけに反応し、行動することができる。・身近な大人の膝の上に乗ろうとしたり、抱き着こうとしたりするなどの身体・接触が好きである。【集団参加】・誰とでも手を繋いだり、関わったりすることができる。】
④ 環境の把握（感覚の活用、認知面、学習面など）【学習の様子】
【例：【学習の様子】・シールを自分で好きなように貼れる。丸い紙やタイルを一直線に貼れる。・色の区別ができる。・３０面までのパズルができる。・ひらがなやイラストのマッチングができる。】
⑤ 身体の動き（運動・動作、作業面など）【身体の動き】【手指の操作】
【例：【身体の動き】・音楽が好きで、聴きながら身体を動かすことができる。・ブランコに一人で乗れる。・ボールを投げることができる。支援を受けてボールを蹴ることができる。【手指の操作】・利き手がまだ定まっていないが、右手を日常的に使用する。・支援を受けてハサミやのりなどの道具を使うことができる。・粗大模倣は、教員の手本や映像を観たりしながら行うことができる。・つまむ、ひねる、回す、押すなど手指を使った活動ができる。・爪がないため微細な動きは苦手である。・自助箸を使用して食事が取れる。】
⑥ コミュニケーション（意思の伝達、言語の形成など）【ｺﾐｭﾆｹｰｼｮﾝの理解】【ｺﾐｭﾆｹｰｼｮﾝの表出】
【例：【ｺﾐｭﾆｹｰｼｮﾝの理解】・教員の指示をある程度理解していて、指示通り動くことができる。【ｺﾐｭﾆｹｰｼｮﾝの表出】・促されると､「ちょうだい」のサインを出すことができる。サインと一緒に・口を動かすことができる。サインを出している大人に物を渡すことができる。・教員を呼ぶときに、肩をトントンと叩くことができる。・「トイレ」「ごめん」など簡単な言葉の発語ができる。・排泄の意思表示は「トイレ」と伝えることができる。・口形模倣や単音の発声はできるようになってきている。】
⑦ その他（性格、行動特徴、興味関心など）【興味関心】
【例：【興味関心】・活動中に身体を大きく左右に動かしたり飛び跳ねたりするときがある。・おもちゃを床にたたきつけるように投げる。】
・【入力】の実態・課題をもとに、可能な限り多くの具体的内容を盛り込む。
・1回で書ききれない場合は、何回になってもよいので、複数回に分けて出力する。

【条件】：
- 添付資料があれば参考にしてください（プランBや個別の指導計画）。
- 「～です。～ます。」調ではなく、「～である。」調で文章を作成してください。
- 【入力】の内容だけでなく、これまでの特別な教育的ニーズと所属校の支援目標から発展させて作成する。
- 「1.指導方針」特別な教育的ニーズと所属校の支援目標より具体的な内容にする
- 「1.指導方針」は特別な教育的ニーズと所属校の支援目標の①～③に連動した形で（②までしかない場合は同様に①、②でOK）
- ① 指導方針の例：「現在、本生徒は、右目の視力が無く左目も視力が弱く視野が狭い。また、聴力は、全く聞こえていないと思われ、日常生活の殆どを教員に任せきりにしていたり、教員に対して常に触れ合い・揺さぶりなどの刺激を求めている。また、不適切な行動が多く見られ、刺激を求めて、自分の顔に唾や水・おしっこをかけたり、吹き出したりすることや物を投げたり、倒したり衝動的な行動、人とのかかわりの中で抓ったり、叩いたり、髪の毛を引っ張ったりすることがある。コミュケーション面では、手話によるサインが２～３個理解できる。また、自分で1個「トイレ」のサインを行う時がある。その他、相手の手を取り直接手を動かしての要求をすることが多い。
従って、以下の①～③の指導が必要だと考える。
　①トイレや食事、着替えなど日常生活の中で、教員に頼らずにひとりでできることを増やす。
　②不適切行動が起きた時に繰り返さないようにする。
　③絵カードや手話による要求を増やす。
これらの指導を元に本生徒の生活面での自立、行動面・コミュニケーション面での成長につなげていく。」
- 1回で書ききれない場合は、何回になってもよいので、複数回に分けて出力する。
- 指導方針は全体的な視点で、各実態は200〜300文字で丁寧に描写してください。""", language="text")

 # --- 新プロンプト④ ---
with st.expander("プロンプト④【個別の指導計画：目標と手立て】"):
    with st.container(border=True):
        st.subheader("プロンプト④【個別の指導計画：目標と手立て】")
        st.write("個別の指導計画の目標と具体的な手立てを、選択された教科ごとに生成します。")

        # 教科の選択
        subject_options = [
            "自立活動","日常生活の指導","職業","生活単元学習","作業学習","国語", "算数", "美術", "理科", "社会", "音楽", "図画工作", "体育", "家庭", 
            "外国語活動", "総合的な学習の時間", "自立活動", "日常生活の指導","保険","数学"
        ]
        selected_subjects = st.multiselect("✅ 目標と手立てを作成する教科を選択（複数選択可）", subject_options, key="selected_subjects_4")

        # 実態や課題の入力（各教科用）
        jittai_inputs_4 = {}
        st.markdown("---")
        st.subheader("💡 各教科の実態や課題を入力してください")
        for subject in selected_subjects:
            jittai_inputs_4[subject] = st.text_area(f"✅ 【{subject}】に関する内容、お子さんの実態や課題を入力",
                                                      value="（例：ミニトマトの植生を行った（種上・観察・記録・収穫・調理）",
                                                      height=100, key=f"jittai_4_{subject}")

        # 指導方針の入力（参考情報として）
        shido_hoshin_4 = st.text_area("✅ 実態や課題",
                                      value="（例：文字を読むことに抵抗がある、数の概念が理解しづらい、落ち着いて座っていられない、友達とのコミュニケーションが苦手など）、不適切行動が起きた時に繰り返さないようにする。絵カードや手話による要求を増やす。など）",
                                      height=100, key="shido_hoshin_4_global")

        if st.button("プロンプト④ を生成", key="btn_4", use_container_width=True):
            full_prompt_output = []
            for subject in selected_subjects:
                num_items = 3 if subject in ["自立活動", "日常生活の指導"] else 2
                current_jittai = jittai_inputs_4.get(subject, "")

                prompt_for_subject = f"""
以下の情報をもとに、個別の指導計画における【{subject}】の目標と手立てを作成してください。

【入力】
教科：{subject}
教科の内容：{current_jittai}
参考指導方針：{shido_hoshin_4}

【出力項目】
1. 目標（{num_items}つ）：
   ・各目標は30字以内程度で、お子さんが達成すべき具体的な行動や状態を示すこと。
   ・教育的で柔らかい表現にすること。

2. 手立て（{num_items}つ）：
   ・各手立ては30字から50字程度で、目標達成のために学校現場で実践可能な具体的な支援内容や方法を示すこと。
   ・お子さんの実態や課題、指導方針を考慮し、個別具体的な内容にすること。

【出力フォーマット例】
【{subject}】
目標：
・（目標1：30字以内）
・（目標2：30字以内）
{"・（目標3：30字以内）" if num_items == 3 else ""}

手立て：
・（手立て1：30～50字）
・（手立て2：30～50字）
{"・（手立て3：30～50字）" if num_items == 3 else ""}

【条件】：
- 「～です。～ます。」調ではなく、「～である。」調で統一してください。
- 添付資料（個別の指導計画など）がある場合は、その書き方を参考にしてください。
- 他の教科の目標や手立ては出力せず、指定された【{subject}】のみを出力してください。
- 目標と手立ての数は、自立活動と日常生活の指導は3つ以上、それ以外は2つとしてください。
- 目標と手立ての内容は、入力された実態や課題、参考指導方針と連動させて具体的に記述してください。
"""
                full_prompt_output.append(prompt_for_subject)

            st.subheader("📄 生成されたプロンプト④（コピーして使ってください）")
            if not full_prompt_output:
                st.warning("教科が選択されていません。")
            else:
                st.code("\n---\n".join(full_prompt_output), language="text") # 各教科のプロンプトを区切り線で結合して表示

# --- プロンプト⑤ ---
with st.expander("プロンプト⑤【個別の指導計画：評価】"):
    with st.container(border=True):
        st.subheader("プロンプト⑤【個別の指導計画：評価】")
        st.write("指導計画を基に、活動の様子を評価する文章を作成します。")

        use_file_4 = st.checkbox(
            "AIにWord/Excel等のファイルを添付して、主たる情報源として利用する", 
            key="use_file_4"
        )
        st.caption("💡 ファイルを添付する場合、下のテキストエリアは補足として利用できます。")

        reference_text_4 = st.text_area(
            "✅ 参考にする指導計画のテキスト（補足など）",
            value="（例：個別の指導計画の「指導の目標および内容」の全文や、特に見てほしい部分など）",
            height=150,
            key="reference_4"
        )
        
        evaluation_activities_4 = st.text_area(
            "✅ 教科ごとの「できたこと・活動の様子」を具体的に入力",
            value="【自立活動】：・教員の誘導で肩や首の力を抜き、胸を張った姿勢で活動できた。・片手で支えながら片足立ちができた。\n【国語】：自分の名前を丁寧になぞり書きできた。",
            height=150,
            key="evaluation_activities_4"
        )

        if st.button("プロンプト⑤ を生成", key="btn_5", use_container_width=True):
            prompt_intro_4 = ""
            prompt_main_source_4 = ""

            if use_file_4:
                prompt_intro_4 = "添付した指導計画のファイルを主たる情報源とし、"
                if reference_text_4.strip() and reference_text_4 != "（例：個別の指導計画の「指導の目標および内容」の全文や、特に見てほしい部分など）":
                    prompt_main_source_4 = f"以下の【参考テキスト】も補足情報として考慮した上で、"
                else:
                     prompt_main_source_4 = "以下の"

            else:
                prompt_intro_4 = "以下の【指導計画のテキスト】を主たる情報源として、"
            
            prompt_text_part_4 = f"""【指導計画のテキスト】：
{reference_text_4}
""" if not use_file_4 or (use_file_4 and reference_text_4.strip() and reference_text_4 != "（例：個別の指導計画の「指導の目標および内容」の全文や、特に見てほしい部分など）") else ""


            prompt_full_4 = f"""{prompt_intro_4}{prompt_main_source_4}【できたこと・活動の様子】とを関連付けながら、教科ごとの「個別の指導の評価」（振り返り文）を作成してください。
{prompt_text_part_4}
【できたこと・活動の様子】：
{evaluation_activities_4}

【出力ルール】：
- まず、主たる情報源（添付ファイルまたは上記テキスト）を読み込み、そこに書かれている目標や内容を完全に理解してください。
- 「～です。～ます。」調ではなく、「～である。」調で文章を作成してください。
- その上で、【できたこと・活動の様子】が、計画のどの目標・内容に対応するのかを分析し、目標の達成度合いが分かるように評価文を作成してください。
- 計画で言及されているすべての教科・領域について、評価文を個別に出力してください。
- 各教科について、【教科名の見出し】と200～300文字程度の評価文を作成してください。
- 文体は、実務で使用されるような柔らかく教育的な表現にしてください。"""

            st.subheader("📄 生成されたプロンプト⑤（コピーして使ってください）")
            st.code(prompt_full_4, language="text")


# --- プロンプト⑥ ---
with st.expander("プロンプト⑥【前期・後期の所見】"):
    with st.container(border=True):
        st.subheader("プロンプト⑥【前期・後期の所見】")
        st.write("評価文や計画書を基に、総合的な所見を作成します。")

        term_choice = st.radio("どちらの所見を作成しますか？", ("前期", "後期／学年末"), key="term_choice", horizontal=True)

        use_file_5 = st.checkbox(
            "AIに評価文等のファイルを添付して、主たる情報源として利用する",
            key="use_file_5"
        )
        st.caption("💡 ファイルを添付する場合、下のテキストエリアは補足として利用できます。")

        reference_text_5 = st.text_area(
            "✅ 参考にする評価文や計画のテキスト（補足など）",
            value="（例：プロンプト④で作成した評価文の全体、または特に見てほしい部分など）",
            height=200,
            key="reference_5"
        )
        
        shoken_input = st.text_area(
            "✅ 所見で特に強調したいポイントを入力（箇条書きでOK）",
            value="- 大きなけがもなく元気に登校できたことの喜び。\n- 友人との関わりが前向きになった点。\n- 宿泊学習などの大きな行事を乗り越えた自信。\n- 家庭との連携への感謝。",
            height=150,
            key="shoken_input"
        )

        if st.button("プロンプト⑥ を生成", key="btn_6", use_container_width=True):
            prompt_intro_5 = ""
            prompt_main_source_5 = ""

            if use_file_5:
                prompt_intro_5 = "添付したファイル（評価文や計画書など）を主たる情報源とし、"
                if reference_text_5.strip() and reference_text_5 != "（例：プロンプト④で作成した評価文の全体、または特に見てほしい部分など）":
                    prompt_main_source_5 = "以下の【参考テキスト】も補足情報として考慮し、"
                else:
                    prompt_main_source_5 = ""
            else:
                prompt_intro_5 = "以下の【参考テキスト】を主たる情報源として、"

            prompt_text_part_5 = f"""【参考テキスト】：
{reference_text_5}
""" if not use_file_5 or (use_file_5 and reference_text_5.strip() and reference_text_5 != "（例：プロンプト④で作成した評価文の全体、または特に見てほしい部分など）") else ""

            if term_choice == "前期":
                specific_conditions = """- 「前期は、〜」といった書き出しで始めてください。
- 200～400文字程度の文章量で作成してください。
- 文末には「後期も引き続き、ご家庭と連携を取りながら、成長を見守っていきたいと思います。よろしくお願いいたします。」など、後期への連携を意識した一文を入れてください。"""
            else: # 後期／学年末
                specific_conditions = """- 「この1年間で〜」や「いよいよ来年度は〜」など、年度の区切りを感じさせる書き出しにしてください。
- 200〜450文字程度の文章量で作成してください。
- 文末には、保護者への感謝と、次年度に向けた応援の言葉を必ず含めてください。"""

            prompt_full_5 = f"""{prompt_intro_5}{prompt_main_source_5}さらに【強調したいポイント】を盛り込みながら、保護者向けの「{term_choice}の所見」を作成してください。
{prompt_text_part_5}
【強調したいポイント】：
{shoken_input}

【全体の共通条件】：
- 主たる情報源（添付ファイルまたは上記テキスト）から全体的な成長の様子を読み取り、【強調したいポイント】を特に意識して、自然な文章を作成してください。
- 添付資料内に具体的事象（例：大きな行事の達成、友人とのやりとり、けがの有無）がある場合は具体例を1つ以上挙げて所見に反映すること。
- 丁寧な語り口で、前向きな表現を心がけてください。
- 保護者の方が読んで、お子さんの具体的な成長が伝わるような文章にしてください。
- 「～です。～ます。」調ではなく、「～である。」調で文章を作成してください。
- もし【入力】や添付資料の内容が極端に短い・情報不足な場合は、前期は200字、後期は200字を下回らないように、実務的に妥当な記述を参考テキストに基づき推測して補完すること

【{term_choice}用の個別条件】：
{specific_conditions}"""

            st.subheader(f"📄 生成されたプロンプト⑥（{term_choice}の所見用）")
            st.code(prompt_full_5, language="text")

st.markdown("---")
st.warning("""
**【利用上の注意】**
AIが生成する内容は、入力された情報に基づく提案であり、必ずしも正確性や適切性を保証するものではありません。自分の判断と合わせてご活用ください。
""")