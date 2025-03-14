# tests/test_sources.py

from unittest.mock import patch, MagicMock

import pytest

from src.sources import YouTubeSource, ArticleSource


# Tests for YouTubeSource
@pytest.mark.parametrize("url, expected_type", [
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "youtube"),
    ("https://youtu.be/dQw4w9WgXcQ", "youtube"),
])
def test_youtube_source_valid_url(url, expected_type):
    source = YouTubeSource(url)
    content = source.get_content()
    assert content.error_message is None
    assert content.source_type == expected_type

    if expected_type == "youtube":
        assert content.source_url == url
        assert content.text is not None
        # assert content.image_url is not None


@pytest.mark.parametrize("invalid_url", [
    ("invalid-url"),  # Invalid URL
    ("https://example.com"),  # Not a YouTube URL
    ("https://www.youtube.com/playlist?list=PL12345"),  # playlist
])
def test_youtube_source_invalid_url(invalid_url):
    source = YouTubeSource(invalid_url)
    content = source.get_content()
    assert content.error_message is not None  # Expect an error


# Mock YoutubeLoader to avoid making real network requests
@patch('sources.YoutubeLoader.from_youtube_url')  # specify the full path
def test_youtube_source_loader_error(mock_loader):
    mock_loader.side_effect = Exception("Test error")  # Simulate an error
    source = YouTubeSource("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    content = source.get_content()
    assert content.error_message is not None


@patch('sources.YoutubeLoader.from_youtube_url')
def test_youtube_source_no_docs(mock_loader):
    mock_loader.return_value.load.return_value = []  # if load returned empty list.
    source = YouTubeSource("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    content = source.get_content()
    assert content.error_message is not None


# Tests for ArticleSource

@patch('sources.requests.get')
def test_article_source_valid_url(mock_get):
    # Create a mock response object
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"<html><body><p>Test text</p><img src='https://example.com/image.jpg'></body></html>"  # Simulate response
    mock_get.return_value = mock_response  # Substitute

    source = ArticleSource("https://www.example.com/article")
    content = source.get_content()

    assert content.error_message is None
    assert content.text == "Test text"  # Check
    assert content.source_type == "article"
    assert content.image_url == "https://example.com/image.jpg"


@patch('sources.requests.get')
def test_article_source_relative_image_url(mock_get):
    # Test handling of relative image URLs
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"<html><body><p>Test text</p><img src='/image.jpg'></body></html>"  # Relative path
    mock_get.return_value = mock_response

    source = ArticleSource("https://www.example.com/article")
    content = source.get_content()
    assert content.image_url == "https://www.example.com/image.jpg"


@patch('sources.requests.get')
def test_article_source_no_image(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"<html><body><p>Test text</p></body></html>"  # No image
    mock_get.return_value = mock_response

    source = ArticleSource("https://www.example.com/article")
    content = source.get_content()
    assert content.image_url is None  # Check that image_url is None


@pytest.mark.parametrize("invalid_url", [
    ("invalid-url"),
    ("ftp://example.com")

])
def test_article_source_invalid_url(invalid_url):
    source = ArticleSource(invalid_url)
    content = source.get_content()
    assert content.error_message is not None


@patch('sources.requests.get')
def test_article_source_request_error(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("Test error")  # Simulate a request error
    source = ArticleSource("https://www.example.com/article")
    content = source.get_content()
    assert content.error_message is not None
