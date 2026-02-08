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
        'quiet': False, # Enable logs
        'no_warnings': False, # Enable warnings
        'verbose': True, # FORCE VERBOSE LOGGING
    }
    
    # Check for cookies file
    # Check for cookies file
    if os.path.exists("cookies.txt"):
        print(f"DEBUG: youtube.py found cookies.txt (Size: {os.path.getsize('cookies.txt')} bytes)")
        ydl_opts['cookiefile'] = "cookies.txt"
    else:
        print("DEBUG: youtube.py did NOT find cookies.txt")

    # Check for PO Token
    po_token = os.getenv("YOUTUBE_PO_TOKEN")
    if po_token:
        print("DEBUG: Using YOUTUBE_PO_TOKEN")
        ydl_opts['extractor_args'] = {'youtube': {'po_token': [po_token]}}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            audio_filename = os.path.splitext(filename)[0] + ".mp3"
            
            return {
                "title": info.get('title', 'Unknown Title'),
                "upload_date": info.get('upload_date', 'Unknown Date'),
                "thumbnail": info.get('thumbnail', ''),
                "audio_path": audio_filename,
                "description": info.get('description', ''),
                "webpage_url": info.get('webpage_url', url),
                "uploader": info.get('uploader', 'Unknown Author')
            }
            
    except yt_dlp.utils.DownloadError as e:
        print(f"WARNING: Download failed with primary options. Error: {e}")
        print("WARNING: Retrying with fallback configuration (Format: best)...")
        
        # Fallback: Simple 'best' format (video+audio) and extract audio.
        # Create a FRESH options dictionary to avoid any pollution
        fallback_opts = {
            'format': 'best', # Explicitly request 'best' which is usually available
            'outtmpl': f'{output_dir}/{video_id}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,
            'verbose': True,
            'no_warnings': False,
        }
        
        if os.path.exists("cookies.txt"):
             fallback_opts['cookiefile'] = "cookies.txt"
        
        # Try PO token again if present
        if po_token:
             fallback_opts['extractor_args'] = {'youtube': {'po_token': [po_token]}}

        try:
            with yt_dlp.YoutubeDL(fallback_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                audio_filename = os.path.splitext(filename)[0] + ".mp3"
                
                return {
                    "title": info.get('title', 'Unknown Title'),
                    "upload_date": info.get('upload_date', 'Unknown Date'),
                    "thumbnail": info.get('thumbnail', ''),
                    "audio_path": audio_filename,
                    "description": info.get('description', ''),
                    "webpage_url": info.get('webpage_url', url),
                    "uploader": info.get('uploader', 'Unknown Author')
                }
        except Exception as retry_error:
            print(f"ERROR: Fallback download also failed: {retry_error}")
            # Raise the ORIGINAL error as it's usually more descriptive, 
            # unless the retry error is different.
            raise e
