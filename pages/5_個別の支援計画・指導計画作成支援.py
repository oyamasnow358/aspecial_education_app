import streamlit as st

# --- ▼ 共通CSSの読み込み（メインページからコピー） ▼ ---
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
            margin-bottom: 20px; /* カード間の余白 */
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
        }

        /* --- st.infoのカスタムスタイル --- */
        .st-emotion-cache-1wivap1 { /* st.infoのコンテナ */
             background-color: rgba(232, 245, 253, 0.7); /* 淡い青 */
             border-left: 5px solid #4a90e2;
             border-radius: 8px;
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
    必要な項目を入力し、「プロンプトを生成」ボタンを押してください。
    生成されたプロンプトをコピーし、ChatGPTなどのAIチャットに貼り付けて使用します。
    """
)

# ChatGPTへのリンク
st.markdown("---")
col1, col2 = st.columns([3, 1])
with col1:
    st.write("#### プロンプトをコピーしたら、下のボタンからChatGPTを開いて貼り付け！")
with col2:
    st.link_button("ChatGPT を開く ↗", "https://chat.openai.com/", type="primary", use_container_width=True)
st.markdown("---")


# --- プロンプト① ---
with st.container(border=True):
    st.header("プロンプト①【プランA：特別な教育的ニーズ／合理的配慮】")
    jittai_1 = st.text_area(
        "✅ お子さんの実態や課題を入力してください",
        value="視力が弱い、落ち着きがない、疲れやすい、音に敏感、話しかけられると混乱する、同じ行動を繰り返す",
        height=100, key="jittai_1"
    )
    if st.button("プロンプト① を生成", key="btn_1", use_container_width=True):
        prompt_text_1 = f"""以下の実態や課題をもとに、特別支援教育に関する「プランA」の以下の項目を作成してください。

【入力】実態や課題（単語や短文、複数）：
{jittai_1}

【出力項目】：
① 特別な教育的ニーズ（3つに分類）
② 上記ニーズ①～③と連動した、合理的配慮の実施内容（3つ）

【条件】：
- 「特別な教育的ニーズ」は、入力された情報を3つの観点から分類し、①〜③として明確に提示してください。
- 「合理的配慮の実施内容」は、上記①〜③のニーズそれぞれに対応した具体的な支援内容を記述してください。
- 各項目の文量は200〜300文字程度。
- 添付資料の文体（柔らかく、教育的な表現）を参考にし、読んで納得しやすい表現で整えてください。"""
        st.subheader("📄 生成されたプロンプト①（コピーして使ってください）")
        st.code(prompt_text_1, language="text")

# --- プロンプト② ---
with st.container(border=True):
    st.header("プロンプト②【プランA：所属校の支援】")
    needs_2 = st.text_area(
        "✅ プロンプト①でAIが生成した「特別な教育的ニーズ①〜③」をここに貼り付けてください",
        value="① 感覚過敏があり、環境刺激に影響を受けやすい\n② 注意の持続が難しく、集中が途切れやすい\n③ コミュニケーションに混乱が見られ、一斉指示に反応しづらい",
        height=150, key="needs_2"
    )
    if st.button("プロンプト② を生成", key="btn_2", use_container_width=True):
        prompt_text_2 = f"""以下の「特別な教育的ニーズ①〜③」に基づいて、「所属校による支援計画（プランA）」の以下項目を作成してください。

【参考】特別な教育的ニーズ：
{needs_2}

【出力項目】：
① 所属校の支援目標（3つ）
② 必要に応じた支援機関名（例：特別支援教育コーディネーター、巡回相談員など）
③ 各目標に連動した支援内容（3つ）

【条件】：
- 各支援目標は「特別な教育的ニーズ①～③」に対応する形で記述してください。
- 支援内容には、どのような工夫・体制・周囲の支援が必要かを具体的に示してください。
- 文章量は1項目あたり200文字前後。過剰に専門的すぎず、実践的な記述を心がけてください。
- 添付資料の文体と構成を意識し、教育現場向けの整った記述としてください。"""
        st.subheader("📄 生成されたプロンプト②（コピーして使ってください）")
        st.code(prompt_text_2, language="text")

# --- プロンプト③ ---
with st.container(border=True):
    st.header("プロンプト③【プランB：指導方針・7項目の実態】")
    jittai_3 = st.text_area(
        "✅ お子さんの実態や課題を入力してください（プロンプト①と同じ内容で構いません）",
        value="視力が弱い、落ち着きがない、疲れやすい、音に敏感、話しかけられると混乱する、同じ行動を繰り返す",
        height=100, key="jittai_3"
    )
    if st.button("プロンプト③ を生成", key="btn_3", use_container_width=True):
        prompt_text_3 = f"""以下の実態・課題をもとに、特別支援計画「プランB」における以下項目を作成してください。

【入力】実態・課題（単語や短文、複数）：
{jittai_3}

【出力項目】：
① 指導方針（全体の方針や教育的視点）
② 実態（以下の7つの観点から、それぞれ200〜300文字で記述）：
　- 健康・生活
　- 心理
　- 行動
　- 人間関係・集団参加
　- 学習
　- 身体・感覚
　- 家庭・地域との連携

【条件】：
- 指導方針は上記の実態や課題に応じた全体的な教育的視点で記述。
- 各7項目は、児童生徒の様子・特性・課題を丁寧に描写してください。
- プランAで設定した「特別な教育的ニーズ①～③」と内容的な整合性が取れるようにしてください。
- 添付資料の文体を踏襲し、専門性と実用性のバランスを意識してください。"""
        st.subheader("📄 生成されたプロンプト③（コピーして使ってください）")
        st.code(prompt_text_3, language="text")

# --- プロンプト④ ---
with st.container(border=True):
    st.header("プロンプト④【個別の指導計画：評価】")
    evaluation_input = st.text_area(
        "✅ 教科ごとの「できたこと・活動の様子」を入力してください",
        value="""【自立活動】：【教育活動全般】・教員の誘導に合わせて、肩や首、股関節を弛め、その後の学習活動でも胸や肩を開いた状態で参加することができた。・巧技台やキャスターボードに片足を乗せた状態で姿勢を安定させて保つことができた。また、片手で教員の肩を掴み片足立ちができた。【教育活動全般】・「ご馳走様」や「分かった」のハンドサインを教員の合図を受けて行うことができるようになった。・両手を離した状態で階段を登れるようになった。下りも近くに教員がいる状態であればできるようになった。
【国語】：自分の名前が書けた。音読が上手だった。文章の意味も少し理解できた。
【算数】：ブロックを使って10までの数を作ることができた。自分の方法を説明できた。""",
        height=250, key="evaluation_input"
    )
    if st.button("プロンプト④ を生成", key="btn_4", use_container_width=True):
        prompt_text_4 = f"""以下の入力内容をもとに、教科ごとの「個別の指導の評価」（振り返り文）を作成してください。

【入力内容】：
{evaluation_input}

【出力ルール】：
- 入力内容に「・」で区切られた目標がある場合、その目標の数だけ評価文も記述してください（例：・○○のように友達を意識して関わることできた。・○○の作業では、自分から率先して□□できた、など）。
- 入力された教科すべてについて、評価文を個別に出力してください。
- 各教科について、【教科名の見出し】と200～300文字程度の評価文を作成してください。
- 評価文は、各教科の一般的な目標と入力された「できたこと」を結びつけた内容にしてください。
- 文体は、実務で使用されるような柔らかく教育的な表現にしてください。
- 教科の目標は、AIが学習している一般的な指導要領などを参考に、入力内容から推測して適切なものを採用してください（たとえば、国語なら「語句を読む・書く」「文章理解」、自立活動なら「身体の動き」や「コミュニケーション」など）。"""
        st.subheader("📄 生成されたプロンプト④（コピーして使ってください）")
        st.code(prompt_text_4, language="text")

# --- ▼▼▼【NEW】ここからが追加した機能です ▼▼▼ ---
with st.container(border=True):
    st.header("プロンプト⑤【前期・後期の所見】")
    st.markdown("#### <span style='color: #8A2BE2;'>NEW!</span> 通知表などの総合的な所見作成に", unsafe_allow_html=True)
    st.write("学期・学年末の総合的な所見を作成します。下の選択肢に応じて、AIへの指示が自動で変わります。")

    term_choice = st.radio(
        "どちらの所見を作成しますか？",
        ("前期", "後期／学年末"),
        key="term_choice",
        horizontal=True
    )

    shoken_input = st.text_area(
        "✅ 所見の材料となる情報を入力してください（箇条書きで構いません）",
        value="""- 大きなけがもなく元気に登校していた。
- 友人との関わりにおいて少しずつ改善が見られた。
- 【国語】音読や名前を書く練習に意欲的だった。
- 【生活】自分で身の回りを整える力が育ってきた。
- 宿泊学習や校外学習にも落ち着いて対応できた。
- ご家庭とも連携しながら指導を行っている。""",
        height=250,
        key="shoken_input"
    )

    if st.button("プロンプト⑤ を生成", key="btn_5", use_container_width=True):
        
        # 時期によって条件を切り替える
        if term_choice == "前期":
            specific_conditions = """- 「前期は、〜」といった書き出しで始めてください。
- 200～400文字程度の文章量で作成してください。
- 文末には「後期も引き続き、ご家庭と連携を取りながら、成長を見守っていきたいと思います。よろしくお願いいたします。」など、後期への連携を意識した一文を入れてください。"""
        else: # 後期／学年末
            specific_conditions = """- 「この1年間で〜」や「いよいよ来年度は〜」など、年度の区切りを感じさせる書き出しにしてください。
- 200〜450文字程度の文章量で作成してください。
- 文末には、保護者への感謝（例：「1年間、本校の教育活動にご理解とご協力をいただき、誠にありがとうございました。」）と、次年度に向けた応援の言葉（例：「これからも応援しています」「新しい学年でも、○○さんらしさを大切に頑張ってくれることを楽しみにしています」）を必ず含めてください。"""

        prompt_text_5 = f"""以下の情報と条件をもとに、保護者向けの「{term_choice}の所見（総合的な所見）」を作成してください。

【参考情報】：
{shoken_input}

【全体の共通条件】：
- 丁寧な語り口で、前向きな表現を心がけてください。
- 情報が足りない場合、これまでの教科ごとの評価（特に自立活動や日常生活の指導）を参考にし、内容を補って構いません。
- 学校生活全体の様子、各教科や生活面での成長をバランスよく含めてください。
- 保護者の方が読んで、お子さんの成長が具体的に伝わるような文章にしてください。

【{term_choice}用の個別条件】：
{specific_conditions}

【出力形式（参考例）】：
前期は、大きなけがもなく毎日、元気に楽しく学校生活を送ることができました。授業や活動にも積極的に取り組む姿が見られ、特に国語では音読や名前を書く練習に意y欲的でした。生活面でも、自分で身の回りを整える力が育ってきており、日常の切り替えにも落ち着きが感じられるようになっています。宿泊学習などの行事にも前向きに参加し、集団での役割を意識しながら行動することができました。これらの経験が自信となり、学校生活全体に良い影響を与えているように感じます。後期も引き続き、ご家庭と連携を取りながら、成長を見守っていきたいと思います。よろしくお願いいたします。"""

        st.subheader(f"📄 生成されたプロンプト⑤（{term_choice}の所見用）")
        st.code(prompt_text_5, language="text")

# --- ▲▲▲ 追加機能はここまで ▲▲▲ ---

st.markdown("---")
st.warning("""
**【利用上の注意】**
AIが生成する内容は、入力された情報に基づく提案であり、必ずしも正確性や適切性を保証するものではありません。自分の判断と合わせてご活用ください。
""")