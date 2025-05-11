import os
import logging
import aioboto3
from botocore.exceptions import ClientError
from typing import List, Optional
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class S3Client:
    """Client for interacting with AWS S3 using aioboto3"""
    
    def __init__(self, bucket_name: str):
        """
        Initialize the S3 client
        
        Args:
            bucket_name: The name of the S3 bucket to use
        """
        self.bucket_name = bucket_name
        self.session = aioboto3.Session()
        
    async def upload_file(self, file_path: str, s3_key: str, content_type: Optional[str] = None) -> bool:
        """
        Upload a file to S3
        
        Args:
            file_path: Local path to the file
            s3_key: S3 object key (path in the bucket)
            content_type: Optional content type (MIME type)
            
        Returns:
            bool: True if upload was successful, False otherwise
        """
        try:
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
            
            async with self.session.client('s3') as s3:
                await s3.upload_file(
                    file_path, 
                    self.bucket_name, 
                    s3_key,
                    ExtraArgs=extra_args
                )
            logger.info(f"Uploaded {file_path} to s3://{self.bucket_name}/{s3_key}")
            return True
        except ClientError as e:
            logger.error(f"Error uploading file to S3: {e}")
            return False