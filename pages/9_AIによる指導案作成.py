import streamlit as st
import openpyxl
from openpyxl.styles import Alignment
from openpyxl.cell.cell import MergedCell
import json
import io
import os
import re

# ==========================================
# 0. ページ設定 & デザイン定義 (Mirairo共通)
# ==========================================
st.set_page_config(
    page_title="Mirairo - 指導案作成",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    css = """
    <style>
        /* --- 全体 --- */
        html, body, [class*="css"] {
            font-family: 'Noto Sans JP', sans-serif !important;
        }

        /* --- 背景 (黒) --- */
        [data-testid="stAppViewContainer"] {
            background-color: #000000;
            background-image: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url("https://i.imgur.com/AbUxfxP.png");
            background-size: cover;
            background-attachment: fixed;
        }

        /* --- 文字色 (白・影付き) --- */
        h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown {
            color: #ffffff !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.9) !important;
        }

        /* --- サイドバー --- */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        [data-testid="stSidebarNavCollapseButton"] { color: #fff !important; }

        /* --- 機能カード (白枠・アニメーション) --- */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        [data-testid="stBorderContainer"], .header-box {
            background-color: #151515 !important;
            border: 2px solid #ffffff !important;
            border-radius: 16px !important;
            padding: 20px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.8) !important;
            animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        }
        
        [data-testid="stBorderContainer"]:hover, .header-box:hover {
            border-color: #4a90e2 !important;
            background-color: #000000 !important;
            transform: translateY(-5px);
            box-shadow: 0 0 20px rgba(74, 144, 226, 0.4) !important;
            transition: all 0.3s ease;
        }

        /* --- ボタン --- */
        .stButton > button {
            width: 100%;
            background-color: #000000 !important;
            border: 2px solid #ffffff !important;
            color: #4a90e2 !important;
            font-weight: bold !important;
            border-radius: 30px !important;
            transition: all 0.3s ease !important;
            height: 3em !important;
        }
        .stButton > button:hover {
            border-color: #4a90e2 !important;
            color: #ffffff !important;
            background-color: #4a90e2 !important;
        }
        
        /* Primaryボタン */
        .stButton > button[kind="primary"] {
            background-color: #4a90e2 !important;
            color: #ffffff !important;
            border: 2px solid #4a90e2 !important;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #ffffff !important;
            color: #4a90e2 !important;
        }

        /* --- 入力フォーム --- */
        .stTextInput input, .stTextArea textarea {
            background-color: #222 !important;
            color: #fff !important;
            border-color: #555 !important;
        }

        /* --- エキスパンダー --- */
        .streamlit-expanderHeader {
            background-color: rgba(255,255,255,0.1) !important;
            color: #fff !important;
            border-radius: 8px !important;
            border: 1px solid #555;
        }
        .streamlit-expanderContent {
            background-color: rgba(0,0,0,0.5) !important;
            border: 1px solid #444;
            border-top: none;
            border-radius: 0 0 8px 8px;
        }

        /* --- ステップヘッダー --- */
        .step-header {
            color: #4a90e2 !important;
            border-bottom: 2px solid #4a90e2;
            padding-bottom: 10px;
            margin-top: 40px;
            font-weight: bold;
            font-size: 1.5em;
            text-shadow: none !important;
        }

        /* --- 戻るボタン --- */
        .back-link a {
            display: inline-block;
            padding: 8px 16px;
            background: rgba(255,255,255,0.1);
            border: 1px solid #fff;
            border-radius: 20px;
            color: #fff !important;
            text-decoration: none;
            margin-bottom: 20px;
            transition: all 0.3s;
        }
        .back-link a:hover {
            background: #fff;
            color: #000 !important;
        }
        
        /* コードブロック */
        code {
            background-color: #222 !important;
            color: #e0e0e0 !important;
        }
        
        hr { border-color: #666; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# ==========================================
# 1. ユーティリティ関数（Excelエラー回避用）
# ==========================================
def safe_write(ws, cell_address, value):
    """
    結合セルエラー（MergedCell...read-only）を回避して書き込む関数。
    """
    try:
        if value is None:
            value = ""
        value = str(value)

        if isinstance(ws[cell_address], MergedCell):
            for merged_range in ws.merged_cells.ranges:
                if cell_address in merged_range:
                    top_left_coord = merged_range.start_cell.coordinate
                    ws[top_left_coord] = value
                    ws[top_left_coord].alignment = Alignment(wrap_text=True, vertical='top', horizontal='left')
                    return
        else:
            ws[cell_address] = value
            ws[cell_address].alignment = Alignment(wrap_text=True, vertical='top', horizontal='left')

    except Exception as e:
        st.warning(f"⚠️ セル {cell_address} への書き込み中に警告: {e}")

# ==========================================
# 2. プロンプト生成ロジック
# ==========================================
def generate_prompt_text(data):
    prompt = f"""
あなたは特別支援学校および公立学校における【熟練の教員】です。
以下の【授業情報】を基に、学習指導案に必要な情報を補完し、指定の【JSON形式】のみで出力してください。
前置きや解説は一切不要です。JSONデータだけを返してください。

■ 【授業情報】
[必須項目]
・学部学年: {data['grade']}
・教科単元: {data['subject']}
・日時: {data['date']}
・時間: {data['time']}
・場所: {data['place']}
・本時の内容: {data['content']}

[任意項目（ユーザー入力があれば反映、なければ教育的観点で補完）]
・目標: {data['goals_in'] if data['goals_in'] else "未定（文脈に合わせて最大3つ生成せよ）"}
・評価の基準: {data['eval_in'] if data['eval_in'] else "未定（3観点：知識・技能、思考判断表現、主体的態度を含めて生成せよ）"}
・学習内容のメモ: {data['flow_in'] if data['flow_in'] else "未定（自然な流れで構成せよ）"}
・備考: {data['remarks_in'] if data['remarks_in'] else "なし"}

■ 【出力フォーマット（厳守）】
以下のJSON構造を絶対に崩さずに返してください。
{{
  "basic_info": {{
    "grade": "{data['grade']}",
    "subject": "{data['subject']}",
    "date": "{data['date']}",
    "time": "{data['time']}",
    "place": "{data['place']}",
    "content": "{data['content']}"
  }},
  "goals": ["目標1", "目標2", "目標3"],
  "evaluation": ["評価基準1（知識技能）", "評価基準2（思考判断）", "評価基準3（主体性）"],
  "flow": [
    {{
      "time": "5",
      "activity": "導入：挨拶...",
      "notes": "配慮事項..."
    }},
    {{
      "time": "10",
      "activity": "展開1：...",
      "notes": "..."
    }}
  ],
  "materials": "準備物リスト",
  "remarks": "備考の内容（特になければ空欄でも可）"
}}
"""
    return prompt

# ==========================================
# 3. Excel出力ロジック
# ==========================================
def create_excel(template_path, json_data):
    try:
        wb = openpyxl.load_workbook(template_path)
        ws = wb.active
    except Exception as e:
        return None, f"テンプレート読み込みエラー: {e}"

    # --- ① 基本情報 ---
    bi = json_data.get('basic_info', {})
    safe_write(ws, 'C2', bi.get('grade', ''))
    safe_write(ws, 'I2', bi.get('subject', ''))
    safe_write(ws, 'C3', bi.get('date', ''))
    safe_write(ws, 'K3', bi.get('time', ''))
    safe_write(ws, 'N3', bi.get('place', ''))
    safe_write(ws, 'C4', bi.get('content', ''))

    # --- ② 目標 (C5, C6, C7) ---
    goals = json_data.get('goals', [])
    if len(goals) > 0: safe_write(ws, 'C5', f"・{goals[0]}")
    if len(goals) > 1: safe_write(ws, 'C6', f"・{goals[1]}")
    if len(goals) > 2: safe_write(ws, 'C7', f"・{goals[2]}")

    # --- ③ 評価の基準 (C8, C9, C10) ---
    evals = json_data.get('evaluation', [])
    if len(evals) > 0: safe_write(ws, 'C8', f"・{evals[0]}")
    if len(evals) > 1: safe_write(ws, 'C9', f"・{evals[1]}")
    if len(evals) > 2: safe_write(ws, 'C10', f"・{evals[2]}")

    # --- ④ 本時の展開 (A13～ 2行空け) ---
    flow_list = json_data.get('flow', [])
    current_row = 13
    
    for item in flow_list:
        safe_write(ws, f'A{current_row}', item.get('time', ''))
        safe_write(ws, f'B{current_row}', item.get('activity', ''))
        safe_write(ws, f'K{current_row}', item.get('notes', ''))
        current_row += 2

    # --- ⑤ 準備物 (N13) ---
    safe_write(ws, 'N13', json_data.get('materials', ''))

    # --- ⑥ 備考 (B33) ---
    safe_write(ws, 'B33', json_data.get('remarks', ''))

    # 保存処理
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output, None

# ==========================================
# 4. メイン画面 UI
# ==========================================

# --- 戻るボタン ---
st.markdown('<div class="back-link"><a href="Home" target="_self">« TOPページに戻る</a></div>', unsafe_allow_html=True)

# --- ヘッダーエリア ---
st.markdown("<div class='header-box'>", unsafe_allow_html=True)
st.title("📝 指導案作成 AIエージェント")
st.markdown("入力情報を元にプロンプトを作成し、AIとの連携で指導案Excelを完成させます。")
st.markdown("</div>", unsafe_allow_html=True)

# --- AIリンクボタン (白枠カード内) ---
with st.container(border=True):
    st.markdown("### 🔗 まずはAIを開く")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.link_button("🤖 ChatGPT を開く ↗", "https://chat.openai.com/", type="primary", use_container_width=True)
    with col_btn2:
        st.link_button("✨ Gemini を開く ↗", "https://gemini.google.com/", type="primary", use_container_width=True)

st.markdown("---")

# --- Step 1: 情報入力 ---
st.markdown("<h3 class='step-header'>Step 1. 基本情報を入力</h3>", unsafe_allow_html=True)

# 白枠コンテナで囲む
with st.container(border=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        in_grade = st.text_input("🎓 学部学年", "小学部 5年")
        in_date = st.text_input("📅 日時", "令和6年11月20日")
    with c2:
        in_subject = st.text_input("📚 教科単元", "生活単元学習「お祭りを開こう」")
        in_place = st.text_input("🏫 場所", "5年1組教室")
    with c3:
        in_time = st.text_input("⏰ 時間", "45分")
        in_content = st.text_input("📝 本時の内容", "模擬店の商品作り")

    st.markdown("---")
    # 詳細設定（アコーディオン）
    with st.expander("⚙️ 詳細設定（目標・評価・備考など） ※空欄でもAIが補完します", expanded=False):
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            in_goals = st.text_area("🎯 目標（最大3つ）", height=100, placeholder="例：\n・道具を正しく使うことができる\n・友達と協力することができる")
            in_eval = st.text_area("📊 評価の基準", height=100, placeholder="知識・技能、思考・判断・表現、主体的に取り組む態度の観点で生成されます。")
        with col_ex2:
            in_flow = st.text_area("💡 学習内容のメモ・ヒント", height=100, placeholder="授業の流れや、必ず入れたい活動があれば箇条書きで。")
            in_remarks = st.text_area("📌 備考（特記事項）", height=100, placeholder="Excelの下部（B33）に入力されます。")

# データをまとめる
input_data = {
    "grade": in_grade, "subject": in_subject, "date": in_date,
    "time": in_time, "place": in_place, "content": in_content,
    "goals_in": in_goals, "eval_in": in_eval, "flow_in": in_flow,
    "remarks_in": in_remarks
}

# --- Step 2: プロンプト生成 ---
st.markdown("<h3 class='step-header'>Step 2. プロンプトをコピー</h3>", unsafe_allow_html=True)

with st.container(border=True):
    if st.button("📋 プロンプトを作成する", type="primary", use_container_width=True):
        prompt_text = generate_prompt_text(input_data)
        st.code(prompt_text, language="text")
        st.success("👆 右上のアイコンでコピーし、ChatGPTやGeminiに貼り付けてください。")
    else:
        st.info("上のボタンを押すと、AIへの指令文が表示されます。")

# --- Step 3: AI出力貼り付け & Excel生成 ---
st.markdown("<h3 class='step-header'>Step 3. AIの回答を貼り付けてExcel作成</h3>", unsafe_allow_html=True)

with st.container(border=True):
    json_input_str = st.text_area("ここにAIからの回答（JSONコード）を貼り付け", height=300, placeholder='{\n  "basic_info": { ... },\n  "goals": [ ... ]\n}')

    if st.button("🚀 指導案Excelを出力する", type="primary", use_container_width=True):
        if not json_input_str.strip():
            st.error("⚠️ AIの回答が貼り付けられていません。")
        else:
            try:
                # 1. JSONクリーニング
                clean_json = re.sub(r"```json\s*|\s*```", "", json_input_str).strip()
                start_idx = clean_json.find('{')
                end_idx = clean_json.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    clean_json = clean_json[start_idx:end_idx]
                
                data_dict = json.loads(clean_json)
                
                # 2. テンプレート検索
                current_dir = os.path.dirname(os.path.abspath(__file__))
                base_dir = os.path.dirname(current_dir)
                template_file = os.path.join(base_dir, "指導案.xlsx") # 親フォルダ検索
                
                if not os.path.exists(template_file):
                    template_file = os.path.join(current_dir, "指導案.xlsx") # 現フォルダ検索

                if not os.path.exists(template_file):
                    st.error(f"❌ エラー: テンプレートファイルが見つかりません。\n{base_dir} または {current_dir} に '指導案.xlsx' を配置してください。")
                else:
                    # 3. Excel生成
                    excel_data, err = create_excel(template_file, data_dict)
                    if err:
                        st.error(err)
                    else:
                        st.balloons()
                        st.success("✨ 指導案Excelが完成しました！")
                        st.download_button(
                            label="📥 完成した指導案をダウンロード",
                            data=excel_data,
                            file_name="完成_指導案.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True,
                            type="primary"
                        )
                        
            except json.JSONDecodeError:
                st.error("❌ JSON解析エラー: 貼り付けたテキストが正しいJSON形式か確認してください。")
            except Exception as e:
                st.error(f"❌ 予期せぬエラー: {e}")