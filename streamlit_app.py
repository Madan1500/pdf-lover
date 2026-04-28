import os
import streamlit as st
import requests

# ── Backend endpoints ──────────────────────────────────────────────────────────
BACKEND_MERGE = os.getenv("BACKEND_MERGE", "http://127.0.0.1:8000/merge")
BACKEND_COMPRESS = os.getenv("BACKEND_COMPRESS", "http://127.0.0.1:8000/compress")

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PDFKit",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f0f0f !important;
    border-right: 1px solid #1e1e1e;
}
[data-testid="stSidebar"] * {
    color: #c8c8c8 !important;
}
[data-testid="stSidebar"] .sidebar-logo {
    padding: 1.5rem 1.25rem 1rem;
    border-bottom: 1px solid #1e1e1e;
    margin-bottom: 0.5rem;
}
[data-testid="stSidebar"] .sidebar-logo h1 {
    font-size: 1.4rem;
    font-weight: 600;
    color: #ffffff !important;
    letter-spacing: -0.5px;
    margin: 0;
}
[data-testid="stSidebar"] .sidebar-logo p {
    font-size: 0.72rem;
    color: #555 !important;
    margin: 2px 0 0;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* Nav buttons in sidebar */
[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    border: none !important;
    color: #888 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 400 !important;
    text-align: left !important;
    width: 100% !important;
    padding: 0.55rem 1.25rem !important;
    border-radius: 0 !important;
    transition: all 0.15s ease;
    cursor: pointer;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: #1a1a1a !important;
    color: #fff !important;
}
[data-testid="stSidebar"] .stButton.active-nav button {
    background: #1a1a1a !important;
    color: #ffffff !important;
    border-left: 2px solid #e05c2a !important;
}

/* ── Main area ── */
.main .block-container {
    padding: 2.5rem 3rem 3rem;
    max-width: 900px;
}

/* Page header */
.page-header {
    margin-bottom: 2.5rem;
}
.page-header h2 {
    font-size: 1.6rem;
    font-weight: 600;
    color: #111;
    letter-spacing: -0.5px;
    margin: 0 0 0.3rem;
}
.page-header p {
    color: #666;
    font-size: 0.88rem;
    margin: 0;
}

/* Home hero */
.home-hero {
    background: #0f0f0f;
    border-radius: 16px;
    padding: 3rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.home-hero::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: radial-gradient(circle, #e05c2a22 0%, transparent 70%);
}
.home-hero h1 {
    font-size: 2.4rem;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: -1px;
    margin: 0 0 0.6rem;
    line-height: 1.2;
}
.home-hero p {
    color: #888;
    font-size: 0.95rem;
    margin: 0;
    max-width: 480px;
    line-height: 1.6;
}

/* Feature cards */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.feature-card {
    background: #fafafa;
    border: 1px solid #ebebeb;
    border-radius: 12px;
    padding: 1.25rem;
    cursor: pointer;
    transition: all 0.15s ease;
}
.feature-card:hover {
    border-color: #e05c2a;
    box-shadow: 0 4px 16px #e05c2a18;
}
.feature-card .icon {
    font-size: 1.5rem;
    margin-bottom: 0.6rem;
    display: block;
}
.feature-card h3 {
    font-size: 0.9rem;
    font-weight: 600;
    color: #111;
    margin: 0 0 0.25rem;
}
.feature-card p {
    font-size: 0.78rem;
    color: #888;
    margin: 0;
    line-height: 1.5;
}

/* Upload zone */
.upload-hint {
    font-size: 0.8rem;
    color: #999;
    margin-top: 0.5rem;
}

/* Pill badge */
.badge {
    display: inline-block;
    background: #fff3ee;
    color: #e05c2a;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 20px;
    letter-spacing: 0.3px;
    margin-bottom: 1rem;
    text-transform: uppercase;
}

/* Divider */
.section-divider {
    border: none;
    border-top: 1px solid #ebebeb;
    margin: 1.5rem 0;
}

/* File list */
.file-list {
    background: #f7f7f7;
    border: 1px solid #e8e8e8;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin: 0.75rem 0 1rem;
}
.file-list .file-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 0;
    font-size: 0.83rem;
    color: #444;
    border-bottom: 1px solid #eeeeee;
}
.file-list .file-item:last-child { border-bottom: none; }
.file-list .file-item .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #e05c2a;
    flex-shrink: 0;
}

/* Primary action button override */
[data-testid="stButton"] > button[kind="primary"],
.stButton > button {
    background: #0f0f0f !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.55rem 1.5rem !important;
    transition: background 0.15s !important;
}
[data-testid="stButton"] > button:hover {
    background: #333 !important;
}

/* Sidebar section label */
.sidebar-section-label {
    font-size: 0.65rem;
    color: #444 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 1.25rem 1.25rem 0.4rem;
}

/* Coming soon */
.coming-soon-banner {
    background: #f7f7f7;
    border: 1px dashed #ddd;
    border-radius: 10px;
    padding: 2.5rem;
    text-align: center;
}
.coming-soon-banner p {
    color: #aaa;
    font-size: 0.9rem;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

# ── Session state for navigation ──────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h1>PDFKit</h1>
        <p>PDF Tools Suite</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">Navigation</div>', unsafe_allow_html=True)
    if st.button("🏠  Home"):
        st.session_state.page = "home"

    st.markdown('<div class="sidebar-section-label">Tools</div>', unsafe_allow_html=True)
    if st.button("🔗  Merge PDFs"):
        st.session_state.page = "merge"
    if st.button("✂️  Split PDF"):
        st.session_state.page = "split"
    if st.button("🔄  Convert PDF"):
        st.session_state.page = "convert"
    if st.button("🗜️  Compress PDF"):
        st.session_state.page = "compress"
    if st.button("🔒  Protect PDF"):
        st.session_state.page = "protect"
    if st.button("💧  Watermark"):
        st.session_state.page = "watermark"


# ── Page: Home ─────────────────────────────────────────────────────────────────
def page_home():
    st.markdown("""
    <div class="home-hero">
        <h1>Everything you need<br>for PDFs.</h1>
        <p>Merge, split, convert, compress and protect your PDF files — fast, simple, and right in your browser.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <span class="icon">🔗</span>
            <h3>Merge PDFs</h3>
            <p>Combine multiple PDF files into one in seconds.</p>
        </div>
        <div class="feature-card">
            <span class="icon">✂️</span>
            <h3>Split PDF</h3>
            <p>Extract pages or split a PDF into separate files.</p>
        </div>
        <div class="feature-card">
            <span class="icon">🔄</span>
            <h3>Convert</h3>
            <p>Convert PDF to Word, Excel, PNG, and more.</p>
        </div>
        <div class="feature-card">
            <span class="icon">🗜️</span>
            <h3>Compress</h3>
            <p>Reduce file size without losing quality.</p>
        </div>
        <div class="feature-card">
            <span class="icon">🔒</span>
            <h3>Protect</h3>
            <p>Add passwords and permissions to your PDFs.</p>
        </div>
        <div class="feature-card">
            <span class="icon">💧</span>
            <h3>Watermark</h3>
            <p>Add text or image watermarks to your PDFs.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="font-size:0.78rem; color:#bbb; text-align:center; margin-top:1rem;">
        Select a tool from the sidebar to get started.
    </p>
    """, unsafe_allow_html=True)


# ── Page: Merge ────────────────────────────────────────────────────────────────
def page_merge():
    st.markdown("""
    <div class="page-header">
        <span class="badge">Tool</span>
        <h2>Merge PDFs</h2>
        <p>Upload two or more PDF files and combine them into a single document.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded:
        file_items = "".join(
            f'<div class="file-item"><span class="dot"></span>{f.name}</div>'
            for f in uploaded
        )
        st.markdown(f"""
        <div class="file-list">{file_items}</div>
        <p class="upload-hint">{len(uploaded)} file{"s" if len(uploaded) != 1 else ""} selected</p>
        """, unsafe_allow_html=True)
    else:
        st.markdown(
            '<p class="upload-hint">No files selected yet. Drag & drop or click above.</p>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 4])
    with col1:
        merge_clicked = st.button("Merge PDFs", type="primary")

    if merge_clicked:
        if not uploaded:
            st.warning("Please upload at least two PDF files.")
        elif len(uploaded) < 2:
            st.warning("Please upload at least two PDF files to merge.")
        else:
            files = [
                ("files", (f.name, f.getvalue(), "application/pdf"))
                for f in uploaded
            ]
            with st.spinner("Merging your PDFs…"):
                try:
                    resp = requests.post(BACKEND_MERGE, files=files, stream=True, timeout=120)
                except Exception as e:
                    st.error(f"Request failed: {e}")
                else:
                    if resp.status_code == 200:
                        st.success("Merge complete! Your file is ready to download.")
                        st.download_button(
                            "⬇ Download merged PDF",
                            resp.content,
                            file_name="merged.pdf",
                            mime="application/pdf",
                        )
                    else:
                        st.error(f"Merge failed ({resp.status_code}): {resp.text}")


# ── Page: Coming soon (reusable) ───────────────────────────────────────────────
def page_coming_soon(title, icon, description):
    st.markdown(f"""
    <div class="page-header">
        <span class="badge">Tool</span>
        <h2>{icon} {title}</h2>
        <p>{description}</p>
    </div>
    <div class="coming-soon-banner">
        <p style="font-size:2rem; margin-bottom:0.5rem;">🚧</p>
        <p>This tool is coming soon.<br>Check back shortly!</p>
    </div>
    """, unsafe_allow_html=True)


# ── Router ─────────────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "home":
    page_home()
elif page == "merge":
    page_merge()
elif page == "split":
    page_coming_soon("Split PDF", "✂️", "Extract specific pages or split a PDF into separate files.")
elif page == "convert":
    page_coming_soon("Convert PDF", "🔄", "Convert your PDF to Word, Excel, PNG, JPEG, and more.")
elif page == "compress":
    # Implement compress page
    def page_compress():
        st.markdown("""
        <div class="page-header">
            <span class="badge">Tool</span>
            <h2>Compress PDF</h2>
            <p>Upload a PDF and reduce its size by lowering image quality.</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Upload a PDF file to compress",
            type=["pdf"],
            accept_multiple_files=False,
            label_visibility="collapsed",
        )

        quality = st.slider("Image quality (lower = smaller file)", min_value=10, max_value=95, value=60)

        use_range = st.checkbox("Use page range", value=False)
        start_page = None
        end_page = None
        if use_range:
            cols = st.columns(2)
            with cols[0]:
                start_page = st.number_input("Start page", min_value=1, value=1, step=1)
            with cols[1]:
                end_page = st.number_input("End page", min_value=1, value=1, step=1)

        if uploaded:
            st.markdown(f"<div class='file-list'><div class='file-item'><span class='dot'></span>{uploaded.name}</div></div>", unsafe_allow_html=True)

        # Preview size automatically when inputs change
        preview_col = st.empty()
        preview_text = ""
        if uploaded:
            try:
                files = [("file", (uploaded.name, uploaded.getvalue(), "application/pdf"))]
                data = {"quality": str(quality), "preview": "true"}
                if use_range:
                    data["start_page"] = str(start_page)
                    data["end_page"] = str(end_page)
                preview_col.info("Estimating compressed size...")
                resp = requests.post(BACKEND_COMPRESS, files=files, data=data, timeout=120)
                if resp.status_code == 200:
                    js = resp.json()
                    size_bytes = js.get("size_bytes")
                    if size_bytes is not None:
                        kb = size_bytes / 1024
                        if kb < 1024:
                            preview_text = f"Estimated size: {kb:.1f} KB"
                        else:
                            preview_text = f"Estimated size: {kb/1024:.2f} MB"
                        preview_col.success(preview_text)
                    else:
                        preview_col.warning("Could not determine size preview.")
                else:
                    preview_col.error(f"Compression preview failed ({resp.status_code}): {resp.text}")
            except Exception as e:
                preview_col.error(f"Preview request failed: {e}")

        if st.button("Compress PDF"):
            if not uploaded:
                st.warning("Please upload a PDF file to compress.")
            else:
                files = [("file", (uploaded.name, uploaded.getvalue(), "application/pdf"))]
                data = {"quality": str(quality)}
                if use_range:
                    data["start_page"] = str(start_page)
                    data["end_page"] = str(end_page)
                with st.spinner("Compressing..."):
                    try:
                        resp = requests.post(BACKEND_COMPRESS, files=files, data=data, stream=True, timeout=180)
                    except Exception as e:
                        st.error(f"Request failed: {e}")
                    else:
                        if resp.status_code == 200:
                            st.success("Compression complete — download below")
                            st.download_button("⬇ Download compressed PDF", resp.content, file_name="compressed.pdf", mime="application/pdf")
                        else:
                            st.error(f"Compression failed ({resp.status_code}): {resp.text}")

    page_compress()
elif page == "protect":
    page_coming_soon("Protect PDF", "🔒", "Add passwords and restrict permissions on your PDFs.")
elif page == "watermark":
    page_coming_soon("Watermark PDF", "💧", "Stamp a text or image watermark on every page.")