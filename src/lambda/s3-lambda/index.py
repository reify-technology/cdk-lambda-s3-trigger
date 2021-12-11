from handler import S3Lambda


def on_event(event, context):

    handler = S3Lambda()

    return handler.lambda_handler(event)
