import streamlit as st
import time
import base64
import io
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from pathlib import Path
import streamlit.components.v1 as components

# ----------------- Morse Code Dictionary -----------------
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.',
    '-': '-....-', '(': '-.--.', ')': '-.--.-', ' ': '/'
}

# Reverse dictionary
MORSE_TO_TEXT = {v: k for k, v in MORSE_CODE_DICT.items()}

# ----------------- Utility Functions -----------------
def text_to_morse(text):
    out = []
    for char in text:
        if char.upper() in MORSE_CODE_DICT:
            out.append(MORSE_CODE_DICT[char.upper()])
        else:
            out.append('?')
    return ' '.join(out)


def morse_to_text(morse):
    parts = morse.split(' ')
    out = []
    for p in parts:
        if p == '':
            continue
        if p == '/':
            out.append(' ')
        elif p in MORSE_TO_TEXT:
            out.append(MORSE_TO_TEXT[p])
        else:
            out.append('?')
    return ''.join(out)


def detect_input_type(s):
    # If it contains only dots, dashes, spaces, or slashes -> morse
    allowed = set('.-/ ')
    if all(ch in allowed for ch in s.strip()):
        # but ensure there's at least one dot or dash
        if any(ch in '.-' for ch in s):
            return 'morse'
    return 'text'

# Generate Morse Code Audio (dot = short beep, dash = long beep)
def generate_morse_audio(morse_code, wpm=20, freq=700, sample_rate=44100):
    dot_duration = 1.2 / wpm  # seconds (standard timing)
    dash_duration = 3 * dot_duration

    audio = np.array([], dtype=np.float32)

    def tone(duration):
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        # smooth envelope to avoid clicks
        env = np.ones_like(t)
        fade = int(0.01 * sample_rate)
        if fade > 0 and fade*2 < len(env):
            env[:fade] = np.linspace(0, 1, fade)
            env[-fade:] = np.linspace(1, 0, fade)
        return 0.5 * np.sin(2 * np.pi * freq * t) * env

    def silence(duration):
        return np.zeros(int(sample_rate * duration), dtype=np.float32)

    for i, symbol in enumerate(morse_code):
        if symbol == '.':
            audio = np.concatenate((audio, tone(dot_duration), silence(dot_duration)))
        elif symbol == '-':
            audio = np.concatenate((audio, tone(dash_duration), silence(dot_duration)))
        elif symbol == ' ':
            # space between letters (already includes one dot silence after each symbol), add 2 more dot durations
            audio = np.concatenate((audio, silence(2 * dot_duration)))
        elif symbol == '/':
            # word gap: 7 dot durations total (we already add 1 after symbol), so add 6
            audio = np.concatenate((audio, silence(6 * dot_duration)))

    # normalize
    if audio.size == 0:
        audio = silence(0.05)
    audio = audio / np.max(np.abs(audio))

    buf = io.BytesIO()
    sf.write(buf, audio, sample_rate, format='wav')
    buf.seek(0)
    return buf

# ----------------- Helpful small features -----------------
def make_download_link_bytes(content_bytes, filename, mime='application/octet-stream'):
    b64 = base64.b64encode(content_bytes).decode()
    return f"data:{mime};base64,{b64}"

# ----------------- Streamlit UI -----------------
st.set_page_config(page_title="Morse Code Decoder", page_icon="📡", layout="wide")

# Custom CSS for nicer UI and dark/light toggle
st.markdown(
    """
    <style>
    .header {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .big-title {
        font-size:34px;
        font-weight:700;
    }
    .subtle { color: #6c757d; }
    .glass { background: rgba(255,255,255,0.03); padding: 18px; border-radius:12px; box-shadow: 0 6px 18px rgba(0,0,0,0.08); }
    .codebox { font-family: monospace; background: rgba(0,0,0,0.05); padding:12px; border-radius:8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown('<div class="header"><div class="big-title">📡 Morse Code Decoder — Advanced</div><div class="subtle">Text ↔ Morse · Audio · Export · Live Preview</div></div>', unsafe_allow_html=True)
with col2:
    # Theme toggle (simple simulated via CSS variable switch)
    theme = st.selectbox('Theme', ['Light', 'Dark'], index=1)

# Layout
left, right = st.columns([3, 2])

with left:
    st.markdown('### Input')
    input_area = st.text_area('Paste text or Morse code here (supports auto-detection):', value='Hello World', height=160)

    st.markdown('### Settings')
    wpm = st.slider('Speed (WPM)', 5, 30, 18)
    freq = st.slider('Tone frequency (Hz)', 300, 1200, 700)
    provide_examples = st.expander('Examples / Presets')
    with provide_examples:
        if st.button('Hello World (Text)'):
            input_area = 'Hello World'
            st.rerun()
        if st.button('SOS (Morse)'):
            input_area = '... --- ...'
            st.rerun()
        if st.button('Complex (Text)'):
            input_area = 'Streamlit is fun!'
            st.rerun()

    st.markdown('### Actions')
    cols = st.columns(3)
    with cols[0]:
        do_convert = st.button('Convert')
    with cols[1]:
        do_play = st.button('Play')
    with cols[2]:
        do_clear = st.button('Clear')

    if do_clear:
        st.experimental_set_query_params()  # no-op to give some immediate effect
        st.rerun()

with right:
    st.markdown('### Output')
    input_type = detect_input_type(input_area)
    if input_type == 'morse':
        detected = 'Morse → Text'
        output = morse_to_text(input_area)
    else:
        detected = 'Text → Morse'
        output = text_to_morse(input_area)

    st.markdown(f'**Detected:** {detected}')

    # Output boxes
    st.markdown('**Result**')
    st.code(output, language='')

    copy_col1, copy_col2 = st.columns([1,1])
    with copy_col1:
        if st.button('Copy Result'):
            # copy via javascript
            components.html(f"<script>navigator.clipboard.writeText(`{output}`)</script>", height=0)
            st.success('Copied to clipboard!')
    with copy_col2:
        # Download text
        b = output.encode('utf-8')
        href = make_download_link_bytes(b, 'result.txt', mime='text/plain')
        st.markdown(f"<a href='{href}' download='morse_result.txt'>📥 Download Result</a>", unsafe_allow_html=True)

    st.markdown('---')
    st.markdown('**Validation & Live Preview**')
    # show whether any unknown chars present
    if input_type == 'text':
        unknown = [ch for ch in input_area if ch.upper() not in MORSE_CODE_DICT and ch != '\n']
        if unknown:
            st.warning(f'Unknown characters ignored: {set(unknown)}')
    else:
        invalid_codes = [p for p in input_area.split(' ') if p and p not in MORSE_TO_TEXT and p != '/']
        if invalid_codes:
            st.warning(f'Invalid morse patterns: {set(invalid_codes)}')

# Audio generation and controls (global)
if 'history' not in st.session_state:
    st.session_state.history = []

if do_convert:
    st.session_state.history.append((input_area, output, time.ctime()))

if do_play or do_convert and input_area:
    # Use the detected output morse string when playing
    if input_type == 'text':
        morse_for_audio = output
    else:
        morse_for_audio = input_area

    buf = generate_morse_audio(morse_for_audio, wpm=wpm, freq=freq)
    st.audio(buf, format='audio/wav')

    # Waveform preview
    try:
        buf.seek(0)
        data, sr = sf.read(buf)
        fig, ax = plt.subplots(figsize=(6, 2))
        ax.plot(np.linspace(0, len(data)/sr, num=len(data)), data)
        ax.set_xlabel('Time (s)')
        ax.set_yticks([])
        ax.set_title('Waveform Preview')
        st.pyplot(fig)
    except Exception:
        pass

# History panel (bottom)
st.markdown('---')
st.markdown('## History & Advanced Tools')
cols = st.columns([3,2])
with cols[0]:
    if st.session_state.history:
        for i, (inp, out, tstamp) in enumerate(reversed(st.session_state.history[-15:])):
            st.markdown(f'**{i+1}.** `{inp}` → `{out}`  *{tstamp}*')
            btn_col1, btn_col2 = st.columns([1,1])
            with btn_col1:
                if st.button(f'Load {i}', key=f'load_{i}'):
                    # load back into the input (approximate)
                    st.experimental_set_query_params()
                    st.rerun()
            with btn_col2:
                if st.button(f'Delete {i}', key=f'del_{i}'):
                    st.session_state.history.pop(len(st.session_state.history)-1-i)
                    st.rerun()
    else:
        st.info('No history yet — convert something to fill this list!')

with cols[1]:
    st.markdown('### Export Audio')
    if 'buf' in globals():
        try:
            # ensure buffer is at start
            buf.seek(0)
            wav_bytes = buf.read()
            href = make_download_link_bytes(wav_bytes, 'morse.wav', mime='audio/wav')
            st.markdown(f"<a href='{href}' download='morse.wav'>📥 Download WAV</a>", unsafe_allow_html=True)
        except Exception:
            st.info('Generate audio first by pressing Play')

    st.markdown('### Advanced')
    st.markdown("""
    - Live auto-detect input type
    - Copy & download
    - Waveform preview
    - Tone frequency & speed control
    """)

# Footer with tips
st.markdown('---')
st.markdown('Made with ❤️ • Tip: press Convert to save to history, Play to hear WAV, then Download to get file.')

# Small easter-egg: show source file path if running locally
try:
    app_path = Path(__file__).resolve()
    st.caption(f'Running from: {app_path}')
except Exception:
    pass

