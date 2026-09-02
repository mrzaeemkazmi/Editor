import streamlit as st
import os
import gdown
from moviepy import VideoFileClip

# Page Configuration (Wide Layout)
st.set_page_config(page_title="Kazmi Cloud Video Studio", page_icon="🎬", layout="wide")

# 🎨 Custom CSS: Streamlit slider ko CapCut jaisa modern aur glowing banane ke liye
st.markdown("""
<style>
div[data-baseweb="slider"] {
    padding-top: 10px !important;
    padding-bottom: 10px !important;
}
/* Playhead Handle Design (CapCut Style White/Cyan Bar) */
div[data-baseweb="slider"] div[role="slider"] {
    width: 10px !important;
    height: 32px !important;
    border-radius: 4px !important;
    background-color: #ffffff !important;
    border: 1px solid #00f2fe !important;
    box-shadow: 0 0 12px rgba(0,242,254,0.8) !important;
    cursor: ew-resize !important;
}
/* Active Track Progress Color */
div[data-baseweb="slider"] > div > div > div:nth-child(1) {
    background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%) !important;
    height: 6px !important;
    border-radius: 3px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Kazmi Cloud Video Studio - Pro Studio")

# Helper: Seconds to MM:SS
def format_time(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes:02d}:{remaining_seconds:02d}"

# Helper: Safe Subclip
def safe_subclip(clip, start, end):
    if hasattr(clip, 'subclipped'):
        return clip.subclipped(start, end)
    return clip.subclip(start, end)

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
        st.markdown(f"**Duration:** {format_time(duration)} ({round(duration, 2)}s)")
        st.markdown(f"**Resolution:** {size[0]} x {size[1]}")
        st.markdown(f"**Frame Rate:** {fps} fps")
        
        st.divider()
        st.subheader("📐 Free Crop Settings")
        crop_mode = st.selectbox("Aspect Ratio Select Karein:", ["Original (No Crop)", "9:16 (Shorts / Reels)", "1:1 (Square)", "4:3 (Classic)"])
        
        st.divider()
        st.markdown("### ⚙️ Action Panel")
        render_btn = st.button("🚀 Render All Clips", use_container_width=True)

    with col_player:
        st.subheader("🎥 Live Video Preview & Connected Playhead")
        
        # Mode Selection
        edit_mode = st.radio("🛠️ Editing Tool:", ["✂️ Trim Range", "🔪 Multi-Split (Kai Tukron Mein Torna)"], horizontal=True)
        
        # 🔗 DIRECTLY CONNECTED PLAYHEAD / SLIDER
        if "Trim" in edit_mode:
            start_time, end_time = st.slider(
                "🎚️ CapCut Style Timeline (Select Start & End):",
                0.0, float(duration), (0.0, float(duration)), step=1.0
            )
            st.info(f"📍 **Trim Selection:** Start: `{format_time(start_time)}` ➔ End: `{format_time(end_time)}`")
            # Video automatically jumps to start_time when slider moves!
            st.video(output_path, start_time=int(start_time))
        else:
            split_time = st.slider(
                "🎚️ Timeline Playhead (Preview & Split Point):",
                0.0, float(duration), 0.0, step=1.0
            )
            split_input = st.text_input("Splits ke timestamps seconds ya minutes mein commas daal kar likhein (Maslan: `300, 600, 1200`):", str(int(split_time)))
            st.info(f"🔪 **Current Playhead Position:** `{format_time(split_time)}` — Yeh tool diye gaye points par video ko multi-split kar dega!")
            # Video jumps to the exact playhead position in split mode too!
            st.video(output_path, start_time=int(split_time))

    # 3. RENDERING ENGINE (Multi-Splits & Free Crop Support)
    if render_btn:
        original_clip = VideoFileClip(output_path)
        w, h = original_clip.size
        
        def apply_free_crop(clip_obj):
            if crop_mode == "Original (No Crop)":
                return clip_obj
            cw, ch = clip_obj.size
            if "9:16" in crop_mode:
                target_w = int(ch * 9 / 16)
                x_c = cw / 2
                return clip_obj.crop(x1=x_c - target_w/2, y1=0, x2=x_c + target_w/2, y2=ch)
            elif "1:1" in crop_mode:
                target = min(cw, ch)
                x_c, y_c = cw / 2, ch / 2
                return clip_obj.crop(x1=x_c - target/2, y1=y_c - target/2, x2=x_c + target/2, y2=y_c + target/2)
            elif "4:3" in crop_mode:
                target_w = int(ch * 4 / 3)
                x_c = cw / 2
                return clip_obj.crop(x1=x_c - target_w/2, y1=0, x2=x_c + target_w/2, y2=ch)
            return clip_obj

        if "Trim" in edit_mode:
            with st.spinner("Video trim aur crop ho rahi hai..."):
                edited_path = "output_trimmed.mp4"
                trimmed = safe_subclip(original_clip, start_time, end_time)
                final_trimmed = apply_free_crop(trimmed)
                final_trimmed.write_videofile(edited_path, codec="libx264", audio_codec="aac")
                
                st.success("✅ Trimmed & Cropped Video Tayyar Hai!")
                st.video(edited_path)
                with open(edited_path, "rb") as f:
                    st.download_button("📥 Download Trimmed Video", data=f, file_name="kazmi_trimmed.mp4", mime="video/mp4")
                
                final_trimmed.close()
                trimmed.close()
        
        else:
            with st.spinner("Video ko multiple hisson mein split aur render kiya ja raha hai..."):
                try:
                    user_splits = [0.0] + sorted([float(x.strip()) for x in split_input.split(",") if x.strip()]) + [float(duration)]
                    user_splits = sorted(list(set([s for s in user_splits if 0 <= s <= duration])))
                    
                    split_files = []
                    for i in range(len(user_splits) - 1):
                        s_time = user_splits[i]
                        e_time = user_splits[i+1]
                        if e_time - s_time < 1:
                            continue
                            
                        part_path = f"output_part_{i+1}.mp4"
                        if os.path.exists(part_path):
                            os.remove(part_path)
                            
                        chunk = safe_subclip(original_clip, s_time, e_time)
                        final_chunk = apply_free_crop(chunk)
                        final_chunk.write_videofile(part_path, codec="libx264", audio_codec="aac")
                        split_files.append((i+1, s_time, e_time, part_path))
                        
                        final_chunk.close()
                        chunk.close()
                    
                    st.success(f"✅ Kamyabi se {len(split_files)} tukron mein split ho gayi!")
                    
                    for part_num, st_t, en_t, p_path in split_files:
                        st.markdown(f"**Part {part_num}** (`{format_time(st_t)}` ➔ `{format_time(en_t)}`)")
                        st.video(p_path)
                        with open(p_path, "rb") as f:
                            st.download_button(f"📥 Download Part {part_num}", data=f, file_name=f"kazmi_part_{part_num}.mp4", mime="video/mp4", key=f"dl_{part_num}")
                        st.divider()
                        
                except Exception as e:
                    st.error(f"Split karne mein error aya: {e}")

        original_clip.close()
else:
    st.info("👈 Baraye meharbani sidebar mein Google Drive ka link de kar pehle video import karein!")
