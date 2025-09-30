import streamlit as st

st.set_page_config(page_title="フィードバック", page_icon="📝", layout="wide")
# --- ▼ 戻るボタンの配置 (メインコンテンツの左上) ▼ ---
# st.columnsを使って、左端に配置する
col_back, _ = st.columns([0.15, 0.85]) # ボタン用に狭いカラムを確保
with col_back:
    # `st.page_link` を使用すると、直接ページに遷移できてより確実です。
    st.page_link("tokusi_app.py", label="« TOPページに戻る", icon="🏠")
# --- ▲ 戻るボタンの配置 ▲ ---

st.title("📝 フィードバック")
st.write("アプリの改善や、新しい指導実践の共有など、皆様からのご意見をお待ちしています。")
st.info("下のタブから使いやすい方のフォームを選択してご入力ください。")

tab1, tab2 = st.tabs(["Microsoft Forms", "Google Forms"])

with tab1:
    st.header("Microsoft Forms")
    form_url_ms = "https://forms.office.com/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAMAANa6zUxUQjRFQ1NRUFhJODhKVFMzUkdVVzVCR0JEVS4u&embed=true"
    st.components.v1.iframe(form_url_ms, height=800, scrolling=True)

with tab2:
    st.header("Google Forms")
    form_url_google = "https://docs.google.com/forms/d/1xXzq0vJ9E5FX16CFNoTzg5VAyX6eWsuN8Xl5qEwJFTc/preview"
    st.components.v1.iframe(form_url_google, height=800, scrolling=True)