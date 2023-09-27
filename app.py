import streamlit as st
import os
import PyPDF2
import openai
from gtts import gTTS
import io
import base64

def generate_audio(summary_text, path):
    # Create a gTTS object
    tts = gTTS(text = summary_text, lang='en')
    
    # Create a BytesIO object
    #mp3_fp = io.BytesIO()
    
    # Save the audio in memory
    tts.save("test.mp3")
    
    # Go to the beginning of the BytesIO object
    #mp3_fp.seek(0)
    
    #return mp3_fp

st.title("Insights For Me")

# Capture user inputs
user_name = st.text_input("Enter your name:", "John Doe")
month = st.selectbox("Select the month:", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
condition = st.text_input("Enter the topic or condition you're interested in:", "Rosacea")
closure = " Until next month, keep your curiosity alive and your research glasses on!"
intro = f"Hello {user_name}! It is {month} first. The month is new, and so are the insights we've got just for you. Buckle up for another exciting journey through the world of {condition}!"

summary_01 = " Based on the sentences that contain keywords related to conclusions or findings, the main conclusions of the text are as follows: Elevated levels of serum 25OHD were found to be inversely correlated with the risk of incident rosacea. A Mendelian Randomization (MR) study supported this finding, indicating that each standard deviation increase in serum 25OHD concentrations correlates to a 23% reduced risk of rosacea. The study suggests a potential protective role for vitamin D in preventing rosacea, though it notes that the efficacy of vitamin D supplementation as a preventive strategy requires further investigation. The external quality assurance for vitamin D in the study was 100%, implying high reliability in the measurement of vitamin D levels. In summary, the study finds a negative correlation between serum 25OHD levels and the risk of developing rosacea, suggesting that higher vitamin D levels may offer some protective effect. However, the text also emphasizes the need for further research to definitively establish the role of vitamin D supplementation in preventing rosacea."

summaries = [summary_01]
titles = ["Vitamin D Status, Vitamin D Receptor Polymorphisms, and the Risk of Incident Rosacea: Insights from Mendelian Randomization and Cohort Study in the UK Biobank."]

n_papers = f" This month we have {len(summaries)} papers for you. Let's get started!"

full_text = intro + n_papers

for i, s in enumerate(summaries):
    full_text += f"The first paper is about {titles[i]}"
    full_text += s.replace("\n", " ").replace("\n\n", " ")

full_text += closure

# Dynamically generate and display the phrase with Markdown and inline HTML for color
st.markdown(f"""
    <h2>Hello <span style='color: blue;'>{user_name}</span>! 
    Below you can find your <span style='color: green;'>{month}</span> 
    dose of research on the topic of <span style='color: red;'>{condition}</span>.</h2>
    """, unsafe_allow_html=True)


st.write(full_text)


st.write("")
st.write("")
st.write("")
st.write("")

if summaries:
    audio_data = generate_audio(full_text, "/audio")

    st.audio("test.mp3", format="audio/mp3", start_time=0)