# backend.py
import logging

import boto3
from botocore.exceptions import ClientError


class BackendManager:
    def __init__(
        self,
        bucket_name: str,
        region: str,
    ):
        self.bucket_name = bucket_name
        self.region = region

    def ensure_backend(self):
        s3 = boto3.client("s3")

        try:
            logging.info(f"Checking for {self.bucket_name}")
            s3.head_bucket(Bucket = self.bucket_name)
        except ClientError:
            logging.warning(f"Creating {self.bucket_name}")

            s3.create_bucket(
                Bucket = self.bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": self.region
                })

            # Important to ensure that user error is recoverable
            s3.put_bucket_versioning(
                Bucket = self.bucket_name,
                VersioningConfiguration = {
                    "Status": "Enabled"
                })

            s3.put_bucket_encryption(
                Bucket = self.bucket_name,
                ServerSideEncryptionConfiguration={
                    "Rules": [{
                        "ApplyServerSideEncryptionByDefault": {
                            "SSEAlgorithm":"AES256"
                        }
                    }]
                })