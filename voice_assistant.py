"""
Voice Assistant Core Module
Handles speech recognition, text-to-speech, and AI functionalities
"""

import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pyjokes
import os
import json
from openai import OpenAI
import threading
import time
from utils import save_conversation, get_time_based_greeting

class VoiceAssistant:
    def __init__(self):
        """Initialize the voice assistant with all required components"""
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.microphone_available = False
        
        # Initialize text-to-speech
        self.tts_engine = None
        self.tts_available = False
        self.setup_audio_components()
        
        # Initialize OpenAI client
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"))
        
        # Assistant state
        self.is_listening = False
        self.last_response = ""
        
    def setup_audio_components(self):
        """Setup audio components with fallback for environments without audio hardware"""
        # Try to initialize microphone
        try:
            self.microphone = sr.Microphone()
            # Test microphone by calibrating for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.microphone_available = True
            print("Microphone initialized successfully")
        except Exception as e:
            print(f"Microphone not available: {e}")
            self.microphone_available = False
        
        # Try to initialize text-to-speech
        try:
            self.tts_engine = pyttsx3.init()
            self.setup_tts()
            self.tts_available = True
            print("Text-to-speech initialized successfully")
        except Exception as e:
            print(f"Text-to-speech not available: {e}")
            self.tts_available = False
        
    def setup_tts(self):
        """Configure text-to-speech settings"""
        if not self.tts_engine:
            return
            
        try:
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Prefer female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                else:
                    self.tts_engine.setProperty('voice', voices[0].id)
            
            # Set speech rate
            self.tts_engine.setProperty('rate', 200)
            # Set volume
            self.tts_engine.setProperty('volume', 0.9)
        except Exception as e:
            print(f"TTS setup error: {e}")
    
    def speak(self, text):
        """Convert text to speech"""
        try:
            self.last_response = text
            print(f"KiddoBot: {text}")
            
            # Only use TTS if available
            if self.tts_available and self.tts_engine:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")
    
    def listen(self, timeout=5):
        """Listen for voice input and convert to text"""
        if not self.microphone_available or not self.microphone:
            return "no_microphone"
            
        try:
            with self.microphone as source:
                print("Listening...")
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
            print("Processing speech...")
            # Convert speech to text
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            return "timeout"
        except sr.UnknownValueError:
            return "unknown"
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return "error"
        except Exception as e:
            print(f"Listen error: {e}")
            return "error"
    
    def get_current_time(self):
        """Get current time and date"""
        now = datetime.datetime.now()
        time_str = now.strftime("It's %I:%M %p on %A, %B %d, %Y")
        return time_str
    
    def search_wikipedia(self, query):
        """Search Wikipedia and return summary"""
        try:
            # Remove common words from query
            query = query.replace("tell me about", "").replace("search for", "").strip()
            
            if not query:
                return "Please specify what you'd like me to search for."
            
            # Search Wikipedia
            summary = wikipedia.summary(query, sentences=2)
            return f"Here's what I found about {query}: {summary}"
            
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle multiple results
            try:
                summary = wikipedia.summary(e.options[0], sentences=2)
                return f"I found multiple results. Here's information about {e.options[0]}: {summary}"
            except:
                return f"I found multiple results for {query}. Please be more specific."
        except wikipedia.exceptions.PageError:
            return f"Sorry, I couldn't find any information about {query} on Wikipedia."
        except Exception as e:
            return f"Sorry, I encountered an error while searching: {str(e)}"
    
    def tell_joke(self):
        """Get a random joke"""
        try:
            joke = pyjokes.get_joke()
            return joke
        except Exception as e:
            return "Sorry, I couldn't fetch a joke right now. Here's one: Why don't scientists trust atoms? Because they make up everything!"
    
    def open_website(self, command):
        """Open websites based on voice command"""
        try:
            if "youtube" in command:
                webbrowser.open("https://www.youtube.com")
                return "Opening YouTube for you!"
            elif "google" in command:
                webbrowser.open("https://www.google.com")
                return "Opening Google for you!"
            elif "open" in command and "http" in command:
                # Extract URL from command
                words = command.split()
                for word in words:
                    if word.startswith("http"):
                        webbrowser.open(word)
                        return f"Opening {word} for you!"
                return "Please provide a valid URL starting with http or https."
            else:
                return "I can open YouTube, Google, or any URL you specify."
        except Exception as e:
            return f"Sorry, I couldn't open that website: {str(e)}"
    
    def ask_openai(self, question):
        """Get response from OpenAI GPT"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",  # the newest OpenAI model is "gpt-4o"
                messages=[
                    {"role": "system", "content": "You are KiddoBot, a friendly and helpful voice assistant. Keep responses concise but informative, suitable for voice output."},
                    {"role": "user", "content": question}
                ],
                max_tokens=150,
                temperature=0.7
            )
            if response.choices and response.choices[0].message and response.choices[0].message.content:
                return response.choices[0].message.content.strip()
            else:
                return "I received an empty response. Please try asking something else."
        except Exception as e:
            return f"Sorry, I couldn't process your question right now. Error: {str(e)}"
    
    def process_command(self, command):
        """Process voice command and return appropriate response"""
        command = command.lower().strip()
        
        # Save the conversation
        save_conversation(f"User: {command}")
        
        # Exit commands
        if any(word in command for word in ["stop", "quit", "bye", "goodbye", "exit"]):
            response = "Goodbye! It was nice talking to you!"
            save_conversation(f"KiddoBot: {response}")
            return response, "exit"
        
        # Greeting
        if any(word in command for word in ["hello", "hi", "hey"]):
            greeting = get_time_based_greeting()
            response = f"Hi! I'm KiddoBot, your smart buddy! {greeting}"
            save_conversation(f"KiddoBot: {response}")
            return response, "continue"
        
        # Time and date
        if any(word in command for word in ["time", "date", "today"]):
            response = self.get_current_time()
            save_conversation(f"KiddoBot: {response}")
            return response, "continue"
        
        # Wikipedia search
        if any(phrase in command for phrase in ["tell me about", "search for", "what is", "who is", "wikipedia"]):
            response = self.search_wikipedia(command)
            save_conversation(f"KiddoBot: {response}")
            return response, "continue"
        
        # Jokes
        if any(word in command for word in ["joke", "funny", "laugh"]):
            response = self.tell_joke()
            save_conversation(f"KiddoBot: {response}")
            return response, "continue"
        
        # Website opening
        if any(word in command for word in ["open", "youtube", "google"]) or "http" in command:
            response = self.open_website(command)
            save_conversation(f"KiddoBot: {response}")
            return response, "continue"
        
        # Default: Ask OpenAI
        response = self.ask_openai(command)
        save_conversation(f"KiddoBot: {response}")
        return response, "continue"
    
    def start_listening_loop(self, callback=None):
        """Start continuous listening in a separate thread"""
        def listen_loop():
            self.is_listening = True
            greeting = get_time_based_greeting()
            initial_message = f"Hi! I'm KiddoBot, your smart buddy! {greeting} How can I help you today?"
            
            if callback:
                callback(initial_message, "KiddoBot")
            else:
                self.speak(initial_message)
            
            while self.is_listening:
                try:
                    command = self.listen(timeout=10)
                    
                    if command in ["timeout", "unknown", "error", "no_microphone"]:
                        if command == "timeout":
                            continue  # Just continue listening
                        elif command == "no_microphone":
                            message = "Microphone not available. Please use text input."
                            if callback:
                                callback(message, "KiddoBot")
                            self.is_listening = False
                            break
                        elif command == "unknown":
                            message = "Sorry, I didn't understand that. Could you please repeat?"
                        else:
                            message = "Sorry, I'm having trouble hearing you. Please try again."
                        
                        if callback:
                            callback(message, "KiddoBot")
                        else:
                            self.speak(message)
                        continue
                    
                    # Process the command
                    response, action = self.process_command(command)
                    
                    if callback:
                        callback(f"You: {command}", "User")
                        callback(response, "KiddoBot")
                    else:
                        self.speak(response)
                    
                    if action == "exit":
                        self.is_listening = False
                        break
                        
                except Exception as e:
                    error_msg = f"An error occurred: {str(e)}"
                    if callback:
                        callback(error_msg, "System")
                    else:
                        print(error_msg)
        
        # Start listening in a separate thread
        listen_thread = threading.Thread(target=listen_loop, daemon=True)
        listen_thread.start()
        return listen_thread
    
    def stop_listening(self):
        """Stop the listening loop"""
        self.is_listening = False
    
    def process_text_input(self, text):
        """Process text input (for GUI mode)"""
        if not text.strip():
            return "Please enter a message."
        
        response, action = self.process_command(text)
        return response
