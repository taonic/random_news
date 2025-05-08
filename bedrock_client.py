import boto3
import json

class BedrockClient:
    def __init__(self):
        """Initialize the Bedrock client"""
        self.bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-east-1'  # Change to your preferred region
        )
        self.model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'  # Using Claude 3 Sonnet

    def generate_content(self, prompt, max_tokens=1000):
        """Generate content using Amazon Bedrock"""
        try:
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
            
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response.get('body').read())
            return response_body['content'][0]['text']
        
        except Exception as e:
            print(f"Error generating content with Bedrock: {str(e)}")
            # Return a fallback content instead of an error message
            return self.generate_fallback_content(prompt)
    
    def generate_fallback_content(self, prompt):
        """Generate fallback content when Bedrock API fails"""
        # Extract headline from prompt if possible
        headline = ""
        if "Headline:" in prompt:
            headline_parts = prompt.split("Headline:")
            if len(headline_parts) > 1:
                headline = headline_parts[1].split("\n")[0].strip()
        
        # Extract basic info from prompt if possible
        basic_info = ""
        if "Basic information:" in prompt:
            info_parts = prompt.split("Basic information:")
            if len(info_parts) > 1:
                basic_info = info_parts[1].split("\n")[0].strip()
        
        # Generate a longer version of the basic info
        fallback = basic_info
        
        # Add some additional paragraphs
        fallback += "\n\nIndustry experts have been closely monitoring these developments, with many suggesting this could represent a significant shift in the market. Stakeholders from various sectors have expressed both excitement and caution about the potential implications."
        
        fallback += "\n\nWhile it's still early to determine the long-term impact, analysts predict this news could influence related industries and potentially spark similar innovations from competitors. As more details emerge, we'll continue to provide updates on this evolving story."
        
        return fallback