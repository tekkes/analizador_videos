import yt_dlp
import os

def download_audio_and_metadata(url: str, output_dir: str, video_id: str):
    """
    Downloads audio from YouTube video and returns metadata.
    """
    import shutil
    if not shutil.which("ffmpeg"):
        print("ERROR: FFmpeg not found in youtube.py check!")
        raise Exception("FFmpeg not found in system PATH.")

    print(f"Starting download for URL: {url} to {output_dir}")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/{video_id}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        audio_filename = os.path.splitext(filename)[0] + ".mp3"
        
        # Ensure path is correct as yt-dlp might put it different places depending on config
        # We forced outtmpl so it should be in output_dir
        
        return {
            "title": info.get('title', 'Unknown Title'),
            "upload_date": info.get('upload_date', 'Unknown Date'),
            "thumbnail": info.get('thumbnail', ''),
            "audio_path": audio_filename,
            "description": info.get('description', ''),
            "webpage_url": info.get('webpage_url', url),
            "uploader": info.get('uploader', 'Unknown Author')
        }
