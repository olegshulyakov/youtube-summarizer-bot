# youtube_summarizer_bot/handlers.py

import io
from abc import ABC, abstractmethod

import requests
import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters

from factories import SourceFactory  # Relative import
from logger import setup_logger
from processors import TextProcessor

logger = setup_logger(__name__)


class BaseHandler(ABC):  # Keep the abstract base class
    """
    Abstract base class for all handlers.
    Defines the common interface for handling requests.
    """

    @abstractmethod
    def run(self):
        """Starts the handler. Renamed for clarity."""
        pass


class TelegramHandler(BaseHandler):
    """Handles requests from Telegram."""

    def __init__(self, bot_token):
        """
        Initializes the Telegram handler.

        Args:
            bot_token (str): The Telegram bot token.
        """
        self.updater = telegram.ext.Updater(token=bot_token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.bot = self.updater.bot  # save bot variable

        # Register handlers (using methods, not external functions)
        start_handler = CommandHandler('start', self.start)
        message_handler = MessageHandler(Filters.text & ~Filters.command, self.handle_message)

        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(message_handler)

    def run(self):
        """Starts the Telegram bot (starts polling)."""
        logger.info("Starting polling...")
        self.updater.start_polling()
        self.updater.idle()

    def start(self, update, context):
        """Handles the /start command."""
        logger.info("Start command received")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Send me the link and I'll make a summary!")

    def handle_message(self, update, context):
        """Handles text messages (presumably URLs)."""
        source_string = update.message.text
        chat_id = update.effective_chat.id
        self.bot.send_message(chat_id=chat_id, text="Processing the request...")

        try:
            source = SourceFactory.create_source(source_string)
            content = source.get_content()
            if content.error_message:
                logger.error(content.error_message)
                self.bot.send_message(chat_id=chat_id, text=content.error_message)
                return

            processor = TextProcessor()
            result = processor.process(content)

            if result.error_message:
                logger.error(result.error_message)
                self.bot.send_message(chat_id=chat_id, text=result.error_message)
                return

            # Send image and text
            if content.image_url:
                try:
                    response = requests.get(content.image_url)
                    response.raise_for_status()
                    image_file = io.BytesIO(response.content)
                    self.bot.send_photo(chat_id=chat_id, photo=image_file, caption=result.summary)

                except requests.exceptions.RequestException as e:
                    logger.error(f"Error downloading image: {e}")
                    self.bot.send_message(chat_id=chat_id, text=f"Error downloading image: {e}")
                    self.bot.send_message(chat_id=chat_id, text=result.summary)  # Send text only
                except Exception as e:
                    logger.exception(f"Unexpected error with image: {e}")
                    self.bot.send_message(chat_id=chat_id, text=result.summary)
            else:
                self.bot.send_message(chat_id=chat_id, text=result.summary)

        except ValueError as e:
            logger.error(str(e))
            self.bot.send_message(chat_id=chat_id, text=str(e))

        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
            self.bot.send_message(chat_id=chat_id, text=f"An unexpected error occurred: {e}")
