import streamlit as st
import whisper
import eng_to_ipa as ipa
from gtts import gTTS
import io
import difflib
import os
import re

# Page Config
st.set_page_config(page_title="AI Pronunciation Coach", page_icon="🎤")

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

model = load_whisper_model()

def clean_text(text):
    """Removes punctuation and extra spaces for cleaner IPA conversion."""
    return re.sub(r'[^\w\s]', '', text).lower().strip()

def get_phonetic_feedback(target_text, user_audio_path):
    # 1. Transcribe User Audio
    result = model.transcribe(user_audio_path)
    user_text = clean_text(result['text'])
    
    # 2. Convert to IPA (Cleaned versions)
    target_clean = clean_text(target_text)
    target_ipa = ipa.convert(target_clean)
    user_ipa = ipa.convert(user_text)
    
    # 3. Calculate Similarity
    score = difflib.SequenceMatcher(None, target_ipa, user_ipa).ratio()
    return user_text, target_ipa, user_ipa, int(score * 100)

# --- UI Layout ---
st.title("🗣️ AI Pronunciation Coach")

# Use session state to track which sentence we are working on
if 'current_sentence' not in st.session_state:
    st.session_state.current_sentence = ""

target_sentence = st.text_input("Target Sentence:", "The quick brown fox jumps over the lazy dog.")

# Check if the sentence has changed
sentence_changed = target_sentence != st.session_state.current_sentence

if target_sentence:
    # Update state
    st.session_state.current_sentence = target_sentence
    
    # 1. Reference Audio
    tts = gTTS(text=target_sentence, lang='en', tld='com')
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Reference")
        st.audio(audio_fp, format="audio/mp3")
        # Display IPA without the trailing period
        clean_target = clean_text(target_sentence)
        st.info(f"Target IPA: `{ipa.convert(clean_target)}`")

    # 2. User Recording
    with col2:
        st.subheader("2. Your Turn")
        # If sentence changed, we show a fresh input
        # Adding a unique key based on the sentence ensures the widget resets
        user_audio = st.audio_input("Record your voice", key=f"audio_{target_sentence}")

    # Only run analysis if there is audio AND it's not a leftover from a previous sentence
    if user_audio and not sentence_changed:
        with open("temp_audio.wav", "wb") as f:
            f.write(user_audio.getbuffer())
        
        with st.spinner("Analyzing..."):
            heard_text, t_ipa, u_ipa, score = get_phonetic_feedback(target_sentence, "temp_audio.wav")
            
            st.divider()
            st.header(f"Score: {score}/100")
            
            # Use columns for a nice side-by-side IPA view
            res_col1, res_col2 = st.columns(2)
            res_col1.metric("Target IPA", t_ipa)
            res_col2.metric("Your IPA", u_ipa)
            
            st.write(f"**I heard:** \"{heard_text}\"")
            
            if score > 85:
                st.success("Excellent pronunciation!")
            elif score > 60:
                st.warning("Good, but try to be clearer.")
            else:
                st.error("Needs more practice.")

        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")
    elif sentence_changed:
        st.light_bulb("New sentence detected. Please record your voice for the new target!")