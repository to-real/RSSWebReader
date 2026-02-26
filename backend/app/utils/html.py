import re
from bs4 import BeautifulSoup

def clean_html(html: str) -> str:
    """Extract clean text content from HTML"""
    soup = BeautifulSoup(html, 'html.parser')
    # Remove script and style elements
    for script in soup(['script', 'style']):
        script.decompose()
    text = soup.get_text()
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text
