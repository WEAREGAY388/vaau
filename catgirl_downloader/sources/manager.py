from typing import Dict, List, Optional
from .base import BaseSource
from .yande import YandeSource
from .nekos import NekosSource
from .waifu_im import WaifuImSource
from .danbooru import DanbooruSource

class SourceManager:
    def __init__(self):
        self.sources: Dict[str, BaseSource] = {}
        self._register_default_sources()

    def _register_default_sources(self):
        for src in [YandeSource(), NekosSource(), WaifuImSource(), DanbooruSource()]:
            self.register_source(src)

    def register_source(self, source: BaseSource):
        self.sources[source.name] = source

    def get_source(self, name: str) -> Optional[BaseSource]:
        return self.sources.get(name)

    def list_sources(self) -> List[str]:
        return list(self.sources.keys())
