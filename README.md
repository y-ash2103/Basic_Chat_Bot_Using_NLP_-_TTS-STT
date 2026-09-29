# 🎙️ Python Voice Assistant

A simple **Python-based Voice Assistant** that listens to your voice, converts speech into text, processes the command using NLP tokenization, and responds using **Text-to-Speech (TTS)**.

This project is designed as a beginner-friendly introduction to combining **Speech Recognition, NLP, Text-to-Speech, and Python automation**.

---

## 📌 Project Overview

The **Python Voice Assistant** continuously listens to the user's voice through a microphone and performs actions based on recognized commands.

The assistant can:

* 👋 Respond to greetings
* 😊 Tell you how it is doing
* 🤖 Tell you its name
* 🕐 Tell the current time
* 📅 Tell today's date
* 🐍 Explain Python
* 🧠 Explain Artificial Intelligence
* 🙏 Respond to thank-you messages
* 🆘 Provide help
* 🔁 Handle repeat requests
* 👋 Exit when requested

The project uses **Google Speech Recognition** to convert speech into text and **pyttsx3** to convert the assistant's responses back into speech.

---

## 🧠 How It Works

The complete workflow is:

```text
             🎤 Microphone
                   │
                   ▼
          Speech Recognition
                   │
                   ▼
             Speech → Text
                   │
                   ▼
            NLTK Tokenization
                   │
                   ▼
          Command Identification
                   │
          ┌────────┴────────┐
          │                 │
       Known Command     Unknown Command
          │                 │
          ▼                 ▼
      Generate Reply    Error Response
          │
          ▼
       Text → Speech
          │
          ▼
          🔊 Speaker
```

---

# 🛠️ Technologies Used

| Technology           | Purpose                    |
| -------------------- | -------------------------- |
| 🐍 Python            | Core programming language  |
| 🎤 SpeechRecognition | Converts speech into text  |
| 🔊 pyttsx3           | Converts text into speech  |
| 🧠 NLTK              | Tokenization and basic NLP |
| 🎙️ PyAudio          | Microphone/audio input     |
| 🕐 datetime          | Current date and time      |

---

# 📂 Project Structure

A recommended project structure:

```text
Python-Voice-Assistant/
│
├── .venv/
│
├── main.py
│
├── requirements.txt
│
├── README.md
│
└── .gitignore
```

### File Description

| File               | Description                  |
| ------------------ | ---------------------------- |
| `main.py`          | Main voice assistant program |
| `requirements.txt` | Required Python packages     |
| `README.md`        | Project documentation        |
| `.gitignore`       | Files excluded from GitHub   |
| `.venv/`           | Python virtual environment   |

> ⚠️ Do not upload `.venv/` to GitHub.

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Python-Voice-Assistant.git
```

Move into the project directory:

```bash
cd Python-Voice-Assistant
```

---

## 2️⃣ Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

---

# 📦 Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

---

# 🧠 Download NLTK Resources

The project uses NLTK's `word_tokenize()`.

Run Python and download the required tokenizer resources:

```python
import nltk

nltk.download("punkt")
nltk.download("punkt_tab")
```

Depending on your NLTK version, `punkt_tab` may be required.

---

# 🎤 Microphone Setup

Your computer needs a working microphone.

You can check whether Python can detect your microphone with:

```python
import speech_recognition as sr

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(index, name)
```

If your microphone is not detected, check:

* Windows microphone permissions
* Default input device
* Microphone drivers
* PyAudio installation

---

# ▶️ Running the Project

Start the assistant with:

```bash
python main.py
```

You should see:

```text
Listening...
```

Speak into your microphone.

For example:

```text
You: Hello
Bot: Hello boss! How can I help you?
```

---

# 💬 Supported Commands

The assistant currently supports the following types of commands.

### 👋 Greeting

You can say:

```text
Hello
Hi
Hey
```

Response:

```text
Hello boss! How can I help you?
```

---

### 😊 How Are You?

You can say:

```text
How are you?
```

Response:

```text
I am doing great boss. Thank you for asking!
```

---

### 🤖 Assistant Name

You can say:

```text
What is your name?
```

Response:

```text
My name is your Python voice assistant.
```

---

### 🕐 Current Time

You can say:

```text
What is the time?
```

The assistant uses Python's `datetime` module to retrieve the current system time.

Example:

```text
The current time is 07:30 PM
```

---

### 📅 Current Date

You can say:

```text
What is today's date?
```

Example:

```text
Today's date is 29 September 2026
```

---

### 🐍 Python

You can ask:

```text
What is Python?
```

Response:

```text
Python is a high level programming language.
```

---

### 🧠 Artificial Intelligence

You can say:

```text
What is AI?
```

Response:

```text
Artificial intelligence allows computers to perform
tasks that normally require human intelligence.
```

---

### 🙏 Thank You

You can say:

```text
Thank you
Thanks
```

Response:

```text
You're welcome boss!
```

---

### 🆘 Help

You can say:

```text
Help me
I need help
```

Response:

```text
Sure boss! Tell me what you need help with.
```

---

### 🔁 Repeat

You can say:

```text
Repeat
```

Response:

```text
Sure boss, I can repeat what you say.
```

---

### 👋 Exit

You can say:

```text
Bye
Goodbye
Exit
```

Response:

```text
Thank you so much boss, have a great day ahead!
```

The program then terminates.

---

# 🔍 Code Explanation

## 1. Import Libraries

```python
import pyttsx3
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from datetime import datetime
```

These libraries provide the main functionality:

* `pyttsx3` → Text-to-Speech
* `speech_recognition` → Speech-to-Text
* `word_tokenize` → NLP tokenization
* `datetime` → Date and time

---

# 🎤 Speech Recognition

The `recognize_speech()` function listens to the microphone.

```python
r = sr.Recognizer()
```

A `Recognizer` object processes the incoming audio.

The microphone is accessed using:

```python
with sr.Microphone() as s:
```

---

## 🌊 Background Noise Reduction

Before listening, the program adjusts itself to the surrounding environment:

```python
r.adjust_for_ambient_noise(s, duration=1)
```

This helps improve recognition when there is background noise.

---

## 🎧 Listening

```python
audio = r.listen(s)
```

The microphone captures the user's speech.

---

## 🔄 Speech → Text

```python
text = r.recognize_google(audio)
```

Google's speech recognition service is used to convert the captured audio into text.

For example:

```text
🎤 "What is the time?"

        ↓

"What is the time?"
```

---

# 🧠 NLP Tokenization

After speech is converted into text:

```python
token = word_tokenize(user)
```

For example:

```text
"What is the current time?"
```

can become:

```python
["what", "is", "the", "current", "time", "?"]
```

The program then checks whether important keywords are present.

For example:

```python
elif "time" in token:
```

If `"time"` exists, the assistant knows that the user is asking about the current time.

---

# 🔊 Text-to-Speech

The `speak()` function converts text into audio.

```python
def speak(text):
    engine = pyttsx3.init()

    print("Bot:", text)

    engine.say(text)
    engine.runAndWait()

    engine.stop()
```

The process is:

```text
Text
 ↓
pyttsx3
 ↓
System Speech Engine
 ↓
🔊 Voice Output
```

---

# 🧩 Command Processing

The assistant uses conditional statements to determine what the user wants.

Example:

```python
if "hello" in token or "hi" in token or "hey" in token:
    speak("Hello boss! How can I help you?")
```

Another example:

```python
elif "time" in token:
    current_time = datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")
```

This is a basic **rule-based NLP system**.

---

# 🔄 Continuous Conversation

The assistant runs inside:

```python
while True:
```

This creates a continuous loop:

```text
Listen
  ↓
Understand
  ↓
Process
  ↓
Respond
  ↓
Listen Again
  ↓
...
```

The loop stops when the user says:

```text
bye
goodbye
exit
```

because the program executes:

```python
break
```

---

# ⚠️ Error Handling

The project handles two important speech recognition errors.

### Cannot Understand Speech

```python
except sr.UnknownValueError:
```

This happens when the speech recognition system cannot understand the audio.

The assistant responds:

```text
Sorry, I could not understand.
```

### Internet / Recognition Service Error

```python
except sr.RequestError:
```

This handles problems connecting to the speech recognition service.

The assistant responds:

```text
Speech recognition service is unavailable.
```

---

# 🔐 Important Note

`recognize_google()` generally requires an internet connection because the audio is processed through Google's speech recognition service.

For completely offline speech recognition, you can later replace it with an offline engine such as:

* Vosk
* Whisper
* Faster-Whisper
* Piper + another STT engine

---

# 🚀 Future Improvements

This project can be expanded significantly.

### 🔹 Level 1 — Better NLP

Replace simple keyword matching with:

* Intent classification
* Lemmatization
* Stopword removal
* Named Entity Recognition
* Sentence similarity

---

### 🔹 Level 2 — More Commands

Add commands for:

```text
Open Chrome
Open VS Code
Search Google
Play music
Open YouTube
Calculate something
Set a reminder
Tell a joke
```

---

### 🔹 Level 3 — AI Integration

Integrate an LLM such as:

* Gemini
* OpenAI
* Local LLMs

Then unknown commands can be sent to an AI model.

For example:

```text
User
 ↓
Speech-to-Text
 ↓
Intent Detection
 ↓
┌─────────────────┐
│ Known Command?  │
└────────┬────────┘
         │
    Yes  │  No
         │
         ▼
      Command       LLM
         │            │
         └─────┬──────┘
               ▼
          Text Response
               │
               ▼
              TTS
```

---

# 🤖 Future Agentic AI Version

The project can eventually evolve from a simple voice assistant into an **Agentic AI Assistant**.

Possible architecture:

```text
                 🎤 Voice
                    │
                    ▼
              Speech-to-Text
                    │
                    ▼
              🧠 AI Agent
                    │
          ┌─────────┼─────────┐
          │         │         │
          ▼         ▼         ▼
       Search     Python    Computer
        Tool       Tool      Control
          │         │         │
          └─────────┼─────────┘
                    ▼
                AI Reasoning
                    │
                    ▼
                Text-to-Speech
                    │
                    ▼
                   🔊
```

This could turn the project into a much larger **AI/ML + NLP + Generative AI + Voice Assistant** portfolio project.

---

# 📈 Learning Outcomes

By building this project, you learn:

* Python functions
* Loops and conditionals
* Exception handling
* Speech Recognition
* Text-to-Speech
* NLP tokenization
* API-based speech processing
* Microphone/audio handling
* Date and time processing
* Basic conversational AI architecture

---

# 🧪 Example Interaction

```text
Listening...

You said: hello
Bot: Hello boss! How can I help you?

Listening...

You said: what is python
Bot: Python is a high level programming language.

Listening...

You said: what is the time
Bot: The current time is 07:30 PM

Listening...

You said: thank you
Bot: You're welcome boss!

Listening...

You said: goodbye
Bot: Thank you so much boss, have a great day ahead!
```

---

# ⭐ Project Highlights

```text
🎙️ Voice Input
       ↓
📝 Speech-to-Text
       ↓
🧠 NLP Tokenization
       ↓
⚙️ Rule-Based Intent Detection
       ↓
💬 Response Generation
       ↓
🔊 Text-to-Speech
```

This project provides a foundation for building more advanced **AI-powered voice assistants and Agentic AI systems**.

---

# 👨‍💻 Author

**Yash**

Built with ❤️ using Python, NLP and Speech Technologies.

---

# 📄 License

This project is open-source and available for educational and personal use.
