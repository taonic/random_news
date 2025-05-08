import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import timedelta

from temporalio.client import Client, RPCError
from temporal_workflows import NewsGenerationWorkflow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TemporalNewsClient:
    """Client for interacting with Temporal news generation workflows"""
    
    def __init__(self):
        self.client = None
        self.initialized = False
    
    async def initialize(self):
        """Initialize the Temporal client"""
        if self.initialized:
            return
        
        try:
            self.client = await Client.connect("localhost:7233")
            self.initialized = True
            logger.info("Temporal client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Temporal client: {e}")
            raise

    async def get_news_for_section(self, section: str) -> List[Dict[str, Any]]:
        """
        Get news for a specific section by querying the workflow
        
        Args:
            section: The news section to get content for
            
        Returns:
            List of news items
        """
        if not self.initialized:
            await self.initialize()
        
        workflow_id = f"news_generation_{section.lower()}"
        
        try:
            # Get handle to the workflow
            handle = self.client.get_workflow_handle(workflow_id)
            
            # Query the workflow for news
            news_items = await handle.query(NewsGenerationWorkflow.get_news)
            logger.info(f"Retrieved {len(news_items)} news items for {section}")
            
            return news_items
        except Exception as e:
            logger.error(f"Error getting news for {section}: {e}")
            return []
    
# Create a singleton instance
temporal_news_client = TemporalNewsClient()

# Synchronous wrapper functions for Flask
def get_news_for_section_sync(section: str) -> List[Dict[str, Any]]:
    """Synchronous wrapper for get_news_for_section"""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(temporal_news_client.get_news_for_section(section))
    finally:
        loop.close()