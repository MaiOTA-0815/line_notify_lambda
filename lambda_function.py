import json
import requests
from datetime import datetime, timedelta, timezone

# 🔐 チャンネルアクセストークンとグループID（ここは必ず正しく！）
CHANNEL_ACCESS_TOKEN = "XXXXXXX"
GROUP_ID = "XXXXXXXX"
test_mode = False  # ← True にするといつでも通知される（デバッグ用）

# 📤 LINEメッセージ送信関数
def push_line_message(message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    body = {
        "to": GROUP_ID,
        "messages": [{"type": "text", "text": message}]
    }
    response = requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        data=json.dumps(body)
    )
    print("🌸 LINE送信レスポンス:", response.status_code)
    print(response.text)

# 🚀 Lambdaメイン関数
def lambda_handler(event, context):
    # 📩 Webhookイベントかどうかを正確に判定
    if event.get("headers", {}).get("x-line-signature"):
        print("📩 Webhookイベント：通知せず終了します。")
        return {
            'statusCode': 200,
            'body': json.dumps('No action on webhook event')
        }

    # 📅 JST時間で現在日を取得
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    today_str = now.strftime("%Y年%m月%d日 (%A)")
    print(f"📅 現在日時（JST）：{today_str}")

    # ✅ 通知条件：1日 or 15日、もしくは test_mode=True のとき
    if test_mode or now.day in [1, 15]:
        message = (
            f"おはようございます！☀今日は{today_str}です。\n"
            "今日もすてきな一日になりますように✨"
        )
        push_line_message(message)
    else:
        print("⏸ 本日は通知対象日ではありません。")

    return {"statusCode": 200, "body": json.dumps("Lambda実行完了")}
