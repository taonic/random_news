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
    region: str = "us-east-1"
    model_id: str = ""

# Import activities
with workflow.unsafe.imports_passed_through():
    from activities import generate, GenerateInput, deploy, DeployInput

# Define workflow interface
@workflow.defn
class GenNewsWorkflow:
    """Workflow that generates news for a specific section periodically and can deploy to S3"""
    
    def __init__(self):
        self._section = ""
        self._count = 5
        self._running = True
        self._s3_bucket = ""
        self._region = "us-east-1"
        self._model_id = ""
        self._iterations = 0
        self._news_items = []
    
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
        self._region = input.region
        self._model_id = input.model_id
        
        # Set up timer for periodic regeneration
        try:
            while self._running:
                retry_policy = RetryPolicy(
                    initial_interval=timedelta(seconds=1),
                    maximum_interval=timedelta(seconds=10),
                )
                
                new_item = await workflow.execute_activity(
                    generate,
                    GenerateInput(
                        section=self._section,
                        count=self._count,
                        model_id=self._model_id,
                        region=self._region
                    ),
                    retry_policy=retry_policy,
                    start_to_close_timeout=timedelta(seconds=60)
                )
                
                self._news_items = self._news_items + [new_item]
                
                await workflow.execute_activity(
                    deploy,
                    DeployInput(
                        section=self._section,
                        news_data=self._news_items,
                        bucket_name=self._s3_bucket,
                        region=self._region
                    ),
                    retry_policy=retry_policy,
                    start_to_close_timeout=timedelta(seconds=120)
                )
                
                self._iterations += 1
                if self._iterations >= 10:
                    await workflow.continue_as_new(input)
                
                await workflow.sleep(30)
        except CancelledError:
            # Handle workflow cancellation
            workflow.logger.info(f"News generation workflow for {self._section} was cancelled")
            self._running = False
            raise
