import logging
from datetime import timedelta
from typing import List, Dict, Any

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import CancelledError

# Import activities
with workflow.unsafe.imports_passed_through():
    from temporal_activities import generate_news_for_section, GenerationInput

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define workflow interface
@workflow.defn
class NewsGenerationWorkflow:
    """Workflow that generates news for a specific section periodically"""
    
    def __init__(self):
        self._news_items = []
        self._section = ""
        self._count = 5
        self._running = True
    
    @workflow.run
    async def run(self, input: GenerationInput) -> List[Dict[str, Any]]:
        """
        Run the news generation workflow.
        
        Args:
            section: The news section to generate content for
            count: Number of news items to generate
            
        Returns:
            List of news items
        """
        self._section = input.section
        self._count = input.count
        
        # Generate initial news
        await self._generate_news()
        
        # Set up timer for periodic regeneration
        try:
            while self._running:
                # Wait for 30 seconds before regenerating
                # Using workflow.sleep instead of asyncio.sleep for proper workflow state management
                await workflow.sleep(30)
                # Generate new news
                await self._generate_news()
        except CancelledError:
            # Handle workflow cancellation
            workflow.logger.info(f"News generation workflow for {self._section} was cancelled")
            self._running = False
            raise
            
        return self._news_items
    
    async def _generate_news(self):
        """Generate news using the activity"""
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=10),
            maximum_attempts=3
        )
        
        self._news_items = await workflow.execute_activity(
            generate_news_for_section,
            GenerationInput(self._section, self._count),
            retry_policy=retry_policy,
            start_to_close_timeout=timedelta(seconds=60)
        )
        
        workflow.logger.info(f"Generated {len(self._news_items)} news items for {self._section}")
    
    @workflow.query
    def get_news(self) -> List[Dict[str, Any]]:
        """Query to get the current news items"""
        return self._news_items
    
    @workflow.signal
    def stop(self):
        """Signal to stop the workflow"""
        self._running = False