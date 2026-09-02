import streamlit as st
import os
import gdown
from moviepy import VideoFileClip

# Page Configuration
st.set_page_config(page_title="Kazmi Cloud Video Editor", page_icon="🎬", layout="wide")

st.title("🎬 Kazmi Cloud Video Studio")

# Time Formatter
def format_time(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes:02d}:{remaining_seconds:02d}"

# 1. SIDEBAR PANEL
with st.sidebar:
    st.header("📁 Media & Import")
    drive_link = st.text_input("🔗 Google Drive Shareable Link:")
    import_btn = st.button("📥 Import Video")

output_path = "temp_video.mp4"

# Handle Import
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

# 2. MAIN WORKSPACE (Connected Player & Timeline)
if os.path.exists(output_path):
    # Get Video Details
    try:
        clip = VideoFileClip(output_path)
        duration = clip.duration
        size = clip.size
        fps = clip.fps
        clip.close()
    except Exception as e:
        st.error("Error reading video details.")
        duration = 0

    col_player, col_details = st.columns([2, 1])

    with col_details:
        st.subheader("📊 Video Details")
        st.markdown(f"**Duration:** {format_time(duration)} ({round(duration, 2)}s)")
        st.markdown(f"**Resolution:** {size[0]} x {size[1]}")
        st.markdown(f"**Frame Rate:** {fps} fps")
        st.divider()
        st.markdown("### ⚙️ Action")
        render_btn = st.button("🚀 Video Edit & Render", use_container_width=True)

    with col_player:
        st.subheader("🎥 Live Video Preview")
        
        # PLAYHEAD SLIDER (Placed above video for CTI feel)
        start_time, end_time = st.slider(
            "✂️ Timeline / Playhead (Select Start & End Time):",
            0.0, float(duration), (0.0, float(duration)),
            step=1.0
        )
        
        st.info(f"📍 **Selection:** Start: `{format_time(start_time)}` ➔ End: `{format_time(end_time)}` | (Selected: `{format_time(end_time - start_time)}`)")
        
        # 🔗 CONNECTED VIDEO PLAYER: Jumps to the start_time selected in the slider!
        st.video(output_path, start_time=int(start_time))

    # 3. RENDERING ENGINE
    if render_btn:
        with st.spinner("Video render ho rahi hai... Thora intezaar karein."):
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
