
from django.utils.functional import SimpleLazyObject
from storages.backends.s3boto import S3BotoStorage




AWS_ACCESS_KEY_ID='AKIAJD2OM3MYDTC2BFRQ'
AWS_SECRET_ACCESS_KEY='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'
StaticRootS3BotoStorage = lambda: S3BotoStorage(location='static')
MediaRootS3BotoStorage  = lambda: S3BotoStorage(location='media')