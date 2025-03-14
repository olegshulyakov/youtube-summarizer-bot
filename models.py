# models.py
from dataclasses import dataclass


@dataclass
class Content:
    text: str = None
    audio_path: str = None
    source_type: str = None
    source_url: str = None
    image_url: str = None
    error_message: str = None


@dataclass
class SummaryResult:
    summary: str = None
    error_message: str = None
