# YouTube & Article Summarizer Bot

This project implements a Telegram bot and a REST API that summarize YouTube videos and web articles. It uses the following technologies:

* **Python:** The primary programming language.
* **Telegram Bot API:** For interacting with Telegram.
* **LangChain:** For loading and processing YouTube transcripts.
* **Hugging Face Transformers:** For text summarization (using the BART model).
* **Beautiful Soup:** For parsing HTML content from articles.
* **Docker:** For containerization.
* **pytest:** For testing.
* **python-dotenv:** To manage environment variables.

## Features

* **Telegram Bot:**
    * Responds to the `/start` command.
    * Accepts YouTube video URLs and web article URLs.
    * Fetches the video transcript (or article content).
    * Summarizes the text using the BART model.
    * Sends the summary and a preview image (if available) to the user.

* **REST API:**
    * Provides a `/summarize` endpoint (POST request).
    * Accepts a JSON payload with a `url` field.
    * Returns a JSON response with the summary, source type, source URL, and image URL (if available).

## Project Structure

```
youtube_summarizer_bot/
├── main.py # Main application logic (Telegram bot and REST API startup)
├── sources.py # Data source classes (YouTubeSource, ArticleSource)
├── processors.py # Content processing classes (TextProcessor)
├── factories.py # Factory for creating Source objects
├── models.py # Data classes (Content, SummaryResult)
├── requirements.txt # Python dependencies
├── .env # Environment variables (e.g., Telegram bot token)
├── logger.py # Logging configuration
├── handlers.py # Handles interactions (Telegram, REST API)
└── tests/ # Unit tests
├── init.py
├── test_models.py
├── test_sources.py
├── test_processors.py
└── test_factories.py
Dockerfile # Docker configuration
```

## Setup and Installation

**Prerequisites:**

* Python 3.9+ (or a compatible version, as specified in the `Dockerfile`)
* pip
* Docker (optional, for containerized deployment)

**1. Clone the repository:**

```bash
git clone <your_repository_url>
cd <your_repository_directory>
```

**2. Create a virtual environment (recommended):**

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate  # On Windows
```

**3. Install dependencies:**
`pip install -r requirements.txt`

**4. Create a .env file:**
Create a .env file in the root directory of the project and add your Telegram bot token:
`TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN`
Replace YOUR_TELEGRAM_BOT_TOKEN with your actual token.

**5. Run the tests (optional but recommended):**
`pytest tests/`

## Running the Application

**Locally:**
```
python youtube_summarizer_bot/main.py
```

**With Docker:**

1. Build the Docker image: `docker build -t youtube-summarizer-bot .`
2. Run the Docker container: `docker run youtube-summarizer-bot`

## Contributing

Contributions are welcome! Please submit pull requests with your changes.