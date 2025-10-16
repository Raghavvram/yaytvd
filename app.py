import gradio as gr
import yt_dlp
import os
import webbrowser
from pathlib import Path
from threading import Timer

# --- Helper Functions ---

def open_browser():
    """Automatically open the app URL in default browser."""
    webbrowser.open("http://127.0.0.1:7860")

def extract_dir(file_paths):
    """
    Given a list of file paths returned by gr.File(
    file_count="directory"), return the parent directory.
    """
    if not file_paths:
        return str(Path.home() / "Downloads")
    # file_paths is a list of absolute file paths under the selected directory
    dir_path = os.path.dirname(file_paths[0])
    return dir_path

# --- Core Downloader Class ---

class YouTubeDownloader:
    def __init__(self):
        self.video_info = None
        self.formats = []

    def get_video_info(self, url):
        """Fetch video metadata and available formats."""
        if not url or not url.strip():
            return (
                gr.update(choices=[], value=None, visible=False),
                "",
                "❌ Please enter a valid YouTube URL",
                gr.update(visible=False)
            )
        try:
            ydl_opts = {"quiet": True, "no_warnings": True, "extract_flat": False}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.video_info = ydl.extract_info(url, download=False)

            title    = self.video_info.get("title", "Unknown")
            duration = self.video_info.get("duration", 0)
            uploader = self.video_info.get("uploader", "Unknown")
            minutes, seconds = divmod(duration, 60)
            duration_str = f"{int(minutes)}:{int(seconds):02d}"

            # Build format list
            self.formats = ["best"]
            format_choices = ["Best Available (Auto)"]
            for fmt in self.video_info.get("formats", []):
                fmt_id    = fmt.get("format_id")
                ext       = fmt.get("ext", "unknown")
                res       = fmt.get("resolution", "audio only")
                vcodec    = fmt.get("vcodec", "none")
                acodec    = fmt.get("acodec", "none")
                fsize     = fmt.get("filesize", 0)
                if vcodec != "none" and acodec != "none":
                    ftype = "Video+Audio"
                elif vcodec != "none":
                    ftype = "Video Only"
                elif acodec != "none":
                    ftype = "Audio Only"
                else:
                    continue
                size_str = f"{fsize/1024/1024:.1f} MB" if fsize else "Unknown size"
                desc = f"{ftype} - {res} - {ext} - {size_str}"
                format_choices.append(desc)
                self.formats.append(fmt_id)

            info_md = (
                "### 📹 Video Information\n\n"
                f"**Title:** {title}  \n"
                f"**Uploader:** {uploader}  \n"
                f"**Duration:** {duration_str}  \n"
                f"**Available Formats:** {len(format_choices)}"
            )
            return (
                gr.update(choices=format_choices, value=format_choices[0], visible=True),
                info_md,
                "✅ Video details fetched successfully!",
                gr.update(visible=True)
            )
        except Exception as e:
            return (
                gr.update(choices=[], value=None, visible=False),
                "",
                f"❌ Error: {str(e)}",
                gr.update(visible=False)
            )

    def download_video(self, url, format_choice, save_location, auto_download):
        """Download the video based on user selection."""
        if not url or not url.strip():
            return "❌ Please enter a valid YouTube URL"
        if not save_location or not os.path.isdir(save_location):
            return "❌ Please select a valid save location"
        try:
            # Determine format code
            if auto_download or format_choice == "Best Available (Auto)":
                fmt_code = "best"
            else:
                idx = format_choice and 1
                fmt_code = self.formats[idx] if idx < len(self.formats) else "best"

            ydl_opts = {
                "format": fmt_code,
                "outtmpl": os.path.join(save_location, "%(title)s.%(ext)s"),
                "progress_hooks": []
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            return f"✅ Download completed successfully!\n📁 Saved to: {filename}"
        except Exception as e:
            return f"❌ Download failed: {str(e)}"

# --- Instantiate Downloader ---

downloader = YouTubeDownloader()

# --- Gradio Interface ---

dark_css = """
.container {
  max-width: 900px;
  margin: auto;
  padding: 24px;
  font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
}
.header {
  text-align: center;
  margin-bottom: 32px;
}
.main-content {
  background: #23272f;
  color: #f2f2f2;
  padding: 20px;
  border-radius: 14px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.18);
}
.info-section {
  background: #22252c;
  color: #e0e3e9;
  padding: 14px;
  border-radius: 10px;
  margin: 12px 0;
}
.status-box {
  background: #181c20;
  color: #e0e3e9;
  padding: 18px;
  border-radius: 10px;
}
.gradio-dropdown, .gradio-textbox, .gradio-checkbox label {
  font-size: 17px;
  border-radius: 7px;
  padding: 10px 14px;
  background: #262a32;
  color: #f2f2f2;
}
.gradio-button {
  font-size: 18px;
  border-radius: 8px;
  padding: 12px 22px;
}
.gradio-file {
  font-size: 17px;
  border-radius: 7px;
  padding: 10px 14px;
  background: #262a32;
  color: #f2f2f2;
}
footer { display: none !important; }
"""

with gr.Blocks(
    title="YouTube Video Downloader",
    theme=gr.themes.Monochrome(),
    css=dark_css
) as app:

    with gr.Column(elem_classes="container"):
        # Header
        with gr.Row(elem_classes="header"):
            gr.Markdown(
                "# 🎥 YouTube Video Downloader\n"
                "### Download YouTube videos in your preferred format using yt-dlp"
            )

        # Main content
        with gr.Column(elem_classes="main-content"):
            # URL & fetch
            with gr.Row():
                with gr.Column(scale=5):
                    url_input = gr.Textbox(
                        label="YouTube Video URL",
                        placeholder="https://www.youtube.com/watch?v=...",
                        lines=1
                    )
                with gr.Column(scale=1, min_width=150):
                    fetch_btn = gr.Button("🔍 Get Details", variant="primary", size="lg")

            # Status & info
            with gr.Row():
                with gr.Column(scale=1):
                    status_msg = gr.Textbox(
                        label="📊 Status",
                        lines=4,
                        interactive=False,
                        elem_classes="status-box"
                    )
                with gr.Column(scale=1):
                    video_info = gr.Markdown(
                        "*No video loaded yet*",
                        elem_classes="info-section"
                    )

            # Download options (hidden initially)
            with gr.Row(visible=False) as download_section:
                with gr.Column():
                    with gr.Row():
                        with gr.Column(scale=2):
                            format_dropdown = gr.Dropdown(
                                label="📝 Select Format",
                                choices=[],
                                interactive=True
                            )
                        with gr.Column(scale=2):
                            save_location = gr.Textbox(
                                label="💾 Save Location",
                                value=str(Path.home() / "Music"),
                                lines=1,
                                interactive=True
                            )
                    with gr.Row():
                        with gr.Column(scale=3):
                            auto_download_check = gr.Checkbox(
                                label="⚡ Auto-download best available format",
                                value=False
                            )
                        with gr.Column(scale=1, min_width=150):
                            download_btn = gr.Button(
                                "⬇️ Download",
                                variant="secondary",
                                size="lg"
                            )

        # Instructions accordion
        with gr.Accordion("📝 How to Use", open=False):
            gr.Markdown(
                "1. Paste URL and click **Get Details**\n"
                "2. Select format or enable auto-download\n"
                "3. Choose folder (above) to set save location\n"
                "4. Click **Download**\n"
            )

    # Event bindings
    fetch_btn.click(
        fn=downloader.get_video_info,
        inputs=[url_input],
        outputs=[format_dropdown, video_info, status_msg, download_section]
    )
    download_btn.click(
        fn=downloader.download_video,
        inputs=[url_input, format_dropdown, save_location, auto_download_check],
        outputs=[status_msg]
    )

if __name__ == "__main__":
    Timer(1.5, open_browser).start()
    app.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=False,
        show_error=True
    )
