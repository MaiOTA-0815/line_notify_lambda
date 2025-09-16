import os
import json
import logging
from datetime import datetime, timedelta, timezone
from time import sleep
import urllib.request
from typing import Optional

# ===== ログ設定 =====
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ===== タイムゾーン =====
JST = timezone(timedelta(hours=9))
UTC = timezone.utc

# ===== 環境変数 =====
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]  # LINEチャネルアクセストークン
GROUP_ID = os.environ["GROUP_ID"]                          # 送信先グループID (Cxxxxxxxx...)
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"  # "true"/"false"
LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"

# ===== 入口判定 =====
def is_webhook(event: dict) -> bool:
    """LINEのWebhook経由かどうか（署名検証は別途実装する場合のみ）"""
    headers = (event or {}).get("headers") or {}
    keys = {str(k).lower(): v for k, v in headers.items()}
    return "x-line-signature" in keys

def is_scheduler(event: dict) -> bool:
    """EventBridge（rules/scheduler）経由かどうか"""
    return (event or {}).get("source") in ("aws.events", "aws.scheduler")

# ===== 安全弁（時刻ガード） =====
def should_send_now(now_utc: Optional[datetime] = None, *, slack_min: int = 2) -> bool:
    """
    毎月1日/15日の 09:00 JST ぴったり（±slack_min分）だけ True を返す安全弁。
    EventBridge を UTC 00:00（= JST 09:00）で発火させる前提。
    """
    now_utc = now_utc or datetime.now(UTC)
    now_jst = now_utc.astimezone(JST)

    # 日付ガード
    if now_jst.day not in (1, 15):
        return False

    # 時刻ガード（±数分の遅延許容）
    target = now_jst.replace(hour=9, minute=0, second=0, microsecond=0)
    delta_sec = abs((now_jst - target).total_seconds())
    return delta_sec <= slack_min * 60

# ===== LINE送信（標準ライブラリで実装：簡易リトライ付き） =====
def push_line_message(text: str) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
    }
    body = {
        "to": GROUP_ID,
        "messages": [{"type": "text", "text": text}],
    }
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")

    # 429/5xx を想定した指数バックオフ風リトライ（1s,2s,3s）
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
        sleep(1 + attempt)

    raise RuntimeError("LINE push failed after 3 attempts")

# ===== メイン =====
def lambda_handler(event, context):
    now_utc = datetime.now(UTC)
    now_jst = now_utc.astimezone(JST)

    logger.info(json.dumps({
        "event_source": (event or {}).get("source"),
        "entrypoint": "webhook" if is_webhook(event) else ("schedule" if is_scheduler(event) else "manual"),
        "now_utc": now_utc.isoformat(timespec="seconds"),
        "now_jst": now_jst.isoformat(timespec="seconds"),
        "jst_day": now_jst.day,
        "test_mode": TEST_MODE,
    }, ensure_ascii=False))

    # Webhook（LINEからの呼び出し）は通知せず終了
    if is_webhook(event):
        logger.info("📩 Webhookイベント：通知せず終了します。")
        return {"statusCode": 200, "body": "ok(webhook)"}

    # スケジュール or 手動：安全弁で厳密判定
    if TEST_MODE or should_send_now(now_utc, slack_min=2):
        message = (
            f"おはようございます！☀ 今日は {now_jst:%Y年%m月%d日 (%a)}、レボリューション・デーです。\n"
            "少しでも良いのでお題目をあげましょう〜✨"
        )
        try:
            push_line_message(message)
            logger.info("✅ LINE push OK")
        except Exception as e:
            logger.exception(f"❌ LINE push failed: {e}")
            raise
    else:
        logger.info("⏸ 本日は通知対象時間ではありません。（安全弁で抑止）")

    return {"statusCode": 200, "body": "ok"}
