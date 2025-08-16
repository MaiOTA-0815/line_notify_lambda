import os
import json
import logging
from datetime import datetime, timedelta, timezone
from time import sleep
import urllib.request


# ==== 環境変数 ====
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]  # LINEチャネルアクセストークン
GROUP_ID = os.environ["GROUP_ID"]                          # 送信先グループID (Cxxxxxxxx...)
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"  # "true"/"false"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


JST = timezone(timedelta(hours=9))



LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"

# ==== 入口判定 ====
def is_webhook(event: dict) -> bool:
    headers = event.get("headers") or {}
    keys = {k.lower(): v for k, v in headers.items()}
    return "x-line-signature" in keys  # 署名検証は別途入れる場合のみ

def is_scheduler(event: dict) -> bool:
    return event.get("source") in ("aws.events", "aws.scheduler")

# ==== LINE送信（標準ライブラリで実装） ====
def push_line_message(text: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
    }
    body = {
        "to": GROUP_ID,
        "messages": [{"type": "text", "text": text}],
    }
    data = json.dumps(body).encode("utf-8")

    # 簡易リトライ（429/5xx）
    for attempt in range(3):
        req = urllib.request.Request(LINE_PUSH_URL, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = resp.getcode()
                resp_body = resp.read().decode("utf-8")
                logger.info(f"LINE push attempt={attempt+1} status={status} body={resp_body}")
                if status < 400:
                    return
        except Exception as e:
            logger.warning(f"LINE push attempt={attempt+1} failed: {e}")
        sleep(1 + attempt)  # 1s, 2s, 3s

    raise RuntimeError("LINE push failed after 3 attempts")

# ==== メイン ====
def lambda_handler(event, context):
    now_utc = datetime.utcnow()
    now_jst = datetime.now(JST)
    logger.info(json.dumps({
        "event_source": event.get("source"),
        "entrypoint": "webhook" if is_webhook(event) else ("schedule" if is_scheduler(event) else "manual"),
        "now_utc": now_utc.isoformat(timespec="seconds") + "Z",
        "now_jst": now_jst.isoformat(timespec="seconds"),
        "jst_day": now_jst.day,
        "test_mode": TEST_MODE,
    }))

    # Webhook（LINEからの呼び出し）は通知しないで終了
    if is_webhook(event):
        logger.info("📩 Webhookイベント：通知せず終了します。")
        return {"statusCode": 200, "body": "ok(webhook)"}

    # スケジュール or 手動: 条件判定
    if TEST_MODE or now_jst.day in (1, 15):
        message = (
<<<<<<< HEAD
            f"おはようございます！☀今日は{today_str}です。\n"
            "今日もすてきな一日になりますように✨"
=======
            f"おはようございます！☀ 今日は {now_jst:%Y年%m月%d日 (%a)}、レボリューション・デーです。\n"
            "少しでも良いのでお題目をあげましょう〜✨"
>>>>>>> 9c0b7fd (chore: stop tracking build artifacts and update .gitignore)
        )
        try:
            push_line_message(message)
            logger.info("✅ LINE push OK")
        except Exception as e:
            logger.exception(f"❌ LINE push failed: {e}")
            raise
    else:
        logger.info("⏸ 本日は通知対象日ではありません。")

    return {"statusCode": 200, "body": "ok"}
