# [Fitbit-Summary]Fitbitを使った健康報告バッチ

毎晩23時にFitbit APIを使って健康情報をTwitterに投稿する
プログラムの実行はGithub Action で行う。

## Fitbit Web API

[https://dev.fitbit.com/build/reference/web-api/](https://dev.fitbit.com/build/reference/web-api/)

## エントリーポイント

```bash
python ./main.py
```

## Dependencies

* requests
* tweepy
* matplotlib

## スクリプトについて

- *main.py* エントリーポイント
- *api.py* Fitbit Web APIの実行
- *graph.py* 心拍数やSpO2データをグラフ化し画像にする
- *consts.py* 定数を定義する

## 必要なファイル

### ■ *conf.json* fitbit conf file

```json
{
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "access_token": "your-access-token",
  "refresh_token": "your-refresh-token",
  "redirect_uri": "your-redirect-url",
  "user_id": "your-user-id",
  "scope": "your-scope"
}
```

*client_id*,*access_token*,*refresh_token*の3点あれば動きます。

### ■ *twitter_conf.json* twitter conf file

```json
{
  "API_KEY": "MY-API-KEY",
  "API_SECRET": "MY-API-SECRET",
  "BEARER": "MY-BEARER",
  "ACCESS_TOKEN": "MY-ACCESS-TOKEN",
  "ACCESS_SECRET": "MY-ACCESS-SECRET"
}
```

## 出力されるファイル

- **heart-spo.png** tweetする画像

## Github Action

環境変数にconf.json,twitter_conf.jsonの内容を設定する。

### スケジュール

| 分 | 時 | 日 | 月 | 曜日 |
|----|----|----|----|----|
| 0-59 | 0-23 | 1-31 | 1-12 | 0-7 |

- 曜日は0,7が日曜日。
- ```*```は全ての値を設定したことになる。分を*にすると毎分になる。
- ex: 0 2 * * * 毎日2時00分に実行
- ex: * 2 * * * 毎日2時の**毎分**実行

