import asyncio
import logging
import signal
import sys
import os
from datetime import timedelta

from temporalio.client import Client
from temporalio.worker import Worker

# Import workflow and activities
from temporal_workflows import NewsGenerationWorkflow
from temporal_activities import generate_news_for_section, GenerationInput

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Define news sections
NEWS_SECTIONS = [
    "Technology",
    "Sports",
    "Entertainment",
    "Business",
    "Health"
]

# Global variables for cleanup
client = None
worker = None
workflow_handles = {}

async def start_worker():
    """Start the Temporal worker"""
    global client, worker
    
    # Connect to Temporal server
    temporal_host = os.environ.get("TEMPORAL_HOST", "localhost")
    temporal_port = os.environ.get("TEMPORAL_PORT", "7233")
    temporal_address = f"{temporal_host}:{temporal_port}"
    
    logger.info(f"Connecting to Temporal server at {temporal_address}...")
    client = await Client.connect(temporal_address)
    
    # Create worker
    logger.info("Starting Temporal worker...")
    worker = Worker(
        client,
        task_queue="news_generation_queue",
        workflows=[NewsGenerationWorkflow],
        activities=[generate_news_for_section],
    )
    
    # Start worker
    await worker.run()

async def start_workflows():
    """Start workflows for each news section"""
    global client, workflow_handles
    
    if not client:
        logger.error("Temporal client not initialized")
        return
    
    logger.info("Starting news generation workflows...")
    
    for section in NEWS_SECTIONS:
        workflow_id = f"news_generation_{section.lower()}"
        try:
            # Start new workflow
            handle = await client.start_workflow(
                NewsGenerationWorkflow.run,
                GenerationInput(section, 5),
                id=workflow_id,
                task_queue="news_generation_queue",
            )
            workflow_handles[section] = handle
        except Exception:
            pass
        
        logger.info(f"Started workflow for {section} with ID: {workflow_id}")

async def main():
    """Main entry point"""

    # Start worker in the background
    worker_task = asyncio.create_task(start_worker())
    
    # Give the worker a moment to start
    await asyncio.sleep(2)
    
    # Start workflows
    await start_workflows()
    
    # Wait for worker to complete (should run indefinitely)
    await worker_task

if __name__ == "__main__":
    asyncio.run(main())