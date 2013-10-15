
from django.utils.functional import SimpleLazyObject
from storages.backends.s3boto import S3BotoStorage




AWS_ACCESS_KEY_ID='AKIAIKGQ5IBXP5TT4ZBA'
AWS_SECRET_ACCESS_KEY='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'
StaticRootS3BotoStorage = lambda: S3BotoStorage(location='static')
MediaRootS3BotoStorage  = lambda: S3BotoStorage(location='media')