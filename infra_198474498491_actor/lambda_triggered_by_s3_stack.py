from aws_cdk import (
    core as cdk,
    aws_lambda as _lambda
)


class LambdaTriggeredByS3Stack(cdk.Stack):
    def __init__(
            self,
            scope: cdk.Construct,
            construct_id: str,
            **kwargs) -> None:

        super().__init__(scope, construct_id, **kwargs)

        _lambda.Function(
            self,
            "MyTddLambda",
            code=_lambda.Code.from_asset("src/lambda_modules/lambda_s3"),
            handler="handler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            environment={
                "AWS_REGION": "eu-west-1",
                "DB_TABLE_NAME": "chnaged-by-cdk-stack",
            }
        )
