from aws_cdk import Stack
from constructs import Construct
from .constructs.s3_bucket import S3BucketConstruct
from .constructs.iam_roles import IAMRolesConstruct
from .constructs.lambda_function import LambdaFunctionConstruct
from .constructs.outputs import StackOutputsConstruct


class LambdaIamLabStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 Bucket
        s3_bucket = S3BucketConstruct(self, "VjeaiS3Bucket")

        # Create IAM Role
        iam_roles = IAMRolesConstruct(self, "VjeaiIAMRoles")

        # Grant S3 access to role
        iam_roles.grant_s3_access(s3_bucket.bucket)

        # Create Lambda Function
        lambda_function = LambdaFunctionConstruct(
            self,
            "VjeaiLambdaFunction",
            bucket_name=s3_bucket.bucket_name,
            role=iam_roles.unified_role,
        )

        # Create Outputs
        StackOutputsConstruct(
            self,
            "VjeaiOutputs",
            bucket_name=s3_bucket.bucket_name,
            lambda_function_name=lambda_function.function_name,
            role_arn=iam_roles.unified_role.role_arn,
        )
