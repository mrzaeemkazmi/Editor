import streamlit as st
import streamlit.components.v1 as components

# Page Layout Setup
st.set_page_config(page_title="Kazmi Cloud Video Editor", layout="wide")

# Custom Dark Styling
st.markdown("""
<style>
    .stApp { background-color: #0e0e10; color: #ffffff; }
    div[data-testid="stSidebar"] { background-color: #18181c; }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.header("📁 Media & Import")
    drive_link = st.text_input("Google Drive Shareable Link:", value="https://drive.google.com/file/d/1yLV1xlU")
    if st.button("📥 Import Video"):
        st.success("Video Loaded Successfully!")

# ----------------- PLAYER & DETAILS -----------------
col1, col2 = st.columns([2.5, 1])

with col1:
    st.subheader("📺 Video Player Preview")
    # Video player placeholder
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

with col2:
    st.subheader("📊 Video Details")
    st.write("**Duration:** 06:49 (409.03s)")
    st.write("**Resolution:** 426 x 240")
    st.write("**Frame Rate:** 24.0 fps")

st.divider()

# ----------------- PLAYHEAD & TIMELINE -----------------
st.subheader("✂️ Playhead & Timeline Studio")

# Interactive Visual Playhead Component (HTML + JS)
timeline_html = """
<style>
    .timeline-container {
        position: relative;
        width: 100%;
        height: 100px;
        background-color: #121214;
        border: 1px solid #2a2a2e;
        border-radius: 8px;
        user-select: none;
        overflow: hidden;
        cursor: pointer;
    }
    .time-ruler {
        position: absolute;
        top: 5px;
        width: 100%;
        display: flex;
        justify-content: space-between;
        padding: 0 15px;
        color: #71717a;
        font-size: 11px;
        font-family: monospace;
    }
    .video-track {
        position: absolute;
        top: 32px;
        left: 15px;
        right: 15px;
        height: 48px;
        background: #064e3b;
        border: 1px solid #10b981;
        border-radius: 4px;
        display: flex;
        align-items: center;
        padding-left: 12px;
        color: #e4e4e7;
        font-size: 12px;
        font-weight: 600;
    }
    /* CapCut Vertical White Playhead Line */
    .playhead-line {
        position: absolute;
        top: 0;
        bottom: 0;
        width: 2px;
        background-color: #ffffff;
        box-shadow: 0 0 8px rgba(255, 255, 255, 0.9);
        z-index: 10;
        left: 20%;
    }
    .playhead-pointer {
        position: absolute;
        top: 0;
        left: -6px;
        width: 14px;
        height: 12px;
        background-color: #ffffff;
        clip-path: polygon(0 0, 100% 0, 50% 100%);
    }
</style>

<div class="timeline-container" id="timeline">
    <div class="time-ruler">
        <span>00:00</span>
        <span>01:40</span>
        <span>03:20</span>
        <span>05:00</span>
        <span>06:49</span>
    </div>
    <div class="video-track">🎬 Video Track (17 Rabi Ul Awal...)</div>
    <div class="playhead-line" id="playhead">
        <div class="playhead-pointer"></div>
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

# Render Playhead HTML Component
components.html(timeline_html, height=115)

# Backend Time Range Slider
st.caption("Playhead Range Selection (Seconds):")
start_time, end_time = st.slider(
    "Playhead Position Selector",
    min_value=0.0,
    max_value=409.03,
    value=(67.0, 131.0),
    step=1.0,
    label_visibility="collapsed"
)

st.info(f"📍 **Current Selection:** Start: `{start_time}s` ➔ End: `{end_time}s` | **Selected Duration:** `{round(end_time - start_time, 2)}s`")
