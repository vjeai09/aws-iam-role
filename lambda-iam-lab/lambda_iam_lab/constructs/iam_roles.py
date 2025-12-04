from aws_cdk import aws_iam as iam
from constructs import Construct


class IAMRolesConstruct(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.unified_role = iam.Role(
            self,
            "VjeaiUnifiedRole",
            role_name="vjeai-unified-role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ],
        )

    def grant_s3_access(self, bucket) -> None:
        bucket.grant_read_write(self.unified_role)

