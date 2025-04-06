#!/usr/bin/env python3
"""
YouTube Video Transcriber

This script downloads a YouTube video and transcribes it using Faster-Whisper.
"""

import os
import argparse
import tempfile
import yt_dlp
from faster_whisper import WhisperModel

def download_audio(youtube_url, output_path=None):
    """
    Download the audio from a YouTube video using yt-dlp.
    
    Args:
        youtube_url (str): The URL of the YouTube video
        output_path (str, optional): Path to save the audio file. If None, uses a temporary directory.
        
    Returns:
        tuple: (Path to the downloaded audio file, Video title)
    """
    print(f"Downloading audio from: {youtube_url}")
    
    # Use a temporary directory if no output path is specified
    if not output_path:
        output_dir = tempfile.gettempdir()
        video_id = youtube_url.split("v=")[-1].split("&")[0]
        output_file = os.path.join(output_dir, f"youtube_audio_{video_id}")
    else:
        output_file = output_path
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_file,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': False
    }
    
    # Download the audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        title = info.get('title', 'Unknown Title')
    
    # yt-dlp may add extensions or modify the path
    actual_file = output_file + ".mp3"
    if os.path.exists(actual_file):
        output_file = actual_file
    
    print(f"Audio downloaded to: {output_file}")
    return output_file, title

def transcribe_audio(audio_path, model_size="base", output_format="txt", output_path=None):
    """
    Transcribe the audio using Faster-Whisper.
    
    Args:
        audio_path (str): Path to the audio file
        model_size (str): Size of the Whisper model to use
        output_format (str): Format to save the transcription (txt, srt, vtt)
        output_path (str, optional): Path to save the transcription. If None, outputs to console.
        
    Returns:
        str: The transcription text
    """
    print(f"Transcribing audio using {model_size} model...")
    
    # Load the Whisper model
    model = WhisperModel(model_size)
    
    # Transcribe the audio
    segments, info = model.transcribe(audio_path)
    
    # Process the transcription based on the output format
    if output_format == "txt":
        transcript = ""
        for segment in segments:
            transcript += segment.text + " "
        
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(transcript)
            print(f"Transcription saved to: {output_path}")
        else:
            print("\nTranscription:")
            print(transcript)
        
        return transcript
    
    elif output_format in ["srt", "vtt"]:
        try:
            # Try to import format_timestamp from faster_whisper.utils
            from faster_whisper.utils import format_timestamp
        except ImportError:
            # Define our own format_timestamp function if import fails
            def format_timestamp(seconds, always_include_hours=False, decimal_marker='.'):
                hours = int(seconds / 3600)
                seconds %= 3600
                minutes = int(seconds / 60)
                seconds %= 60
                
                if always_include_hours or hours > 0:
                    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace('.', decimal_marker)
                else:
                    return f"{minutes:02d}:{seconds:06.3f}".replace('.', decimal_marker)
        
        transcript = []
        for i, segment in enumerate(segments):
            if output_format == "srt":
                # SRT format
                transcript.append(f"{i+1}")
                transcript.append(f"{format_timestamp(segment.start, always_include_hours=True)} --> {format_timestamp(segment.end, always_include_hours=True)}")
                transcript.append(segment.text)
                transcript.append("")
            else:
                # VTT format
                if i == 0:
                    transcript.append("WEBVTT")
                    transcript.append("")
                transcript.append(f"{format_timestamp(segment.start, always_include_hours=True, decimal_marker='.')} --> {format_timestamp(segment.end, always_include_hours=True, decimal_marker='.')}")
                transcript.append(segment.text)
                transcript.append("")
        
        transcript_text = "\n".join(transcript)
        
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(transcript_text)
            print(f"Transcription saved to: {output_path}")
        else:
            print("\nTranscription:")
            print(transcript_text)
        
        return transcript_text

def main():
    """Main function to parse arguments and run the transcription."""
    parser = argparse.ArgumentParser(description="Transcribe a YouTube video")
    parser.add_argument("url", help="URL of the YouTube video")
    parser.add_argument("--model", choices=["tiny", "base", "small", "medium", "large"], default="base", 
                        help="Size of the Whisper model to use (default: base)")
    parser.add_argument("--format", choices=["txt", "srt", "vtt"], default="txt", 
                        help="Output format for the transcription (default: txt)")
    parser.add_argument("--output", help="Path to save the transcription (default: video_title.format)")
    parser.add_argument("--keep-audio", action="store_true", help="Keep the downloaded audio file")
    parser.add_argument("--audio-output", help="Path to save the audio file")
    
    args = parser.parse_args()
    
    # Download the audio
    audio_path, video_title = download_audio(args.url, args.audio_output)
    
    # Generate default output path if not provided
    if not args.output:
        safe_title = "".join([c if c.isalnum() or c in " ._-" else "_" for c in video_title])
        args.output = f"{safe_title}.{args.format}"
    
    # Transcribe the audio
    transcribe_audio(audio_path, args.model, args.format, args.output)
    
    # Clean up the audio file if not keeping it
    if not args.keep_audio and not args.audio_output:
        try:
            os.remove(audio_path)
            print(f"Deleted temporary audio file: {audio_path}")
        except OSError as e:
            print(f"Warning: Could not delete temporary audio file: {e}")

if __name__ == "__main__":
    main()
