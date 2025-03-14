# tests/test_processors.py
from unittest.mock import patch, MagicMock

from models import Content
from processors import TextProcessor


@patch('processors.pipeline')  # Mock pipeline
def test_text_processor_valid_content(mock_pipeline):
    # Create a mock object for summarizer
    mock_summarizer = MagicMock()
    mock_summarizer.return_value = [{'summary_text': 'Test summary'}]  # expected result
    mock_pipeline.return_value = mock_summarizer  # set return value

    processor = TextProcessor()
    content = Content(text="Test text", source_type="test")
    result = processor.process(content)

    assert result.error_message is None
    assert result.summary == "Test summary"
    mock_summarizer.assert_called_once()  # Check that summarizer was called


def test_text_processor_no_text():
    processor = TextProcessor()
    content = Content(source_type="test")  # No text
    result = processor.process(content)
    assert result.error_message is not None


def test_text_processor_error_content():
    processor = TextProcessor()
    content = Content(error_message="Test error", source_type="test")  # Error in Content
    result = processor.process(content)
    assert result.error_message == "Test error"


@patch('processors.pipeline')  # Mock pipeline
def test_text_processor_long_text(mock_pipeline):
    # Create mock object for summarizer
    mock_summarizer = MagicMock()
    mock_summarizer.side_effect = lambda x, **kwargs: [{'summary_text': f'Summary of {x}'}]
    mock_pipeline.return_value = mock_summarizer

    processor = TextProcessor()
    long_text = "a" * 2048  # Long text
    content = Content(text=long_text, source_type="test")
    result = processor.process(content)
    assert result.summary is not None
    # Additional checks if needed (e.g., that summary contains "Summary of")
    assert mock_summarizer.call_count > 1  # Should be called multiple times


@patch('processors.pipeline')
def test_text_processor_summarization_error(mock_pipeline):
    # Create a mock that raises an exception
    mock_summarizer = MagicMock()
    mock_summarizer.side_effect = Exception("Test summarization error")  # Simulate a summarization error
    mock_pipeline.return_value = mock_summarizer

    processor = TextProcessor()
    content = Content(text="Test text", source_type="test")
    result = processor.process(content)
    assert result.error_message is not None
