import os
import subprocess
import threading
import time
from flask import Flask, render_template, redirect, url_for, jsonify
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

# Import Temporal client for news retrieval
from temporal_client import get_news_for_section_sync

URL_PREFIX = "/proxy/8081"

app = Flask(__name__)

# There should be a better way to do this.
def my_url_for(endpoint, **values):
    url = url_for(endpoint, **values)
    return URL_PREFIX + url

app.add_template_global(my_url_for, 'my_url_for')   

# Define our news sections
NEWS_SECTIONS = [
    "Technology",
    "Sports",
    "Entertainment",
    "Business",
    "Health"
]

@app.route('/')
def index():
    """Homepage with links to each section"""
    return render_template('index.html', sections=NEWS_SECTIONS)

@app.route('/section/<section_name>')
def section(section_name):
    """Display news for a specific section"""
    if section_name not in NEWS_SECTIONS:
        return redirect(url_for('index'))
    
    # Get news from Temporal workflow
    news_content = get_news_for_section_sync(section_name)
    
    # If no news is available yet, show a message
    if not news_content:
        news_content = [{
            "headline": "News is being generated...",
            "content": "Please wait while we generate news for this section. Refresh the page in a few seconds.",
            "author": "System",
            "date": "Just now"
        }]
    
    return render_template('section.html', 
                          section=section_name, 
                          news_content=news_content,
                          sections=NEWS_SECTIONS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)