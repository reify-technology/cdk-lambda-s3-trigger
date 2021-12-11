import boto3
import os


class S3Lambda:
    def lambda_handler(event):
        # s3 = boto3.client('s3')
        bucket_name = (os.environ['BUCKET_NAME'])
        key = event['Records'][0]['s3']['object']['key']

        try:
            # Log the event
            print("[LambdaListenet] New file with name {} created in bucket {}".format(key, bucket_name))
            response = {'status': 'success', 'key': key}
            return response
        except Exception as e:
            print(e)
            print("[Error] :: Error processing file {} from bucket {}.   ".format(key, bucket_name))
            raise e
