import logging

from minio import Minio
from minio.error import S3Error

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(levelname)s - %(asctime)s - %(lineno)s - %(message)s"))
logger.addHandler(handler)


class MinioInstance:
    def __init__(self, url, acc_key, sec_key):
        self.client = Minio(url, access_key=acc_key, secret_key=sec_key, secure=False)


    def put_from_url(self, source: str, dest: str, bucket_name: str):
        try:
            if not self.client.bucket_exists(bucket_name):
                logger.info(f"Create bucket {bucket_name}")
                self.client.make_bucket(bucket_name)

            content_type =source.info().get("Content-Type")
            print(f"this is the content type {content_type}")

            result = self.client.put_object(bucket_name = bucket_name,
                                            object_name=dest,
                                            data=source,
                                            length=-1,
                                            part_size=10*1024*1024,
                                            )
            return result
        except S3Error as e:
            logger.error("put_from_url method error: %s", e)


    def get_by_name(self, bucket: str, name: str):
        try:
            response = self.client.get_object(bucket_name=bucket, object_name=name)
            return response.data
        finally:
            response.close()
            response.release_conn()


    def replace_by_name(self, bucket: str, name: str, url: str):
        try:
            _ = self.client.remove_object(bucket_name=bucket, object_name=name)
            _ = self.put_from_url(url, name, bucket)
        except S3Error as e:
            logger.error("put_by_name method error: %s", e)


    def remove_by_name(self, bucket: str, name: str):
        try:
            _ = self.client.remove_object(bucket_name=bucket, object_name=name)
        except S3Error as e:
            logger.error("remove_by_name method error: %s", e)