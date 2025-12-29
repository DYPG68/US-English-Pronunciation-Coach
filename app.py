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
    """Removes punctuation for cleaner IPA conversion."""
    return re.sub(r'[^\w\s]', '', text).lower().strip()

def get_highlighted_ipa(target_ipa, user_ipa):
    """
    Compares two IPA strings and highlights the user's mistakes in red.
    Target: The correct sequence
    User: What the user actually said
    """
    result = ""
    # SequenceMatcher finds the differences between the two strings
    matcher = difflib.SequenceMatcher(None, target_ipa, user_ipa)
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            # Matching parts are normal
            result += user_ipa[j1:j2]
        elif tag in ('replace', 'insert'):
            # Mistaken or extra sounds are highlighted in red
            result += f'<span style="color:#FF4B4B; font-weight:bold;">{user_ipa[j1:j2]}</span>'
        elif tag == 'delete':
            # Missing sounds are indicated with a red placeholder
            result += '<span style="color:#FF4B4B; font-weight:bold;">_</span>'
            
    return result

def get_phonetic_feedback(target_text, user_audio_path):
    result = model.transcribe(user_audio_path)
    user_text = clean_text(result['text'])
    
    target_clean = clean_text(target_text)
    target_ipa = ipa.convert(target_clean)
    user_ipa = ipa.convert(user_text)
    
    score = int(difflib.SequenceMatcher(None, target_ipa, user_ipa).ratio() * 100)
    highlighted_user_ipa = get_highlighted_ipa(target_ipa, user_ipa)
    
    return user_text, target_ipa, highlighted_user_ipa, score

# --- UI Layout ---
st.title("🗣️ AI Pronunciation Coach")

if 'current_sentence' not in st.session_state:
    st.session_state.current_sentence = ""

target_sentence = st.text_input("Target Sentence:", "The quick brown fox jumps over the lazy dog.")
sentence_changed = target_sentence != st.session_state.current_sentence

if target_sentence:
    st.session_state.current_sentence = target_sentence
    
    # 1. Reference Audio
    tts = gTTS(text=target_sentence, lang='en', tld='com')
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Reference")
        st.audio(audio_fp, format="audio/mp3")
        
        clean_target = clean_text(target_sentence)
        t_ipa_display = ipa.convert(clean_target)
        
        # --- FIXED REFERENCE BOX STYLING ---
        st.markdown(
            f"""
            <div style='
                font-family: "Courier New", Courier, monospace; 
                background-color: #1E1E1E; 
                color: #FFFFFF; 
                padding: 15px; 
                border-radius: 10px;
                border: 1px solid #4B4B4B;
                margin-top: 5px;
            '>
                <span style='color: #888888; font-size: 0.8em;'>Target IPA:</span><br>
                {t_ipa_display}
            </div>
            """, 
            unsafe_allow_html=True
        )

    # 2. User Recording
    with col2:
        st.subheader("2. Your Turn")
        user_audio = st.audio_input("Record your voice", key=f"audio_{target_sentence}")

    # 3. Analysis Logic
    if user_audio and not sentence_changed:
        with open("temp_audio.wav", "wb") as f:
            f.write(user_audio.getbuffer())
        
        with st.spinner("Comparing sounds..."):
            heard_text, t_ipa, h_u_ipa, score = get_phonetic_feedback(target_sentence, "temp_audio.wav")
            
            st.divider()
            st.header(f"Score: {score}/100")
            
            st.write("**Phonetic Comparison (Red = Incorrect/Extra):**")
            
            # --- FIXED BOX STYLING ---
            # background-color: #1E1E1E (Dark background)
            # color: #FFFFFF (White text)
            st.markdown(
                f"""
                <div style='
                    font-family: "Courier New", Courier, monospace; 
                    line-height: 2.2; 
                    background-color: #1E1E1E; 
                    color: #FFFFFF; 
                    padding: 20px; 
                    border-radius: 10px;
                    border: 1px solid #4B4B4B;
                    font-size: 1.1em;
                '>
                    <span style='color: #888888;'>Target:</span> {t_ipa}<br>
                    <span style='color: #888888;'>Yours:</span>&nbsp; {h_u_ipa}
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.write(f"**I heard:** \"{heard_text}\"")
            
            if score > 85:
                st.success("Excellent! Almost native.")
            else:
                st.warning("Take a look at the red sounds to improve.")

        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")
            
    elif sentence_changed:
        st.info("New sentence detected. Please record your voice for the new target!")
