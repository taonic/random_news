from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import os
import asyncio

from activities.s3_client import S3Client
from activities.static_generator import StaticSiteGenerator
from temporalio import activity

@dataclass
class DeployInput:
    bucket_name: str
    region: str = "us-east-1"
    section: str = ""
    news_data: List[Dict] = None

@activity.defn
async def deploy(input: DeployInput):
    """
    Standalone activity to generate and upload the static site to S3
    
    Args:
        input: DeployInput containing bucket name, region, and news_data
    """
    # Generate site
    activity.logger.info(f"Generating static site for deployment")
    output_dir = StaticSiteGenerator().generate_site(input.section, input.news_data)
            
    # Upload all files from the output directory
    activity.logger.info(f"Deploying static site to S3 bucket: {input.bucket_name}")
    s3_client = S3Client(input.bucket_name)
    upload_tasks = []
    for root, _, files in os.walk(output_dir):
        for file in files:
            local_path = os.path.join(root, file)
            
            # Calculate S3 key (path in the bucket)
            s3_key = os.path.relpath(local_path, output_dir)
            
            # Determine content type
            content_type = None
            if file.endswith('.html'):
                content_type = 'text/html'
            elif file.endswith('.css'):
                content_type = 'text/css'
            elif file.endswith('.js'):
                content_type = 'application/javascript'
            elif file.endswith('.json'):
                content_type = 'application/json'
            
            # Add upload task
            upload_tasks.append(s3_client.upload_file(local_path, s3_key, content_type))
    
    # Wait for all uploads to complete
    await asyncio.gather(*upload_tasks)