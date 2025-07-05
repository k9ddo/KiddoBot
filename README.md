# KiddoBot - Python Voice Assistant 🤖

A friendly Python desktop voice assistant with speech recognition, AI integration, and a graphical interface designed for kids and beginners.

![KiddoBot](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features ✨

- **Voice Recognition**: Accepts voice commands using your microphone
- **Text-to-Speech**: Responds with voice output
- **AI Integration**: Powered by OpenAI's GPT-4o for intelligent conversations
- **GUI Interface**: User-friendly chat window with text input option
- **Time & Date**: Tells current time with time-based greetings
- **Wikipedia Search**: Search and get summaries from Wikipedia
- **Jokes**: Tell random jokes to make you laugh
- **Web Browser**: Opens YouTube, Google, or any URL on command
- **Conversation History**: Saves last 5 conversations

## Requirements 📋

- Python 3.7 or higher
- OpenAI API key (for AI features)
- Microphone (optional - text input works without it)
- Internet connection

## Installation 🚀

1. Clone this repository:
```bash
git clone https://github.com/yourusername/kiddobot.git
cd kiddobot
```

2. Install required packages:
```bash
pip install openai speechrecognition pyttsx3 wikipedia pyjokes pyaudio
```

3. Set up your OpenAI API key:
   - Get your API key from https://platform.openai.com
   - Set it as an environment variable:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## Usage 💻

Run the application:
```bash
python main.py
```

### Voice Commands

- **Greet**: "Hello" or "Hi"
- **Time**: "What time is it?"
- **Jokes**: "Tell me a joke"
- **Wikipedia**: "Tell me about [topic]"
- **Websites**: "Open YouTube" or "Open Google"
- **Exit**: "Stop", "Quit", or "Bye"

### Text Mode

If voice isn't available, you can type messages in the text box and press Enter to send.

## Project Structure 📁

```
kiddobot/
├── main.py                 # Application entry point
├── voice_assistant.py      # Core voice processing logic
├── gui_interface.py        # GUI interface
├── config.py              # Configuration settings
├── utils.py               # Helper functions
└── kiddo_history.txt      # Conversation history (auto-generated)
```

## Configuration ⚙️

Edit `config.py` to customize:
- Speech recognition timeout
- Text-to-speech voice and speed
- GUI window size
- Wikipedia summary length
- Conversation history size

## Troubleshooting 🔧

**No microphone detected**: The app will work in text-only mode. Audio warnings in the console can be ignored.

**OpenAI errors**: Make sure your API key is valid and you have credits available.

**GUI not showing**: Ensure you have tkinter installed (comes with Python by default).

## Contributing 🤝

Feel free to submit issues and enhancement requests!

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- OpenAI for GPT integration
- Speech Recognition library contributors
- pyttsx3 for text-to-speech functionality