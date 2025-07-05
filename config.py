"""
Configuration Module
Handles application settings and configuration
"""

import os
import json

# Application Settings
APP_NAME = "KiddoBot"
APP_VERSION = "1.0.0"
HISTORY_FILE = "kiddo_history.txt"
MAX_HISTORY_ENTRIES = 5

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")

# Speech Recognition Settings
SPEECH_TIMEOUT = 10  # seconds
PHRASE_TIME_LIMIT = 10  # seconds
AMBIENT_NOISE_DURATION = 1  # seconds

# Text-to-Speech Settings
TTS_RATE = 200  # words per minute
TTS_VOLUME = 0.9  # 0.0 to 1.0

# Wikipedia Settings
WIKIPEDIA_SENTENCES = 2  # Number of sentences in summary

# GUI Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_MIN_WIDTH = 600
WINDOW_MIN_HEIGHT = 400

# Voice Commands Mapping
GREETING_COMMANDS = ["hello", "hi", "hey", "greetings"]
TIME_COMMANDS = ["time", "date", "today", "what time"]
WIKI_COMMANDS = ["tell me about", "search for", "what is", "who is", "wikipedia"]
JOKE_COMMANDS = ["joke", "funny", "laugh", "humor"]
WEBSITE_COMMANDS = ["open", "youtube", "google", "website"]
EXIT_COMMANDS = ["stop", "quit", "bye", "goodbye", "exit"]

def get_config():
    """Get application configuration as dictionary"""
    return {
        "app_name": APP_NAME,
        "app_version": APP_VERSION,
        "history_file": HISTORY_FILE,
        "max_history": MAX_HISTORY_ENTRIES,
        "openai_api_key": OPENAI_API_KEY,
        "speech_timeout": SPEECH_TIMEOUT,
        "phrase_time_limit": PHRASE_TIME_LIMIT,
        "tts_rate": TTS_RATE,
        "tts_volume": TTS_VOLUME,
        "wikipedia_sentences": WIKIPEDIA_SENTENCES,
        "window_size": (WINDOW_WIDTH, WINDOW_HEIGHT),
        "min_window_size": (WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
    }

def save_config(config_dict):
    """Save configuration to file"""
    try:
        with open("kiddo_config.json", "w") as f:
            json.dump(config_dict, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def load_config():
    """Load configuration from file"""
    try:
        if os.path.exists("kiddo_config.json"):
            with open("kiddo_config.json", "r") as f:
                return json.load(f)
        return get_config()
    except Exception as e:
        print(f"Error loading config: {e}")
        return get_config()
