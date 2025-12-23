① プロジェクト概要
卒業制作として制作中の Django Webアプリです。
開発環境では SQLite、本番環境では PostgreSQL を使用予定です。

② 技術構成
Python
Django
SQLite（開発）
PostgreSQL（本番予定）

③ 設計上の工夫
## 設計のポイント
- 機密情報（SECRET_KEY, DB接続情報）は .env ファイルで管理
- .env は .gitignore に含め、GitHub には公開しない設計
- 開発環境と本番環境でデータベースを切り替え可能な構成

settings.py の「抜粋＋解説」

from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("SECRET_KEY")
本アプリでは、機密情報を GitHub に含めないため、
.env ファイルを用いて SECRET_KEY を管理している。

開発時は SQLite を使用し、本番環境では環境変数（DATABASE_URL）から接続情報を読み込み上書きする構成としている。
# config/settings.py（抜粋）

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# 本番環境（DATABASE_URLがある場合は上書き）
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    import dj_database_url
    DATABASES["default"] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)

## ディレクトリ構成
config/
  Django全体の設定を管理するディレクトリ（settings.py, urls.py など）

dicon_app/
  本アプリの主要機能を担うアプリケーションディレクトリ

templates/
  HTMLテンプレートを配置

static/
  CSS・画像などの静的ファイルを管理

設定ファイルとアプリケーションを分離することで、保守性と可読性を高めた構成としている。


## DATABASE（開発／本番の切り替え方）
本アプリは、開発環境と本番環境でデータベースを切り替えられるように設計している。
- 開発環境：SQLite（手軽に動作確認できるため）
- 本番環境：PostgreSQL（運用を想定し、環境変数から接続情報を読み込む）

開発時は `db.sqlite3` を使用し、本番では `.env`（または DATABASE_URL）で指定したPostgreSQLへ接続する。
機密情報（DB接続情報）をGitHubに含めないため、設定は環境変数で管理している。
READMEに「設定例（抜粋）」も入れるなら（さらに加点）


## dicon_app の役割
dicon_app は本アプリの主要機能（画面表示、データ登録、業務ロジック）を担当するDjangoアプリである。

- models.py：データ構造（テーブル設計）
- views.py：画面表示や処理（ルーティング先の処理）
- urls.py：ページURLと処理の紐付け（※作成予定）
- templates/：画面（HTML）（※作成予定）


## 今後の実装予定（開発ロードマップ）

- トップページ（home）の表示（URL / View / Template の接続）
- ユーザー機能（ログイン／ログアウト／権限に応じた表示）
- 商品・依頼情報の登録／一覧／詳細表示（DB連携）
- 注文（依頼）フローの実装（作成・確認・完了）
- 管理画面（admin）からのデータ管理

### 発展的な機能（卒業制作として検討）

- 外部決済サービス（例：Stripe 等）との連携
- LINE通知・連携（注文完了通知、店舗向け通知など）
- 本番環境（PostgreSQL）へのデプロイ


1. admin.py に list_display を追加
2. 一覧で price が出るのを確認
管理画面では商品名・価格を一覧表示できるよう設定している。