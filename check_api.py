import httpx
from openai import OpenAI, AuthenticationError

# --- ▼ ここにあなたのAPIキーを直接貼り付けてください ▼ ---
my_api_key = "AIzaSyD4c2LNcfcKJojQnyzm3lZkteX5xvgOUyI"
# --- ▲ ここまで ▲ ---

print("--- OpenAI APIキーの有効性チェックを開始します (プロキシ回避モード) ---")

if not my_api_key or "sk-xxxxxx" in my_api_key:
    print("エラー: APIキーが設定されていないか、仮のキーのままです。")
    print("`my_api_key = ...` の部分を、あなたの実際のキーに書き換えてください。")
else:
    try:
        # プロキシ設定を明示的に無効にしたHTTPクライアントを作成
        http_client = httpx.Client(proxies={})
        
        # 作成したクライアントを使って、OpenAIのクライアントを初期化
        client = OpenAI(api_key=my_api_key, http_client=http_client)

        print("APIサーバーに接続を試みています...")
        client.models.list() 

        print("\n🎉【成功】APIキーは有効です！認証に成功しました。")
        print("原因はネットワークのプロキシ設定でした。アプリ本体のコードも同様の修正が必要です。")

    except AuthenticationError:
        print("\n❌【失敗】認証エラーが発生しました。")
        print("APIキーが正しくないか、無効になっている可能性があります。")
        print("OpenAIのダッシュボードでキーを再確認・再発行してください。")
    except Exception as e:
        print(f"\n❌【失敗】予期せぬエラーが発生しました: {e}")

print("--- チェックを終了します ---")