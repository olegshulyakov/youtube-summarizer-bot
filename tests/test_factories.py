# tests/test_factories.py

import pytest

from src.factories import SourceFactory
from src.sources import YouTubeSource, ArticleSource


@pytest.mark.parametrize("url, expected_class", [
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", YouTubeSource),
    ("https://youtu.be/dQw4w9WgXcQ", YouTubeSource),
    ("https://www.example.com/article", ArticleSource),
])
def test_source_factory_valid_url(url, expected_class):
    source = SourceFactory.create_source(url)
    assert isinstance(source, expected_class)


@pytest.mark.parametrize("invalid_url", [
    ("invalid-url"),
    ("ftp://example.com"),
    ("")
])
def test_source_factory_invalid_url(invalid_url):
    with pytest.raises(ValueError):  # Expect a ValueError
        SourceFactory.create_source(invalid_url)
