import streamlit as st
import openpyxl
from openpyxl.styles import Alignment, Border, Side
import json
import io
import os
import re

# ページ設定
st.set_page_config(page_title="指導案作成WEBアプリ", layout="wide")

# ==========================================
# 1. プロンプト生成ロジック
# ==========================================
def generate_prompt_text(data):
    """ユーザー入力を基に、ChatGPT/Geminiへ投げるプロンプトを作成する"""
    
    prompt = f"""
あなたは特別支援学校および公立学校における熟練の教員です。
以下の【授業情報】を基に、学習指導案に必要な情報を補完し、指定の【JSON形式】のみで出力してください。
余計な挨拶や解説は不要です。JSONデータだけを返してください。

■ 【授業情報】
[必須項目]
・学部学年: {data['grade']}
・教科単元: {data['subject']}
・日時: {data['date']}
・時間: {data['time']}
・場所: {data['place']}
・本時の内容: {data['content']}

[任意項目（空欄の場合はあなたが教育的観点から最適に補完すること）]
・目標: {data['goals_in'] if data['goals_in'] else "未定（文脈に合わせて最大3つ生成せよ）"}
・評価の基準: {data['eval_in'] if data['eval_in'] else "未定（観点別：知識・技能、思考判断表現、主体的態度の3点を含めて生成せよ）"}
・学習内容のヒント: {data['flow_in'] if data['flow_in'] else "未定（自然な流れで導入・展開・まとめを構成せよ）"}

■ 【生成ルール】
1. **目標**: 最大3つ。簡潔に。
2. **評価の基準**: 30字程度で3項目（または文章で）。
3. **本時の展開**: 
   - 4～6ステップ程度で構成。
   - 1項目の学習内容は100字以内。
   - 「留意点」は学習内容とリンクさせ、特別支援（支援・配慮）の視点を入れること。
4. **準備物**: 必要なものを列挙。

■ 【出力フォーマット（厳守）】
以下のJSON構造を崩さずに返してください。
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
  "evaluation": ["評価基準1", "評価基準2", "評価基準3"],
  "flow": [
    {{
      "time": "5",
      "activity": "導入：挨拶と出席確認...",
      "notes": "元気よく挨拶するよう促す..."
    }},
    {{
      "time": "10",
      "activity": "展開1：...",
      "notes": "..."
    }}
  ],
  "materials": "iPad, プロジェクター, ワークシート..."
}}
"""
    return prompt

# ==========================================
# 2. Excel出力ロジック
# ==========================================
def create_excel(template_path, json_data):
    try:
        wb = openpyxl.load_workbook(template_path)
        ws = wb.active
    except Exception as e:
        return None, f"テンプレート読み込みエラー: {e}"

    # --- ① 基本情報の入力 ---
    # ユーザー入力そのものを優先するか、JSON(AI)を優先するかですが、
    # 基本情報はユーザー入力が正なのでJSON内のbasic_infoを使います。
    bi = json_data.get('basic_info', {})
    
    ws['C2'] = bi.get('grade', '')      # 学部学年
    ws['I2'] = bi.get('subject', '')    # 教科単元
    ws['C3'] = bi.get('date', '')       # 日時
    ws['K3'] = bi.get('time', '')       # 時間
    ws['N3'] = bi.get('place', '')      # 場所
    ws['C4'] = bi.get('content', '')    # 本時の内容

    # --- ② 目標（B10, B11, B12） ---
    goals = json_data.get('goals', [])
    # 最大3つまで
    if len(goals) > 0: ws['B10'] = f"・{goals[0]}"
    if len(goals) > 1: ws['B11'] = f"・{goals[1]}"
    if len(goals) > 2: ws['B12'] = f"・{goals[2]}"

    # --- ③ 評価の基準（B14） ---
    evals = json_data.get('evaluation', [])
    eval_text = "\n".join([f"・{e}" for e in evals])
    ws['B14'] = eval_text
    ws['B14'].alignment = Alignment(wrap_text=True, vertical='top')

    # --- ④ 本時の展開（A13～ 1行あけ） ---
    flow_list = json_data.get('flow', [])
    current_row = 13
    
    for item in flow_list:
        # 時間 (A列)
        ws[f'A{current_row}'] = item.get('time', '')
        ws[f'A{current_row}'].alignment = Alignment(horizontal='center', vertical='center')

        # 学習内容 (B列) ※テンプレート側でB-J結合されている前提
        ws[f'B{current_row}'] = item.get('activity', '')
        ws[f'B{current_row}'].alignment = Alignment(wrap_text=True, vertical='top')

        # 留意点 (K列) ※テンプレート側でK-M結合されている前提
        ws[f'K{current_row}'] = item.get('notes', '')
        ws[f'K{current_row}'].alignment = Alignment(wrap_text=True, vertical='top')

        # 次の項目は1行空ける（仕様に従う）
        current_row += 2 

    # --- 準備物 (N13) ---
    ws['N13'] = json_data.get('materials', '')
    ws['N13'].alignment = Alignment(wrap_text=True, vertical='top')

    # 保存
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output, None

# ==========================================
# 3. メイン画面 UI
# ==========================================
st.title("📝 指導案作成WEBアプリ")
st.markdown("ChatGPTやGeminiを使って指導案を作成し、Excelに出力します。")

# --- Step 1: 情報入力 ---
st.header("1. 基本情報を入力")
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        in_grade = st.text_input("学部学年", "小学部 5年")
        in_subject = st.text_input("教科単元", "生活単元学習「お祭りを開こう」")
        in_date = st.text_input("日時", "令和6年11月20日")
    with col2:
        in_time = st.text_input("時間", "45分")
        in_place = st.text_input("場所", "5年1組教室")
        in_content = st.text_input("本時の内容", "模擬店の商品作り")

    with st.expander("詳細設定（任意入力）- 空欄でもAIが補完します"):
        in_goals = st.text_area("目標（最大3つ）", height=68)
        in_eval = st.text_area("評価の基準", height=68)
        in_flow = st.text_area("学習内容・メモ（箇条書きなど）", height=100)

# データをまとめる
input_data = {
    "grade": in_grade, "subject": in_subject, "date": in_date,
    "time": in_time, "place": in_place, "content": in_content,
    "goals_in": in_goals, "eval_in": in_eval, "flow_in": in_flow
}

# --- Step 2: プロンプト生成 ---
st.header("2. AI用プロンプトを生成")
st.info("下のボタンを押すと、ChatGPT/Gemini用の命令文が作成されます。")

if st.button("プロンプト作成 📋"):
    prompt_text = generate_prompt_text(input_data)
    st.code(prompt_text, language="text")
    st.success("上のボックスの右上にあるコピーボタンでコピーし、ChatGPTやGeminiに貼り付けてください。")

# --- Step 3: AI出力の貼り付け ---
st.header("3. AIからの回答を貼り付け")
st.warning("AIから返ってきたJSONコード（{...} で始まる部分）をそのままここに貼り付けてください。")
json_input_str = st.text_area("ここにAIの回答をペースト", height=300)

# --- Step 4: Excel生成 ---
st.header("4. 指導案Excelのダウンロード")

if st.button("Excel作成実行 🚀"):
    if not json_input_str.strip():
        st.error("AIの回答が貼り付けられていません。")
    else:
        # JSON解析の試み（Markdownの ```json 等が含まれていても除去して解析）
        try:
            # ```json 等の除去
            clean_json = re.sub(r"```json\s*|\s*```", "", json_input_str).strip()
            # 先頭と末尾が { } でない場合のトリミング処理（簡易）
            start_idx = clean_json.find('{')
            end_idx = clean_json.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                clean_json = clean_json[start_idx:end_idx]
            
            data_dict = json.loads(clean_json)
            
            # Excel生成
            template_file = "指導案.xlsx"
            if not os.path.exists(template_file):
                st.error(f"サーバー上にテンプレートファイル '{template_file}' が見つかりません。")
            else:
                excel_data, err = create_excel(template_file, data_dict)
                if err:
                    st.error(err)
                else:
                    st.success("Excel生成に成功しました！")
                    st.download_button(
                        label="📥 指導案.xlsx をダウンロード",
                        data=excel_data,
                        file_name="完成_指導案.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
        except json.JSONDecodeError:
            st.error("貼り付けられたテキストをJSONとして解析できませんでした。AIが正しくJSON形式で返しているか確認してください。")
        except Exception as e:
            st.error(f"予期せぬエラーが発生しました: {e}")