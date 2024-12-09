from minio import Minio
from minio.error import S3Error

class Settings:
    def __init__(self):
        self.url = None
        self.bucket = None
        self.access_key = None
        self.secret_key = None

class S3Client(object):
    def __init__(self, url, access_key, secret_key, bucket):
        self._url = url
        self._access_key = access_key
        self._secret_key = secret_key
        self._bucket = bucket

        self.client = Minio(
            endpoint=self._url,
            access_key=self._access_key,
            secret_key=self._secret_key,
            secure=False)
        
    def upload_image(self, object_name, data, metadata=None):
        try:
            self.client.put_object(
                bucket_name=self._bucket,
                object_name=object_name,
                data=data,
                length=data.getbuffer().nbytes,
                content_type='image/png',
                metadata=metadata
            )
        except S3Error as err:
            print(err)
    
    def upload_meta(self, object_name, data):
        try:
            self.client.put_object(
                bucket_name=self._bucket,
                object_name=object_name,
                data=data,
                length=data.getbuffer().nbytes,
                content_type='application/json',
            )
        except S3Error as err:
            print(err)

g_settings = Settings()
g_s3_client = None


def clear_s3_client():
    global g_s3_client
    g_s3_client = None

def get_s3_client():
    global g_s3_client
    global g_settings
    if g_s3_client is None:
        g_s3_client = S3Client(g_settings.url, g_settings.access_key, g_settings.secret_key, g_settings.bucket)
    return g_s3_client