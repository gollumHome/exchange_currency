# -*- coding: utf-8 -*-

#import oss2
import logging


logger = logging.getLogger(__name__)


class AliyunOss:
    def __init__(self, app):
        self.NO_AUTH_HOST = app.config['NO_AUTH_HOST']
        self.auth = oss2.Auth(app.config['OSS_ACCESSKEY_ID'], app.config['OSS_ACCESSKEY_SECRET'])
        self.public_bucket = app.config['OSS_PUBLIC_BUCKET']
        self.private_bucket = app.config['OSS_PRIVATE_BUCKET']

    def _upload_to_public(self, img_name, file_bytes):
        # Endpoint
        bucket = oss2.Bucket(self.auth, 'oss-us-west-1.aliyuncs.com', self.public_bucket)
        bucket.put_object(img_name, file_bytes)

    def _upload_to_private(self, img_name, file_bytes):
        # Endpoint
        bucket = oss2.Bucket(self.auth, 'oss-us-west-1.aliyuncs.com', self.private_bucket)
        bucket.put_object(img_name, file_bytes)

    def upload_image(self, auth_access, img_name, file_bytes):
        if auth_access == 'yes':
            self._upload_to_private(img_name, file_bytes)
            image_url = self.sign_url('GET', img_name, 5 * 60)
        else:
            self._upload_to_public(img_name, file_bytes)
            image_url = self.NO_AUTH_HOST + '/' + img_name
        return image_url

    def sign_url(self, method, key, expires, headers=None, params=None):
        """生成签名URL。
                常见的用法是生成加签的URL以供授信用户下载，如为log.jpg生成一个5分钟后过期的下载链接::
                    >>> bucket.sign_url('GET', 'log.jpg', 5 * 60)
                    r'http://your-bucket.oss-cn-hangzhou.aliyuncs.com/logo.jpg?OSSAccessKeyId=YourAccessKeyId\&Expires=1447178011&Signature=UJfeJgvcypWq6Q%2Bm3IJcSHbvSak%3D'
                :param method: HTTP方法，如'GET'、'PUT'、'DELETE'等
                :type method: str
                :param key: 文件名
                :param expires: 过期时间（单位：秒），链接在当前时间再过expires秒后过期
                :param headers: 需要签名的HTTP头部，如名称以x-oss-meta-开头的头部（作为用户自定义元数据）、
                    Content-Type头部等。对于下载，不需要填。
                :type headers: 可以是dict，建议是oss2.CaseInsensitiveDict
                :param params: 需要签名的HTTP查询参数
                :return: 签名URL。
                """
        bucket = oss2.Bucket(self.auth, 'oss-us-west-1.aliyuncs.com', self.private_bucket)
        return bucket.sign_url(method, key, expires, headers, params)
