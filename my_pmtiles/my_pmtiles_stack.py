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

        # add tile server 

        # Define the Lambda function
        tile_server_lambda = _lambda.Function(
            self, 'TileServerLambda',
            runtime=_lambda.Runtime.NODEJS_18_X,
            handler='index.handler',
            code=_lambda.Code.from_asset('tile_server_lambda'),
            architecture=_lambda.Architecture.ARM_64,
            memory_size=512,
            environment={
                'BUCKET': bucket.bucket_name,
                'PUBLIC_HOSTNAME': 'denk0m991obk6.cloudfront.net'
            }
        )

        # Grant the Lambda function read/write permissions to the bucket
        bucket.grant_read_write(tile_server_lambda)

        # Enable Function URL with no authentication
        tile_server_lambda.add_permission(
            "FunctionURLPermission",
            principal=iam.ServicePrincipal("lambda.amazonaws.com"),
            action="lambda:InvokeFunctionUrl",
            function_url_auth_type=_lambda.FunctionUrlAuthType.NONE
        )