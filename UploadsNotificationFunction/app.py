import boto3
import os

sns = boto3.client('sns')
topic_arn = os.environ['TOPIC_ARN']

def lambda_handler(event, context):
    print("Hello world lambda!!!")
    print(topic_arn)
    
    for record in event['Records']:
        message = record['body']
        message = record['body']
        print(f"Received message: {message}")
        sns.publish(TopicArn=topic_arn, Message=message)
    return {'status': 'done'}