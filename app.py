import streamlit as st
import os
import openai
from gtts import gTTS
import io
import base64
from datetime import datetime
import calendar
import imageio_ffmpeg as ffmpeg


from pydub import AudioSegment
#AudioSegment.ffprobe = "/Users/p.timofeeva:/Users/p.timofeeva/Documents/Projects/insightsforme/venv/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

def get_current_month():
    # Get the current date
    current_date = datetime.now()

    # Get the current month and year
    current_month = current_date.month

    # Calculate the previous month and year
    previous_month = current_month 

    if previous_month == 0:
        previous_month = 12

    return calendar.month_name[previous_month]


def generate_audio(summary_text, path):
    # Create a gTTS object
    tts = gTTS(text = summary_text, lang='en')

    # Save the audio in memory
    tts.save("voice.mp3")

def add_background_music(voice_path, music_path, output_path, delay_seconds=5, volume_adjustment=-10):
    """
    Adds background music to a voice layover with a specified delay.
    
    Parameters:
        voice_path (str): Path to the voice layover audio file.
        music_path (str): Path to the background music audio file.
        output_path (str): Path to save the combined audio.
        delay_seconds (int): The delay for the voice layover in seconds.
        volume_adjustment (int): Amount to adjust the volume of the background music. Negative to reduce volume.
    
    Returns:
        None: The combined audio is saved to `output_path`.
    """
    # Load voice and music
    voice = AudioSegment.from_file(voice_path, format="mp3")
    music = AudioSegment.from_file(music_path, format="mp3")
    
    # Ensure both audio clips have the same frame rate and number of channels
    voice = voice.set_frame_rate(music.frame_rate).set_channels(music.channels)
    
    # Optionally, lower the volume of the music
    music = music + volume_adjustment
    
    # Add delay to voice layover
    delay_time = delay_seconds * 1000  # Convert to milliseconds
    voice = AudioSegment.silent(duration=delay_time) + voice
    
    # Calculate lengths and make sure they match
    voice_length = len(voice)
    music_length = len(music)
    
    # If the music is shorter/longer, you might have to loop/cut it
    if music_length < voice_length:
        loops = voice_length // music_length + 1
        music = music * loops
    
    # Overlay voice on music
    combined = music.overlay(voice)
    
    # Export the mixed audio
    combined.export(output_path, format="mp3")

# Example usage
# add_background_music_with_delay("voice.mp3", "music.mp3", "combined_delayed.mp3")



st.title("Insights For Me")

# Capture user inputs
user_name = st.text_input("Enter your name:", "John Doe")
month = get_current_month()
condition = st.text_input("Enter the topic or condition you're interested in:", "Rosacea")
closure = " This is all for today. Until next month, keep your curiosity alive and your research glasses on!"
intro = f"Hello {user_name}! It is {month} first. The month is new, and so are the insights we've got just for you!"

summary_01 = " According to this paper elevated levels of serum 25OHD were found to be inversely correlated with the risk of incident rosacea. A Mendelian Randomization (MR) study supported this finding, indicating that each standard deviation increase in serum 25OHD concentrations correlates to a 23% reduced risk of rosacea. The study suggests a potential protective role for vitamin D in preventing rosacea, though it notes that the efficacy of vitamin D supplementation as a preventive strategy requires further investigation. The external quality assurance for vitamin D in the study was 100%, implying high reliability in the measurement of vitamin D levels. In summary, the study finds a negative correlation between serum 25OHD levels and the risk of developing rosacea, suggesting that higher vitamin D levels may offer some protective effect. However, the text also emphasizes the need for further research to definitively establish the role of vitamin D supplementation in preventing rosacea."
summary_02 = " The study investigates the impact of long-term administration of LL-37 intradermal injections on Balb/c mice, aiming to understand if this leads to irreversible rosacea-like skin lesions. Using continuous injections of LL-37, the research focuses on observing changes in skin lesions and histopathological aspects over a 20-day period. The findings reveal that mice receiving long-term treatment showed more severe rosacea-like skin lesions compared to those with short-term treatment. Although the text didn't include specific conclusions, the results imply that long-term use of LL-37 could be a significant factor in inducing severe rosacea-like conditions. This could serve as a basis for further studies to understand similar skin conditions in humans."

title_01 = "Vitamin D Status, Vitamin D Receptor Polymorphisms, and the Risk of Incident Rosacea: Insights from Mendelian Randomization and Cohort Study in the UK Biobank"
title_02 = "Long-term administration of LL-37 can induce irreversible rosacea-like lesion"

summaries = [summary_01, summary_02]
titles = [title_01, title_02]

n_papers = f" This month we have {len(summaries)} papers about {condition}. Let's get started!"

full_text = intro + n_papers + "\n\n"

for i, s in enumerate(summaries):
    if i == 0:
        n = "first"
    elif i == 1:
        n = "second"
    full_text += f" The {n} paper is about {titles[i]}. \n\n"
    full_text += s.replace("\n", " ").replace("\n\n", " ")
    full_text += "\n\n"

full_text += "\n\n" + closure

# Dynamically generate and display the phrase with Markdown and inline HTML for color
st.markdown(f"""
    <h2>Hello <span style='color: #3a86ff;'>{user_name}</span>! 
    Below you can find your <span style='color: #8338ec;'>{month}</span> 
    dose of research on the topic of <span style='color: #ff006e;'>{condition}</span></h2>
    """, unsafe_allow_html=True)


st.write(full_text)

st.write("")
st.write("")
st.write("")
st.write("")

if summaries:
    generate_audio(full_text, "/audio")

    add_background_music("voice.mp3", "music.mp3", "combined.mp3", delay_seconds=5)

    st.audio("combined.mp3", format="audio/mp3", start_time=0)