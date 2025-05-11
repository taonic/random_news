import logging
import random
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from temporalio import activity
from activities.bedrock_client import bedrock_client

# News sections
NEWS_SECTIONS = [
    "Technology",
    "Sports",
    "Entertainment",
    "Business",
    "Health"
]

# Generate author names
def random_author():
    first_names = ["John", "Sarah", "Michael", "Emma", "David", "Olivia", "James", "Sophia", "Robert", "Emily"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

@dataclass
class GenerateInput:
    section: str
    count: int

@activity.defn
async def generate(input: GenerateInput) -> List[Dict[str, Any]]:
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
    
    activity.logger.info(f"Generating {count} news articles for section: {section} using Bedrock")
    
    # Create a prompt for Bedrock to generate multiple news articles at once
    prompt = f"""
    Generate {count} unique and interesting news articles for the {section} section of a news website.
    
    For each article, provide:
    1. A catchy, funny headline
    2. A detailed news article with at least 300 words
    
    Make the articles diverse in topics but all related to {section}.
    Include quotes from relevant experts or stakeholders in each article.
    Make the content informative, engaging, and following professional news reporting style.
    
    Ensure the articles are returned in a valid json list format, e.g.:
    [
        {{
            "headline": "Headline of the article 1",
            "content": "Detailed content of the article 1",
            "author": "Author Name 1",
            "date": "Date and time of generation"
        }},
        {{
            "headline": "Headline of the article 2",
            "content": "Detailed content of the article 2",
            "author": "Author Name 2",
            "date": "Date and time of generation"
        }}
    ]
    
    Current date and time: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
    """
    
    generated_content = await bedrock_client.generate_content(prompt, max_tokens=4000)
    
    try:
        # Parse the generated content
        news_items = json.loads(generated_content)
    except json.JSONDecodeError as e:
        activity.logger.error(f"Failed to parse generated content: {str(generated_content)}")
        raise e
    
    activity.logger.info(f"Generated {len(news_items)} news items for {section}")
    return news_items