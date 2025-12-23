🚀 Django環境構築ガイド (ローカル: SQLite / 本番: PostgreSQL想定)

現在、dicon_project フォルダの中にいる想定です。
以下のコマンドを順番にターミナルに入力してください。

1. 仮想環境（venv）の作成
Pythonの「専用の部屋」を作ります。
python3 -m venv venv

2. 仮想環境の有効化
部屋に入ります。コマンドラインの先頭に (venv) と表示されれば成功です。
source venv/bin/activate

※もしWindowsの場合は venv\Scripts\activate ですが、Macの場合は上記でOKです。

3. Djangoのインストール
Django本体をインストールします。（MySQL用のライブラリは不要なので省きます）

pip install django

4. pipのアップグレード（念のため）
インストーラー自体を最新にしておきます。

pip install --upgrade pip

5. プロジェクトの作成
ここがポイントです！
config という名前で設定フォルダを作ると、管理がしやすくなります。
最後の「 . 」（ドット）を忘れないように注意してください。

django-admin startproject config .

6. データベースの初期化（マイグレーション）
SQLiteのデータベースファイルを作成します。

python manage.py migrate

7. サーバー起動確認
正しくインストールできたか確認します。
python manage.py runserver

🎉 成功したら...

ターミナルに以下のようなURLが表示されます。
Starting development server at http://127.0.0.1:8000/

キーボードの Command キーを押しながら、このURLをクリックしてみてください。
ブラウザで**「ロケットが発射された画面（The install worked successfully!）」**が表示されれば、環境構築は完璧です！

サーバーを止める時は、ターミナルで Ctrl + C を押してください。