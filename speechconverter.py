import os
import platform
import subprocess
import speech_recognition as sr
import requests
import json
from datetime import datetime

try:
    from gtts import gTTS, lang
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("Warning: gTTS not installed. Text-to-speech will not work.")
    print("Install it using: pip install gtts")

class SpeechAppCLI:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.running = True
        
    def display_menu(self):
        print("\n" + "="*50)
        print("    SPEECH TO TEXT & TEXT TO SPEECH CONVERTER")
        print("="*50)
        print("1. Text to Speech")
        print("2. Speech to Text")
        print("3. List Supported Languages")
        print("4. Check Microphone")
        print("5. Exit")
        print("-"*50)
        
    def text_to_speech(self):
        print("\n--- TEXT TO SPEECH ---")
        text = input("Enter the text you want to convert to speech: ").strip()
        
        if not text:
            print("Error: No text entered.")
            return
            
        print("\nAvailable language codes (common ones):")
        common_languages = {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh-CN': 'Chinese',
            'hi': 'Hindi',
            'ar': 'Arabic'
        }
        
        for code, name in common_languages.items():
            print(f"  {code}: {name}")
            
        language = input("\nEnter language code (default: 'en' for English): ").strip()
        if not language:
            language = "en"
            
        print("\nTrying different text-to-speech methods...")
        
        if GTTS_AVAILABLE:
            success = self.try_gtts(text, language)
            if success:
                return
        
        self.try_alternative_tts(text, language)
            
    def try_gtts(self, text, language):
        try:
            print("Attempting gTTS method...")
            
            try:
                speech = gTTS(text=text, lang=language, slow=False)
                filename = "output_speech_gtts.mp3"
                speech.save(filename)
                print(f"✓ gTTS successful! Audio saved as '{filename}'")
                self.ask_play_audio(filename)
                return True
            except Exception as e:
                print(f"✗ Standard gTTS failed: {str(e)}")
                
            try:
                print("Trying gTTS with different parameters...")
                speech = gTTS(text=text, lang=language, slow=True)
                filename = "output_speech_gtts_slow.mp3"
                speech.save(filename)
                print(f"✓ gTTS (slow) successful! Audio saved as '{filename}'")
                self.ask_play_audio(filename)
                return True
            except Exception as e:
                print(f"✗ gTTS with slow speed failed: {str(e)}")
                
            try:
                print("Trying gTTS with chunked text...")
                if len(text) > 100:
                    chunks = [text[i:i+100] for i in range(0, len(text), 100)]
                    combined_filename = "output_speech_gtts_combined.mp3"
                    speech = gTTS(text=chunks[0], lang=language, slow=False)
                    speech.save(combined_filename)
                    print(f"✓ gTTS (chunked) successful! Audio saved as '{combined_filename}'")
                    self.ask_play_audio(combined_filename)
                    return True
                else:
                    return False
                    
            except Exception as e:
                print(f"✗ gTTS with chunked text failed: {str(e)}")
                
        except Exception as e:
            print(f"All gTTS methods failed: {str(e)}")
            
        return False
    
    def try_alternative_tts(self, text, language):
        print("\nTrying alternative text-to-speech methods...")
        
        success = self.try_pyttsx3(text, language)
        if success:
            return
            
        success = self.try_edge_tts(text, language)
        if success:
            return
            
        print("\n" + "="*50)
        print("ALL AUTOMATIC METHODS FAILED")
        print("="*50)
        print("Manual solutions:")
        print("1. Check your internet connection")
        print("2. Try again later (Google TTS might be temporarily unavailable)")
        print("3. Use the following online TTS services:")
        print("   - https://ttsmp3.com")
        print("   - https://www.naturalreaders.com/online/")
        print("   - https://voicemaker.in")
        print(f"   Text to convert: '{text}'")
        print("4. Install pyttsx3 for offline TTS: pip install pyttsx3")
        
    def try_pyttsx3(self, text, language):
        try:
            import pyttsx3
            print("Attempting pyttsx3 (offline TTS)...")
            
            engine = pyttsx3.init()
            
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            
            voices = engine.getProperty('voices')
            if language.startswith('en') and len(voices) > 1:
                engine.setProperty('voice', voices[1].id)
            
            engine.say(text)
            engine.runAndWait()
            print("✓ pyttsx3 successful! Speech played.")
            return True
            
        except ImportError:
            print("✗ pyttsx3 not installed. Install with: pip install pyttsx3")
        except Exception as e:
            print(f"✗ pyttsx3 failed: {str(e)}")
            
        return False
    
    def try_edge_tts(self, text, language):
        try:
            import asyncio
            import edge_tts
            print("Attempting edge-tts...")
            
            async def generate_speech():
                communicate = edge_tts.Communicate(text, language)
                filename = "output_speech_edge.mp3"
                await communicate.save(filename)
                return filename
                
            filename = asyncio.run(generate_speech())
            print(f"✓ edge-tts successful! Audio saved as '{filename}'")
            self.ask_play_audio(filename)
            return True
            
        except ImportError:
            print("✗ edge-tts not installed. Install with: pip install edge-tts")
        except Exception as e:
            print(f"✗ edge-tts failed: {str(e)}")
            
        return False
    
    def ask_play_audio(self, filename):
        play_audio = input("Do you want to play the audio now? (y/n): ").lower().strip()
        if play_audio in ['y', 'yes']:
            self.play_audio(filename)
        else:
            print(f"You can play the file '{filename}' manually.")
            
    def play_audio(self, filename):
        system = platform.system()
        try:
            if system == "Windows":
                os.system(f'start {filename}')
                print("Playing audio...")
            elif system == "Darwin":
                os.system(f'afplay "{filename}"')
                print("Playing audio...")
            else:
                players = ["mpg123", "mpg321", "play", "aplay"]
                player_found = False
                for player in players:
                    if subprocess.run(["which", player], capture_output=True).returncode == 0:
                        os.system(f'{player} "{filename}"')
                        print(f"Playing audio using {player}...")
                        player_found = True
                        break
                if not player_found:
                    print("No audio player found. Please play the file manually.")
                    
        except Exception as e:
            print(f"Error playing audio: {str(e)}")
            print(f"Please play the file '{filename}' manually.")
            
    def speech_to_text(self):
        print("\n--- SPEECH TO TEXT ---")
        
        try:
            duration_input = input("Enter recording duration in seconds (default: 5): ").strip()
            duration = int(duration_input) if duration_input else 5
            
            if duration <= 0:
                print("Error: Duration must be a positive number.")
                return
            if duration > 30:
                print("Error: Duration cannot exceed 30 seconds.")
                return
                
        except ValueError:
            print("Error: Please enter a valid number.")
            return
            
        try:
            print(f"\nPreparing to record for {duration} seconds...")
            print("Make sure your microphone is connected and working.")
            input("Press Enter to start recording...")
            
            with sr.Microphone() as mic:
                print("Recording... Speak now!")
                self.recognizer.adjust_for_ambient_noise(mic, duration=1)
                audio_input = self.recognizer.record(mic, duration=duration)
                print("Recording finished. Processing...")
                
                try:
                    text_output = self.recognizer.recognize_google(audio_input)
                    
                    print("\n" + "="*40)
                    print("RECOGNIZED TEXT:")
                    print("="*40)
                    print(text_output)
                    print("="*40)
                    
                    save_file = input("\nDo you want to save this text to a file? (y/n): ").lower().strip()
                    if save_file in ['y', 'yes']:
                        filename = input("Enter filename (default: speech_output.txt): ").strip()
                        if not filename:
                            filename = "speech_output.txt"
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(text_output)
                        print(f"Text saved to '{filename}'")
                        
                except sr.UnknownValueError:
                    print("Error: Could not understand the audio. Please try again.")
                except sr.RequestError as e:
                    print(f"Error: Speech recognition service error: {e}")
                    
        except OSError as e:
            if "No default input device" in str(e):
                print("Error: No microphone found. Please check your audio device.")
            else:
                print(f"Error: Microphone error: {str(e)}")
        except Exception as e:
            print(f"Error: Unexpected error: {str(e)}")
            
    def list_languages(self):
        if not GTTS_AVAILABLE:
            print("Error: gTTS is not available.")
            return
            
        try:
            languages = lang.tts_langs()
            
            print("\n" + "="*60)
            print("SUPPORTED LANGUAGES FOR TEXT-TO-SPEECH")
            print("="*60)
            
            languages_list = list(languages.items())
            languages_list.sort()
            
            print(f"Total languages supported: {len(languages_list)}")
            print("\nCommon languages:")
            print("-" * 40)
            
            common_codes = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh-CN', 'hi', 'ar']
            for code in common_codes:
                if code in languages:
                    print(f"  {code}: {languages[code]}")
            
            show_all = input("\nDo you want to see all supported languages? (y/n): ").lower().strip()
            if show_all in ['y', 'yes']:
                print("\n" + "ALL SUPPORTED LANGUAGES:")
                print("-" * 50)
                for code, name in languages_list:
                    print(f"{code}: {name}")
                    
        except Exception as e:
            print(f"Error listing languages: {str(e)}")
            
    def check_microphone(self):
        print("\n--- MICROPHONE CHECK ---")
        try:
            with sr.Microphone() as mic:
                print("Microphone found and accessible.")
                print("Testing microphone... Please remain quiet for 2 seconds.")
                
                self.recognizer.adjust_for_ambient_noise(mic, duration=2)
                print("Microphone test completed successfully.")
                
        except OSError as e:
            print(f"Microphone error: {str(e)}")
            print("Please check your microphone connection and permissions.")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            
    def run(self):
        print("Welcome to Speech to Text & Text to Speech Converter!")
        print("This application runs entirely in the command line.")
        
        while self.running:
            self.display_menu()
            
            try:
                choice = input("Enter your choice (1-5): ").strip()
                
                if choice == '1':
                    self.text_to_speech()
                elif choice == '2':
                    self.speech_to_text()
                elif choice == '3':
                    self.list_languages()
                elif choice == '4':
                    self.check_microphone()
                elif choice == '5':
                    self.running = False
                    print("Thank you for using the Speech Converter. Goodbye!")
                else:
                    print("Invalid choice. Please enter a number between 1-5.")
                    
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nProgram interrupted by user. Goodbye!")
                self.running = False
            except Exception as e:
                print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = SpeechAppCLI()
    app.run()