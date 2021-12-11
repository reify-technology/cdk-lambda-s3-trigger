import json
import os
import unittest
import boto3
import mock
from moto import mock_s3
from moto import mock_dynamodb2

S3_BUCKET_NAME = 'amaksimov-s3-bucket'
DEFAULT_REGION = 'us-east-1'
S3_TEST_FILE_KEY = 'prices/new_prices.json'
S3_TEST_FILE_CONTENT = [
    {"product": "Apple", "price": 15},
    {"product": "Oranges", "price": 25}
]

DYNAMODB_TABLE_NAME = 'default-test'


@mock_s3
@mock_dynamodb2
@mock.patch.dict(os.environ, {'DB_TABLE_NAME': DYNAMODB_TABLE_NAME})
class TestLambdaFunction(unittest.TestCase):
    def setUp(self):
        # S3 setup
        self.s3 = boto3.resource('s3', region_name=DEFAULT_REGION)
        self.s3_bucket = self.s3.create_bucket(Bucket=S3_BUCKET_NAME)
        self.s3_bucket.put_object(Key=S3_TEST_FILE_KEY,
                                  Body=json.dumps(S3_TEST_FILE_CONTENT))

        # DynamoDB setup
        self.dynamodb = boto3.client('dynamodb')
        try:
            self.table = self.dynamodb.create_table(
                TableName=DYNAMODB_TABLE_NAME,
                KeySchema=[
                    {'KeyType': 'HASH', 'AttributeName': 'product'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'product', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
        except self.dynamodb.exceptions.ResourceInUseException:
            self.table = boto3.resource('dynamodb').Table(DYNAMODB_TABLE_NAME)

    def test_get_data_from_file(self):
        from src.lambda_modules.lambda_s3.index import get_data_from_file

        file_content = get_data_from_file(S3_BUCKET_NAME, S3_TEST_FILE_KEY)
        self.assertEqual(file_content, S3_TEST_FILE_CONTENT)

    def test_save_data_to_db(self):
        from src.lambda_modules.lambda_s3.index import save_data_to_db

        for item in S3_TEST_FILE_CONTENT:
            save_data_to_db(item)

        db_response = self.table.scan(Limit=1)

        db_records = db_response['Items']

        while 'LastEvaluatedKey' in db_response:
            db_response = self.table.scan(
                Limit=1,
                ExclusiveStartKey=db_response['LastEvaluatedKey']
            )
            db_records += db_response['Items']

        self.assertEqual(len(S3_TEST_FILE_CONTENT), len(db_records))

    def test_handler(self):
        from src.lambda_modules.lambda_s3.index import handler

        event = {
            'Records': [
                {
                    's3': {
                        'bucket': {
                            'name': S3_BUCKET_NAME
                        },
                        'object': {
                            'key': S3_TEST_FILE_KEY
                        }
                    }
                }
            ]
        }

        result = handler(event, {})
        self.assertEqual(result, {'StatusCode': 200, 'Message': 'SUCCESS'})
