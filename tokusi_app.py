# streamlit_app.py (メインエントリーポイントとなるファイル)

import streamlit as st

# ここに、現在のTOPページで定義されている st.set_page_config を移動
st.set_page_config(
    page_title="特別支援教育サポートアプリ",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# st.Page を使って各ページを登録し、表示名を指定
# Home.py 以外のファイル名にすることで、Homeという表示にならず、指定した表示名になる
pg1 = st.Page("main_page.py", title="TOPページ", icon="🌟") # TOPページをここで登録し、表示名を「TOPページ」に設定
pg2 = st.Page("pages/1_指導支援内容.py", title="指導支援内容", icon="📚")
pg3 = st.Page("pages/2_発達チャート.py", title="発達チャート作成", icon="📊")
pg4 = st.Page("pages/3_分析方法.py", title="分析方法", icon="📈")
pg5 = st.Page("pages/4_個別の支援計画・指導計画作成支援.py", title="計画作成サポート", icon="🤖")
# ... 他のページも同様に st.Page で登録していく ...
pg6 = st.Page("pages/6_知的段階_学習指導要領.py", title="知的段階（学習指導要領）", icon="📜")
pg7 = st.Page("pages/7_動画ギャラリー.py", title="動画ギャラリー", icon="▶️")
pg8 = st.Page("pages/8_授業カードライブラリー.py", title="授業カードライブラリー", icon="🃏")
pg9 = st.Page("pages/9_フィードバック.py", title="フィードバック", icon="📝")

# ページをまとめて表示
pgs = [pg1, pg2, pg3, pg4, pg5, pg6, pg7, pg8, pg9] # 登録したページをリストに追加

# Streamlitにページを登録
st.navigation(pages=pgs)

# ここに現在のTOPページのコンテンツは書かない。
# 代わりに、main_page.py で TOPページのコンテンツを記述する。