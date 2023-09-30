"""
Fitbit APIで心拍、アクティビティ、睡眠、SPO2情報を取得。
グラフ化してtwitterに投稿する。
ex: main()
"""
import datetime
from graph import graph_heart_spo
import pytweet
from api import heartbeat, spo2_intraday, activity_summary, sleep_log
from consts import TWEET_IMAGE, TWITTER

TAGS = "#Fitbit #Fitbit_Web_API"


def min_to_hr(t: int) -> str:
    """XX(分)→〇時館△分に変換

    Args:
        t (int): 分

    Returns:
        str: 〇時館△分
    """
    hr = t // 60
    m = t % 60
    if hr == 0:
        return str(m) + "分"
    return str(hr) + "時間" + str(m) + "分"


def today() -> str:
    """本日の日付を返す。

    Returns:
        str: YYYY-MM-DD
    """
    now = datetime.datetime.now()
    return f"{now.year}-{now.month}-{now.day}"


def main():
    """main処理
    Fitbit APIで心拍、アクティビティ、睡眠、SPO2情報を取得。
    グラフ化してtwitterに投稿
    """
    # データ取得
    heart = heartbeat().json()
    spo = spo2_intraday().json()
    sleep = sleep_log().json()
    act = activity_summary().json()

    # データ取得にエラーが無いかチェック
    is_error = heart.get("errors") is not None \
        or spo.get("errors") is not None \
        or sleep.get("errors") is not None \
        or act.get("errors") is not None

    # エラーになってなくてもデータが入ってない場合もあるので
    # 必要なデータ（キー）が存在しているかチェック
    # spo.get("minutes") is None \ は除外。しばしば取得できないので。
    # sleep["summary"].get("stages") is Noneも除外。しばしば取得できないので。
    is_empty = heart.get("activities-heart") is None \
        or act.get("summary") is None \
        or sleep.get("summary") is None

    # error時はerrorツイートをして終了
    if is_error or is_empty:
        msg = "[" + today() + "]" + "\n"
        msg += "今日はエラーになったみたい\n"
        msg += TAGS
        twitter = Pytweet(TWITTER)
        twitter.tweet(msg)
        return

    # 歩数、フロア数、カロリーをactivityから取得
    act_summary = act["summary"]
    print(act_summary)
    steps = act_summary["steps"]
    calories = act_summary["caloriesOut"]

    # 睡眠情報をsleepから取得
    sleep_summary = sleep["summary"]
    bed_time = sleep_summary["totalTimeInBed"]
    # sleep_summary["stages"]が設定されていない場合もあるので、、、
    is_stages = sleep_summary.get("stages")
    deep = 0 if not is_stages else sleep_summary["stages"]["deep"]
    light = 0 if not is_stages else sleep_summary["stages"]["light"]
    rem = 0 if not is_stages else sleep_summary["stages"]["rem"]
    wake = 0 if not is_stages else sleep_summary["stages"]["wake"]

    # 上記からメッセージを生成
    msg = "🏃くろみーの日報\n"
    msg += "[" + today() + "]" + "\n"
    msg += "👟運動情報👟\n"
    msg += "歩数: " + str(steps) + "\n"
    msg += "消費cal: " + str(calories) + "\n"
    msg += "💤睡眠情報💤\n"
    msg += "ベッド時間: " + min_to_hr(bed_time) + "\n"
    msg += "深い睡眠: " + min_to_hr(deep) + "\n"
    msg += "浅い睡眠: " + min_to_hr(light) + "\n"
    msg += "レム睡眠: " + min_to_hr(rem) + "\n"
    msg += "覚醒: " + min_to_hr(wake) + "\n"
    msg += TAGS + "\n"
    # グラフ生成(heart-spo.pngが出力される)
    graph_heart_spo(heart, spo, sleep, TWEET_IMAGE)

    # tweetする
    # tweet(msg, TWEET_IMAGE)
    twitter = Pytweet(TWITTER)
    twitter.tweet(msg, TWEET_IMAGE)


main()
