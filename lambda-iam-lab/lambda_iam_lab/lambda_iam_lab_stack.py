from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_s3 as s3,
    RemovalPolicy,
    Duration,
)
from constructs import Construct

class LambdaIamLabStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 Bucket with auto-delete for clean destroy
        bucket = s3.Bucket(
            self, "LambdaDataBucket",
            bucket_name=None,  # Let CDK generate a unique name
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,  # Automatically delete objects on destroy
            versioned=False,
            encryption=s3.BucketEncryption.S3_MANAGED,
        )

        # Create IAM Role for Lambda with S3 access
        lambda_role = iam.Role(
            self, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="IAM role for Lambda function with S3 access",
            managed_policies=[
                # Basic Lambda execution permissions (CloudWatch Logs)
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ]
        )

        # Grant the Lambda role read/write access to the S3 bucket
        bucket.grant_read_write(lambda_role)

        # Create Lambda function
        lambda_function = lambda_.Function(
            self, "S3ProcessorFunction",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="index.lambda_handler",
            code=lambda_.Code.from_inline("""
import json
import boto3
import os

s3_client = boto3.client('s3')
bucket_name = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    try:
        # Example: List objects in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        
        object_count = response.get('KeyCount', 0)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully accessed bucket: {bucket_name}',
                'object_count': object_count
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
            """),
            role=lambda_role,
            environment={
                "BUCKET_NAME": bucket.bucket_name
            },
            timeout=Duration.seconds(30),
            memory_size=128
        )

        # Optional: Create additional IAM role for S3-only access (no Lambda)
        s3_only_role = iam.Role(
            self, "S3AccessRole",
            assumed_by=iam.AccountPrincipal(self.account),
            description="IAM role with S3 read/write access only",
        )
        
        bucket.grant_read_write(s3_only_role)

        # Export important values
        from aws_cdk import CfnOutput
        
        CfnOutput(
            self, "BucketName",
            value=bucket.bucket_name,
            description="S3 Bucket Name"
        )
        
        CfnOutput(
            self, "LambdaFunctionName",
            value=lambda_function.function_name,
            description="Lambda Function Name"
        )
        
        CfnOutput(
            self, "LambdaRoleArn",
            value=lambda_role.role_arn,
            description="Lambda Execution Role ARN"
        )
        
        CfnOutput(
            self, "S3RoleArn",
            value=s3_only_role.role_arn,
            description="S3 Access Role ARN"
        )
