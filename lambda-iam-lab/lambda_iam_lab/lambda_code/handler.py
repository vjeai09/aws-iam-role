LAMBDA_HANDLER_CODE = """
import json
import boto3
import os

s3_client = boto3.client('s3')
bucket_name = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        object_count = response.get('KeyCount', 0)
        objects = [obj['Key'] for obj in response.get('Contents', [])]
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully accessed bucket: {bucket_name}',
                'object_count': object_count,
                'objects': objects
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
"""
