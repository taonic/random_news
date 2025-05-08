import logging
import random
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass

from temporalio import activity
from bedrock_client import bedrock_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
class GenerationInput:
    section: str
    count: int

@activity.defn
async def generate_news_for_section(input: GenerationInput) -> List[Dict[str, Any]]:
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
    
    logger.info(f"Generating {count} news articles for section: {section} using Bedrock")
    
    news_items = []
    
    # Get current date and time
    current_datetime = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    # Create a prompt for Bedrock to generate multiple news articles at once
    prompt = f"""
    Generate {count} unique and realistic news articles for the {section} section of a news website.
    
    For each article, provide:
    1. A catchy, realistic headline
    2. A detailed news article with 3-4 paragraphs
    
    Make the articles diverse in topics but all related to {section}.
    Include quotes from relevant experts or stakeholders in each article.
    Make the content informative, engaging, and following professional news reporting style.
    
    Format each article as:
    
    HEADLINE: [The headline]
    
    [Article content with 3-4 paragraphs]
    
    ---
    
    (Repeat this format for all {count} articles)
    """
    
    try:
        # Use Bedrock to generate all articles at once
        generated_content = await bedrock_client.generate_content(prompt, max_tokens=4000)
        
        # Split the content into individual articles
        articles = generated_content.split("---")
        
        # Process each article
        for article in articles:
            if not article.strip():
                continue
                
            try:
                # Extract headline and content
                if "HEADLINE:" in article:
                    parts = article.split("HEADLINE:", 1)
                    if len(parts) > 1:
                        article_parts = parts[1].strip().split("\n", 1)
                        if len(article_parts) > 1:
                            headline = article_parts[0].strip()
                            content = article_parts[1].strip()
                            
                            # Create news item with current datetime
                            news_items.append({
                                "headline": headline,
                                "content": content,
                                "author": random_author(),
                                "date": current_datetime
                            })
                            
                            logger.info(f"Generated news item: {headline}")
                else:
                    # Try to extract headline from first line
                    lines = article.strip().split("\n")
                    if lines:
                        headline = lines[0].strip()
                        content = "\n".join(lines[1:]).strip()
                        
                        # Create news item with current datetime
                        news_items.append({
                            "headline": headline,
                            "content": content,
                            "author": random_author(),
                            "date": current_datetime
                        })
                        
                        logger.info(f"Generated news item: {headline}")
            except Exception as e:
                logger.error(f"Error processing article: {e}")
                continue
                
        # If we didn't get enough articles, generate more individually
        while len(news_items) < count:
            try:
                # Generate a single article
                single_prompt = f"""
                Generate a single realistic news article for the {section} section of a news website.
                
                Provide:
                1. A catchy, realistic headline
                2. A detailed news article with 3-4 paragraphs
                
                Include quotes from relevant experts or stakeholders.
                Make the content informative, engaging, and following professional news reporting style.
                
                Format as:
                
                HEADLINE: [The headline]
                
                [Article content with 3-4 paragraphs]
                """
                
                article = await bedrock_client.generate_content(single_prompt, max_tokens=1000)
                
                # Extract headline and content
                if "HEADLINE:" in article:
                    parts = article.split("HEADLINE:", 1)
                    if len(parts) > 1:
                        article_parts = parts[1].strip().split("\n", 1)
                        if len(article_parts) > 1:
                            headline = article_parts[0].strip()
                            content = article_parts[1].strip()
                            
                            # Create news item with current datetime
                            news_items.append({
                                "headline": headline,
                                "content": content,
                                "author": random_author(),
                                "date": current_datetime
                            })
                            
                            logger.info(f"Generated additional news item: {headline}")
                
            except Exception as e:
                logger.error(f"Error generating additional article: {e}")
                # Add a placeholder article if we can't generate enough
                news_items.append({
                    "headline": f"Latest {section} News",
                    "content": f"Our {section} reporters are working on bringing you the latest updates. Check back soon for more information.",
                    "author": random_author(),
                    "date": current_datetime
                })
    
    except Exception as e:
        logger.error(f"Error generating content with Bedrock: {e}")
        # Generate fallback content
        for i in range(count):
            news_items.append({
                "headline": f"Latest {section} News #{i+1}",
                "content": f"Our {section} reporters are working on bringing you the latest updates. Check back soon for more information.",
                "author": random_author(),
                "date": current_datetime
            })
    
    # Ensure we have exactly the requested number of items
    news_items = news_items[:count]
    
    logger.info(f"Generated {len(news_items)} news items for {section}")
    return news_items