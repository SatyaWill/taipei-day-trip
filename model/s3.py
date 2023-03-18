import boto3, datetime
from botocore.config import Config
from setting import REGION, S3_ID, S3_KEY, BUCKET

s3 = boto3.client('s3',
                  region_name = REGION,
                  aws_access_key_id = S3_ID,
                  aws_secret_access_key = S3_KEY,
                  config=Config(signature_version='s3v4'))

def generate_upload_url():
    params = {
        'Bucket': BUCKET,
        'Key': "trip" + '/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S"), # S3檔案名稱
    }
    upload_url = s3.generate_presigned_url(ClientMethod='put_object', Params=params, ExpiresIn=3600)
    return upload_url

def delete_pic(url):
    if url.count('/') < 2:
        return
    file_key = url.split('/')[-2] + '/' + url.split('/')[-1]
    s3.delete_object(Bucket=BUCKET, Key=file_key)
    

    
