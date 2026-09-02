import streamlit as st
import os
import gdown
from moviepy import VideoFileClip

# Page Configuration (Wide Mode for Studio Look)
st.set_page_config(page_title="Kazmi Cloud Video Editor", page_icon="🎬", layout="wide")

st.title("🎬 Kazmi Cloud Video Studio (Playhead & Time Format)")

# Helper Function: Seconds ko Minutes:Seconds (MM:SS) mein convert karne ke liye
fn format_time(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes:02d}:{remaining_seconds:02d}"

# 1. SIDEBAR PANEL (Media Import)
with st.sidebar:
    st.header("📁 Media & Import")
    drive_link = st.text_input("🔗 Google Drive Shareable Link:")
    import_btn = st.button("📥 Import Video")

output_path = "temp_video.mp4"

# Handle Google Drive Import
if import_btn and drive_link:
    with st.spinner("Google Drive se video download ho rahi hai..."):
        try:
            if os.path.exists(output_path):
                os.remove(output_path)
            gdown.download(drive_link, output_path, quiet=False)
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                st.sidebar.success("Video Import Ho Gayi!")
            else:
                st.sidebar.error("Download fail ho gayi. Link check karein.")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

# 2. MAIN WORKSPACE (Player & Details)
if os.path.exists(output_path):
    col_player, col_details = st.columns([2, 1])

    with col_player:
        st.subheader("🎥 Video Player Preview")
        st.video(output_path)

    with col_details:
        st.subheader("📊 Video Details")
        try:
            clip = VideoFileClip(output_path)
            duration = clip.duration
            size = clip.size
            fps = clip.fps
            clip.close()

            st.markdown(f"**Duration:** {format_time(duration)} ({round(duration, 2)}s)")
            st.markdown(f"**Resolution:** {size[0]} x {size[1]}")
            st.markdown(f"**Frame Rate:** {fps} fps")
        except Exception as e:
            st.error("Details load nahi ho sakein.")

    st.divider()

    # 3. PLAYHEAD & TIMELINE STUDIO (Bottom Panel with MM:SS)
    st.subheader("✂️ Playhead & Timeline Studio")
    
    if 'duration' in locals():
        # Trimming Slider with Seconds underlying value
        start_time, end_time = st.slider(
            "Playhead Position (Minutes:Seconds select karein):",
            0.0, float(duration), (0.0, float(duration)),
            step=1.0
        )
        
        # Playhead Current Time Indicator Display (MM:SS Format)
        st.info(f"📍 **Current Playhead / Selection:** Start: `{format_time(start_time)}` ➔ End: `{format_time(end_time)}` | (Selected Duration: `{format_time(end_time - start_time)}`)")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            render_btn = st.button("🚀 Video Edit & Render Karein")
            
        if render_btn:
            with st.spinner("Video render ho rahi hai..."):
                edited_path = "output_edited.mp4"
                if os.path.exists(edited_path):
                    os.remove(edited_path)
                
                original_clip = VideoFileClip(output_path)
                if hasattr(original_clip, 'subclipped'):
                    trimmed_clip = original_clip.subclipped(start_time, end_time)
                else:
                    trimmed_clip = original_clip.subclip(start_time, end_time)
                
                trimmed_clip.write_videofile(edited_path, codec="libx264", audio_codec="aac")
                original_clip.close()
                trimmed_clip.close()
                
                st.success("✅ Video kamyabi se render ho gayi hai!")
                st.video(edited_path)
                
                with open(edited_path, "rb") as f:
                    st.download_button(
                        label="📥 Edited Video Download Karein",
                        data=f,
                        file_name="kazmi_studio_edited.mp4",
                        mime="video/mp4"
                    )
else:
    st.info("👈 Baraye meharbani sidebar mein Google Drive ka link de kar pehle video import karein!")
