# Morse Code Decoder — Streamlit App

<p align="center">
  👉 <a href="https://morsecode-decoder.streamlit.app/" target="_blank"><b>🌐 Live Demo: Morse Code Decoder</b></a> 👈
</p>

📡 A modern, advanced **Morse Code Encoder & Decoder** built with [Streamlit](https://streamlit.io/). This project converts **Text ↔ Morse Code**, plays audio beeps, and provides export options with a beautiful UI.

---

## 🚀 Features

- **Bidirectional Conversion**
  - Text → Morse
  - Morse → Text
- **Audio Playback** with configurable speed (WPM) and frequency (Hz).
- **Waveform Preview** of generated Morse code audio.
- **Copy & Download** results as text or audio (WAV).
- **History Panel** to track and reload previous conversions.
- **Advanced Options**:
  - Auto-detect input type (Text vs Morse).
  - Dark/Light theme toggle.
  - Preset examples (Hello World, SOS, etc).
  - Validation for unknown characters or invalid Morse patterns.
- **Polished UI** with custom CSS, cards, and responsive layout.

---

## 📂 Project Structure

```
├── morse_code_decoder.py   # Main Streamlit app
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
```

---

## ⚙️ Installation

### 1. Clone this repository
```bash
git clone https://github.com/your-username/morse-code-decoder.git
cd morse-code-decoder
```

### 2. Create and activate virtual environment (optional but recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the app with:
```bash
streamlit run morse_code_decoder.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📊 Examples

**Text → Morse**
```
Hello World
```
➡️ `.... . .-.. .-.. --- / .-- --- .-. .-.. -..`

**Morse → Text**
```
... --- ...
```
➡️ `SOS`

---

## 🛠️ Requirements

- Python 3.8+
- Streamlit
- Numpy
- Soundfile
- Matplotlib

(See `requirements.txt` for full list)

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to your fork (`git push origin feature-name`)
5. Create a Pull Request

---

## 📌 Roadmap

- [ ] Add keyboard shortcuts (e.g., Ctrl+Enter to convert)
- [ ] Animated visual dot/dash playback
- [ ] Deploy demo to Streamlit Cloud
- [ ] Add unit tests & CI workflow

---

## 🙌 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [International Morse Code Standard](https://en.wikipedia.org/wiki/Morse_code)
- Inspiration from HAM radio operators and signal processing enthusiasts.

---

Made with ❤️ using Python & Streamlit.
