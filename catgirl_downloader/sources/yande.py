import requests
from typing import List, Dict, Any
from .base import BaseSource

class YandeSource(BaseSource):
    """API source handler for yande.re"""
    
    def __init__(self):
        super().__init__(name="yande.re", base_url="https://yande.re/post.json")
        
    def fetch_images(self, tags: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        params = {"limit": limit, "tags": tags}
        headers = {"User-Agent": "CatgirlDownloader/1.1.0 (Python/GTK4)"}
        
        try:
            response = requests.get(self.base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            posts = response.json()
            
            formatted_images = []
            for post in posts:
                image_url = post.get("file_url")
                if image_url:
                    formatted_images.append({
                        "id": str(post.get("id")),
                        "source": self.name,
                        "image_url": image_url,
                        "preview_url": post.get("preview_url"),
                        "tags": post.get("tags", "").split(),
                        "width": post.get("width"),
                        "height": post.get("height"),
                        "rating": post.get("rating")
                    })
            return formatted_images
        except requests.RequestException as e:
            print(f"[yande.re] Error fetching posts: {e}")
            return []
