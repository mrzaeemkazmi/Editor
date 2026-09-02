import streamlit as st
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.all import crop

st.set_page_config(page_title="Kazmi Cloud Video Editor", page_icon="🎬", layout="centered")

st.title("🎬 Kazmi Cloud Video Editor & Cropper")
st.write("Apni video upload karein, timestamps dein, aur aik click par 9:16 Shorts/Reels tayar karein!")

# Video Upload Option
uploaded_file = st.file_uploader("Apni Video File Select Karein (MP4, MKV)", type=["mp4", "mkv", "mov"])

# Timestamps Input
timestamps_input = st.text_input("Timestamps (Format: 00:00:10, 00:00:45)", "00:00:05, 00:00:20")

# Options
col1, col2 = st.columns(2)
with col1:
    crop_vertical = st.checkbox("Crop to Vertical 9:16 (Shorts/Reels)", value=True)
with col2:
    shuffle_clips = st.checkbox("Shuffle Clips", value=False)

def time_to_seconds(t_str):
    parts = list(map(int, t_str.strip().split(":")))
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return parts[0]

if st.button("🚀 Process & Edit Video", type="primary"):
    if uploaded_file is not None:
        try:
            with st.spinner("Video process ho rahi hai, thoda intezaar karein..."):
                # Save uploaded video temporarily
                input_path = "temp_input.mp4"
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                video = VideoFileClip(input_path)
                clips = []
                
                # Parse timestamps
                segments = timestamps_input.split(";")
                for seg in segments:
                    if "," in seg:
                        start_str, end_str = seg.split(",")
                        start = time_to_seconds(start_str.strip())
                        end = time_to_seconds(end_str.strip())
                        subclip = video.subclip(start, end)
                        
                        # 9:16 Vertical Crop Logic
                        if crop_vertical:
                            w, h = subclip.size
                            target_w = int(h * 9 / 16)
                            if target_w < w:
                                x1 = (w - target_w) // 2
                                x2 = x1 + target_w
                                subclip = crop(subclip, x1=x1, y1=0, x2=x2, y2=h)
                        
                        clips.append(subclip)
                
                if shuffle_clips:
                    import random
                    random.shuffle(clips)
                
                final_clip = concatenate_videoclips(clips)
                output_path = "output_video.mp4"
                final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
                
                video.close()
                
                st.success("Video kamyabi se tayar ho gayi hai!")
                
                # Download Button for Final Video
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Edited Video",
                        data=file,
                        file_name="Kazmi_Edited_Short.mp4",
                        mime="video/mp4"
                    )
        except Exception as e:
            st.error(f"Koi masla aa gaya: {str(e)}")
    else:
        st.warning("Pehle koi video file upload karein!")
