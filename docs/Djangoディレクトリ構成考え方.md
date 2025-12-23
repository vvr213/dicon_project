Djangoのディレクトリ構成、悩みますよね。「正解」が一つではないので、余計に混乱しやすい部分です。

授業で習う「教科書通り」の方法と、実際の開発現場で好まれる「モダン」な方法、そしてテンプレート（HTML）の置き場所による違いで、代表的な4つのパターンに整理しました。

それぞれの特徴を比較表にまとめましたので、自分のプロジェクトにどれが合うか選んでみましょう。
Django_構成パターン比較.md
12月20日 10:51

補足とアドバイス
後藤田さんの今回のプロジェクト（dicon_project）では、ガイドでお伝えした手順（django-admin startproject config .）を使っているので、すでにベースは**「パターン2（config型）」**になっています。

ここから**「パターン3（Webサイト重視型）」**にするのはとても簡単です。

プロジェクトの一番上に templates というフォルダを自分で作る。

その中に login.html を置く。

settings.py を一行書き換える（上記ファイルの最後を参照）。

これで、「HTMLの置き場所どこだっけ？」と迷うことなく、**「templatesフォルダを見れば全部ある！」**という分かりやすい状態で開発を進められます。

この構成で進めてみませんか？
ーーーーーーーーーーーーーーーーーーーーーーーーーーー

🏗️ Djangoプロジェクト構成：代表的な4パターン比較

「dicon_project」を作る場合の例で比較します。

📊 比較表

パターン

① 教科書デフォルト型

② config改名型

③ Webサイト重視型

④ 大規模開発型 (src)

コマンド

startproject dicon

startproject config .

startproject config .

(手動で構成変更)

設定フォルダ

dicon/dicon/

dicon/config/

dicon/config/

dicon/src/config/

HTMLの場所

各アプリの中

各アプリの中

一番外のフォルダ

各アプリの中

メリット

参考書と同じで安心

フォルダの役割が明確

HTMLが見つけやすい

本番環境が綺麗

デメリット

名前が被って混乱する

初見で少し戸惑う

アプリの再利用性が下がる

設定が複雑で難しい

おすすめ度

★☆☆ (学習用)

★★☆ (アプリ開発)

★★★ (卒業制作推奨)

★☆☆ (プロ向け)

📂 各パターンの詳細解説

1. 教科書デフォルト型（おすすめしません）

参考書でよく見る形です。プロジェクト名と設定フォルダ名が同じになります。

構成:

dicon_project/
├── manage.py
├── dicon/          <-- 設定フォルダ（名前が被って紛らわしい！）
│   ├── settings.py
│   └── urls.py
└── accounts/       <-- アプリ
    └── templates/
        └── accounts/
            └── login.html  <-- 深い...


なぜ微妙？: 「どっちのdiconフォルダの話？」と混乱しがちです。

2. config改名型（スマートな標準）

設定フォルダを config という名前にする方法です。私が先ほどのガイドで案内したのはこれです。

構成:

dicon_project/
├── manage.py
├── config/         <-- 「ここは設定だ」とすぐ分かる
│   ├── settings.py
│   └── urls.py
└── accounts/
    └── templates/
        └── accounts/
            └── login.html


良さ: import config と書けるのでコードが読みやすくなります。

3. Webサイト重視型（卒業制作にイチオシ！）

②の派生形です。 HTMLファイル（テンプレート）を、アプリの中ではなく、プロジェクトの一番外側にまとめます。

構成:

dicon_project/
├── manage.py
├── config/
├── accounts/       <-- アプリ（中身はPythonコードだけ！）
├── shop/           <-- アプリ
└── templates/      <-- ここに全部のHTMLを置く
    ├── base.html
    ├── index.html
    └── login.html  <-- すぐ見つかる！


なぜおすすめ？:

「デザイン修正したいな」と思った時、あちこちのアプリフォルダを開かなくて済みます。

Webサイト全体で共通のデザイン（ヘッダーやフッター）を管理しやすいです。

必要な設定: settings.py の TEMPLATES の DIRS に BASE_DIR / 'templates' を追記するだけ。

4. 大規模開発型（srcフォルダ）

全てのプログラムを src フォルダに閉じ込め、Dockerfileなどを外に出す構成です。

構成:

dicon_project/
├── Dockerfile
├── requirements.txt
└── src/            <-- ソースコード用フォルダ
    ├── manage.py
    ├── config/
    └── accounts/


良さ: フォルダ直下がスッキリしますが、コマンドを打つときに cd src が必要だったり、パスの設定が難しくなるので、今回は避けましょう。

🏆 結論：今回の「dicon_project」には？

【パターン3：Webサイト重視型】 がおすすめです！

理由:

config フォルダ方式なら、設定ファイルがどこにあるか一発でわかります。

templates フォルダを外に出すと、「HTMLどこだっけ？」と探す時間が激減します。

卒業制作のような「一つのWebサービス」を作る場合、アプリごとにHTMLを分けるメリットがあまりありません。

パターン3にするための settings.py 設定例

config/settings.py を開き、TEMPLATES の部分を少し書き換えるだけで実現できます。

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],  <-- 元はこれ
        'DIRS': [BASE_DIR / 'templates'],  # <-- こう書き換えるだけ！
        'APP_DIRS': True,
        # ...省略
    },
]
