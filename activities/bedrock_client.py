import json
import aioboto3
from botocore.config import Config

class BedrockClient:
    def __init__(self):
        """Initialize the Bedrock client"""
        self.region_name = 'ap-southeast-2'  # Change to your preferred region
        self.model_id = 'arn:aws:bedrock:ap-southeast-2:913031218565:inference-profile/apac.amazon.nova-pro-v1:0'
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
    
    async def generate_content(self, prompt, max_tokens=4000):
        """Generate content using Amazon Bedrock asynchronously"""
        try:
            # Ensure client is initialized
            await self.initialize()

            request_body = {
                "messages": [
                    {
                        "role": "user",
                        "content": [ { "text": prompt} ]
                    }
                ],
                "inferenceConfig": { "maxTokens": max_tokens, "temperature": 1, "topP": 1 }
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
                    body=json.dumps(request_body),
                    accept="application/json"
                )
                
                model_response = json.loads(await response["body"].read())
                response_text = model_response["output"]["message"]['content'][0]['text']
                
                return response_text
        except Exception as e:
            print(f"Error generating content with Bedrock: {str(e)}")
            raise e

# Create a singleton instance for reuse
bedrock_client = BedrockClient()
