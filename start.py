import asyncio
import logging
import signal
import sys
import os
import argparse
from datetime import timedelta

from temporalio.client import Client
from temporalio.worker import Worker

# Import workflows and activities
from temporal_workflows import GenNewsWorkflow, WorkflowInput
from activities import deploy, generate
from constants import TASK_QUEUE, NEWS_SECTIONS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_workflows(client, s3_bucket, s3_region, count):
    """Start news generation workflows for all sections"""
    for section in NEWS_SECTIONS:
        workflow_id = f"news_generation_{section.lower()}"
        
        try:
            await client.start_workflow(
                GenNewsWorkflow.run,
                WorkflowInput(section=section, count=count, s3_bucket=s3_bucket, s3_region=s3_region),
                id=workflow_id,
                task_queue=TASK_QUEUE,
            )
            logger.info(f"Started news generation workflow for {section}")
        except Exception as e:
            logger.error(f"Error starting workflow for {section}: {e}")

async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Start Temporal worker and workflows')
    parser.add_argument('--bucket', default='agentic-hackathon-wlg', help='S3 bucket name for deployment')
    parser.add_argument('--region', default='ap-southeast-2', help='AWS region (default: us-east-1)')
    parser.add_argument('--count', type=int, default=5, help='Number of news items per section (default: 5)')
    
    args = parser.parse_args()
    
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")
    
    logger.info("Starting workflows")
    await start_workflows(client, args.bucket, args.region, args.count)
    
    # Run the worker
    interrupt_event = asyncio.Event()
    
    logger.info("Starting worker")
    async with Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[GenNewsWorkflow],
        activities=[generate, deploy]
    ):
        print("Worker started. Press Ctrl+C to exit.")
        await interrupt_event.wait()
        print("Worker stopped.")

if __name__ == "__main__":
    asyncio.run(main())