import streamlit as st
from dotenv import load_dotenv

load_dotenv() # load all env variables like google_api_key

import os
import google.generativeai as ggenai

from youtube_transcript_api import YouTubeTranscriptApi

ggenai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """
you are youtube video summarizer. You will be taking the transcript text and summarizing the entire video
and providing the important summary in points within 250 words.
Please provide the summary of the text given here: """

# getting transcript data from YT videos

def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""

        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e

# getting the summary based on prompt from Google gemini

def generate_gemini_content(transcript_text,text,prompt):

    model = ggenai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)

    return response.text

# streamlit app ; running locally
st.title("YouTube Videos Summarizer: Transcription to Notes Converter")
youtube_link = st.text_input("Enter YouTube video's link : ")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
