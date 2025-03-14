# sources.py
from abc import ABC, abstractmethod
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import YoutubeLoader
from langchain_yt_dlp.youtube_loader import YoutubeLoaderDL

from logger import setup_logger
from models import Content

logger = setup_logger(__name__)

TRANSCRIPT_LANGUAGE = "ru,ru_auto,en,en_auto"  # a list of languages from highest priority to lowest
TRANSCRIPT_TRANSLATE = "ru"  # The language you want the transcript to auto-translate to, if it does not already exist.


class Source(ABC):
    def __init__(self, source_string):
        self.source_string = source_string

    @abstractmethod
    def get_content(self) -> Content:
        pass


class YouTubeSource(Source):

    def __init__(self, url):
        super().__init__(url)

    def get_content(self) -> Content:
        # Check if the URL is valid
        if not self.source_string or self.source_string == "":
            logger.error(f"Invalid YouTube URL: {self.source_string}")
            return Content(source_type="youtube", source_url=self.source_string, error_message=f"Invalid YouTube URL: {self.source_string}")

        try:
            details = YoutubeLoaderDL.from_youtube_url(self.source_string, add_video_info=True).load()

            if len(details) == 0:
                logger.warning(f"Failed to get video details: {self.source_string}")
                return Content(source_type="youtube", source_url=self.source_string, error_message="Failed to get video details")

            image_url = details[0].metadata.get("thumbnail_url")

            docs = YoutubeLoader.from_youtube_url(
                self.source_string,
                add_video_info=True,
                language=TRANSCRIPT_LANGUAGE.split(","),
                translation=TRANSCRIPT_TRANSLATE,
            ).load()
        except Exception as e:
            logger.exception(f"Error YouTube: {e}")
            return Content(source_type="youtube", source_url=self.source_string, error_message=f"Error YouTube: {e}")

        if not docs:  # If the download failed
            logger.warning(f"Subtitles could not be downloaded: {self.source_string}")
            return Content(source_type="youtube", source_url=self.source_string, error_message="Subtitles could not be downloaded")

        text = ""
        for doc in docs:
            try:
                text += doc.page_content
            except AttributeError:
                logger.error(f"Error processing document: {doc}")

        return Content(text=text, source_type="youtube", source_url=self.source_string, image_url=image_url)


class ArticleSource(Source):
    def __init__(self, url):
        super().__init__(url)

    def get_content(self) -> Content:
        try:
            response = requests.get(self.source_string)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            text = "\n".join([p.get_text() for p in paragraphs])

            image_url = None
            img_tag = soup.find('img')
            if img_tag and img_tag.get('src'):
                image_url = img_tag.get('src')

                if not image_url.startswith("http"):
                    base_url = urlparse(self.source_string).scheme + "://" + urlparse(self.source_string).netloc
                    image_url = base_url + image_url

            return Content(text=text, source_type="article", source_url=self.source_string, image_url=image_url)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error loading the article: {e}")
            return Content(error_message=f"Error loading the article: {e}")

        except Exception as e:
            logger.exception(f"Error when extracting the text of the article: {e}")
            return Content(error_message=f"Error when extracting the text of the article: {e}")
