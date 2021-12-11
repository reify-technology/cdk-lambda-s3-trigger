#!/usr/bin/env python3
from aws_cdk import core

from infra_198474498491_actor.lambda_triggered_by_s3_stack import (
    LambdaTriggeredByS3Stack
)

from infra_198474498491_actor.lambda_with_athena_stack import (
    LambdaAthenaStack
)

STACKS = {
    "lambdaS3": LambdaTriggeredByS3Stack,
    "lambdaAthena": LambdaAthenaStack
}


app = core.App()

for key, stack in STACKS.items():
    stack(
        app,
        key,
    )

# Infra198474498491ActorStack(
#     app,
#     "Infra198474498491ActorStack",
#     # If you don't specify 'env', this stack will be environment-agnostic.
#     # Account/Region-dependent features and context lookups will not work,
#     # but a single synthesized template can be deployed anywhere.
#     # Uncomment the next line to specialize this stack for the AWS Account
#     # and Region that are implied by the current CLI configuration.
#     # env=core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
#     # Uncomment the next line if you know exactly what Account and Region you
#     # want to deploy the stack to. */
#     # env=core.Environment(account='123456789012', region='us-east-1'),
#     # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
# )

app.synth()
