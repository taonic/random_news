# Random News Generator

A project that generates random news articles using Amazon Bedrock and publishes them to an S3 static website.

## Overview

This project uses:
- Amazon Bedrock for AI-generated news content
- Temporal for workflow orchestration
- AWS S3 for static website hosting (using aioboto3)

## AWS Setup

1. Create an AWS account if you don't have one

2. Set up AWS credentials:
   - Go to AWS IAM console and create a new user with programmatic access
   - Attach policies for Bedrock and S3 access:
     - `AmazonBedrockFullAccess`
     - `AmazonS3FullAccess`
   - Save the Access Key ID and Secret Access Key

3. Configure AWS credentials locally using one of these methods:
   
   **Option 1: AWS CLI**
   ```
   aws configure
   ```
   Enter your Access Key ID, Secret Access Key, default region, and output format.

   **Option 2: Environment variables**
   ```
   export AWS_ACCESS_KEY_ID=your_access_key_id
   export AWS_SECRET_ACCESS_KEY=your_secret_access_key
   export AWS_DEFAULT_REGION=your_region
   ```

   **Option 3: Credentials file**
   Create or edit `~/.aws/credentials`:
   ```
   [default]
   aws_access_key_id = your_access_key_id
   aws_secret_access_key = your_secret_access_key
   ```

4. Set up Amazon Bedrock:
   - Go to the Amazon Bedrock console
   - Request access to the model you want to use (e.g., Claude, Titan)
   - Create an inference profile for the model
   - Note the inference profile ARN or ID

## Project Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Start a Temporal server locally
   ```
   temporal server start-dev
   ```

3. Start the Temporal worker and workflows:
   ```
   python start.py --bucket your-bucket-name --inference-profile your-inference-profile-id
   ```

## Worker Options

- `--bucket`: S3 bucket name for deployment (default: news-generator-bucket)
- `--region`: AWS region (default: ap-southeast-2)
- `--count`: Number of news items per section (default: 5)
- `--model-id`: Bedrock model ID (default: anthropic.claude-v2)
- `--inference-profile`: Bedrock inference profile ID or ARN (required)

Examples:

Start worker with specific model and inference profile:
```
python start.py --bucket your-bucket-name --model-id anthropic.claude-v2 --inference-profile your-inference-profile-id
```

## Environment Variables

- `AWS_ACCESS_KEY_ID`: Your AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key
- `AWS_DEFAULT_REGION`: Your AWS default region
- `BEDROCK_MODEL_ID`: Bedrock model ID to use
- `BEDROCK_INFERENCE_PROFILE_ID`: Bedrock inference profile ID or ARN

## Project Structure

- `temporal_workflows.py`: Temporal workflow for news generation and S3 deployment
- `activities.py`: Temporal activities for news generation and S3 deployment
- `start.py`: Script to start worker and workflows
- `static_generator.py`: Utility for generating static HTML files
- `s3_client.py`: Utility for interacting with AWS S3 using aioboto3
- `bedrock_client.py`: Client for Amazon Bedrock
- `templates/`: HTML templates (created automatically if not present)
- `output/`: Generated static files (created during deployment)

## Workflow Architecture

The project uses a single Temporal workflow:

**GenNewsWorkflow**: Handles both news generation and S3 deployment
- Generates news content for a specific section
- Deploys the content to S3
- Periodically regenerates content and redeploys to S3

## Troubleshooting

### Bedrock API Errors

If you encounter the error "Retry your request with the ID or ARN of an inference profile that contains this model", make sure:
1. You have created an inference profile in the Amazon Bedrock console
2. You are providing the inference profile ID using the `--inference-profile` parameter or `BEDROCK_INFERENCE_PROFILE_ID` environment variable
3. You have proper permissions to access the model

### S3 Access Issues

If you encounter S3 access issues:
1. Verify your AWS credentials are correctly configured
2. Check that your IAM user has the necessary S3 permissions
3. Ensure the bucket name is globally unique
4. Verify the region is correct

## License

This project is for demonstration purposes only.
