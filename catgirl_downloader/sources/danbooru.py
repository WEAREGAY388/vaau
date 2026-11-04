import requests
from typing import List, Dict, Any
from .base import BaseSource

class DanbooruSource(BaseSource):
    def __init__(self):
        super().__init__(name="danbooru", base_url="https://danbooru.donmai.us/posts.json")

    def fetch_images(self, tags: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        params = {"limit": limit, "tags": tags}
        headers = {"User-Agent": "CatgirlDownloader/1.1.0"}
        try:
            res = requests.get(self.base_url, params=params, headers=headers, timeout=10)
            res.raise_for_status()
            posts = res.json()
            results = []
            for post in posts:
                file_url = post.get("file_url") or post.get("large_file_url")
                if file_url:
                    results.append({
                        "id": str(post.get("id")),
                        "source": self.name,
                        "image_url": file_url,
                        "preview_url": post.get("preview_file_url"),
                        "tags": post.get("tag_string", "").split(),
                        "width": post.get("image_width"),
                        "height": post.get("image_height"),
                        "rating": post.get("rating")
                    })
            return results
        except Exception as e:
            print(f"[danbooru] Error: {e}")
            return []
