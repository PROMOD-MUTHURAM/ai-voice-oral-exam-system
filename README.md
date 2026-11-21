# AI-Based Voice Recognition Oral Examination System

An automated desktop oral examination prototype built with **Python, OpenAI Whisper, and Tkinter**. The system conducts voice-based student assessments by reading questions aloud, transcribing spoken answers in real time, and grading responses semantically.

## Key Features
- **Automated Voice Question Delivery:** Uses **Text-to-Speech (TTS)** to read exam questions aloud to candidates.
- **Real-Time Speech-to-Text Transcription:** Captures live microphone audio and transcribes spoken responses accurately using **OpenAI Whisper**.
- **Semantic Answer Evaluation:** Compares transcribed student responses against reference answers to automatically classify answers as **Correct**, **Partially Correct**, or **Wrong** with automated mark calculation.
- **Multi-Student Exam Sessions & Reports:** Supports consecutive student assessments and generates detailed result reports with total marks, percentages, **PASS/FAIL** status, transcript logs, and rank lists.
- **Desktop GUI:** Clean, interactive interface built with **Tkinter**.

## Tech Stack
- **Language:** Python
- **Speech Recognition:** OpenAI Whisper (Speech-to-Text)
- **Audio & TTS:** Python Text-to-Speech & Microphone Audio Capture libraries
- **Evaluation & Logic:** Semantic Text Similarity / NLP Evaluation
- **GUI Framework:** Tkinter

## Setup & Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd ai-voice-oral-exam-system
   ```
2. **Install required dependencies:**
   ```bash
   pip install openai-whisper torch pyttsx3 pyaudio SpeechRecognition
   ```
   *(Note: Ensure `ffmpeg` is installed and added to your system PATH for OpenAI Whisper audio processing.)*
3. **Run the application:**
   ```bash
   python main.py
   ```
   *(Replace `main.py` with the exact entry filename in this repository.)*

## Author
**Promod Muthuram R**  
- LinkedIn: [://linkedin.com](https://www.://linkedin.com/)  
- Email: promodmuthuram29@gmail.com
