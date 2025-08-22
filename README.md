# Smart First-Aid Assistant (Offline)



**Smart First-Aid Assistant** is an **offline AI-powered first-aid assistant** with voice and GUI support. It helps users get quick instructions for emergencies like bleeding, burns, fractures, and more — all without an internet connection.

---

## Features

- ✅ **Offline first-aid guidance** based on preloaded knowledge.  
- ✅ **Voice input and output** using your microphone and text-to-speech.  
- ✅ **GUI interface** built with Tkinter for easy use.  
- ✅ **Keyword and small-talk handling** to understand common phrases.  
- ✅ **Safe and fast**, no personal data is sent online.  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/smart-first-aid.git
cd smart-first-aid
```

2. Create and activate a virtual environment:
```bash
python -m venv env
# Windows
.\env\Scripts\activate
# macOS / Linux
source env/bin/activate
```
3. Install dependencies:

```bash
pip install -r requirements.txt
```
4. Make sure you have a microphone set up for voice input.

### Usage
Run the application:

```bash
python offline_agent.py
```
- Text Input: Type your question in the input box and press Enter or click Ask.
- Voice Input: Click Speak and talk to the AI.
- Mic Selection: Choose the correct microphone index if multiple devices are available.
---
### Example Questions
- “What should I do if someone is bleeding?”
- “How to treat burns?”
- “If someone is having a seizure?”
- Greetings: “Hello”, “Hi”, “Who are you?”

The AI will read instructions aloud and display them in the chat window.

---

### Project Structure
```graphql
smart-first-aid/
│
├─ data/
│   ├─ first_aid.txt       # First-aid instructions
│   ├─ keywords.txt        # Keywords mapping
│   └─ small_talk.txt      # Small talk responses
│
├─ offline_agent.py        # Main Python GUI and logic
├─ requirements.txt        # Python dependencies
├─ README.md
└─ .gitignore
```
### Dependencies
- Python 3.10+
- tkinter – GUI
- speechrecognition – Voice input
- pyttsx3 – Offline text-to-speech
- difflib – String similarity for keyword matching

Install dependencies via:

```bash
pip install -r requirements.txt
```
### Contribution
Contributions are welcome!
- Fork the repository.
- Create a new branch: git checkout -b feature/my-feature.
- Commit your changes: git commit -m "Add feature".
- Push to the branch: git push origin feature/my-feature.
- Open a pull request.

---

### License
This project is licensed under the MIT License – see the LICENSE file for details.

---

### Notes
- Works fully offline; no internet connection is required.
- Voice output is powered by your system’s TTS engine.
- Ensure your microphone is functioning for voice input.

Made with ❤️ by KSOMSAP

---