"""
Django settings for config project.
"""

# ==========================================
# 1. インポート（全部ここにまとめる）
# ==========================================
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url  # 本番用DBツール

# ==========================================
# 2. パスと環境変数の設定
# ==========================================
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# .envファイルを読み込む
load_dotenv(BASE_DIR / ".env")

# ==========================================
# 3. セキュリティ設定
# ==========================================
# SECRET_KEYは必ず環境変数から読み込む
SECRET_KEY = os.environ.get('SECRET_KEY')

# デフォルトはFalse（安全策）、環境変数があればそれに従う
# 手元の開発環境(.env)では DEBUG=True になっていればOK
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Renderの本番環境用設定
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# まだRenderの環境変数が設定できていないとき用の予備（全許可）
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['*']


# ==========================================
# 4. アプリケーション定義
# ==========================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 自作アプリ
    'dicon_app',
    'payments',
    'orders',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 画像・CSS対策
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # テンプレートフォルダ
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ==========================================
# 5. データベース設定（ここをスマートに修正！）
# ==========================================
# 基本はSQLite（手元用）だが、DATABASE_URL（本番用）があればそちらを使う
# この1行で自動切替できます
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}


# ==========================================
# 6. パスワード・言語・時間
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True


# ==========================================
# 7. 静的ファイル (CSS/JS/Image) 設定
# ==========================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 開発中に読み込む場所
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# 本番環境での圧縮配信設定（WhiteNoise）
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 画像アップロード設定
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==========================================
# 8. ログイン・ログアウト設定
# ==========================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = "dicon_app:home"
LOGOUT_REDIRECT_URL = "dicon_app:home"
LOGIN_URL = "accounts:login"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# ==========================================
# 9. 本番環境（Render）向けのセキュリティ微調整
# ==========================================
# Render上で動いているときはデバッグをオフにする
if 'RENDER' in os.environ:
    DEBUG = False