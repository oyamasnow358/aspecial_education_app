import streamlit as st

# 指導データ
guidance_data = {
    "日常生活における実態": {
        "身辺自立が未熟な生徒": {
            "衣服の着脱練習": [
                "具体的教材の導入: 実際のボタン付きシャツやファスナーを取り付けたパネル教材を使い、繰り返し練習する。",
                "段階的指導: まずは「袖に手を通す」「ボタンをつまむ」など簡単なステップに分け、一つずつ練習を進める。",
                "視覚支援の活用: 着替えの順序をイラストや写真で示し、見通しを持たせる。",
                "実践的練習: 毎朝の登校後や体育の後など、実際の生活場面での練習を取り入れる。",
            ]
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
                "ジェスチャー活用: 視覚的な動きで意思を伝える練習（例: 「飲みたい」「行きたい」など）。",
                "指文字練習: 手話に加え、指文字を活用する場面を設定。",
                "タブレットでのコミュニケーション: 音声入力から文字表示を活用したアプリでの意思疎通。",
            ],
        },
    },
}

# Streamlitアプリ
st.title("指導支援内容の参照")

menu = st.sidebar.selectbox("メニューを選択してください", ["指導支援内容"])

# 指導支援内容表示
if menu == "指導支援内容":
    st.subheader("📚 指導支援内容の参照")
    st.text("1から順番に選択してください")

    # カテゴリー選択
    selected_category = st.selectbox("1. カテゴリーを選択してください:", list(guidance_data.keys()))
    # サブカテゴリー選択
    selected_subcategory = st.selectbox(
        "2. 該当する項目を選択してください:", list(guidance_data[selected_category].keys())
    )

    # 辞書かリストかを確認して処理
    if isinstance(guidance_data[selected_category][selected_subcategory], dict):
        selected_detail = st.selectbox(
            "3. 具体的な支援内容を選択してください:",
            list(guidance_data[selected_category][selected_subcategory].keys())
        )
    elif isinstance(guidance_data[selected_category][selected_subcategory], list):
        selected_detail = st.selectbox(
            "3. 具体的な支援内容を選択してください:",
            guidance_data[selected_category][selected_subcategory]
        )
    else:
        st.error("不明なデータ形式です。")
        selected_detail = None

    # 内容表示
    if selected_detail and st.button("適した指導・支援を表示"):
        st.subheader("📌 適した指導・支援")
        # 結果の整形
        if isinstance(guidance_data[selected_category][selected_subcategory], dict):
            detail = guidance_data[selected_category][selected_subcategory][selected_detail]
        else:
            detail = selected_detail

        # リスト形式であれば改行して表示
        if isinstance(detail, list):
            formatted_detail = "\n".join([f"- {item}" for item in detail])
        else:
            formatted_detail = detail

        # 直接表示
        st.markdown(f"**{selected_detail}**:  \n{formatted_detail}")

    # 具体的な支援内容の表示（詳細ボタン付き）
    for item in guidance_data[selected_category][selected_subcategory]:
        if isinstance(item, dict):  # 詳細を持つ項目の場合
            st.markdown(f"**{item['title']}**")
            with st.expander("詳細を見る"):
                for detail in item["details"]:
                    st.write(f"- {detail}")
        else:  # 文字列の項目の場合
            st.write(f"- {item}")
