from constructs import Construct

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_iam as iam,
    Duration
)
from aws_cdk.aws_lambda_event_sources import S3EventSource
from aws_cdk.aws_lambda_python_alpha import PythonFunction

class MyPmtilesStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket
        bucket = s3.Bucket(self, "MyDestinationBucket",
            bucket_name="my-pmtiles-basemap",
            auto_delete_objects=False  # Prevents automatic deletion of bucket contents
        )

        # Create Lambda function
        lambda_function = _lambda.Function(self, 
            id = "FetchLatestPMtiles",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset("lambda/"),  # Directory containing your Lambda code
            timeout = Duration.minutes(15),
            memory_size=2000,
            environment={
                "DESTINATION_BUCKET": bucket.bucket_name
            }
        )

        bucket.grant_write(lambda_function)
        lambda_function.add_to_role_policy(iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=["arn:aws:s3:::us-west-2.opendata.source.coop/*"]
        ))

        lambda_function.add_to_role_policy(iam.PolicyStatement(
            actions=["sts:AssumeRole"],
            resources=[
                f"arn:aws:iam::{self.account}:role/ReadRole",  # Use self.account for current account ID
            ]
        ))