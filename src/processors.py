# processors.py
from abc import ABC, abstractmethod

from transformers import pipeline

from models import Content, SummaryResult


class Processor(ABC):
    @abstractmethod
    def process(self, content: Content) -> SummaryResult:
        pass

# import speech_recognition as sr
# class AudioProcessor(Processor):
#     def __init__(self, summarizer_model="facebook/bart-large-cnn"):
#         self.r = sr.Recognizer()
#         self.summarizer = pipeline("summarization", model=summarizer_model)
#
#     def process(self, content: Content) -> SummaryResult:
#         if content.error_message:
#             return SummaryResult(error_message=content.error_message)
#
#         if not content.audio_path:
#             return SummaryResult(error_message="AudioProcessor: No audio file path.")
#
#         try:
#             with sr.AudioFile(content.audio_path) as source:
#                 audio = self.r.record(source)
#             text = self.r.recognize_google(audio, language="ru-RU")
#             max_chunk_length = 1024
#             chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]
#             summaries = []
#             for chunk in chunks:
#                 summary = self.summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
#                 summaries.append(summary)
#             os.remove(content.audio_path)
#             return SummaryResult(summary=" ".join(summaries))
#
#         except sr.UnknownValueError:
#             return SummaryResult(error_message="Speech recognition failed")
#         except sr.RequestError as e:
#             return SummaryResult(error_message=f"Speech recognition service error; {e}")
#         except Exception as e:
#             return SummaryResult(error_message=f"Error on audio processing: {e}")


class TextProcessor(Processor):
    def __init__(self, summarizer_model="facebook/bart-large-cnn"):
        self.summarizer = pipeline("summarization", model=summarizer_model)

    def process(self, content: Content) -> SummaryResult:
        if content.error_message:
            return SummaryResult(error_message=content.error_message)

        if not content.text:
            return SummaryResult(error_message="TextProcessor: No text for processing.")
        try:
            max_chunk_length = 1024
            chunks = [content.text[i:i + max_chunk_length] for i in range(0, len(content.text), max_chunk_length)]
            summaries = []
            for chunk in chunks:
                summary = self.summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
                summaries.append(summary)

            return SummaryResult(summary=" ".join(summaries))

        except Exception as e:
            return SummaryResult(error_message=f"Error on summarizing: {e}")
