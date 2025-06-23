#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime
import requests

# ── 設定部分 ─────────────────────────────────────────
WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
if not WEBHOOK_URL:
    raise RuntimeError("環境変数 SLACK_WEBHOOK_URL が設定されていません。")

# メンション（例: <!here>, <!channel>, <@USERID> など）
# 必要に応じて環境変数で設定する場合:
# MENTION = os.environ.get("SLACK_MENTION", "<!here>")
# 今回は全員通知の <!here> を使用
MENTION = "<!channel>"

BASE_IMAGE_URL = "https://newsdig.ismcdn.jp/common/weather/latest/3hour/WM3hour_C46218.png"

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
# ── 設定部分 ここまで ─────────────────────────────────

def build_image_url() -> str:
    """
    キャッシュ回避のため、現在時刻を rd パラメータに付与。
    例: WM3hour_C46218.png?rd=202506230815
    """
    ts = datetime.now().strftime("%Y%m%d%H%M")
    url = f"{BASE_IMAGE_URL}?rd={ts}"
    logging.debug(f"生成した画像 URL: {url}")
    return url

def post_to_slack(image_url: str):
    """
    Slack にメンション付きで Block Kit の image ブロックを投稿。
    HTTP ステータス != 200 の場合は例外発生。
    """
    # ブロック組み立て
    blocks = []
    # メンション用セクション
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"{MENTION} 3時間ごとの天気予報をお送りします。"
        }
    })
    # 画像ブロック
    blocks.append({
        "type": "image",
        "image_url": image_url,
        "alt_text": "3時間ごとの天気予報画像"
    })

    payload = {
        "blocks": blocks
    }
    logging.info(f"Slack へ投稿開始: {image_url}")
    resp = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    if resp.status_code != 200:
        logging.error(f"Slack 投稿失敗: HTTP {resp.status_code} – {resp.text}")
        resp.raise_for_status()
    logging.info("Slack 投稿成功")

def main():
    try:
        img_url = build_image_url()
        post_to_slack(img_url)
    except Exception:
        logging.exception("スクリプト実行中にエラーが発生しました。")

if __name__ == "__main__":
    main()
