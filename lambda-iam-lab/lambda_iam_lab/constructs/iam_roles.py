from aws_cdk import aws_iam as iam
from constructs import Construct


class IAMRolesConstruct(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.lambda_role = iam.Role(
            self,
            "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ],
        )

        self.s3_access_role = iam.Role(
            self,
            "S3AccessRole",
            assumed_by=iam.AccountPrincipal(self.node.scope.account),
        )

    def grant_s3_access(self, bucket) -> None:
        bucket.grant_read_write(self.lambda_role)
        bucket.grant_read_write(self.s3_access_role)
