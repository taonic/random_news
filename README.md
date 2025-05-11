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
   - Request access to the model: amazon.nova-pro-v1
   - Find the inference profile ARN by using: `aws bedrock list-inference-profiles --region ap-southeast-2`

5. Update the `bedrock_client.py` file with your inference profile ID:
   ```python
   # In bedrock_client.py
   INFERENCE_PROFILE_ID = "your_inference_profile_id"
   ```

## Project Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Start the Temporal worker and workflows:
   ```
   python start.py --bucket your-bucket-name --region us-east-1
   ```

## Worker Options

- `--bucket`: S3 bucket name for deployment (optional)
- `--region`: AWS region (default: ap-southeast-2)
- `--count`: Number of news items per section (default: 5)

Examples:

Start worker with workflows and S3 deployment:
```
python start.py --bucket your-bucket-name --region us-west-2 --count 5
```

### Deployment Options

- `--bucket`: S3 bucket name (required)
- `--region`: AWS region (default: us-east-1)
- `--count`: Number of news items per section (default: 5)
- `--skip-generation`: Skip news generation and only deploy existing content
- `--wait`: Wait for deployment to complete and show the final URL

Example with all options:
```
python deploy.py --bucket your-bucket-name --region us-west-2 --count 10 --wait
```

To only deploy existing content without regenerating news:
```
python deploy.py --bucket your-bucket-name --skip-generation
```

## Environment Variables

- `S3_BUCKET`: S3 bucket name for deployment (optional)
- `S3_REGION`: AWS region for S3 bucket (default: us-east-1)
- `AWS_ACCESS_KEY_ID`: Your AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key
- `AWS_DEFAULT_REGION`: Your AWS default region

## Project Structure

- `temporal_activities.py`: Temporal activities for news generation and S3 deployment
- `temporal_workflows.py`: Temporal workflow for news generation and S3 deployment
- `temporal_client.py`: Client for interacting with Temporal workflows
- `start.py`: Script to start worker and workflows
- `static_generator.py`: Utility for generating static HTML files
- `s3_client.py`: Utility for interacting with AWS S3 using aioboto3
- `deploy.py`: Command-line tool for deployment
- `bedrock_client.py`: Client for Amazon Bedrock
- `templates/`: HTML templates
- `static/`: Static assets (CSS, JS)
- `output/`: Generated static files (created during deployment)

## Workflow Architecture

The project uses a single Temporal workflow:

**NewsGenerationWorkflow**: Handles both news generation and S3 deployment
- Generates news content for a specific section
- Can be configured to deploy to S3 at creation time
- Can receive signals to trigger S3 deployment at any time
- Periodically regenerates content and redeploys to S3 if configured

This integrated approach simplifies the architecture while maintaining flexibility.

## Performance Benefits of aioboto3

This project uses aioboto3 for asynchronous AWS operations, which provides several benefits:

1. **Concurrent uploads**: Multiple files can be uploaded to S3 simultaneously
2. **Non-blocking I/O**: AWS operations don't block the event loop
3. **Better integration**: Works seamlessly with other async code in the project
4. **Reduced overhead**: Fewer resources needed for handling multiple connections
5. **Faster deployments**: Parallel processing of S3 operations

## Troubleshooting

### Bedrock API Errors

If you encounter the error "Retry your request with the ID or ARN of an inference profile that contains this model", make sure:
1. You have created an inference profile in the Amazon Bedrock console
2. You have updated the `bedrock_client.py` file with your inference profile ID
3. You have proper permissions to access the model

### S3 Access Issues

If you encounter S3 access issues:
1. Verify your AWS credentials are correctly configured
2. Check that your IAM user has the necessary S3 permissions
3. Ensure the bucket name is globally unique
4. Verify the region is correct

## License

This project is for demonstration purposes only.