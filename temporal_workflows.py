import logging
from datetime import timedelta
from typing import List, Dict, Any
from dataclasses import dataclass

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import CancelledError

@dataclass
class WorkflowInput:
    section: str
    count: int = 5
    s3_bucket: str = ""
    s3_region: str = "us-east-1"

# Import activities
with workflow.unsafe.imports_passed_through():
    from activities import generate, GenerateInput, deploy, DeployInput

# Define workflow interface
@workflow.defn
class GenNewsWorkflow:
    """Workflow that generates news for a specific section periodically and can deploy to S3"""
    
    def __init__(self):
        self._news_items = []
        self._section = ""
        self._count = 5
        self._running = True
        self._s3_bucket = ""
        self._s3_region = "us-east-1"
        self._website_url = ""
    
    @workflow.run
    async def run(self, input: WorkflowInput):
        """
        Run the news generation workflow.
        
        Args:
            input: WorkflowInput with section, count, and S3 configuration
            
        Returns:
            Dict with news items and website URL if deployed
        """
        self._section = input.section
        self._count = input.count
        self._s3_bucket = input.s3_bucket
        self._s3_region = input.s3_region
        
        # Set up timer for periodic regeneration
        try:
            while self._running:
                retry_policy = RetryPolicy(
                    initial_interval=timedelta(seconds=1),
                    maximum_interval=timedelta(seconds=10),
                )
                
                news_items = await workflow.execute_activity(
                    generate,
                    GenerateInput(self._section, self._count),
                    retry_policy=retry_policy,
                    start_to_close_timeout=timedelta(seconds=60)
                )
                
                await workflow.execute_activity(
                    deploy,
                    DeployInput(
                        bucket_name=self._s3_bucket,
                        region=self._s3_region,
                        section=self._section,
                        news_data=news_items
                    ),
                    retry_policy=retry_policy,
                    start_to_close_timeout=timedelta(seconds=120)
                )
                    
                await workflow.sleep(30)
        except CancelledError:
            # Handle workflow cancellation
            workflow.logger.info(f"News generation workflow for {self._section} was cancelled")
            self._running = False
            raise