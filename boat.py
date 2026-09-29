import pyttsx3
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from datetime import datetime

r = sr.Recognizer()


def recognize_speech():
    with sr.Microphone() as s:
        print("Listening...")

        # Reduce background noise
        r.adjust_for_ambient_noise(s, duration=1)

        audio = r.listen(s)

        try:
            text = r.recognize_google(audio)
            print("You said:", text)
            return text.lower()

        except sr.UnknownValueError:
            print("Sorry, I could not understand.")
            return ""

        except sr.RequestError:
            print("Speech recognition service is unavailable.")
            return ""


def speak(text):
    engine = pyttsx3.init()

    print("Bot:", text)

    engine.say(text)
    engine.runAndWait()

    engine.stop()


while True:

    user = recognize_speech()

    if user == "":
        continue

    token = word_tokenize(user)

    # 1. Greeting
    if "hello" in token or "hi" in token or "hey" in token:
        speak("Hello boss! How can I help you?")

    # 2. Asking how bot is
    elif "how" in token and "you" in token:
        speak("I am doing great boss. Thank you for asking!")

    # 3. Asking bot's name
    elif "name" in token:
        speak("My name is your Python voice assistant.")

    # 4. Asking current time
    elif "time" in token:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    # 5. Asking about Python
    elif "python" in token:
        speak("Python is a high level programming language.")

    # 6. Asking about AI
    elif "AI" in token or "artificial" in token:
        speak("Artificial intelligence allows computers to perform tasks that normally require human intelligence.")

    # 7. Thank you
    elif "thank" in token or "thanks" in token:
        speak("You're welcome boss!")

    # 8. Asking for help
    elif "help" in token:
        speak("Sure boss! Tell me what you need help with.")

    # 9. Asking assistant to repeat
    elif "repeat" in token:
        speak("Sure boss, I can repeat what you say.")

    # 10. Asking for current date
    elif "date" in token:
        current_date = datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {current_date}")

    # 11. Goodbye
    elif "goodbye" in token or "bye" in token or "exit" in token:
        speak("Thank you so much boss, have a great day ahead!")
        break

    # 12. Unknown command
    else:
        speak("Sorry boss, I don't understand that command yet.")