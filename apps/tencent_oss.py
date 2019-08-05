# -*- coding: utf-8 -*-

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

logger = logging.getLogger(__name__)


class TencentOss:
    def __init__(self):
        self.NO_AUTH_HOST = ""
        self.Region = ""
        self.SecretId = ""
        self.SecretKey = ""
        self.config = None
        self.client = None

    def init_from_app(self, app):
        self.NO_AUTH_HOST = app.config['NO_AUTH_HOST']
        self.Region = app.config['OSS_REGION']
        self.SecretId = app.config['OSS_ACCESSKEY_ID']
        self.SecretKey = app.config['OSS_ACCESSKEY_SECRET']
        self.config = CosConfig(Region=self.Region, SecretId=self.SecretId, SecretKey=self.SecretKey,
                                Token=None, Scheme='https')
        self.client = CosS3Client(self.config)

    def _upload_to_public(self,bucket, file_name, file_bytes):
        # Endpoint
        response = self.client.put_object(
            Bucket=bucket,
            Body=file_bytes,
            Key=file_name,
            EnableMD5=False
        )
        print(response['ETag'])

    def upload_image(self, img_name, file_bytes):
        bucket = 'xiaoyunbao-1253692831'
        self._upload_to_public(bucket,img_name, file_bytes)
        image_url = self.NO_AUTH_HOST + '/' + img_name
        return image_url
