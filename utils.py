"""
Utility Functions Module
Contains helper functions for the voice assistant
"""

import datetime
import os
import json
from config import HISTORY_FILE, MAX_HISTORY_ENTRIES

def get_time_based_greeting():
    """Get appropriate greeting based on current time"""
    current_hour = datetime.datetime.now().hour
    
    if 5 <= current_hour < 12:
        return "Good morning!"
    elif 12 <= current_hour < 17:
        return "Good afternoon!"
    elif 17 <= current_hour < 22:
        return "Good evening!"
    else:
        return "Good night!"

def get_current_timestamp():
    """Get current timestamp in readable format"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_conversation(message):
    """Save conversation to history file (keep last 5 entries)"""
    try:
        # Read existing history
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    history = content.split("\n")
        
        # Add new message with timestamp
        timestamp = get_current_timestamp()
        new_entry = f"[{timestamp}] {message}"
        history.append(new_entry)
        
        # Keep only last MAX_HISTORY_ENTRIES
        if len(history) > MAX_HISTORY_ENTRIES:
            history = history[-MAX_HISTORY_ENTRIES:]
        
        # Write back to file
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(history))
            
    except Exception as e:
        print(f"Error saving conversation: {e}")

def load_conversation_history():
    """Load conversation history from file"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return content.split("\n")
        return []
    except Exception as e:
        print(f"Error loading conversation history: {e}")
        return []

def clear_conversation_history():
    """Clear conversation history file"""
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        return True
    except Exception as e:
        print(f"Error clearing conversation history: {e}")
        return False

def format_response_for_speech(text):
    """Format text response to be more suitable for speech output"""
    # Replace common abbreviations and symbols for better TTS
    replacements = {
        "&": "and",
        "@": "at",
        "%": "percent",
        "$": "dollars",
        "#": "number",
        "www.": "www dot",
        ".com": "dot com",
        ".org": "dot org",
        ".net": "dot net",
        "http://": "",
        "https://": "",
        "CEO": "C E O",
        "USA": "U S A",
        "UK": "U K",
        "AI": "A I",
    }
    
    formatted_text = text
    for old, new in replacements.items():
        formatted_text = formatted_text.replace(old, new)
    
    return formatted_text

def validate_environment():
    """Validate that required environment variables and dependencies are available"""
    issues = []
    
    # Check OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        issues.append("OPENAI_API_KEY environment variable not set")
    
    # Check required modules
    required_modules = [
        "speech_recognition",
        "pyttsx3", 
        "wikipedia",
        "pyjokes",
        "openai",
        "tkinter"
    ]
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            issues.append(f"Required module '{module}' not installed")
    
    return issues

def log_error(error_message, context=""):
    """Log error messages to file"""
    try:
        timestamp = get_current_timestamp()
        log_entry = f"[{timestamp}] ERROR in {context}: {error_message}\n"
        
        with open("kiddo_errors.log", "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Failed to log error: {e}")

def cleanup_temp_files():
    """Clean up temporary files created by the application"""
    temp_files = ["kiddo_errors.log"]
    
    for temp_file in temp_files:
        try:
            if os.path.exists(temp_file) and os.path.getsize(temp_file) > 1024 * 1024:  # > 1MB
                os.remove(temp_file)
        except Exception as e:
            print(f"Error cleaning up {temp_file}: {e}")

def get_system_info():
    """Get basic system information for debugging"""
    import platform
    import sys
    
    info = {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": sys.version,
        "architecture": platform.architecture()[0]
    }
    
    return info

def test_microphone():
    """Test if microphone is available and working"""
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
        return True, "Microphone test successful"
    except Exception as e:
        return False, f"Microphone test failed: {str(e)}"

def test_speakers():
    """Test if speakers/audio output is working"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say("Testing audio output")
        engine.runAndWait()
        return True, "Speaker test successful"
    except Exception as e:
        return False, f"Speaker test failed: {str(e)}"
