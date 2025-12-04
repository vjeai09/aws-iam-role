from aws_cdk import Duration, aws_lambda as lambda_
from constructs import Construct
from ..lambda_code.handler import LAMBDA_HANDLER_CODE


class LambdaFunctionConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        bucket_name: str,
        role,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.function = lambda_.Function(
            self,
            "S3ProcessorFunction",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="index.lambda_handler",
            code=lambda_.Code.from_inline(LAMBDA_HANDLER_CODE),
            role=role,
            environment={"BUCKET_NAME": bucket_name},
            timeout=Duration.seconds(30),
            memory_size=128,
        )

    @property
    def function_name(self) -> str:
        return self.function.function_name
