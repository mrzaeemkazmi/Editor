import streamlit as st
import streamlit.components.v1 as components
import os
import gdown
from moviepy import VideoFileClip

# Page Configuration
st.set_page_config(page_title="Kazmi Cloud Video Editor", page_icon="🎬", layout="wide")

st.title("🎬 Kazmi Cloud Video Studio")

# Helper Function: Seconds ko Minutes:Seconds (MM:SS) mein convert karne ke liye
def format_time(seconds):
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

    # 3. PLAYHEAD & TIMELINE STUDIO
    st.markdown("### ✂️ Playhead & Timeline Studio")
    
    # Custom HTML/CSS/JS Timeline UI (Visual CapCut Look)
    timeline_ui = """
    <style>
        .timeline-wrapper {
            position: relative;
            width: 100%;
            height: 90px;
            background-color: #121212;
            border-radius: 6px;
            border: 1px solid #2e2e2e;
            user-select: none;
            cursor: pointer;
        }
        .track {
            position: absolute;
            top: 25px;
            left: 10px;
            right: 10px;
            height: 45px;
            background: #1f2937;
            border: 1px solid #10b981;
            border-radius: 4px;
        }
        .playhead {
            position: absolute;
            top: 0;
            bottom: 0;
            width: 2px;
            background-color: #ffffff;
            z-index: 10;
            box-shadow: 0 0 6px rgba(255,255,255,0.8);
            left: 10%;
        }
        .playhead-handle {
            position: absolute;
            top: 0;
            left: -5px;
            width: 12px;
            height: 10px;
            background-color: #ffffff;
            clip-path: polygon(0 0, 100% 0, 50% 100%);
        }
    </style>

    <div class="timeline-wrapper" id="timeline">
        <div class="track"></div>
        <div class="playhead" id="playhead">
            <div class="playhead-handle"></div>
        </div>
    </div>

    <script>
        const timeline = document.getElementById('timeline');
        const playhead = document.getElementById('playhead');
        let isDragging = false;

        function movePlayhead(e) {
            const rect = timeline.getBoundingClientRect();
            let x = e.clientX - rect.left;
            x = Math.max(0, Math.min(x, rect.width));
            playhead.style.left = x + 'px';
        }

        timeline.addEventListener('mousedown', (e) => {
            isDragging = true;
            movePlayhead(e);
        });

        document.addEventListener('mousemove', (e) => {
            if (isDragging) movePlayhead(e);
        });

        document.addEventListener('mouseup', () => {
            isDragging = false;
        });
    </script>
    """
    
    # Rendering Custom UI
    components.html(timeline_ui, height=110) 

    if 'duration' in locals():
        # Streamlit Native Slider for actual backend processing
        start_time, end_time = st.slider(
            "Video ka exact waqt set karein (MM:SS ke hisab se):",
            0.0, float(duration), (0.0, float(duration)),
            step=1.0
        )
        
        st.info(f"📍 **Selection:** Start: `{format_time(start_time)}` ➔ End: `{format_time(end_time)}` | (Selected Duration: `{format_time(end_time - start_time)}`)")
        
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
