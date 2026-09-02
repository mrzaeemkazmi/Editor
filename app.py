import streamlit as st
import os
import gdown
from moviepy import VideoFileClip

# Page Configuration
st.set_page_config(page_title="Kazmi Cloud Video Editor", page_icon="🎬", layout="wide")

# 🎨 Custom CSS for Modern CapCut-Style Playhead
st.markdown("""
<style>
div[data-baseweb="slider"] {
    padding-top: 15px !important;
}
div[data-baseweb="slider"] div[role="slider"] {
    width: 8px !important;
    height: 28px !important;
    border-radius: 3px !important;
    background-color: #ffffff !important;
    border: 1px solid #cccccc !important;
    box-shadow: 0 0 8px rgba(0,242,254,0.6) !important;
    cursor: ew-resize !important;
}
div[data-baseweb="slider"] > div > div > div:nth-child(1) {
    background-color: #00f2fe !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Kazmi Cloud Video Studio")

# Time Formatter
def format_time(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes:02d}:{remaining_seconds:02d}"

# Safe Subclip Helper
def safe_subclip(clip, start, end):
    if hasattr(clip, 'subclipped'):
        return clip.subclipped(start, end)
    return clip.subclip(start, end)

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

# 2. MAIN WORKSPACE
if os.path.exists(output_path):
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
        st.markdown(f"**Duration:** {format_time(duration)}")
        st.markdown(f"**Resolution:** {size[0]} x {size[1]}")
        st.markdown(f"**Frame Rate:** {fps} fps")
        
        st.divider()
        st.markdown("### ⚙️ Action")
        render_btn = st.button("🚀 Render Output", use_container_width=True)

    with col_player:
        st.subheader("🎥 Live Video Preview")
        
        # Tool Selection
        edit_mode = st.radio("🛠️ Timeline Tool Select Karein:", ["✂️ Trim (Koi hissa kaat kar nikalna)", "🔪 Split (Video ko 2 hisson mein torna)"], horizontal=True)
        
        if "Trim" in edit_mode:
            start_time, end_time = st.slider(
                "Playhead (Select Start & End):",
                0.0, float(duration), (0.0, float(duration)), step=1.0
            )
            st.info(f"📍 **Selection:** Start: `{format_time(start_time)}` ➔ End: `{format_time(end_time)}`")
            st.video(output_path, start_time=int(start_time))
        else:
            split_time = st.slider(
                "Playhead (Kahan se Split karna hai?):",
                0.0, float(duration), float(duration)/2, step=1.0
            )
            st.info(f"🔪 **Split Point:** `{format_time(split_time)}` (Part 1: 0 ➔ {format_time(split_time)} | Part 2: {format_time(split_time)} ➔ {format_time(duration)})")
            st.video(output_path, start_time=int(split_time))

    # 3. RENDERING ENGINE
    if render_btn:
        original_clip = VideoFileClip(output_path)
        
        if "Trim" in edit_mode:
            with st.spinner("Video Trim aur Render ho rahi hai..."):
                edited_path = "output_trimmed.mp4"
                trimmed_clip = safe_subclip(original_clip, start_time, end_time)
                trimmed_clip.write_videofile(edited_path, codec="libx264", audio_codec="aac")
                
                st.success("✅ Trimmed Video Tayyar Hai!")
                st.video(edited_path)
                with open(edited_path, "rb") as f:
                    st.download_button("📥 Download Trimmed Video", data=f, file_name="kazmi_trimmed.mp4", mime="video/mp4")
                
                trimmed_clip.close()
        
        else:
            with st.spinner("Video Split aur Render ho rahi hai..."):
                part1_path = "output_part1.mp4"
                part2_path = "output_part2.mp4"
                
                clip1 = safe_subclip(original_clip, 0, split_time)
                clip2 = safe_subclip(original_clip, split_time, duration)
                
                clip1.write_videofile(part1_path, codec="libx264", audio_codec="aac")
                clip2.write_videofile(part2_path, codec="libx264", audio_codec="aac")
                
                st.success("✅ Video kamyabi se Split ho gayi!")
                
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.video(part1_path)
                    with open(part1_path, "rb") as f:
                        st.download_button("📥 Download Part 1", data=f, file_name="kazmi_part1.mp4", mime="video/mp4")
                with col_d2:
                    st.video(part2_path)
                    with open(part2_path, "rb") as f:
                        st.download_button("📥 Download Part 2", data=f, file_name="kazmi_part2.mp4", mime="video/mp4")
                
                clip1.close()
                clip2.close()

        original_clip.close()
else:
    st.info("👈 Baraye meharbani sidebar mein Google Drive ka link de kar pehle video import karein!")
