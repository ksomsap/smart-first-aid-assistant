import difflib
import threading
import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import queue

# ----------------------------
# 1. Load first-aid knowledge
# ----------------------------
with open("data/first_aid.txt", "r", encoding="utf-8") as f:
    knowledge_data = f.read()

knowledge = {}
for section in knowledge_data.strip().split("\n\n"):
    lines = section.strip().split("\n")
    topic = lines[0].replace(":", "").strip().lower()
    content = "\n".join(lines[1:]).strip()
    knowledge[topic] = content

# ----------------------------
# 2. Load keywords
# ----------------------------
keywords = {}
with open("data/keywords.txt", "r", encoding="utf-8") as f:
    for line in f:
        if ":" in line:
            topic, key_str = line.strip().split(":", 1)
            keys = [k.strip() for k in key_str.split(",")]
            keywords[topic.strip()] = keys

# ----------------------------
# 3. Load small-talk
# ----------------------------
small_talk = {}
with open("data/small_talk.txt", "r", encoding="utf-8") as f:
    for line in f:
        if ":" in line:
            topic, response = line.strip().split(":", 1)
            small_talk[topic.strip().lower()] = response.strip()

# ----------------------------
# 4. Function to get response
# ----------------------------
def get_response(user_input):
    user_input = user_input.lower()

    # 1️⃣ Small talk
    for topic, response in small_talk.items():
        if topic in user_input:
            return response

    # 2️⃣ First-aid keyword match
    for topic, keys in keywords.items():
        for key in keys:
            if key in user_input:
                return knowledge.get(topic, "Instructions not found, call emergency services.")

    # 3️⃣ Fallback to closest topic
    closest = difflib.get_close_matches(user_input, knowledge.keys(), n=1, cutoff=0.4)
    if closest:
        return knowledge[closest[0]]

    # 4️⃣ Default
    return "Sorry, no instructions found. Call emergency services."

# ----------------------------
# 5. Initialize speech engine with queue
# ----------------------------
engine = pyttsx3.init()
engine.setProperty("rate", 150)
recognizer = sr.Recognizer()

# Create a queue for speech requests
speech_queue = queue.Queue()
is_speaking = False

def speech_worker():
    global is_speaking
    while True:
        text = speech_queue.get()
        if text is None:  # None is our signal to stop
            break
        is_speaking = True
        engine.say(text)
        engine.runAndWait()
        is_speaking = False
        speech_queue.task_done()

# Start the speech worker thread
speech_thread = threading.Thread(target=speech_worker, daemon=True)
speech_thread.start()

def speak(text: str):
    speech_queue.put(text)

# ----------------------------
# 6. GUI functions
# ----------------------------
def ask_question():
    user_input = entry.get()
    if not user_input.strip():
        return
    display_text(f"You: {user_input}")
    response = get_response(user_input)
    display_text(f"AI:\n{response}")
    speak(response)
    entry.delete(0, tk.END)

def voice_input():
    def _listen():
        mic_index = mic_var.get()
        try:
            with sr.Microphone(device_index=mic_index if mic_index else None) as source:
                display_text("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                user_input = recognizer.recognize_google(audio)
                display_text(f"You: {user_input}")
        except sr.UnknownValueError:
            display_text("Could not understand audio.")
            return
        except sr.RequestError:
            display_text("Speech recognition error.")
            return
        except Exception as e:
            display_text(f"Mic error: {e}")
            return

        response = get_response(user_input)
        display_text(f"AI:\n{response}")
        speak(response)

    threading.Thread(target=_listen, daemon=True).start()

def display_text(text):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, text + "\n\n")
    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)

# ----------------------------
# 7. Build GUI
# ----------------------------
root = tk.Tk()
root.title("Smart First-Aid Assistant")
root.geometry("650x500")

chat_box = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD)
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(padx=10, pady=(0,10), fill=tk.X)
entry.bind("<Return>", lambda e: ask_question())

button_frame = tk.Frame(root)
button_frame.pack(padx=10, pady=(0,10))

ask_button = tk.Button(button_frame, text="Ask", command=ask_question, width=12)
ask_button.pack(side=tk.LEFT, padx=5)

voice_button = tk.Button(button_frame, text="Speak", command=voice_input, width=12)
voice_button.pack(side=tk.LEFT, padx=5)

# ----------------------------
# 8. Microphone selection
# ----------------------------
mic_var = tk.IntVar(value=0)
mic_list = sr.Microphone.list_microphone_names()
if mic_list:
    mic_menu = tk.OptionMenu(button_frame, mic_var, *range(len(mic_list)))
    mic_menu.pack(side=tk.LEFT, padx=5)
    mic_label = tk.Label(button_frame, text="Mic Index")
    mic_label.pack(side=tk.LEFT)

# Clean up when closing the window
def on_closing():
    speech_queue.put(None)  # Signal the speech thread to stop
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()