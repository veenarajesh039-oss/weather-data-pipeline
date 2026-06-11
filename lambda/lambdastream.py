import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')

BUCKET = 'your_buckrt_name'

def lambda_handler(event, context):

    for record in event['Records']:

        if record['eventName'] == 'INSERT':

            data = record['dynamodb']['NewImage']

            filename = f"weather/weather_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"

            s3.put_object(
                Bucket=BUCKET,
                Key=filename,
                Body=json.dumps(data)
            )

    return {
        'statusCode': 200
    }