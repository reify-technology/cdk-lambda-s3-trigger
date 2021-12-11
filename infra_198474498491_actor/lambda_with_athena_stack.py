from aws_cdk import core as cdk, aws_lambda as _lambda, aws_iam as iam


class LambdaAthenaStack(cdk.Stack):
    def __init__(
            self,
            scope: cdk.Construct,
            construct_id: str,
            **kwargs) -> None:

        super().__init__(scope, construct_id, **kwargs)

        athena_permission = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "athena:GetWorkGroup",
                "s3:PutObject",
                "s3:GetObject",
                "athena:StartQueryExecution",
                "s3:AbortMultipartUpload",
                "lambda:InvokeFunction",
                "athena:StopQueryExecution",
                "athena:GetQueryExecution",
                "athena:GetQueryResults",
                "s3:ListMultipartUploadParts",
            ],
            resources=[
                "*",
            ],
        )

        my_lambda = _lambda.Function(
            self,
            "MyAthenaLambda",
            code=_lambda.Code.from_asset("src/lambda_modules/lambda_athena"),
            handler="handler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            environment={
                "S3_BUCKET": "my-bucket",
            }
        )

        my_lambda.add_to_role_policy(athena_permission)
