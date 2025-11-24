# 🗣️ Speech to Text & Text to Speech Converter CLI Application

## 💡 Problem Statement

The need exists for a **simple, accessible, and multi-functional command-line interface (CLI) tool** that allows users to easily convert **text into audible speech (TTS)** and **spoken words into digital text (STT)**. Users require a robust solution that can handle different languages and provide fallback mechanisms for TTS if the primary online service (like gTTS) fails, while also offering essential utility functions like checking microphone status and listing supported languages. The primary challenge is ensuring reliability across different operating systems and handling potential network/hardware errors gracefully.

---

## 🎯 Scope of the Project

The scope of this project is to deliver a fully functional, self-contained **Python CLI application** that:

1.  **Implements Text-to-Speech (TTS) functionality** using primarily `gTTS`, with fallback options to other libraries like `pyttsx3` (offline) and `edge-tts` (online) for enhanced reliability.
2.  **Implements Speech-to-Text (STT) functionality** using the `speech_recognition` library (utilizing the Google Web Speech API).
3.  **Manages audio playback** across different operating systems (Windows, macOS, Linux) by calling system-specific or common audio player commands.
4.  **Provides a clear, interactive menu** for navigation and execution of features.
5.  **Handles basic user input validation** (e.g., recording duration, menu choices).
6.  **Includes utility features** for checking the microphone and listing supported TTS languages.

**Out of Scope:** Developing a Graphical User Interface (GUI), advanced voice customization (e.g., specific voice selection beyond language), real-time continuous transcription, or integration with commercial, paid STT/TTS APIs.

---

## 🧑‍💻 Target Users

The primary users for this CLI application are:

* **Developers and Programmers:** Those who prefer using the command line and need a quick way to test TTS or STT functionality in their environment without a heavy application.
* **Students and Educators:** Individuals needing tools for language learning, accessibility purposes, or simple audio-to-text transcription for notes.
* **CLI Enthusiasts:** Users who value lightweight, terminal-based utilities for daily tasks.
* **Users with Accessibility Needs:** Individuals who benefit from having text read aloud (TTS) or who find typing difficult and prefer to dictate text (STT).

---

## ✨ High-Level Features

| Feature Category | Description |
| :--- | :--- |
| **Text to Speech (TTS)** | Converts input text into an audio file (e.g., MP3) and offers to play it immediately. It includes multiple fallback mechanisms (`gTTS`, `pyttsx3`, `edge-tts`) to maximize success. |
| **Speech to Text (STT)** | Records audio from the user's default microphone for a specified duration, converts the speech to text using an online recognition service, and displays the result. |
| **Microphone Check** | Utility function to detect if a microphone is present and accessible, including a brief ambient noise calibration test. |
| **Language Support** | Allows the user to select the language for TTS conversion and provides an option to list all languages supported by the primary TTS engine (`gTTS`). |
| **Data Persistence** | Option to save the transcribed text output from the STT process into a local text file. |
| **Cross-Platform Compatibility** | Uses standard Python libraries and platform-aware commands for audio playback to ensure broad compatibility across Windows, macOS, and Linux. |
