import requests
from typing import List, Dict, Any
from .base import BaseSource

class NekosSource(BaseSource):
    def __init__(self):
        super().__init__(name="nekos.moe", base_url="https://nekos.moe/api/v1/images/search")

    def fetch_images(self, tags: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        payload = {"nsfw": False, "limit": limit}
        headers = {"User-Agent": "CatgirlDownloader/1.1.0"}
        try:
            res = requests.post(self.base_url, json=payload, headers=headers, timeout=10)
            res.raise_for_status()
            data = res.json()
            images = data.get("images", [])
            return [
                {
                    "id": img.get("id"),
                    "source": self.name,
                    "image_url": f"https://nekos.moe/image/{img.get('id')}",
                    "preview_url": f"https://nekos.moe/thumbnail/{img.get('id')}",
                    "tags": img.get("tags", []),
                    "width": None,
                    "height": None,
                    "rating": "s"
                }
                for img in images
            ]
        except Exception as e:
            print(f"[nekos.moe] Error: {e}")
            return []
