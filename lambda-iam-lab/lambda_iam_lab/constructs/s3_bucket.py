from aws_cdk import RemovalPolicy, aws_s3 as s3
from constructs import Construct


class S3BucketConstruct(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucket = s3.Bucket(
            self,
            "VjeaiDataBucket",
            bucket_name="vjeai-data-bucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            versioned=False,
            encryption=s3.BucketEncryption.S3_MANAGED,
        )

    @property
    def bucket_name(self) -> str:
        return self.bucket.bucket_name
