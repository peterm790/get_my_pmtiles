import boto3
import json
import os

def lambda_handler(event, context):
    credentials = event['credentials']
    upload_id = event['upload_id']
    part_num = event['part_num']
    byte_position = event['byte_position']
    part_size = event['part_size']

    source_bucket = event.get('source_bucket', 'us-west-2.opendata.source.coop')
    source_key = event.get('source_key', 'protomaps/openstreetmap/tiles/v3.pmtiles')
    dest_bucket = os.environ['DESTINATION_BUCKET']
    dest_key = 'v3.pmtiles'

    # S3 read client
    s3_client_source = boto3.client(
        's3',
        aws_access_key_id=credentials['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=credentials['AWS_SECRET_ACCESS_KEY'],
        aws_session_token=credentials['AWS_SESSION_TOKEN'],
    )

    # s3 write client
    s3_client_dest = boto3.client('s3')

    # Read the part from the source object
    response = s3_client_source.get_object(
        Bucket=source_bucket,
        Key=source_key,
        Range=f'bytes={byte_position}-{byte_position + part_size - 1}'
    )
    
    part_data = response['Body'].read()
    
    # Upload the part to the destination object
    upload_response = s3_client_dest.upload_part(
        Bucket=dest_bucket,
        Key=dest_key,
        PartNumber=part_num,
        UploadId=upload_id,
        Body=part_data
    )

    return upload_response