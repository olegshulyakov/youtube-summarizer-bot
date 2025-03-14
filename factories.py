# factories.py
from urllib.parse import urlparse

from sources import Source, YouTubeSource, ArticleSource


class SourceFactory:
    @staticmethod
    def create_source(source_string: str) -> Source:
        try:
            parsed_url = urlparse(source_string)
            if parsed_url.netloc == "www.youtube.com" or parsed_url.netloc == "youtu.be":
                return YouTubeSource(source_string)
            elif parsed_url.scheme in ("http", "https"):
                return ArticleSource(source_string)
            else:
                raise ValueError("Not supported source.")
        except Exception as e:
            raise ValueError(f"Cannot determine source type {e}")
