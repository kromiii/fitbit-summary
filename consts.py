"""
Twitter認証ファイル、投稿する画像ファイルのフルパス。
cronで実行する（プロジェクトのルートフォルダから実行しない）ため、
絶対パスにする必要がある。
"""

from pathlib import Path
import json

TWEET_IMAGE = Path(__file__).parent / "tweet.png"
TWITTER_CONF = Path(__file__).parent / "twitter_conf.json"
# check if the file exists
if not TWITTER_CONF.exists():
  TWITTER = None
else:
  TWITTER = json.load(open(TWITTER_CONF, "r"))
