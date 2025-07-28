import streamlit as st

# --- ▼ 共通CSSの読み込み（トップページからコピー） ▼ ---
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
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
# --- ▲ 共通CSSの読み込み ▲ ---

# CSSを適用
load_css()

st.title("🤖 AIによる計画作成サポート")

st.info(
    """
    ここでは、個別の支援計画・指導計画を作成するためのプロンプト（AIへの命令文）を簡単に作成できます。
    お子さんの実態や課題を入力し、「プロンプトを生成」ボタンを押してください。
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
    st.write("お子さんの実態や課題から、「特別な教育的ニーズ」と「合理的配慮」の案を作成します。")

    jittai_1 = st.text_area(
        "✅ お子さんの実態や課題を入力してください",
        value="視力が弱い、落ち着きがない、疲れやすい、音に敏感、話しかけられると混乱する、同じ行動を繰り返す",
        height=100,
        key="jittai_1"
    )

    with st.expander("もっと詳しく ▸ 追記したい内容があれば入力（任意）"):
        tsuiki_1 = st.text_area(
            "特にプロンプトに含めてほしい単語や視点を入力してください",
            value="不安が強い、環境変化に弱い",
            key="tsuiki_1"
        )
        use_tsuiki_1 = st.checkbox("追記内容をプロンプトに含める", key="use_tsuiki_1")

    if st.button("プロンプト① を生成", key="btn_1", use_container_width=True):
        base_prompt_1 = f"""以下の実態や課題をもとに、特別支援教育に関する「プランA」の以下の項目を作成してください。

【入力】実態や課題（単語や短文、複数）：
{jittai_1}"""

        if use_tsuiki_1 and tsuiki_1:
            prompt_text_1 = f"""以下の情報をもとに、特別支援教育プランAの「特別な教育的ニーズ」と「合理的配慮の実施内容」を作成してください。

【実態・課題（入力済）】：
{jittai_1}

【追記してほしい内容・単語】：
{tsuiki_1}

【出力項目】：
① 特別な教育的ニーズ（3つ）
② 合理的配慮の実施内容（3つ）
※上記①〜③のニーズとそれに対応する配慮をそれぞれセットで記述。

【条件】：
- 元の実態・課題と「追記してほしい内容」の両方を考慮して分類してください。
- 「追記してほしい内容」は必ず何らかの形で反映してください。
- 文体は丁寧で実務的、現場で使える表現にしてください。"""
        else:
            prompt_text_1 = f"""{base_prompt_1}

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
    st.header("プロンプト②【プランA：所属校の支援（目標・支援機関・支援内容）】")
    st.write("プロンプト①を使ってAIが生成した「特別な教育的ニーズ」をもとに、所属校での支援計画の案を作成します。")

    needs_2 = st.text_area(
        "✅ プロンプト①でAIが生成した「特別な教育的ニーズ①〜③」をここに貼り付けてください",
        value="① 感覚過敏があり、環境刺激に影響を受けやすい\n② 注意の持続が難しく、集中が途切れやすい\n③ コミュニケーションに混乱が見られ、一斉指示に反応しづらい",
        height=150,
        key="needs_2"
    )

    with st.expander("もっと詳しく ▸ 追記したい内容があれば入力（任意）"):
        tsuiki_2 = st.text_area(
            "特にプロンプトに含めてほしい視点や支援内容を入力してください",
            value="できるだけ本人のペースを尊重した支援、安心できる声掛け",
            key="tsuiki_2"
        )
        use_tsuiki_2 = st.checkbox("追記内容をプロンプトに含める", key="use_tsuiki_2")

    if st.button("プロンプト② を生成", key="btn_2", use_container_width=True):
        if use_tsuiki_2 and tsuiki_2:
            prompt_text_2 = f"""以下の「特別な教育的ニーズ①〜③」に基づいて、所属校による支援内容を作成してください。

【特別な教育的ニーズ】：
{needs_2}

【追記してほしい視点・支援内容】：
{tsuiki_2}

【出力項目】：
- 所属校の支援目標①〜③（上記ニーズに対応）
- 必要に応じた支援機関名（例：特別支援教育コーディネーター、巡回相談員など）
- 各目標に連動した支援内容①〜③

【条件】：
- 「追記してほしい支援内容」は、必ずどこかに含めてください。
- 各支援内容は実行可能で現場で活かしやすいよう具体的に。
- 各支援目標は「特別な教育的ニーズ①～③」に対応する形で記述してください。
- 文章量は1項目あたり200文字前後。過剰に専門的すぎず、実践的な記述を心がけてください。
- 添付資料の文体と構成を意識し、教育現場向けの整った記述としてください。"""
        else:
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
    st.write("お子さんの実態や課題から、より詳細な指導計画（プランB）の案を作成します。")

    jittai_3 = st.text_area(
        "✅ お子さんの実態や課題を入力してください（プロンプト①と同じ内容で構いません）",
        value="視力が弱い、落ち着きがない、疲れやすい、音に敏感、話しかけられると混乱する、同じ行動を繰り返す",
        height=100,
        key="jittai_3"
    )

    with st.expander("もっと詳しく ▸ 追記したい内容があれば入力（任意）"):
        tsuiki_3 = st.text_area(
            "特にプロンプトに含めてほしい内容や観点を入力してください",
            value="家庭ではよく眠れていない、生活リズムが安定しないことが多い",
            key="tsuiki_3"
        )
        use_tsuiki_3 = st.checkbox("追記内容をプロンプトに含める", key="use_tsuiki_3")

    if st.button("プロンプト③ を生成", key="btn_3", use_container_width=True):
        if use_tsuiki_3 and tsuiki_3:
            prompt_text_3 = f"""以下の情報をもとに、教育支援プランBの「指導方針」と「実態（7項目）」を作成してください。

【実態・課題】：
{jittai_3}

【追記してほしい内容・観点】：
{tsuiki_3}

【出力項目】：
① 指導方針（300文字程度）
② 実態（以下の7項目、各200〜300文字）：
　- 健康・生活
　- 心理
　- 行動
　- 人間関係・集団参加
　- 学習
　- 身体・感覚
　- 家庭・地域との連携

【条件】：
- 「追記してほしい内容」は適切な項目に組み込んでください（この場合は「健康・生活」や「家庭・地域との連携」など）。
- 文体は現場で使える記述にしてください。家庭・学校どちらの視点もバランスよく。
- 指導方針は上記の実態や課題に応じた全体的な教育的視点で記述。
- 各7項目は、児童生徒の様子・特性・課題を丁寧に描写してください。
- プランAで設定した「特別な教育的ニーズ①～③」と内容的な整合性が取れるようにしてください。"""
        else:
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

st.markdown("---")
st.warning("""
**【利用上の注意】**
AIが生成する内容は、入力された情報に基づく提案であり、必ずしも正確性や適切性を保証するものではありません。専門家の判断と合わせてご活用ください。
""")