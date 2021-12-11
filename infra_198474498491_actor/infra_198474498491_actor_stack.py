from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3_notify,
    core as cdk
)


class Infra198474498491ActorStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs):

        super().__init__(scope, construct_id, **kwargs)

        # _lambda.Function(
        #     self,
        #     "S3TriggeredLambda",
        #     code=_lambda.Code.from_asset("src/lambda/s3-lambda"),
        #     handler="on_event",
        #     runtime=_lambda.Runtime.PYTHON_3_8,
        # )

        # create new IAM group and use
        group = iam.Group(self, "s3-lambda-group")
        user = iam.User(self, "s3-lambda-user")

        # Add IAM user to the group
        user.add_to_group(group)

        # Create S3 Bucket
        bucket = s3.Bucket(self, 'vs-bucket')
        bucket.grant_read_write(user)
        # Create a lambda function
        lambda_func = _lambda.Function(
            self,
            'LambdaListener',
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler='LambdaListener.handler',
            code=_lambda.Code.from_asset("src/lambda/s3-lambda"),
            environment={'BUCKET_NAME': bucket.bucket_name}
        )
        # Create trigger for Lambda function using suffix
        notification = s3_notify.LambdaDestination(lambda_func)
        notification.bind(self, bucket)
        # Add Create Event only for .jpg files
        bucket.add_object_created_notification(
           notification, s3.NotificationKeyFilter(suffix='.jpg'))
