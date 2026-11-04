#!/usr/bin/env python3
import sys
from sources.yande import YandeSource
from sources.manager import SourceManager

def main():
    print("Initializing CatgirlDownloader with yande.re support...")
    manager = SourceManager()
    manager.register_source(YandeSource())
    
    print("Available sources:", manager.list_sources())
    
    # Test fetch from yande.re
    yande = manager.get_source("yande.re")
    if yande:
        posts = yande.fetch_images(tags="rating:s", limit=3)
        print(f"Fetched {len(posts)} posts from yande.re:")
        for post in posts:
            print(f" - [{post['id']}] {post['image_url']}")

if __name__ == "__main__":
    main()
