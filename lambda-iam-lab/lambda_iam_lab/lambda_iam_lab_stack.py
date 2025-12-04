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
        s3_bucket = S3BucketConstruct(self, "S3Bucket")

        # Create IAM Roles
        iam_roles = IAMRolesConstruct(self, "IAMRoles")

        # Grant S3 access to roles
        iam_roles.grant_s3_access(s3_bucket.bucket)

        # Create Lambda Function
        lambda_function = LambdaFunctionConstruct(
            self,
            "LambdaFunction",
            bucket_name=s3_bucket.bucket_name,
            role=iam_roles.lambda_role,
        )

        # Create Outputs
        StackOutputsConstruct(
            self,
            "Outputs",
            bucket_name=s3_bucket.bucket_name,
            lambda_function_name=lambda_function.function_name,
            lambda_role_arn=iam_roles.lambda_role.role_arn,
            s3_role_arn=iam_roles.s3_access_role.role_arn,
        )
