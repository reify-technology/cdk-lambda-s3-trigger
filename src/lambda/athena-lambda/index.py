from handler import AthenaLambdaHanlder


def on_event(event):

    handler = AthenaLambdaHanlder()

    return handler.lambda_handler(event)
