# Random News Generator with Temporal and Bedrock

A Python Flask application that generates random news articles across multiple sections using Temporal for workflow orchestration and Amazon Bedrock for AI-generated content. Each news section has a dedicated workflow that regenerates content every 30 seconds.

## Features

- 5 different news sections: Technology, Sports, Entertainment, Business, and Health
- Exactly 5 latest news articles per section
- Fully AI-generated news content using Amazon Bedrock (Claude 3 Sonnet)
- Temporal workflows for each news section with 30-second refresh timers
- Responsive design that works on desktop and mobile
- Smooth scrolling navigation

## Architecture

The application uses:
- **Flask** as the web framework
- **Temporal** for workflow orchestration and periodic news generation
- **Amazon Bedrock** (Claude 3 Sonnet model) to generate complete news content

Each news section has its own Temporal workflow that:
1. Generates complete news content using Amazon Bedrock
2. Sets a 30-second timer to regenerate content periodically
3. Exposes a query API to retrieve the latest news

## Installation

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (for running Temporal server)
- AWS account with access to Amazon Bedrock

### Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure AWS credentials for Bedrock access:
   ```
   aws configure
   ```
4. Start the Temporal server using Docker Compose:
   ```
   docker-compose up -d
   ```
5. Run the application:
   ```
   python app.py
   ```
6. Open your browser and navigate to `http://localhost:8081`

## How It Works

1. When the application starts, it launches a Temporal worker process
2. The worker starts workflows for each news section
3. Each workflow:
   - Executes an activity that uses Amazon Bedrock to generate complete news articles
   - Bedrock creates both headlines and detailed content for each article
   - Sets a 30-second timer using workflow.sleep()
   - Regenerates news content when the timer expires
4. When a user visits a section page, the Flask app queries the corresponding workflow
5. The workflow returns the latest generated news content
6. Users can manually refresh all content using the "Refresh" button

## Customization

You can customize the news sections by modifying the `NEWS_SECTIONS` list in `app.py` and `temporal_activities.py`.

## License

This project is for demonstration purposes only.