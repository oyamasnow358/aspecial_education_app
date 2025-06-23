import streamlit as st

st.set_page_config(
    page_title="特別支援教育サポートアプリ",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ▼ここから追加▼ ---
# ページ遷移を管理するための関数
def set_page(page):
    st.session_state.page_to_visit = page

# st.session_stateをチェックしてページ遷移を実行
if "page_to_visit" in st.session_state:
    page = st.session_state.page_to_visit
    del st.session_state.page_to_visit  # 実行後にキーを削除
    st.switch_page(page)
# --- ▲ここまで追加▲ ---


st.title("🌟 特別支援教育サポートアプリ")

# メインイメージ
st.image("https://i.imgur.com/CTSCBYi.png", caption="子どもたちの「できた！」を支援する", use_container_width=True)

st.header("ようこそ！")
st.write("""
このアプリは、特別支援教育に関わる先生方をサポートするためのツールです。
子どもたち一人ひとりのニーズに合わせた指導や支援のヒントを見つけたり、
発達段階を記録・分析したりすることができます。

**サイドバーのメニューから、利用したい機能を選択してください。**
""")

st.subheader("各機能の紹介")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("#### 📚 指導支援内容")
        st.write("日常生活の困りごとに応じた、具体的な指導・支援のアイデアを検索できます。")
        # --- ▼ここを修正▼ ---
        st.button("この機能を使う", on_click=set_page, args=("pages/1_指導支援内容.py",), key="btn_guidance")
        # --- ▲ここまで修正▲ ---

    with st.container(border=True):
        st.markdown("#### 📈 分析方法")
        st.write("教育学や心理学に基づいた様々な分析方法の解説と、実践で使えるツールを提供します。")
        # --- ▼ここを修正▼ ---
        st.button("この機能を使う", on_click=set_page, args=("pages/3_分析方法.py",), key="btn_analysis")
        # --- ▲ここまで修正▲ ---

with col2:
    with st.container(border=True):
        st.markdown("#### 📊 発達チャート作成")
        st.write("お子さんの発達段階を記録し、レーダーチャートで視覚的に確認・保存できます。")
        # --- ▼ここを修正▼ ---
        st.button("この機能を使う", on_click=set_page, args=("pages/2_発達チャート.py",), key="btn_chart")
        # --- ▲ここまで修正▲ ---

    with st.container(border=True):
        st.markdown("#### 📝 フィードバック")
        st.write("アプリの改善や、新しい指導実践の共有など、皆様からのご意見をお待ちしています。")
        # --- ▼ここを修正▼ ---
        st.button("この機能を使う", on_click=set_page, args=("pages/4_フィードバック.py",), key="btn_feedback")
        # --- ▲ここまで修正▲ ---


# --- フッター（外部リンクや注意書き） ---
st.markdown("""
    <hr style="border: none; height: 3px; background: linear-gradient(to right, #4a90e2, #8A2BE2);">
""", unsafe_allow_html=True)

st.subheader("関連ツール＆リンク")
c1, c2 = st.columns(2)
with c1:
    st.markdown("##### 📁 教育・心理分析ツール")
    st.page_link("https://abaapppy-k7um2qki5kggexf8qkfxjc.streamlit.app/", label="応用行動分析", icon="🔗")
    st.page_link("https://kinoukoudou-ptfpnkq3uqgaorabcyzgf2.streamlit.app/", label="機能的行動評価分析", icon="🔗")

with c2:
    st.markdown("##### 📁 統計学分析ツール")
    st.page_link("https://annketo12345py-edm3ajzwtsmmuxbm8qbamr.streamlit.app/", label="アンケートデータ、総合統計分析", icon="🔗")
    st.page_link("https://soukan-jlhkdhkradbnxssy29aqte.streamlit.app/", label="相関分析", icon="🔗")
    st.page_link("https://kaikiapp-tjtcczfvlg2pyhd9bjxwom.streamlit.app/", label="多変量回帰分析", icon="🔗")
    st.page_link("https://tkentei-flhmnqnq6dti6oyy9xnktr.streamlit.app/", label="t検定", icon="🔗")
    st.page_link("https://rojisthik-buklkg5zeh6oj2gno746ix.streamlit.app/", label="ロジスティック回帰分析", icon="🔗")
    st.page_link("https://nonparametoric-nkk2awu6yv9xutzrjmrsxv.streamlit.app/", label="ノンパラメトリック統計分析", icon="🔗")


st.markdown("---")
st.markdown("##### 🗨️ ご意見・ご感想")
st.markdown("自立活動の参考指導、各分析ツールにご意見がある方は以下のフォームから送ってください（埼玉県の学校教育関係者のみＳＴアカウントで回答できます）。")
st.page_link("https://docs.google.com/forms/d/1dKzh90OkxMoWDZXV31FgPvXG5EvNlMFOrvSPGvYTSC8/preview", label="アンケートフォーム", icon="📝")

st.markdown("---")
st.warning("""
**【利用上の注意】**
それぞれのアプリに記載してある内容、分析ツールのデータや図、表を外部（研究発表など）で利用する場合は、管理者(岩槻はるかぜ特別支援学校 小山)までご相談ください。無断での転記・利用を禁じます。
""")