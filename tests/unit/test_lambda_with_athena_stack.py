from aws_cdk import (
    core,
    assertions,
)

from infra_198474498491_actor.lambda_with_athena_stack import (
    LambdaAthenaStack
)


def test_lambda_created():
    app = core.App()
    stack = LambdaAthenaStack(app, "infra-198474498491-actor")
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
                "S3_BUCKET": "my-bucket",
                },
            }
