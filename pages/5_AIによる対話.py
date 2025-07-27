import streamlit as st
import google.generativeai as genai

def create_prompt(child_name, long_term_goal, short_term_goal, consideration, support_idea):
    """AIへの指示（プロンプト）を作成する関数"""
    # (この関数の中身は変更ありません)
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

def main():
    st.title("🤖※未完成です　いじらないで　 AIによる個別指導計画サポート (Google Gemini版)")
    st.info("""
    ここでは、お子さんの情報や目標を入力することで、**GoogleのAI「Gemini」**が個別指導計画の草案や具体的な支援のヒントを提案します。\n
    **生成された内容はあくまで草案です。必ず専門的な知見に基づき、内容を検討・修正してご活用ください。**
    """)

    with st.form("plan_form"):
        st.subheader("お子さんの情報を入力してください")
        
        child_name = st.text_input("お子さんの名前（またはニックネーム）", "Aさん")
        long_term_goal = st.text_area("長期目標（例：年度末の姿）", "自分の気持ちを適切な言葉で伝えられるようになる。")
        short_term_goal = st.text_area("短期目標（例：1学期の目標）", "嫌なことがあった時に、「やめて」と言える場面を増やす。")
        
        consideration_options = ["コミュニケーション", "対人関係", "学習面", "行動面（衝動性など）", "感覚過敏・鈍麻", "身体の動き", "その他（自由記述）"]
        consideration = st.selectbox("特に配慮したい点", consideration_options)
        if consideration == "その他（自由記述）":
            consideration = st.text_input("配慮したい点を具体的に入力してください")

        support_idea = st.text_area("考えている支援のアイデアや、お子さんの好きなことなど", "絵カードを使って気持ちを伝える練習をする。クールダウンできる場所を用意する。電車のおもちゃが好き。")
        submitted = st.form_submit_button("AIに指導計画の草案作成を依頼する", type="primary", use_container_width=True)

    if submitted:
        if not all([child_name, long_term_goal, short_term_goal, support_idea]):
            st.warning("すべての項目を入力してください。")
        else:
            with st.spinner("GoogleのAIが個別指導計画を考えています..."):
                try:
                    # --- ▼▼▼ 読み込み場所を修正 ▼▼▼ ---
                    try:
                        # st.secrets["ai"]["GOOGLE_API_KEY"] のように変更
                        genai.configure(api_key=st.secrets["ai"]["GOOGLE_API_KEY"])
                    except (KeyError, FileNotFoundError):
                        st.error("エラー: Google AIのAPIキーが設定されていません。Streamlit CloudのSecretsを確認してください。")
                        st.stop()
                    
                    prompt = create_prompt(child_name, long_term_goal, short_term_goal, consideration, support_idea)
                    model = genai.GenerativeModel('gemini-1.5-flash-latest')
                    response = model.generate_content(prompt)
                    ai_response = response.text

                    st.subheader("AIからの提案")
                    st.markdown(ai_response)

                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

    st.markdown("---")
    st.warning("...") # 注意喚起文は省略

if __name__ == "__main__":
    main()