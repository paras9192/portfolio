from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]  # Allow all hosts

# 3rd party apps
THIRD_PARTY_APPS = ["corsheaders"]
INSTALLED_APPS += THIRD_PARTY_APPS

# Added middlewares
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", *MIDDLEWARE]

# CORS Configuration (Allow all from local)
CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins (including localhost)
CORS_ALLOW_CREDENTIALS = True  # Allow cookies and authentication headers
CORS_ALLOW_HEADERS = ["*"]  # Allow all headers
CORS_ALLOW_METHODS = ["*"]  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)

# Optional: If you want to allow all from local but restrict to specific domains in production
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.chalkmates\.com$",
    r"^https://.*\.yucampus\.com$",
    r"^http://localhost:\d+$",  # Allow any localhost port
    r"^http://127\.0\.0\.1:\d+$",
]

# Media settings
MEDIA_URL = "/media/"

# AWS S3 Storage
AWS_ACCESS_KEY_ID = ENV.str("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = ENV.str("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = ENV.str("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = "public-read"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_S3_REGION_NAME = ENV.str("AWS_S3_REGION_NAME")
AWS_LOCATION = "media"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
