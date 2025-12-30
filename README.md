# 🗣️ AI Pronunciation Coach (US Accent)

An interactive, AI-powered speech assessment tool built with Python and Streamlit. This application allows users to practice English sentences, receive a standard US accent reference, and get granular, phonetic-level feedback on their pronunciation using deep learning.

---

## 🚀 Features

* **US Accent Reference:** Generates high-quality American English audio for any input sentence using `gTTS`.
* **AI Transcription:** Utilizes **OpenAI's Whisper (Base)** model to accurately transcribe user speech while ignoring background noise.
* **Phonetic Analysis:** Converts both target and user speech into **IPA (International Phonetic Alphabet)** for scientific comparison.
* **Visual Feedback:** Highlights specific phonetic mistakes in **red** using string-alignment algorithms.
* **Dynamic UI:** Custom dark-themed interface for maximum readability of phonetic symbols.

---

## 🛠️ Technical Stack

* **Speech-to-Text:** [OpenAI Whisper](https://github.com/openai/whisper)
* **NLP & Phonetics:** `eng-to-ipa`
* **Audio Processing:** `FFmpeg`, `gTTS`
* **Frontend:** `Streamlit`
* **Algorithm:** `difflib.SequenceMatcher` (Ratcliff/Obershelp algorithm) for phonetic alignment.

---

## 🔍 How It Works

This project solves the challenge of **Phonetic Alignment**. Most speech-to-text tools only tell you *what* you said. This coach tells you *how* you said it.



1.  **Normalization:** Input text is sanitized to remove punctuation that affects phonetic mapping.
2.  **Inference:** The Whisper model processes the user's audio signal into a text string.
3.  **Grapheme-to-Phoneme (G2P):** Both strings are mapped to IPA symbols (e.g., "fox" → `fɑks`).
4.  **Diffing:** A comparison algorithm identifies deletions, insertions, or replacements in the phoneme sequence and injects HTML styling for real-time visual feedback.

---

## 🚀 Live Demo
Try the app right now! No installation needed.

🔗 **Live Version:** [https://ai-pronunciation-coach-9iqr7mscarp2fxrdsfx5ue.streamlit.app](https://ai-pronunciation-coach-9iqr7mscarp2fxrdsfx5ue.streamlit.app)

(Hosted for free on Streamlit Community Cloud)

---

## 📦 Installation & Setup

1. ### Install FFmpeg (Required)
  This tool requires FFmpeg to handle audio files.
  * **Mac:** `brew install ffmpeg`
  * **Windows:** Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), add the `bin` folder to your System PATH.

2. ### Clone and Setup Environment
    ```bash
    git clone https://github.com/DYPG68/ai-pronunciation-coach.git
    cd ai-pronunciation-coach
    python -m venv venv
    venv\Scripts\activate # Windows
    source venv/bin/activate # Mac/Linux
    ```
3. ### Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    (Alternatively: pip install streamlit openai-whisper gtts eng-to-ipa)

3.  ### Launch the app:
    ```bash
    streamlit run app.py
    ```
---

## 📄 License
Distributed under the MIT License. See [LICENSE](https://github.com/DYPG68/ai-pronunciation-coach/blob/main/LICENSE) for details.

