# YouTube Video Transcriber

This tool downloads YouTube videos and transcribes them using Faster-Whisper, a fast implementation of OpenAI's Whisper model.

## Features

- Download audio from YouTube videos using yt-dlp (more reliable than pytube)
- Transcribe audio using Faster-Whisper
- Support for multiple output formats (TXT, SRT, VTT)
- Various Whisper model sizes for different accuracy/speed trade-offs

## Requirements

- Python 3.7+
- FFmpeg (system dependency)

## Installation

1. Clone this repository:
```
git clone https://github.com/ntalekt/youtube-transcriber.git
cd youtube-transcriber
```

2. Install the required Python packages:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Install FFmpeg (if not already installed):
- **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

## Usage

Basic usage:
```
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

This will download the audio from the YouTube video, transcribe it using the base Whisper model, and output the transcription to a text file named after the video title.

### Advanced Options
```
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
--model medium
--format srt
--output my_transcript.srt
--keep-audio
--audio-output my_audio.mp3
```

#### Arguments
- `url`: URL of the YouTube video (required)
- `--model`: Size of the Whisper model to use (choices: tiny, base, small, medium, large; default: base)
- `--format`: Output format for the transcription (choices: txt, srt, vtt; default: txt)
- `--output`: Path to save the transcription (default: video_title.format)
- `--keep-audio`: Keep the downloaded audio file (default: false)
- `--audio-output`: Path to save the audio file (default: temporary file)

## Model Size Comparison

| Model | Parameters | Accuracy | Speed | Disk Space |
|-------|------------|----------|-------|------------|
| tiny  | 39M        | Lowest   | Fastest | ~80MB    |
| base  | 74M        | Low      | Fast    | ~150MB   |
| small | 244M       | Medium   | Medium  | ~500MB   |
| medium| 769M       | High     | Slow    | ~1.5GB   |
| large | 1550M      | Highest  | Slowest | ~3GB     |

Choose the model size based on your accuracy requirements and available resources.

## License

MIT


