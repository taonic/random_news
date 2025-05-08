from flask import Flask, render_template, redirect, url_for
from news_generator import generate_news_for_section
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

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

# Dictionary to store generated news (to avoid regenerating on every page load)
news_cache = {}

@app.route('/')
def index():
    """Homepage with links to each section"""
    return render_template('index.html', sections=NEWS_SECTIONS)

@app.route('/section/<section_name>')
def section(section_name):
    """Display news for a specific section"""
    if section_name not in NEWS_SECTIONS:
        return redirect(url_for('index'))
    
    # Generate news for this section if not in cache
    if section_name not in news_cache:
        news_cache[section_name] = generate_news_for_section(section_name, count=5)
    
    return render_template('section.html', 
                          section=section_name, 
                          news_content=news_cache[section_name],
                          sections=NEWS_SECTIONS)

@app.route('/refresh')
def refresh():
    """Clear the news cache to generate fresh content"""
    global news_cache
    news_cache = {}
    return redirect(my_url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)