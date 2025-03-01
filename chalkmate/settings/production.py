from .base import *

DEBUG = False
ALLOWED_HOSTS = ["*"]  # Allows access from any host

# 3rd party apps
THIRD_PARTY_APPS = ["corsheaders"]
INSTALLED_APPS += THIRD_PARTY_APPS

# added middlewares
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", *MIDDLEWARE]


CORS_ALLOW_ALL_ORIGINS = False
ACCESS_CONTROL_ALLOW_HEADERS=True
CORS_ALLOW_HEADERS=['*']
CORS_ALLOWED_ORIGIN_REGEXES = [
    r'.*'
]

# media
MEDIA_URL = "/media/"

# media & static
AWS_ACCESS_KEY_ID = ENV.str("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = ENV.str("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "nxnearby-assets"
AWS_DEFAULT_ACL = "public-read"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_S3_REGION_NAME = ENV.str("AWS_S3_REGION_NAME")
AWS_LOCATION = "media"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
