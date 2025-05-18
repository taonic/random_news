#!/usr/bin/env python3
import asyncio
import logging
import argparse

from temporalio.client import Client
from temporalio.worker import Worker

# Import workflows and activities
from temporal_workflows import GenNewsWorkflow, WorkflowInput
from activities import generate, deploy
from constants import DEFAULT_MODEL_ID, NEWS_SECTIONS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_workflows(client, s3_bucket="", region="us-east-1", model_id="", count=5):
    """Start news generation workflow for each news section"""
    for section in NEWS_SECTIONS:
        workflow_id = f"news_generation_{section.lower()}"

        try:
            # Check if workflow already exists
            try:
                handle = client.get_workflow_handle(workflow_id)
                # Try to query the workflow to see if it exists
                # If this fails, the workflow doesn't exist
                details = await handle.describe()
                logger.info(f"Workflow for {section} already exists: {details.status}")
                if details.status != "RUNNING":
                    raise Exception("Workflow is not running")
            except Exception as e:
                logger.info(f"Starting new workflow due to: {e}")
                # Workflow doesn't exist, create it
                workflow_input = WorkflowInput(
                    section=section,
                    count=count,
                    s3_bucket=s3_bucket,
                    region=region,
                    model_id=model_id
                )

                await client.start_workflow(
                    GenNewsWorkflow.run,
                    workflow_input,
                    id=workflow_id,
                    task_queue="news-generation"
                )
                logger.info(f"Started news generation workflow for {section}")
        except Exception as e:
            logger.error(f"Error starting workflow for {section}: {e}")

async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Start Temporal worker and workflows')
    parser.add_argument('--bucket', default='agentic-hackathon-wlg', help='S3 bucket name for deployment')
    parser.add_argument('--region', default='ap-southeast-2', help='AWS region (default: ap-southeast-2)')
    parser.add_argument('--model-id', default=DEFAULT_MODEL_ID, help='Bedrock model ID (e.g., anthropic.claude-v2)')
    parser.add_argument('--count', type=int, default=1, help='Number of news items per section (default: 5)')
    args = parser.parse_args()

    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    logger.info("Starting workflows")
    await start_workflows(
        client,
        args.bucket,
        args.region,
        args.model_id,
        args.count
    )

    # Run the worker
    logger.info("Starting worker")
    interrupt_event = asyncio.Event()
    async with Worker(
        client,
        task_queue="news-generation",
        workflows=[GenNewsWorkflow],
        activities=[generate, deploy]
    ):
        print("Worker started. Press Ctrl+C to exit.")
        await interrupt_event.wait()
        print("Worker stopped.")

if __name__ == "__main__":
    asyncio.run(main())
