# main.py
import os

from dotenv import load_dotenv

from handlers import TelegramHandler
from logger import setup_logger

logger = setup_logger(__name__)

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def main():
    """Main function to start the bot."""

    # Create the Telegram handler
    telegram_handler = TelegramHandler(TELEGRAM_BOT_TOKEN)

    # Start the bot (using the handler's 'run' method)
    telegram_handler.run()


if __name__ == '__main__':
    main()
