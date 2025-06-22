#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from datetime import datetime
import os

# ── 設定開始 ──
# 1) Incoming Webhook URL
WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", 
    "https://hooks.slack.com/services/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")

# 2) 投稿先チャンネル（Webhook で固定している場合は不要）
# CHANNEL = "#weather"

# 3) 取得元画像のベース URL
BASE_IMAGE_URL = "https://newsdig.ismcdn.jp/common/weather/latest/3hour/WM3hour_C46218.png"
# ── 設定終了 ──

def build_image_url():
    """キャッシュ回避のため、現在時刻を rd パラメータに付与"""
    ts = datetime.now().strftime("%Y%m%d%H%M")
    return f"{BASE_IMAGE_URL}?rd={ts}"

def post_to_slack(image_url: str):
    """Block Kit の image ブロックで投稿"""
    payload = {
        # "channel": CHANNEL,  # 必要なら有効化
        "blocks": [
            {
                "type": "image",
                "image_url": image_url,
                "alt_text": "3時間ごとの天気予報画像"
            }
        ]
    }
    resp = requests.post(WEBHOOK_URL, json=payload)
    resp.raise_for_status()

def main():
    img_url = build_image_url()
    post_to_slack(img_url)

if __name__ == "__main__":
    main()
