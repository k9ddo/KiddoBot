"""
GUI Interface Module
Provides tkinter-based graphical interface for the voice assistant
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from voice_assistant import VoiceAssistant

class VoiceAssistantGUI:
    def __init__(self, root, assistant):
        """Initialize the GUI interface"""
        self.root = root
        self.assistant = assistant
        self.is_voice_active = False
        
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("KiddoBot - Your Smart Voice Assistant")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Center the window
        self.root.geometry("800x600+300+100")
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🤖 KiddoBot - Your Smart Buddy", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Chat display area
        chat_frame = ttk.LabelFrame(main_frame, text="Conversation", padding="5")
        chat_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        chat_frame.grid_rowconfigure(0, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, 
            wrap=tk.WORD, 
            width=70, 
            height=20,
            font=("Arial", 10),
            state=tk.DISABLED
        )
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for different speakers
        self.chat_display.tag_configure("user", foreground="blue")
        self.chat_display.tag_configure("assistant", foreground="green")
        self.chat_display.tag_configure("system", foreground="red")
        
        # Input area
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="5")
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Text input
        text_input_frame = ttk.Frame(input_frame)
        text_input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        text_input_frame.grid_columnconfigure(0, weight=1)
        
        self.text_input = ttk.Entry(text_input_frame, font=("Arial", 10))
        self.text_input.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.text_input.bind("<Return>", self.send_text_message)
        
        send_button = ttk.Button(text_input_frame, text="Send", command=self.send_text_message)
        send_button.grid(row=0, column=1)
        
        # Control buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=1, column=0, pady=(5, 0))
        
        self.voice_button = ttk.Button(
            button_frame, 
            text="🎤 Start Voice Mode", 
            command=self.toggle_voice_mode
        )
        self.voice_button.grid(row=0, column=0, padx=(0, 5))
        
        clear_button = ttk.Button(button_frame, text="Clear Chat", command=self.clear_chat)
        clear_button.grid(row=0, column=1, padx=(0, 5))
        
        help_button = ttk.Button(button_frame, text="Help", command=self.show_help)
        help_button.grid(row=0, column=2)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Type a message or start voice mode")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        # Welcome message
        self.add_message("Welcome to KiddoBot! I'm your smart voice assistant.", "assistant")
        
        # Check audio availability
        if not self.assistant.microphone_available and not self.assistant.tts_available:
            self.add_message("Note: Audio features are not available in this environment, but text chat works perfectly!", "assistant")
            self.voice_button.config(state="disabled", text="🎤 Voice Not Available")
        elif not self.assistant.microphone_available:
            self.add_message("Note: Microphone not available, but I can still speak responses!", "assistant")
            self.voice_button.config(state="disabled", text="🎤 Microphone Not Available")
        elif not self.assistant.tts_available:
            self.add_message("Note: Text-to-speech not available, but voice input works!", "assistant")
        
        self.add_message("You can type messages below. Try asking me about time, jokes, Wikipedia, or anything else!", "assistant")
    
    def add_message(self, message, sender="user"):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        if sender == "user":
            self.chat_display.insert(tk.END, f"[{timestamp}] You: ", "user")
            self.chat_display.insert(tk.END, f"{message}\n\n")
        elif sender == "assistant" or sender == "KiddoBot":
            self.chat_display.insert(tk.END, f"[{timestamp}] KiddoBot: ", "assistant")
            self.chat_display.insert(tk.END, f"{message}\n\n")
        else:  # system messages
            self.chat_display.insert(tk.END, f"[{timestamp}] System: ", "system")
            self.chat_display.insert(tk.END, f"{message}\n\n")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_text_message(self, event=None):
        """Send text message to assistant"""
        message = self.text_input.get().strip()
        if not message:
            return
        
        self.text_input.delete(0, tk.END)
        self.add_message(message, "user")
        
        # Process message in separate thread to avoid blocking GUI
        def process_message():
            try:
                self.status_var.set("Processing...")
                response = self.assistant.process_text_input(message)
                
                # Update GUI in main thread
                self.root.after(0, lambda: self.add_message(response, "assistant"))
                self.root.after(0, lambda: self.status_var.set("Ready"))
                
                # Speak the response
                if response and not any(word in message.lower() for word in ["stop", "quit", "bye"]):
                    threading.Thread(target=self.assistant.speak, args=(response,), daemon=True).start()
                
            except Exception as e:
                error_msg = f"Error processing message: {str(e)}"
                self.root.after(0, lambda: self.add_message(error_msg, "system"))
                self.root.after(0, lambda: self.status_var.set("Error occurred"))
        
        threading.Thread(target=process_message, daemon=True).start()
    
    def toggle_voice_mode(self):
        """Toggle voice recognition mode"""
        if not self.is_voice_active:
            # Start voice mode
            self.is_voice_active = True
            self.voice_button.config(text="🔴 Stop Voice Mode")
            self.status_var.set("Voice mode active - Listening...")
            
            # Start voice recognition in separate thread
            def voice_callback(message, sender):
                self.root.after(0, lambda: self.add_message(message, sender))
                if sender == "KiddoBot":
                    self.root.after(0, lambda: threading.Thread(
                        target=self.assistant.speak, args=(message,), daemon=True
                    ).start())
            
            self.voice_thread = self.assistant.start_listening_loop(callback=voice_callback)
            
        else:
            # Stop voice mode
            self.is_voice_active = False
            self.voice_button.config(text="🎤 Start Voice Mode")
            self.status_var.set("Voice mode stopped")
            self.assistant.stop_listening()
    
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.add_message("Chat cleared. How can I help you?", "assistant")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
KiddoBot Voice Assistant Help

Voice Commands:
• "Hello" or "Hi" - Greet KiddoBot
• "What time is it?" - Get current time and date
• "Tell me about [topic]" - Search Wikipedia
• "Tell me a joke" - Get a random joke
• "Open YouTube/Google" - Open websites
• "Stop", "Quit", or "Bye" - Exit voice mode

Text Input:
• You can type any message in the text box
• Press Enter or click Send to submit
• KiddoBot will respond with both text and voice

Features:
• Voice recognition and text-to-speech
• Wikipedia search and summaries
• AI-powered responses via OpenAI
• Conversation history (last 5 saved to file)
• Time-based greetings

Tips:
• Speak clearly and wait for the listening prompt
• Use the microphone button to start/stop voice mode
• You can mix voice and text input as needed
        """
        
        messagebox.showinfo("KiddoBot Help", help_text)
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_voice_active:
            self.assistant.stop_listening()
        self.root.destroy()
