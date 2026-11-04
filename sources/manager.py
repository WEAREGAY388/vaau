class SourceManager:
    def __init__(self):
        self.sources = {}

    def register_source(self, source):
        self.sources[source.name] = source

    def get_source(self, name):
        return self.sources.get(name)

    def list_sources(self):
        return list(self.sources.keys())
