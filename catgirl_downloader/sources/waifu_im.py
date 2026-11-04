import requests
from typing import List, Dict, Any
from .base import BaseSource

class WaifuImSource(BaseSource):
    def __init__(self):
        super().__init__(name="waifu.im", base_url="https://api.waifu.im/search")

    def fetch_images(self, tags: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        params = {"is_nsfw": "false", "limit": min(limit, 30)}
        if tags:
            params["selected_tags"] = tags.split()
        headers = {"User-Agent": "CatgirlDownloader/1.1.0"}
        try:
            res = requests.get(self.base_url, params=params, headers=headers, timeout=10)
            res.raise_for_status()
            data = res.json()
            images = data.get("images", [])
            return [
                {
                    "id": str(img.get("image_id")),
                    "source": self.name,
                    "image_url": img.get("url"),
                    "preview_url": img.get("url"),
                    "tags": [t.get("name") for t in img.get("tags", [])],
                    "width": img.get("width"),
                    "height": img.get("height"),
                    "rating": "s"
                }
                for img in images
            ]
        except Exception as e:
            print(f"[waifu.im] Error: {e}")
            return []
