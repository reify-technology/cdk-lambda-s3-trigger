from aws_cdk import core as cdk, aws_lambda as _lambda, aws_iam as iam

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class Infra198474498491ActorStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:

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
            code=_lambda.Code.from_asset("src/lambda/athena-lambda"),
            handler="on_event",
            runtime=_lambda.Runtime.PYTHON_3_8,
        )

        my_lambda.add_to_role_policy(athena_permission)
