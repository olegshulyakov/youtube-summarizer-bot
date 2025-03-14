# tests/test_models.py

from src.models import Content, SummaryResult


def test_content_creation():
    # Test Content object creation
    content = Content(text="Test text", audio_path="test.mp3", source_type="test",
                      source_url="http://example.com", image_url="http://example.com/image.jpg")
    assert content.text == "Test text"
    assert content.audio_path == "test.mp3"
    assert content.source_type == "test"
    assert content.source_url == "http://example.com"
    assert content.image_url == "http://example.com/image.jpg"
    assert content.error_message is None


def test_summary_result_creation():
    # Test SummaryResult creation
    result = SummaryResult(summary="Test summary", error_message="Test error")
    assert result.summary == "Test summary"
    assert result.error_message == "Test error"
