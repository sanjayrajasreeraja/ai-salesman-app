import streamlit as st
import os
from datetime import datetime

st.title("AI Salesman V0 Trial")
st.set_page_config(layout="wide")
st.markdown('<div style="background:#fff3cd; color:#856404; border-radius:6px; padding:0.75em; margin-bottom:1em; font-size:1em;"><b>Note:</b> This process may take time as it runs on Streamlit Cloud and loads models from scratch each time you run it.</div>', unsafe_allow_html=True)

colx, coly = st.columns([1, 5])
with colx:
    lang_display = {
        'English': 'en',
        'Hindi': 'hi',
        'Tamil': 'ta',
        'Malayalam': 'ml',
        'Kannada': 'kn'
    }
    lang_choice = st.selectbox("Language", list(lang_display.keys()), index=0)
    lang_code = lang_display[lang_choice]

col1, col2, col3 = st.columns([3, 1, 1])


with col1:
    audio_file = st.audio_input("Record your audio")

with col2:
    uploaded_file = st.file_uploader("Or upload audio", type=[
                                     "wav", "mp3", "m4a", "ogg"])


selected_audio = None
if audio_file is not None:
    selected_audio = audio_file
elif uploaded_file is not None:
    selected_audio = uploaded_file

if selected_audio is not None:
    recording_dir = 'recording'
    os.makedirs(recording_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    wav_path = os.path.join(recording_dir, f'recording_{timestamp}.wav')
    mp3_path = os.path.join(recording_dir, f'recording_{timestamp}.mp3')

    audio_bytes = selected_audio.read()
    with open(wav_path, 'wb') as wav_file:
        wav_file.write(audio_bytes)

    # Convert WAV to MP3 using ffmpeg
    try:
        # subprocess.run([
        #     'ffmpeg', '-y', '-i', wav_path, mp3_path
        # ], check=True)
        # st.success(f"Audio recorded and saved as {mp3_path}!")

        # Transcribe using Whisper (modularized)
        from whisper_openai import transcribe_audio, translate_to_english
        with st.spinner('Transcribing audio...'):
            transcript, detected_lang = transcribe_audio(
                wav_path, language=lang_code)
        st.subheader('Transcription:')
        st.write(transcript)
        conversation_text = transcript
        if detected_lang != 'en':
            with st.spinner('Translating to English...'):
                translation = translate_to_english(wav_path)
            st.subheader('Translation to English:')
            st.write(translation)
            conversation_text = translation

        # Generate report using main.py's run_report
        try:
            from main import run_report
            with st.spinner('Generating report...'):
                report = run_report(conversation_text)

            st.subheader('Generated Report:')
            # GPT generated
            if isinstance(report, list):
                for product in report:
                    details = product.get('Product Details', {})
                    entity = product.get('Business Entity Classification', {})
                    issues = product.get('Identified Business Issues', {})

                    # Compose a short citation/summary for the expander label
                    product_name = details.get('Product Name', 'Product')
                    brand = details.get('Brand', '')
                    category = details.get('Category', '')
                    citation = f"{product_name}" if brand or category else product_name

                    with st.expander(citation, expanded=False):
                        # Business Entity (Retailer) first
                        st.markdown(
                            '<div style="margin-bottom: 0.5em;"><b>Retailer / Business Entity:</b></div>', unsafe_allow_html=True)
                        for k, v in entity.items():
                            st.markdown(
                                f'<div style="margin-left:1em; margin-bottom:0.2em;"><b>{k}:</b> {v}</div>', unsafe_allow_html=True)

                        # Issues next
                        st.markdown(
                            '<div style="margin: 1em 0 0.5em 0;"><b>Identified Business Issues:</b></div>', unsafe_allow_html=True)
                        for k, v in issues.items():
                            st.markdown(
                                f'<div style="margin-left:1em; margin-bottom:0.2em;"><b>{k}:</b> {v}</div>', unsafe_allow_html=True)

                        st.markdown('<hr style="margin:1em 0;">',
                                    unsafe_allow_html=True)

                        # Product details as a sub-collapsible expander
                        with st.expander("Product Details", expanded=False):
                            for k, v in details.items():
                                st.markdown(
                                    f'<div style="margin-left:1em; margin-bottom:0.2em; color:#888;"><b>{k}:</b> {v}</div>', unsafe_allow_html=True)

            else:
                st.markdown('<b>Report:</b>', unsafe_allow_html=True)
                for k, v in report.items():
                    st.markdown(
                        f'<div style="margin-left:1em; margin-bottom:0.2em;"><b>{k}:</b> {v}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error generating report: {e}")
    except Exception as e:
        st.error(f"Error converting to MP3 or transcribing: {e}")
else:
    st.info("Click the mic button and speak into your mic.")
