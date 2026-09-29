import streamlit as st
import pyttsx3
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from datetime import datetime
import tempfile
import os
import io
import threading
import time
import json
import re

# ---------------------------------------------------------
# Page Configuration & Dark Mode CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Voice & Text Assistant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Dark Theme Styles
st.markdown(
    """
    <style>
    /* Global Background and Typography */
    .stApp {
        background: linear-gradient(145deg, #0B0F19 0%, #111827 50%, #0F172A 100%);
        color: #F1F5F9;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }

    /* Top Hero Header */
    .hero-container {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), 0 0 20px -5px rgba(99, 102, 241, 0.15);
    }
    
    .hero-title {
        font-size: 2.1rem;
        font-weight: 700;
        background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .hero-subtitle {
        color: #94A3B8;
        font-size: 0.98rem;
        margin-top: 8px;
        margin-bottom: 0;
    }

    /* Status Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        background: rgba(16, 185, 129, 0.12);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 10px #10B981;
        animation: pulse-glow 2s infinite ease-in-out;
    }

    @keyframes pulse-glow {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.85); }
    }

    /* Quick Action Chips */
    .quick-chip {
        display: inline-block;
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 6px 14px;
        color: #E2E8F0;
        font-size: 0.85rem;
        margin: 4px 2px;
        transition: all 0.2s ease;
    }

    /* Message Metadata Badges */
    .intent-tag {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 2px 10px;
        border-radius: 6px;
        background: rgba(99, 102, 241, 0.2);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.35);
        margin-left: 8px;
    }

    .time-tag {
        font-size: 0.72rem;
        color: #64748B;
        margin-left: auto;
    }

    /* NLP Tokenizer Pill in Expander */
    .token-pill {
        display: inline-block;
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 3px 8px;
        margin: 2px 3px;
        font-size: 0.78rem;
        font-family: monospace;
        color: #38BDF8;
    }

    /* Glassmorphism sidebar cards */
    .sidebar-card {
        background: rgba(19, 28, 46, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 14px;
    }

    .stat-number {
        font-size: 1.4rem;
        font-weight: 700;
        color: #818CF8;
    }

    .stat-label {
        font-size: 0.78rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Custom Streamlit adjustments */
    div[data-testid="stChatMessage"] {
        background-color: rgba(30, 41, 59, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        margin-bottom: 12px;
        padding: 12px 16px;
    }

    /* Audio widget styling */
    audio {
        width: 100%;
        height: 38px;
        border-radius: 8px;
        margin-top: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Ensure NLTK Resources are Downloaded
# ---------------------------------------------------------
@st.cache_resource(show_spinner=False)
def init_nltk():
    try:
        word_tokenize("test sentence")
    except Exception:
        import nltk
        nltk.download("punkt", quiet=True)
        nltk.download("punkt_tab", quiet=True)

init_nltk()

# ---------------------------------------------------------
# NLP Core & Intent Engine (matching bot.py)
# ---------------------------------------------------------
def process_command(user_text: str, last_response: str = "") -> dict:
    """
    NLP Tokenization and Intent processing based on bot.py rules.
    """
    clean_text = user_text.strip()
    if not clean_text:
        return {
            "response": "Please provide a command or question, boss!",
            "intent": "Empty Input",
            "tokens": [],
            "is_exit": False,
        }

    try:
        raw_tokens = word_tokenize(clean_text)
    except Exception:
        # Fallback to regex tokenizer if NLTK has any runtime glitch
        raw_tokens = re.findall(r"\b\w+\b", clean_text)

    # Lowercase tokens for uniform matching
    tokens = [t.lower() for t in raw_tokens]

    # 1. Greeting
    if any(t in tokens for t in ["hello", "hi", "hey"]):
        return {
            "response": "Hello boss! How can I help you?",
            "intent": "Greeting",
            "tokens": tokens,
            "is_exit": False,
        }

    # 2. Asking how bot is
    elif "how" in tokens and "you" in tokens:
        return {
            "response": "I am doing great boss. Thank you for asking!",
            "intent": "Status Check",
            "tokens": tokens,
            "is_exit": False,
        }

    # 3. Asking bot's name
    elif "name" in tokens:
        return {
            "response": "My name is your Python voice assistant.",
            "intent": "Identity",
            "tokens": tokens,
            "is_exit": False,
        }

    # 4. Asking current time
    elif "time" in tokens:
        current_time = datetime.now().strftime("%I:%M %p")
        return {
            "response": f"The current time is {current_time}",
            "intent": "Current Time",
            "tokens": tokens,
            "is_exit": False,
        }

    # 5. Asking about Python
    elif "python" in tokens:
        return {
            "response": "Python is a high level programming language.",
            "intent": "Knowledge: Python",
            "tokens": tokens,
            "is_exit": False,
        }

    # 6. Asking about AI (handles 'ai', 'artificial', 'intelligence')
    elif "ai" in tokens or "artificial" in tokens or "intelligence" in tokens:
        return {
            "response": "Artificial intelligence allows computers to perform tasks that normally require human intelligence.",
            "intent": "Knowledge: AI",
            "tokens": tokens,
            "is_exit": False,
        }

    # 7. Thank you
    elif "thank" in tokens or "thanks" in tokens:
        return {
            "response": "You're welcome boss!",
            "intent": "Gratitude",
            "tokens": tokens,
            "is_exit": False,
        }

    # 8. Asking for help
    elif "help" in tokens:
        return {
            "response": "Sure boss! Tell me what you need help with. You can ask for the time, date, about AI, Python, or just chat with me.",
            "intent": "Assistance",
            "tokens": tokens,
            "is_exit": False,
        }

    # 9. Asking assistant to repeat
    elif "repeat" in tokens:
        if last_response:
            rep_msg = f"Sure boss, repeating my last answer: \"{last_response}\""
        else:
            rep_msg = "Sure boss, I can repeat what you say."
        return {
            "response": rep_msg,
            "intent": "Echo/Repeat",
            "tokens": tokens,
            "is_exit": False,
        }

    # 10. Asking for current date
    elif "date" in tokens or "today" in tokens:
        current_date = datetime.now().strftime("%d %B %Y")
        return {
            "response": f"Today's date is {current_date}",
            "intent": "Current Date",
            "tokens": tokens,
            "is_exit": False,
        }

    # 11. Goodbye
    elif any(t in tokens for t in ["goodbye", "bye", "exit", "quit"]):
        return {
            "response": "Thank you so much boss, have a great day ahead!",
            "intent": "Farewell",
            "tokens": tokens,
            "is_exit": True,
        }

    # 12. Unknown command / Fallback
    else:
        return {
            "response": "Sorry boss, I don't understand that command yet. You can ask me for the time, today's date, what AI is, or what Python is!",
            "intent": "Unknown Command",
            "tokens": tokens,
            "is_exit": False,
        }

# ---------------------------------------------------------
# Text-to-Speech Engine
# ---------------------------------------------------------
def generate_tts_bytes(text: str, voice_idx: int = 0, rate: int = 160, volume: float = 1.0) -> bytes:
    """
    Synthesize speech using pyttsx3 into in-memory WAV audio bytes.
    """
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        if voice_idx < len(voices):
            engine.setProperty("voice", voices[voice_idx].id)
        engine.setProperty("rate", rate)
        engine.setProperty("volume", volume)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            temp_path = tmp_file.name

        engine.save_to_file(text, temp_path)
        engine.runAndWait()
        engine.stop()

        with open(temp_path, "rb") as f:
            audio_bytes = f.read()

        if os.path.exists(temp_path):
            os.remove(temp_path)

        return audio_bytes
    except Exception as e:
        print(f"TTS Error: {e}")
        return b""


def speak_desktop_async(text: str, voice_idx: int = 0, rate: int = 160, volume: float = 1.0):
    """
    Optional background speaker output directly to PC speakers.
    """
    def _speak():
        try:
            eng = pyttsx3.init()
            voices = eng.getProperty("voices")
            if voice_idx < len(voices):
                eng.setProperty("voice", voices[voice_idx].id)
            eng.setProperty("rate", rate)
            eng.setProperty("volume", volume)
            eng.say(text)
            eng.runAndWait()
            eng.stop()
        except Exception as e:
            print(f"Desktop TTS Error: {e}")

    threading.Thread(target=_speak, daemon=True).start()

# ---------------------------------------------------------
# Speech Recognition Engine
# ---------------------------------------------------------
def record_from_microphone(ambient_duration: float = 1.0, phrase_limit: int = 8, language: str = "en-US"):
    """
    Record directly from local PC microphone using SpeechRecognition (bot.py behavior).
    """
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.toast("🎙️ Calibrating for background noise...", icon="🎧")
            r.adjust_for_ambient_noise(source, duration=ambient_duration)
            st.toast("🗣️ Listening now! Please speak...", icon="🎙️")
            audio = r.listen(source, phrase_time_limit=phrase_limit)

        text = r.recognize_google(audio, language=language)
        return text, None
    except sr.UnknownValueError:
        return "", "Sorry boss, I could not understand what you said."
    except sr.RequestError as e:
        return "", f"Speech recognition service unavailable: {e}"
    except Exception as e:
        return "", f"Microphone error: {e}"


def transcribe_uploaded_audio(audio_file, language: str = "en-US"):
    """
    Transcribe audio recorded via browser st.audio_input.
    """
    r = sr.Recognizer()
    try:
        audio_bytes = audio_file.read()
        audio_io = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_io) as source:
            audio_data = r.record(source)
        text = r.recognize_google(audio_data, language=language)
        return text, None
    except sr.UnknownValueError:
        return "", "Sorry, could not understand the recorded audio."
    except sr.RequestError as e:
        return "", f"Speech recognition service error: {e}"
    except Exception as e:
        return "", f"Transcription error: {e}"

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello boss! I am your Python Voice & Text Assistant. Speak to me or type a message below!",
            "intent": "Welcome",
            "tokens": ["hello", "boss"],
            "timestamp": datetime.now().strftime("%I:%M %p"),
            "audio_bytes": None,
        }
    ]

if "last_bot_reply" not in st.session_state:
    st.session_state.last_bot_reply = "Hello boss! How can I help you?"

if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

if "voice_turns" not in st.session_state:
    st.session_state.voice_turns = 0

# ---------------------------------------------------------
# Sidebar Configuration & Controls
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; padding: 10px 0 16px 0;">
            <div style="font-size: 2.8rem; line-height: 1;">🎙️</div>
            <h2 style="margin: 8px 0 2px 0; font-size: 1.35rem; color: #F8FAFC;">Assistant Hub</h2>
            <div class="status-badge">
                <span class="status-dot"></span>
                <span>SYSTEM ONLINE</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🔊 Text-to-Speech (TTS)")
    tts_enabled = st.toggle("Enable Voice Output", value=True, help="Toggle AI voice response playback")
    autoplay_audio = st.toggle("Autoplay Audio", value=True, help="Automatically play spoken responses upon generation")

    # Get available system voices safely
    voice_options = ["Microsoft David (Male)", "Microsoft Zira (Female)"]
    selected_voice_idx = st.selectbox(
        "Voice Persona",
        options=range(len(voice_options)),
        format_func=lambda i: voice_options[i] if i < len(voice_options) else f"Voice {i}",
        index=0,
    )

    col_rate, col_vol = st.columns(2)
    with col_rate:
        speech_rate = st.slider("Speed (WPM)", min_value=110, max_value=230, value=160, step=10)
    with col_vol:
        speech_vol = st.slider("Volume", min_value=0.1, max_value=1.0, value=1.0, step=0.1)

    desktop_speaker = st.checkbox(
        "📢 Play on PC Speakers (pyttsx3)",
        value=False,
        help="In addition to in-browser player, also play sound directly on computer hardware speakers.",
    )

    st.divider()

    st.markdown("### 🎙️ Speech Recognition (STT)")
    stt_lang = st.selectbox(
        "Spoken Language",
        options=["en-US", "en-IN", "en-GB"],
        index=0,
    )
    ambient_duration = st.slider(
        "Ambient Calibration (sec)",
        min_value=0.5,
        max_value=2.0,
        value=1.0,
        step=0.25,
        help="Seconds spent calibrating microphone for background noise",
    )

    st.divider()

    # Session Stats Card
    st.markdown("### 📊 Session Analytics")
    st.markdown(
        f"""
        <div class="sidebar-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div>
                    <div class="stat-number">{len(st.session_state.messages)}</div>
                    <div class="stat-label">Total Messages</div>
                </div>
                <div>
                    <div class="stat-number">{st.session_state.voice_turns}</div>
                    <div class="stat-label">Voice Inputs</div>
                </div>
                <div>
                    <div class="stat-number">{st.session_state.total_tokens}</div>
                    <div class="stat-label">Tokens Parsed</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Chat cleared boss! How can I help you today?",
                    "intent": "Reset",
                    "tokens": ["chat", "cleared"],
                    "timestamp": datetime.now().strftime("%I:%M %p"),
                    "audio_bytes": None,
                }
            ]
            st.session_state.total_tokens = 0
            st.session_state.voice_turns = 0
            st.rerun()

    with col_btn2:
        # Download conversation transcript
        chat_text = "\n".join(
            [f"[{m.get('timestamp','')}] {m['role'].upper()}: {m['content']}" for m in st.session_state.messages]
        )
        st.download_button(
            label="💾 Export",
            data=chat_text,
            file_name=f"voice_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    # Command Cheat-Sheet
    with st.expander("📖 Available Commands"):
        st.markdown(
            """
            - **Greeting:** `"Hello"`, `"Hi"`, `"Hey"`
            - **Status:** `"How are you?"`
            - **Identity:** `"What is your name?"`
            - **Time:** `"What time is it?"`
            - **Date:** `"What is today's date?"`
            - **Python Info:** `"Tell me about Python"`
            - **AI Info:** `"What is AI?"` or `"Artificial Intelligence"`
            - **Gratitude:** `"Thank you"`, `"Thanks"`
            - **Assistance:** `"Help"`
            - **Echo:** `"Repeat"`
            - **Exit:** `"Goodbye"`, `"Bye"`, `"Exit"`
            """
        )

# ---------------------------------------------------------
# Main Page Hero Header
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero-container">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
            <div>
                <h1 class="hero-title">🎙️ Python Voice & Text Assistant</h1>
                <p class="hero-subtitle">
                    Intelligent voice chatbot powered by <strong>NLTK Tokenization</strong>, 
                    <strong>Google Speech-to-Text</strong>, and <strong>Pyttsx3 TTS</strong>
                </p>
            </div>
            <div>
                <span class="status-badge">
                    <span class="status-dot"></span>
                    <span>NLP Engine Active</span>
                </span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Quick Action Buttons
# ---------------------------------------------------------
st.markdown("<p style='font-size: 0.88rem; color: #94A3B8; margin-bottom: 8px;'>⚡ <strong>Quick Voice / Text Prompts:</strong></p>", unsafe_allow_html=True)
q_cols = st.columns(7)
quick_queries = [
    ("👋 Hello", "Hello boss!"),
    ("⏰ Time", "What is the current time?"),
    ("📅 Date", "What is today's date?"),
    ("🧠 AI", "What is Artificial Intelligence?"),
    ("🐍 Python", "Tell me about Python"),
    ("😊 Status", "How are you?"),
    ("🆘 Help", "Can you help me?"),
]

triggered_prompt = None
for i, (label, prompt_val) in enumerate(quick_queries):
    with q_cols[i]:
        if st.button(label, key=f"quick_{i}", use_container_width=True):
            triggered_prompt = prompt_val

# ---------------------------------------------------------
# Voice Microphone Bar (Hardware Mic & Browser Audio Input)
# ---------------------------------------------------------
mic_col1, mic_col2 = st.columns([1, 1])

with mic_col1:
    listen_btn = st.button(
        "🎤 Click to Speak (PC Microphone)",
        type="primary",
        use_container_width=True,
        help="Listens to your local PC microphone using speech_recognition",
    )

with mic_col2:
    with st.popover("🎙️ Browser Audio Recorder", use_container_width=True):
        st.markdown("<small style='color: #94A3B8;'>Record voice directly inside your web browser:</small>", unsafe_allow_html=True)
        recorded_audio = st.audio_input("Record audio", key="browser_mic")

# Handle Browser Audio Recording if provided
if recorded_audio is not None and "last_processed_audio" != recorded_audio.name:
    with st.spinner("🎧 Transcribing recorded audio..."):
        text_result, err = transcribe_uploaded_audio(recorded_audio, language=stt_lang)
        if err:
            st.error(f"❌ {err}")
        elif text_result:
            triggered_prompt = text_result
            st.session_state.voice_turns += 1

# Handle PC Microphone button
if listen_btn:
    with st.spinner("🎧 Listening to your PC microphone... Speak now!"):
        voice_text, err = record_from_microphone(
            ambient_duration=ambient_duration,
            language=stt_lang,
        )
        if err:
            st.warning(f"⚠️ {err}")
        elif voice_text:
            triggered_prompt = voice_text
            st.session_state.voice_turns += 1

# ---------------------------------------------------------
# Chat Execution Function
# ---------------------------------------------------------
def handle_chat_submission(user_input: str):
    timestamp_str = datetime.now().strftime("%I:%M %p")

    # 1. Append user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp_str,
    })

    # 2. Process through NLP & Intent Engine
    analysis = process_command(user_input, last_response=st.session_state.last_bot_reply)
    bot_reply = analysis["response"]
    st.session_state.last_bot_reply = bot_reply
    st.session_state.total_tokens += len(analysis["tokens"])

    # 3. Generate Speech (TTS)
    audio_data = None
    if tts_enabled:
        with st.spinner("🔊 Generating voice output..."):
            audio_data = generate_tts_bytes(
                bot_reply,
                voice_idx=selected_voice_idx,
                rate=speech_rate,
                volume=speech_vol,
            )

        if desktop_speaker:
            speak_desktop_async(
                bot_reply,
                voice_idx=selected_voice_idx,
                rate=speech_rate,
                volume=speech_vol,
            )

    # 4. Append assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply,
        "intent": analysis["intent"],
        "tokens": analysis["tokens"],
        "timestamp": datetime.now().strftime("%I:%M %p"),
        "audio_bytes": audio_data,
        "autoplay": autoplay_audio if audio_data else False,
    })

    if analysis.get("is_exit"):
        st.toast("👋 Session completed! Assistant bid farewell.", icon="👋")

# If a prompt was triggered via Quick Chips, Mic, or Audio Input
if triggered_prompt:
    handle_chat_submission(triggered_prompt)
    st.rerun()

# ---------------------------------------------------------
# Chat History Display
# ---------------------------------------------------------
chat_box = st.container()

with chat_box:
    for idx, msg in enumerate(st.session_state.messages):
        role = msg["role"]
        is_assistant = role == "assistant"
        avatar = "🤖" if is_assistant else "🧑‍💻"

        with st.chat_message(role, avatar=avatar):
            # Message Header with timestamp and intent
            header_html = f"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                <span style="font-weight: 600; color: {'#A5B4FC' if is_assistant else '#60A5FA'}; font-size: 0.9rem;">
                    {'AI Voice Assistant' if is_assistant else 'You'}
                </span>
                <span style="display: flex; align-items: center;">
                    {f'<span class="intent-tag">{msg.get("intent", "NLP")}</span>' if is_assistant and "intent" in msg else ''}
                    <span class="time-tag" style="margin-left: 10px;">{msg.get("timestamp", "")}</span>
                </span>
            </div>
            """
            st.markdown(header_html, unsafe_allow_html=True)

            # Message Content
            st.markdown(f"<div style='font-size: 1.02rem; line-height: 1.5; color: #F1F5F9;'>{msg['content']}</div>", unsafe_allow_html=True)

            # Audio Player for Voice Output
            if is_assistant and msg.get("audio_bytes"):
                # Play audio automatically only for the latest message if autoplay is on
                is_latest = (idx == len(st.session_state.messages) - 1)
                should_auto = is_latest and msg.get("autoplay", False)
                st.audio(msg["audio_bytes"], format="audio/wav", autoplay=should_auto)

            # Token Breakdown / NLP Inspection
            if is_assistant and msg.get("tokens"):
                with st.expander("🔍 NLP & Token Analysis", expanded=False):
                    tokens_html = "".join([f'<span class="token-pill">{t}</span>' for t in msg["tokens"]])
                    st.markdown(
                        f"""
                        <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 4px;">
                            <strong>Intent Matched:</strong> <code>{msg.get('intent', 'N/A')}</code><br/>
                            <div style="margin-top: 6px;">
                                <strong>Extracted Tokens ({len(msg['tokens'])}):</strong><br/>
                                <div style="margin-top: 4px;">{tokens_html}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

# ---------------------------------------------------------
# Chat Text Input
# ---------------------------------------------------------
if chat_prompt := st.chat_input("Type your command here (or use the microphone above)..."):
    handle_chat_submission(chat_prompt)
    st.rerun()
