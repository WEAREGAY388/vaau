#!/usr/bin/env python3
import sys
import argparse
from catgirl_downloader.sources.manager import SourceManager

def main():
    parser = argparse.ArgumentParser(description="CatgirlDownloader - Anime & Waifu Image Fetcher")
    parser.add_argument("--source", type=str, default="yande.re", help="Image source (e.g., yande.re, nekos.moe, waifu.im, danbooru)")
    parser.add_argument("--tags", type=str, default="", help="Tags to filter images")
    parser.add_argument("--limit", type=int, default=5, help="Number of images to fetch")
    
    args = parser.parse_args()
    
    manager = SourceManager()
    print("=" * 50)
    print(" CatgirlDownloader v1.1.0")
    print(f" Registered sources: {', '.join(manager.list_sources())}")
    print("=" * 50)
    
    source = manager.get_source(args.source)
    if not source:
        print(f"Error: Source '{args.source}' not found. Available: {manager.list_sources()}")
        sys.exit(1)
        
    print(f"Fetching {args.limit} images from {source.name} (tags: '{args.tags}')...")
    images = source.fetch_images(tags=args.tags, limit=args.limit)
    
    if not images:
        print("No images found or request failed.")
        return

    print(f"\nSuccessfully fetched {len(images)} posts:")
    for idx, img in enumerate(images, 1):
        print(f"{idx}. ID: {img['id']} | Dimensions: {img['width']}x{img['height']}")
        print(f"   URL: {img['image_url']}")

if __name__ == "__main__":
    main()
