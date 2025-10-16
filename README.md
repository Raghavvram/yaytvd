# YouTube Video Downloader

A simple and user-friendly YouTube video downloader built with Python, Gradio, and yt-dlp.

## Features

- 🎬 Download YouTube videos in multiple formats
- 📊 View video details (title, uploader, duration)
- 🎯 Select specific video quality and format
- 💾 Choose custom save location
- ⚡ Auto-download best available quality option
- 🖥️ Clean and intuitive web interface

## Requirements

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. **Install required packages:**

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install gradio yt-dlp
```

## Usage

1. **Run the application:**

```bash
python youtube_downloader.py
```

2. **Open your browser:**
   - The application will automatically open at `http://127.0.0.1:7860`
   - If it doesn't open automatically, navigate to that URL manually

3. **Download videos:**
   - Paste a YouTube video URL
   - Click "Get Video Details"
   - Select your preferred format or enable auto-download
   - Specify save location (defaults to Downloads folder)
   - Click "Download Video"

## Features Explained

### Format Selection
The app provides various format options:
- **Best Available (Auto)**: Automatically selects the best quality
- **Video+Audio**: Complete video files with both video and audio
- **Video Only**: Video stream without audio
- **Audio Only**: Audio stream for music/podcasts

### Auto-Download
Enable the "Auto-download best available format" checkbox to skip manual format selection and automatically download the highest quality version.

### Save Location
Specify any folder path where you want to save the downloaded videos. The default is your Downloads folder.

## Troubleshooting

### Common Issues

1. **"ERROR: Unable to extract video data"**
   - Check if the URL is valid
   - Some videos may be region-restricted or private

2. **"ModuleNotFoundError"**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`

3. **Download fails**
   - Ensure you have write permissions for the save location
   - Check your internet connection
   - Update yt-dlp: `pip install --upgrade yt-dlp`

## Technical Details

- **Frontend**: Gradio (Python web UI framework)
- **Backend**: yt-dlp (YouTube download library)
- **Language**: Python 3

## Notes

- This tool is for personal use only
- Respect copyright and YouTube's terms of service
- Some videos may not be downloadable due to restrictions

## License

Free to use for personal projects.
