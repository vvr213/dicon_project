#!/usr/bin/env bash
# エラーが起きたら即停止
set -o errexit

# 1. ライブラリのインストール
pip install -r requirements.txt

# 2. 静的ファイル（画像やCSS）の収集
python manage.py collectstatic --no-input

# 3. データベースの構築
python manage.py migrate

# 4. データの読み込み（data.jsonがあれば）
if [ -f data.json ]; then
    echo "Loading data from data.json..."
    # python manage.py loaddata data.json
fi