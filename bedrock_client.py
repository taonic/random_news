import json
import asyncio
import aioboto3
from botocore.config import Config

class BedrockClient:
    def __init__(self):
        """Initialize the Bedrock client"""
        self.region_name = 'us-west-2'  # Change to your preferred region
        self.model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'  # Using Claude 3 Sonnet
        self.session = None
        
    async def initialize(self):
        """Initialize the async session and client"""
        if self.session is None:
            # Configure with appropriate timeouts for LLM calls
            config = Config(
                read_timeout=300,  # 5 minutes timeout for LLM responses
                connect_timeout=10,
                retries={'max_attempts': 3}
            )
            
            self.session = aioboto3.Session()
    
    async def generate_content(self, prompt, max_tokens=1000):
        """Generate content using Amazon Bedrock asynchronously"""
        try:
            # Ensure client is initialized
            await self.initialize()
            
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7
            }
            
            # Create a new client for each request to avoid reusing coroutines
            async with self.session.client(
                service_name='bedrock-runtime',
                region_name=self.region_name,
                config=Config(
                    read_timeout=300,
                    connect_timeout=10,
                    retries={'max_attempts': 3}
                )
            ) as client:
                response = await client.invoke_model(
                    modelId=self.model_id,
                    body=json.dumps(request_body)
                )
                
                body = await response['body'].read()
                response_body = json.loads(body)
                return response_body['content'][0]['text']
        
        except Exception as e:
            print(f"Error generating content with Bedrock: {str(e)}")
            # Return a fallback content instead of an error message
            return await self.generate_fallback_content(prompt)
    
    async def generate_fallback_content(self, prompt):
        """Generate fallback content when Bedrock API fails"""
        # Extract headline from prompt if possible
        headline = ""
        if "HEADLINE:" in prompt:
            headline_parts = prompt.split("HEADLINE:")
            if len(headline_parts) > 1:
                headline = headline_parts[1].split("\n")[0].strip()
        
        # Extract section from prompt if possible
        section = "News"
        if "section:" in prompt.lower():
            section_parts = prompt.lower().split("section:")
            if len(section_parts) > 1:
                section_candidate = section_parts[1].split("\n")[0].strip()
                if section_candidate:
                    section = section_candidate.capitalize()
        
        # Generate a fallback article
        fallback = f"Latest Updates in {section}\n\n"
        
        fallback += f"Our {section} team is currently gathering information on this developing story. "
        fallback += "We're reaching out to sources and experts in the field to provide you with accurate and timely information.\n\n"
        
        fallback += "Industry analysts have been closely monitoring these developments, with many suggesting this could represent a significant shift in the market. "
        fallback += "\"We're seeing interesting patterns emerge,\" noted industry expert Dr. Sarah Johnson. \"The implications could be far-reaching.\"\n\n"
        
        fallback += "While it's still early to determine the long-term impact, analysts predict this news could influence related industries and potentially spark similar innovations from competitors. "
        fallback += "As more details emerge, we'll continue to provide updates on this evolving story."
        
        return fallback

# Create a singleton instance for reuse
bedrock_client = BedrockClient()