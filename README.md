# Random News Generator

A Python Flask application that generates random news articles across multiple sections. Each time you refresh the page, new random news content is generated using Amazon Bedrock for detailed article content.

## Features

- 5 different news sections: Technology, Sports, Entertainment, Business, and Health
- Exactly 5 latest news articles per section
- AI-generated detailed news content using Amazon Bedrock
- Responsive design that works on desktop and mobile
- Smooth scrolling navigation

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure AWS credentials for Bedrock access:
   ```
   aws configure
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Open your browser and navigate to `http://localhost:8081`

## How It Works

The application uses Flask as the web framework and generates random news headlines based on predefined templates. It then uses Amazon Bedrock (Claude 3 Sonnet model) to generate detailed, realistic news content for each headline. The news content is regenerated each time the page is refreshed.

## AWS Requirements

- AWS account with access to Amazon Bedrock
- Proper IAM permissions for Bedrock API access
- AWS credentials configured locally

## Customization

You can customize the news sections and content by modifying the `NEWS_SECTIONS` list in `app.py` and updating the corresponding generation logic in `news_generator.py`.

## License

This project is for demonstration purposes only.