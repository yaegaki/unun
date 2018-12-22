# unun

## 概要

イオリンの生配信ワードクラウド作成用スクリプトと辞書、マスク画像。  
主に[yaegaki/pteraroron](https://github.com/yaegaki/pteraroron)で取得したコメントを対象とする。

## 使用方法

### 1. wordcloudをインストール

```
pip install wordcloud
```

### 2. MeCabのインストール

なんとかしてMeCabをインストールします。

### 3. mecab-ipadic-neologdの辞書を作成

必要な人は作成してインストールしてください。

### 4. dotlive辞書の作成

既にビルド済みのものが`dotlive.dic`として入っていますが新しく追加する場合は以下のコマンドを実行します。

```
# WSLでMeCabをインストールしたときのサンプル
/usr/lib/mecab/mecab-dict-index -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd -u dotlive.dic -f utf-8 -t utf-8 dotlive_dic.csv
```

### 5. フォントの取得

ワードクラウド用のフォントを取得します。  
基本的にはなんでもいいですが、サンプルではフリーの[源柔ゴシック ](http://jikasei.me/font/genjyuu/)を使用させていただいています。

### 6. コメントの取得

どのような手段でもいいのでコメントを取得します。

取得したコメントを記載したファイルを`livechat`ディレクトリに配置してください。

### 7. スクリプトを実行

```
# font_path: 取得したフォントのパス
python main.py font_path
```

`livechat`ディレクトリのファイルをパースして`output`ディレクトリにワードクラウドを保存します。

## サンプル

### 対象動画

[![video_thumbnail](https://img.youtube.com/vi/D_MtjBSv_AE/0.jpg)](https://www.youtube.com/watch?v=D_MtjBSv_AE)

### all

![iorin_wc_all](https://github.com/yaegaki/unun/blob/master/sample/D_MtjBSv_AE-all.png)

ストップワードを最小限にしたものです。  
すべての配信で共通するような頻出ワードがでかくなっています。  

### part

![iorin_wc_part](https://github.com/yaegaki/unun/blob/master/sample/D_MtjBSv_AE-part.png)

すべての配信で共通するような頻出ワードをストップワードに指定したものです。  
その配信独特のワードがでかくなっています。  
