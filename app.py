import streamlit as st
import os
from moviepy import VideoFileClip, concatenate_videoclips

# Page Configuration
st.set_page_config(page_title="Kazmi Cloud Video Editor", page_icon="🎬", layout="wide")

st.title("🎬 Kazmi Cloud Video Editor")
st.write("Apni videos ko yahan upload karein aur cloud par edit karein!")

# File Uploader
uploaded_file = st.file_uploader("Aik video file select karein", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    # Save video locally in temporary path
    input_path = "temp_video.mp4"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("Video kamyabi se upload ho gayi hai!")
    
    # Preview Video
    st.video(input_path)
    
    if st.button("Video Details Check Karein"):
        with st.spinner("Video load ho rahi hai..."):
            try:
                clip = VideoFileClip(input_path)
                st.info(f"⏱️ Duration: {round(clip.duration, 2)} seconds")
                st.info(f"resolution: {clip.size}")
                clip.close()
            except Exception as e:
                st.error(f"Error: {e}")
