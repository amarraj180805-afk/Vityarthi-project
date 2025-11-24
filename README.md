## 🗣️ Speech Converter CLI

-----

## 📝 Project Overview

The **Speech Converter CLI** is a robust command-line interface (CLI) application developed in **Python** that facilitates conversion between **text and speech**. It offers users a simple, menu-driven way to either turn written text into an audio file or transcribe spoken words into text.

The application implements multiple fallback mechanisms for Text-to-Speech (TTS) using libraries like `gTTS`, `pyttsx3`, and `edge-tts`, ensuring high availability and offering both online and offline conversion options. For Speech-to-Text (STT), it leverages Google's Speech Recognition service via the `speech_recognition` library.

-----

## ✨ Features

  * **Text to Speech (TTS):**
      * Converts user-input text into spoken audio.
      * Supports a wide range of languages.
      * **Multiple TTS Backends:** Attempts conversion using `gTTS` (online), falling back to `pyttsx3` (offline) and `edge-tts` (online) if the primary method fails.
      * Saves generated speech to an MP3 file (e.g., `output_speech_gtts.mp3`).
      * Includes an option to automatically play the saved audio file.
  * **Speech to Text (STT):**
      * Records audio from the user's microphone for a specified duration.
      * Transcribes the recorded speech using Google's Speech Recognition API.
      * Includes **ambient noise adjustment** for clearer transcription.
      * Option to save the recognized text to a file (e.g., `speech_output.txt`).
  * **Utility Functions:**
      * **List Supported Languages:** Displays all language codes available for TTS (via `gTTS`).
      * **Microphone Check:** Tests the availability and accessibility of the default microphone.
      * **Cross-Platform Audio Playback:** Attempts to play the generated audio on Windows, macOS, and common Linux distributions.

-----

## 🛠️ Technologies/Tools Used

| Technology | Purpose |
| :--- | :--- |
| **Python** | Primary programming language. |
| `speech_recognition` | Handles microphone input and interfaces with STT APIs (specifically Google Web Speech API). |
| `gTTS` | Google Text-to-Speech service interface (primary TTS backend). |
| `pyttsx3` | Offline cross-platform TTS library (fallback TTS backend). |
| `edge_tts` | Microsoft Edge TTS service interface (alternative online TTS backend). |
| `os`, `platform`, `subprocess` | System-level operations (file management, audio playback, OS detection). |
| `datetime` | Used for timestamping (though not heavily utilized, it is imported). |

-----

## 🚀 Steps to Install & Run the Project

### 1\. Prerequisites

  * **Python 3.x** installed on your system.
  * A working **Internet connection** is required for `gTTS`, `edge-tts`, and Google's STT service.
  * A functional **microphone** is required for the Speech-to-Text feature.

### 2\. Installation

First, clone the repository or save the provided Python code as a file (e.g., `speech_app.py`).

Next, install the required Python libraries. It's highly recommended to use a **virtual environment**.

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate   # On Windows

# Install the core libraries
pip install speechrecognition gtts

# Install fallback libraries (required for robust TTS)
pip install pyttsx3 edge-tts
```

### 3\. Run the Application

Execute the Python script from your terminal:

```bash
python speech_app.py
```

### 4\. Usage

The application will launch and present a menu. Follow the on-screen prompts to select an option and perform a conversion.

-----

## ✅ Instructions for Testing

Test each feature using the provided menu options:

### A. Test Text to Speech (Option 1)

1.  Select **`1`** (Text to Speech).
2.  Enter a test phrase, e.g., "**Hello, this is a test of the text to speech converter.**"
3.  Enter a language code, e.g., **`en`** for English or **`es`** for Spanish.
4.  **Expected Outcome:**
      * The console should show one of the TTS methods succeeding (`gTTS`, `pyttsx3`, or `edge-tts`).
      * An audio file (`.mp3`) should be created in the current directory.
      * If you select `y` to play the audio, you should hear the spoken phrase.

### B. Test Speech to Text (Option 2)

1.  Select **`2`** (Speech to Text).
2.  Enter a short duration (e.g., **`5`** seconds) and press Enter.
3.  Press Enter to start recording. **Speak clearly** into your microphone for the specified duration, e.g., "**The quick brown fox jumps over the lazy dog.**"
4.  **Expected Outcome:**
      * The console should display the recognized text.
      * If you choose to save, a text file should be created containing the transcribed text.

### C. Test List Supported Languages (Option 3)

1.  Select **`3`** (List Supported Languages).
2.  **Expected Outcome:** A list of common language codes and names is displayed, followed by an option to view all supported languages.

### D. Test Check Microphone (Option 4)

1.  Select **`4`** (Check Microphone).
2.  **Expected Outcome:**
      * If the microphone is working, it should display **"Microphone found and accessible"** followed by **"Microphone test completed successfully."**
      * If there is an issue, an appropriate error message will be displayed (e.g., `No default input device`).
