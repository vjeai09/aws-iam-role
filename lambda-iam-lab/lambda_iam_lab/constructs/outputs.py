from aws_cdk import CfnOutput
from constructs import Construct


class StackOutputsConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        bucket_name: str,
        lambda_function_name: str,
        role_arn: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        CfnOutput(self, "BucketName", value=bucket_name)
        CfnOutput(self, "LambdaFunctionName", value=lambda_function_name)
        CfnOutput(self, "UnifiedRoleArn", value=role_arn)

