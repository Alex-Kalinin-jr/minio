import logging

from minio import Minio
from minio.error import S3Error

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(levelname)s - %(asctime)s - %(lineno)s - %(message)s"))
logger.addHandler(handler)



class MinioInstance:
    def __init__(self, url, acc_key, sec_key):
        self.client = Minio(url, acc_key, sec_key)
    
    def mock(self, source: str, dest: str, bucket_name: str):
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                logger.info(f"Created bucket {bucket_name}")
            self.client.fput_object(bucket_name, dest, source)
            logger.info(f"{source} was successfully uloaded as object {dest} to bucket {bucket_name}")
        except S3Error:
            logger.error("mock method - something went wrong")
