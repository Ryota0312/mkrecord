# 記録書メーカー
+ templates と settings.yaml から記録書作る奴
+ Wiki に設定ファイルのサンプルとか書き方とか
  + http://github.com/Ryota0312/mkrecord/wiki

# Install
1. clone & pip install

```
$ git clone git@github.com:Ryota0312/mkrecord.git
$ pip install -r requirements.txt
```

2. Google Calendar API の有効化と認証情報の取得
   + mkrecord/ 以下に `credentials.json` という名前で認証情報を置いておく必要あり
   + https://console.cloud.google.com/apis/dashboard で取れるはず
	 + 「APIとサービス」でProject作成→「APIとサービスを有効化」→「Google Calendar API」
	 + 「認証情報」→「認証情報を作成」→「OAuth クライアントID」→「その他」を選んで作成
	 + 「JSONをダウンロード」みたいなやつでダウンロードして「credentials.json」という名前で配置

# Usage
+ 乃村研ミーティングの記録書を作る場合

```
$ python mkrecord.py settings/nom_settings.yaml
```

# How to setting
+ YAML形式で設定を記述する

  |項目名|内容|
  |-----|-----|
  |Template|テンプレートファイル(jinja2)|
  |PrevRecord|前回の記録書のパス|
  |Calendars|予定を取得するカレンダ|
  |Start|記録書の開始日|
  |End|記録書の終了日|
  |Date|ミーティングの日|
  |NextDate|今後の予定に入れたい日の終了日|
  |PrevCopy|前回の記録書からコピーする項目|
  |MeetingName|ミーティング名．RangeAutoSetFlagがTrueのときこの名前の予定をカレンダから取得して使用する．（正規表現可）|
  |RangeAutoSetFlag|Trueに設定するとMeetingNameをカレンダから探して自動的に日付関係を決定してくれる|

+ これ以外もそれっぽく埋める
+ TODO:ドキュメントちゃんと書く

# 免責事項
本プログラムを使用したことによる一切の損害について，当方は一切の責任を負いかねますのでご了承ください．
（怒られても責任は取りません!）
