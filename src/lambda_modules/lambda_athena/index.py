import json
import os
import logging
import boto3

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def handler(event, context):
    '''
    Main Lambda function method
    '''
    print("works")
