import os
import logging
import json
import asyncio
from typing import List, Dict, Any
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StaticSiteGenerator:
    """Generator for static HTML files from news content"""
    
    def __init__(self, template_dir: str = 'templates', output_dir: str = 'tmp'):
        """
        Initialize the static site generator
        
        Args:
            template_dir: Directory containing templates
            output_dir: Directory to output generated files
        """
        self.template_dir = template_dir
        self.output_dir = output_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # News sections
        self.news_sections = [
            "Technology",
            "Sports",
            "Entertainment",
            "Business",
            "Health"
        ]
        
    def generate_index_page(self) -> str:
        """
        Generate the index page
        
        Returns:
            str: Path to the generated file
        """
        template = self.env.get_template('index.html')
        
        # Render the template
        output = template.render(
            sections=self.news_sections
        )
        
        # Write to file
        output_path = os.path.join(self.output_dir, 'index.html')
        with open(output_path, 'w') as f:
            f.write(output)
            
        logger.info(f"Generated index page at {output_path}")
        return output_path
        
    def generate_section_page(self, section: str, news_content: List[Dict[str, Any]]) -> str:
        """
        Generate a section page
        
        Args:
            section: Section name
            news_content: List of news items
            
        Returns:
            str: Path to the generated file
        """
        template = self.env.get_template('section.html')
        
        # Render the template
        output = template.render(
            section=section,
            sections=self.news_sections,
            news_content=news_content
        )
        
        # Create section directory if it doesn't exist
        section_dir = os.path.join(self.output_dir, section.lower())
        os.makedirs(section_dir, exist_ok=True)
        
        # Write to file
        output_path = os.path.join(section_dir, 'index.html')
        with open(output_path, 'w') as f:
            f.write(output)

        return output_path
        
    def copy_static_assets(self) -> List[str]:
        """
        Copy static assets to the output directory
        
        Returns:
            List[str]: Paths to copied files
        """
        copied_files = []
        
        # Create static directories
        static_dir = os.path.join(self.output_dir, 'static')
        css_dir = os.path.join(static_dir, 'css')
        js_dir = os.path.join(static_dir, 'js')
        
        os.makedirs(css_dir, exist_ok=True)
        os.makedirs(js_dir, exist_ok=True)
        
        # Copy CSS files
        css_files = os.listdir('static/css')
        for css_file in css_files:
            src_path = os.path.join('static/css', css_file)
            dest_path = os.path.join(css_dir, css_file)
            
            with open(src_path, 'r') as src, open(dest_path, 'w') as dest:
                dest.write(src.read())
                
            copied_files.append(dest_path)
            logger.info(f"Copied {src_path} to {dest_path}")
            
        # Copy JS files
        js_files = os.listdir('static/js')
        for js_file in js_files:
            src_path = os.path.join('static/js', js_file)
            dest_path = os.path.join(js_dir, js_file)
            
            with open(src_path, 'r') as src, open(dest_path, 'w') as dest:
                dest.write(src.read())
                
            copied_files.append(dest_path)
            logger.info(f"Copied {src_path} to {dest_path}")
            
        return copied_files
        
    def generate_site(self, section: str, section_news: List[Dict[str, Any]]) -> str:
        """
        Generate the entire static site
        
        Args:
            news_data: Dictionary mapping section names to news content
        """

        self.generate_index_page()
        
        self.generate_section_page(section, section_news)
            
        self.copy_static_assets()
        
        logger.info(f"Generated static site in {self.output_dir}")
        
        return self.output_dir
