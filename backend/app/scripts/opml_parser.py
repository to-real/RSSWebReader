import xml.etree.ElementTree as ET
from typing import List
from app.schemas import FeedCreate

def parse_opml(file_path: str) -> List[FeedCreate]:
    """Parse OPML file and return list of FeedCreate objects"""
    tree = ET.parse(file_path)
    root = tree.getroot()

    feeds = []
    # OPML uses namespaces, find outline elements
    for outline in root.iter():
        if outline.tag.endswith('outline'):
            xml_url = outline.get('xmlUrl')
            if xml_url:
                feeds.append(FeedCreate(
                    url=xml_url,
                    title=outline.get('title', outline.get('text', '')),
                    description=outline.get('description'),
                ))
    return feeds
