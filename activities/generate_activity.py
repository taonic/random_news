import logging
import random
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from temporalio import activity
from activities.bedrock_client import BedrockClient

@dataclass
class GenerateInput:
    section: str
    count: int
    model_id: str
    region: str

@activity.defn
async def generate(input: GenerateInput) -> Dict[str, Any]:
    """
    Activity to generate news for a specific section using Amazon Bedrock.
    Bedrock will generate the entire content including headlines and article text.

    Args:
        input: GenerationInput containing section and count

    Returns:
        List of news items with AI-generated content
    """
    section = input.section
    count = input.count
    news_items = []
    topics = ["Security", "Generative AI", "Cloud Computing", "Distributed system", "DevX"]
    topic = random.choice(topics)
    activity.logger.info(f"Generating {count} news articles for section: {section} using Bedrock")

    # Create a prompt for Bedrock to generate multiple news articles at once
    prompt = f"""
    You are a product manager at a tech company. You are responsible for writing release notes for new features.

    Generate a new release note for a new feature in {topic}.

    Make it funny.

    Ensure the release note are returned in a valid json, e.g.:
    {{
        "headline": "Headline of the release",
        "content": "Detailed content of the article 1",
        "topic": "Topic of the article 1",
        "date": "Date and time of generation"
    }}

    Current date and time: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
    """

    bedrock_client = BedrockClient()
    generated_content = await bedrock_client.generate_content(
        prompt,
        max_tokens=4000,
        model_id=input.model_id,
        region_name=input.region
    )

    try:
        # Parse the generated content
        new_item = json.loads(generated_content)
    except json.JSONDecodeError as e:
        activity.logger.error(f"Failed to parse generated content: {str(generated_content)}")
        raise e

    activity.logger.info(f"Generated {len(new_item)}")
    return new_item
