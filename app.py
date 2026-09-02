import streamlit as st
import os
import gdown
from moviepy import VideoFileClip

# Page Configuration
st.set_page_config(page_title="Kazmi Cloud Video Editor", page_icon="🎬", layout="wide")

st.title("🎬 Kazmi Cloud Video Editor (Google Drive Integration)")
st.write("Apni Google Drive ki video ka public link yahan paste karein!")

# Google Drive Link Input
drive_link = st.text_input("🔗 Google Drive Shareable Link enter karein:")

if drive_link:
    if st.button("📥 Drive se Video Download & Import Karein"):
        with st.spinner("Google Drive se video download ho rahi hai... Thora intezaar karein!"):
            try:
                output_path = "temp_video.mp4"
                
                # Agar pehle se koi purani file ho toh delete kar dein
                if os.path.exists(output_path):
                    os.remove(output_path)
                
                # gdown ke zariye Google Drive se video download karein
                gdown.download(drive_link, output_path, quiet=False, fuzzy=True)
                
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    st.success("🎉 Video Google Drive se kamyabi se import ho gayi hai!")
                    
                    # Video Preview
                    st.video(output_path)
                    
                    # Video Details
                    clip = VideoFileClip(output_path)
                    st.info(f"⏱️ Duration: {round(clip.duration, 2)} seconds")
                    st.info(f"📐 Resolution: {clip.size}")
                    clip.close()
                else:
                    st.error("❌ Video download nahi ho saki. Please check karein ke aapka Google Drive link 'Anyone with the link can view' par set hai ya nahi.")
            
            except Exception as e:
                st.error(f"Error aa gaya: {e}")
