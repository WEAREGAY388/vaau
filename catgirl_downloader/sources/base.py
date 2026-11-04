from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseSource(ABC):
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url

    @abstractmethod
    def fetch_images(self, tags: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        pass
