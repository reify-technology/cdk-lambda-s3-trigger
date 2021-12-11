from aws_cdk import (
    core,
    assertions,
)

from infra_198474498491_actor.lambda_triggered_by_s3_stack import (
    LambdaTriggeredByS3Stack,
)


def test_lambda_created():
    app = core.App()
    stack = LambdaTriggeredByS3Stack(app, "infra-198474498491-actor")
    template = assertions.Template.from_stack(stack)
    envCapture = assertions.Capture()

    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Handler": "handler",
            "Environment": envCapture,
        }
    )

    assert envCapture.as_object() == {
            "Variables": {
                "AWS_REGION": "eu-west-1",
                "DB_TABLE_NAME": "chnaged-by-cdk-stack",
                },
            }
