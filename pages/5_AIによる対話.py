import streamlit as st
import openai
import time

# --- ▼ 共通CSSの読み込み ▼ ---
def load_css():
    """カスタムCSSを読み込む関数"""
    css = """
    <style>
        /* --- 背景画像の設定 --- */
        /* ご用意された画像のURLを下の 'url(...)' 内に貼り付けてください */
        /* 例: url("https://i.imgur.com/your_image.jpg"); */
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
        /* サイドバーの閉じるボタンのアイコンを強制的に変更 */
        [data-testid="stSidebarNavCollapseButton"]::after { content: '«' !important; }
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

# --- OpenAI APIクライアントの初期化 ---
# st.secretsからAPIキーを読み込む
try:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    API_KEY_CONFIGURED = True
except (KeyError, FileNotFoundError):
    API_KEY_CONFIGURED = False

# --- プロンプトを生成する関数 ---
def create_prompt(child_name, long_term_goal, short_term_goal, consideration, support_idea):
    """AIへの指示（プロンプト）を作成する関数"""
    prompt = f"""
あなたは、特別支援教育の経験豊富な専門家です。
以下の情報に基づき、{child_name}さんの個別指導計画の草案と、具体的な支援のヒントを、丁寧かつ専門的な視点から提案してください。

# 対象となるお子さんの情報
- 名前：{child_name}
- 長期目標：{long_term_goal}
- 短期目標：{short_term_goal}
- 特に配慮したい点：{consideration}
- 教師が考えている支援のアイデア：{support_idea}

# 出力形式の指示
以下の形式で、マークダウンを使用して分かりやすく記述してください。

---

### **個別指導計画（草案）**

**1. 長期目標**
- {long_term_goal}

**2. 短期目標**
- {short_term_goal}

**3. 指導内容・手立て**
（ここでの記述は、入力された情報を基に、より具体的で専門的な表現にしてください）

**4. 評価**
（短期目標に対する具体的な評価方法を提案してください）

### **具体的な支援のヒント**
（入力された「教師が考えている支援のアイデア」を深掘りし、明日から実践できるような具体的なアイデアを3〜5つ提案してください。箇条書きでお願いします。）

### **関わり方のポイント**
（{consideration}の観点を踏まえ、{child_name}さんと関わる上での心構えや、声かけのヒントなどを提案してください。）
"""
    return prompt

# --- メインのアプリケーション ---
def main():
    # 共通のCSSを読み込む
    # load_css() # 必要に応じてコメントアウトを解除

    st.title("🤖 AIによる個別指導計画サポート")
    st.info("""
    ここでは、お子さんの情報や目標を入力することで、AIが個別指導計画の草案や具体的な支援のヒントを提案します。\n
    **生成された内容はあくまで草案です。必ず専門的な知見に基づき、内容を検討・修正してご活用ください。**
    """)

    if not API_KEY_CONFIGURED:
        st.error("エラー: OpenAIのAPIキーが設定されていません。管理者にお問い合わせください。")
        st.warning("（管理者向け）`.streamlit/secrets.toml` ファイルに `OPENAI_API_KEY = 'あなたのキー'` を設定してください。")
        return # APIキーがない場合はここで処理を中断

    # --- 入力フォーム ---
    with st.form("plan_form"):
        st.subheader("お子さんの情報を入力してください")
        
        child_name = st.text_input("お子さんの名前（またはニックネーム）", "Aさん")
        long_term_goal = st.text_area("長期目標（例：年度末の姿）", "自分の気持ちを適切な言葉で伝えられるようになる。")
        short_term_goal = st.text_area("短期目標（例：1学期の目標）", "嫌なことがあった時に、「やめて」と言える場面を増やす。")
        
        consideration_options = [
            "コミュニケーション", "対人関係", "学習面", "行動面（衝動性など）", 
            "感覚過敏・鈍麻", "身体の動き", "その他（自由記述）"
        ]
        consideration = st.selectbox("特に配慮したい点", consideration_options)
        if consideration == "その他（自由記述）":
            consideration = st.text_input("配慮したい点を具体的に入力してください")

        support_idea = st.text_area(
            "考えている支援のアイデアや、お子さんの好きなことなど", 
            "絵カードを使って気持ちを伝える練習をする。クールダウンできる場所を用意する。電車のおもちゃが好き。"
        )

        # フォームの送信ボタン
        submitted = st.form_submit_button("AIに指導計画の草案作成を依頼する", type="primary", use_container_width=True)

    # --- AIからの回答表示 ---
    if submitted:
        # 入力チェック
        if not all([child_name, long_term_goal, short_term_goal, support_idea]):
            st.warning("すべての項目を入力してください。")
        else:
            with st.spinner("AIが個別指導計画を考えています..."):
                try:
                    # AIへのプロンプトを生成
                    prompt = create_prompt(child_name, long_term_goal, short_term_goal, consideration, support_idea)
                    
                    # OpenAI APIを呼び出し
                    response = client.chat.completions.create(
                        model="gpt-4o",  # または "gpt-3.5-turbo"
                        messages=[
                            {"role": "system", "content": "あなたは特別支援教育の専門家です。"},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    ai_response = response.choices[0].message.content

                    # 結果を表示
                    st.subheader("AIからの提案")
                    st.markdown(ai_response)

                except openai.APIError as e:
                    st.error(f"OpenAI APIエラーが発生しました: {e}")
                except Exception as e:
                    st.error(f"予期せぬエラーが発生しました: {e}")

    st.markdown("---")
    st.warning("""
    **【個人情報の取り扱いに関する注意】**
    このフォームに入力された情報は、OpenAI社のサーバーに送信されます。
    **個人が特定できる氏名や詳細な個人情報は入力しないでください。**
    お子さんの名前は「Aさん」のような仮名に、内容は一般化して入力することを強く推奨します。
    """)


if __name__ == "__main__":
    st.set_page_config(
        page_title="AIによる対話",
        page_icon="🤖",
        layout="wide"
    )
    main()