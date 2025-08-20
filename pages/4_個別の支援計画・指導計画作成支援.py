import streamlit as st

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

  
        /* --- 全体のフォント --- */
        html, body, [class*="st-"] {
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
        }

        /* --- 見出しのスタイル --- */
        h1, h2, h3 {
            color: #2c3e50;
        }
        h1 {
            text-align: center;
        }
        h2 {
            border-left: 6px solid #8A2BE2;
            padding-left: 12px;
            margin-top: 40px;
        }
        h3 {
            border-bottom: 2px solid #4a90e2;
            padding-bottom: 8px;
            margin-top: 30px;
        }

        /* --- カードデザイン --- */
        div[data-testid="stVerticalBlock"] div.st-emotion-cache-1r6slb0 {
            background-color: rgba(255, 255, 255, 0.95);
            border: 1px solid #e0e0e0;
            border-radius: 15px;
            padding: 1.5em 1.5em;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
            margin-bottom: 20px;
        }
        
        /* --- ボタンのスタイル --- */
        .stButton>button {
            border-radius: 25px;
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button[kind="primary"] {
            background-color: #4a90e2;
            color: white;
            border: none;
        }
        .stButton>button[kind="primary"]:hover {
            background-color: #357ABD;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
# --- ▲ 共通CSSの読み込み ▲ ---

# CSSを適用
load_css()

st.title("🤖 個別の支援計画・指導計画作成サポート")

st.info(
    """
    ここでは、個別の支援計画・指導計画に関する文章を作成するためのプロンプト（AIへの命令文）を簡単に作成できます。
    下の各セクションで必要な項目を入力し、プロンプトを生成してください。
    """
)

# --- ▼▼▼ ChatGPTへのリンク ▼▼▼ ---
with st.container(border=True):
    st.markdown("""
    <div style="background-color: #e9f5ff; padding: 15px 20px; border: 2px solid #4a90e2; border-radius: 10px;">
        <h2 style="margin-top: 0; color: #2c3e50; border-left: none; text-align: center;">
            🚀 プロンプトをコピーしたら、ChatGPTへ！
        </h2>
        <p style="text-align: center; font-size: 1.1em; margin-bottom: 15px;">
            下のボタンを押すとChatGPTが開きます。コピーしたプロンプトを貼り付けて、文章作成を始めましょう。
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ボタンを中央に配置するための列
    b_col1, b_col2, b_col3 = st.columns([1,1.5,1])
    with b_col2:
        st.link_button("ChatGPT を開いて文章作成を始める ↗", "https://chat.openai.com/", type="primary", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True) # 少し余白を追加

# --- プロンプト① ---
with st.container(border=True):
    st.header("プロンプト①【プランA：特別な教育的ニーズ／合理的配慮】")
    jittai_1 = st.text_area("✅ お子さんの実態や課題を入力", value="視力が弱い、落ち着きがない、疲れやすい、音に敏感、話しかけられると混乱する、同じ行動を繰り返す", height=100, key="jittai_1")
    if st.button("プロンプト① を生成", key="btn_1", use_container_width=True):
        st.code(f"""以下の実態や課題をもとに、特別支援教育に関する「プランA」の以下の項目を作成してください。

【入力】実態や課題：
{jittai_1}

【出力項目】：
① 特別な教育的ニーズ（2つ～3つに分類【抽象的でよい】）
② 上記ニーズ①～③と連動した、合理的配慮の実施内容（2つ以上）

【条件】：
- 添付資料があれば参考にしてください。
- 各項目の文量は200〜300文字程度で、柔らかく教育的な表現で整えてください。""", language="text")

# --- プロンプト② ---
with st.container(border=True):
    st.header("プロンプト②【プランA：所属校の支援】")
    needs_2 = st.text_area("✅ プロンプト①でAIが生成した「特別な教育的ニーズ」を貼り付け", value="① 感覚過敏があり、環境刺激に影響を受けやすい\n② 注意の持続が難しく、集中が途切れやすい\n③ コミュニケーションに混乱が見られ、一斉指示に反応しづらい", height=150, key="needs_2")
    if st.button("プロンプト② を生成", key="btn_2", use_container_width=True):
        st.code(f"""以下の「特別な教育的ニーズ」に基づいて、「所属校による支援計画（プランA）」の項目を作成してください。

【参考】特別な教育的ニーズ：
{needs_2}

【出力項目】：
① 所属校の支援目標（2つ～3つ【特別な教育的ニーズの数に合わせて、特別な教育的ニーズの①～③に連動しさせる】）
② 各目標に連動した支援内容（2つ～3つ【支援目標に数を合わせる】）

【条件】：
- 添付資料があれば参考にしてください。
- 各項目は、ニーズに対応した実践的な内容を200文字前後で記述してください。""", language="text")

# --- プロンプト③ ---
with st.container(border=True):
    st.header("プロンプト③【プランB：指導方針・7項目の実態】")
    jittai_3 = st.text_area("✅ お子さんの実態や課題を入力（プロンプト①と同じでOK）", value="視力が弱い、落ち着きがない、疲れやすい、音に敏感、話しかけられると混乱する、同じ行動を繰り返す", height=100, key="jittai_3")
    if st.button("プロンプト③ を生成", key="btn_3", use_container_width=True):
        st.code(f"""以下の実態・課題をもとに、特別支援計画「プランB」の項目を作成してください。

【入力】実態・課題：
{jittai_3}

【出力項目】：
① 指導方針（具体的に【特別な教育的ニーズ①～③及び、所属校の支援目標①～③と連動させる】）
② 実態【特別支援に蹴る6区分】（健康・生活／心理／行動／人間関係・集団参加／学習／身体・感覚／家庭・地域との連携）

【条件】：
- 添付資料があれば参考にしてください。
- 【入力】の内容だけではなく、今までのやり取りから想定して作成してください。
- 特別な教育的ニーズと所属校の支援目標より具体的な内容にする
- 特別な教育的ニーズと所属校の支援目標の①～③に連動した形で
- ① 指導方針の例：「現在、本生徒は、右目の視力が無く左目も視力が弱く視野が狭い。また、聴力は、全く聞こえていないと思われ、日常生活の殆どを教員に任せきりにしていたり、教員に対して常に触れ合い・揺さぶりなどの刺激を求めている。また、不適切な行動が多く見られ、刺激を求めて、自分の顔に唾や水・おしっこをかけたり、吹き出したりすることや物を投げたり、倒したり衝動的な行動、人とのかかわりの中で抓ったり、叩いたり、髪の毛を引っ張ったりすることがある。コミュケーション面では、手話によるサインが２～３個理解できる。また、自分で1個「トイレ」のサインを行う時がある。その他、相手の手を取り直接手を動かしての要求をすることが多い。
従って、以下の①～③の指導が必要だと考える。
　①トイレや食事、着替えなど日常生活の中で、教員に頼らずにひとりでできることを増やす。
　②不適切行動が起きた時に繰り返さないようにする。
　③絵カードや手話による要求を増やす。
これらの指導を元に本生徒の生活面での自立、行動面・コミュニケーション面での成長につなげていく。」
- 文章が長くなる場合は2回分けてください。
- 指導方針は全体的な視点で、各実態は200〜300文字で丁寧に描写してください。""", language="text")

# --- プロンプト④ ---
with st.container(border=True):
    st.header("プロンプト④【個別の指導計画：評価】")
    st.write("指導計画を基に、活動の様子を評価する文章を作成します。")

    use_file_4 = st.checkbox(
        "ChatGPTにWord/Excel等のファイルを添付して、主たる情報源として利用する", 
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

    if st.button("プロンプト④ を生成", key="btn_4", use_container_width=True):
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
- その上で、【できたこと・活動の様子】が、計画のどの目標・内容に対応するのかを分析し、目標の達成度合いが分かるように評価文を作成してください。
- 計画で言及されているすべての教科・領域について、評価文を個別に出力してください。
- 各教科について、【教科名の見出し】と200～300文字程度の評価文を作成してください。
- 文体は、実務で使用されるような柔らかく教育的な表現にしてください。"""

        st.subheader("📄 生成されたプロンプト④（コピーして使ってください）")
        st.code(prompt_full_4, language="text")


# --- プロンプト⑤ ---
with st.container(border=True):
    st.header("プロンプト⑤【前期・後期の所見】")
    st.write("評価文や計画書を基に、総合的な所見を作成します。")

    term_choice = st.radio("どちらの所見を作成しますか？", ("前期", "後期／学年末"), key="term_choice", horizontal=True)

    use_file_5 = st.checkbox(
        "ChatGPTに評価文等のファイルを添付して、主たる情報源として利用する",
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

    if st.button("プロンプト⑤ を生成", key="btn_5", use_container_width=True):
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
- 丁寧な語り口で、前向きな表現を心がけてください。
- 保護者の方が読んで、お子さんの具体的な成長が伝わるような文章にしてください。

【{term_choice}用の個別条件】：
{specific_conditions}"""

        st.subheader(f"📄 生成されたプロンプト⑤（{term_choice}の所見用）")
        st.code(prompt_full_5, language="text")

st.markdown("---")
st.warning("""
**【利用上の注意】**
AIが生成する内容は、入力された情報に基づく提案であり、必ずしも正確性や適切性を保証するものではありません。自分の判断と合わせてご活用ください。
""")
