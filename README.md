# なにこれ？
manabaをクロールして、manaba内のデータを全検索できるプログラムです。  
お知らせやコースニュースだけではなく、wordやPDFファイル内も検索できます。（予定）  

![EpwVGHwUUAAjNys](https://user-images.githubusercontent.com/45098934/102771713-b63ef980-43c9-11eb-8146-a5f1175f7a81.png)


現在、このアプリはchromeの拡張機能とpythonのローカルサーバの２つで構成されています。  
chrome拡張機能が検索インターフェイス、ローカルサーバがクローリングと検索を行います。   
つまり**拡張機能だけでは使えず、常にローカルサーバを起動していないと使えません。**   
（近いうち拡張機能だけで独立できるような仕組みを考えます…）  


# 開発環境セットアップ
## chromedriverをダウンロード
[ここ](https://sites.google.com/a/chromium.org/chromedriver/downloads) から
自分のchromeバージョン以下で最大のバージョンのchromeをダウンロードして、 chromedriverを`/driver`に入れてください。

`crawl.py`の`driver = webdriver.Chrome(executable_path=<chromedirverへの絶対パス>)`を自分の環境に合うように変更して下さい。
wslでpythonを動かしているような人は、wslから見た絶対パスを入力して下さい。

## 依存ライブラリ
```
pip install selenium
pip install Node
pip install anytree
pip install flask
pip install flask_cors
```

## パスワードを記録
`config/password.py`を作成し manabaにログインするときのIDとパスワード以下のように入力してください。
```
ID = <ID>
PASSWORD = <PASSWORD>
```

## 拡張機能をインストール
chromeの拡張機能の設定から「パッケージ化されていない拡張機能を読み込む」を押して`chrome_extension`フォルダを選択して下さい。

## ローカルサーバ
ローカルサーバはクローリングと検索の２つの役割を持っています。
### クローリング
```
python crawl.py
```

### 検索サーバ
使うときはこれを常に起動していないと動きません…
```
python main.py
```
