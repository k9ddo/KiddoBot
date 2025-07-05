#!/usr/bin/env python3
"""
KiddoBot - A Python Desktop Voice Assistant
Main entry point for the application
"""

import tkinter as tk
from gui_interface import VoiceAssistantGUI
from voice_assistant import VoiceAssistant
import threading
import sys

def main():
    """Main function to start the KiddoBot application"""
    try:
        # Create the main tkinter window
        root = tk.Tk()
        
        # Initialize the voice assistant
        assistant = VoiceAssistant()
        
        # Create and setup the GUI
        gui = VoiceAssistantGUI(root, assistant)
        
        # Start the GUI main loop
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting KiddoBot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
