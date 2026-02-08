from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uuid
from datetime import datetime
from typing import List, Optional
from services.youtube import download_audio_and_metadata
from services.gemini import analyze_content
from services.document_generator import generate_documents
import shutil

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """Checks the health of the system (FFmpeg and API Key)."""
    ffmpeg_installed = shutil.which("ffmpeg") is not None
    node_installed = shutil.which("node") is not None
    api_key_set = bool(os.getenv("GOOGLE_API_KEY"))
    
    status = {
        "status": "healthy" if ffmpeg_installed and api_key_set else "unhealthy",
        "ffmpeg": "installed" if ffmpeg_installed else "missing",
        "node": "installed" if node_installed else "missing",
        "api_key": "set" if api_key_set else "missing"
    }
    return status

import json

from fastapi.staticfiles import StaticFiles

# Output directory
OUTPUT_DIR = "../output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mount static files
app.mount("/download", StaticFiles(directory=OUTPUT_DIR), name="download")

HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# History storage
history_log = load_history()

# Startup Event: Write Cookies
# Helper: Write Cookies at Import Time (Best for Docker/Render)
cookies_content = os.getenv("YOUTUBE_COOKIES")
if cookies_content:
    cookies_path = "cookies.txt"
    try:
        print(f"DEBUG: Found YOUTUBE_COOKIES env var (Length: {len(cookies_content)})")
        with open(cookies_path, "w") as f:
            f.write(cookies_content)
        print(f"DEBUG: Successfully wrote cookies to {cookies_path} (Size: {os.path.getsize(cookies_path)})")
    except Exception as e:
        print(f"DEBUG: Error writing cookies: {e}")
else:
    print("DEBUG: YOUTUBE_COOKIES env var NOT found at module level.")

# Helper: PO Token (Experimental)
po_token_content = os.getenv("YOUTUBE_PO_TOKEN")
if po_token_content:
    print(f"DEBUG: Found YOUTUBE_PO_TOKEN env var (Length: {len(po_token_content)})")
else:
    print("DEBUG: YOUTUBE_PO_TOKEN env var NOT found.")

# Helper: Render Secret File (Method 2 - More robust)
SECRET_FILE_PATH = "/etc/secrets/cookies.txt"
if os.path.exists(SECRET_FILE_PATH):
    print(f"DEBUG: Found Render Secret File at {SECRET_FILE_PATH}")
    # Symlink or copy to cookies.txt so yt-dlp finds it easily, 
    # OR just set COOKIES_FILE_PATH global to point there.
    # For now, let's copy it to be safe and consistent.
    try:
        import shutil
        shutil.copy(SECRET_FILE_PATH, "cookies.txt")
        print(f"DEBUG: Copied Secret File to cookies.txt")
    except Exception as e:
        print(f"DEBUG: Error copying Secret File: {e}")


    cookies_content = os.getenv("YOUTUBE_COOKIES")
    if cookies_content:
        cookies_path = "cookies.txt"
        print(f"DEBUG: Found YOUTUBE_COOKIES env var (Length: {len(cookies_content)})")
        with open(cookies_path, "w") as f:
            f.write(cookies_content)
        print(f"DEBUG: Successfully wrote cookies to {cookies_path}")
    else:
        print("DEBUG: YOUTUBE_COOKIES env var NOT found.")

@app.get("/debug_cookies")
def debug_cookies():
    """Debug endpoint to check if cookies file exists and read first lines."""
    debug_info = {
        "cookies_file": {"exists": False, "size": 0, "content_snippet": "N/A"},
        "secret_file": {
            "exists": os.path.exists("/etc/secrets/cookies.txt"), 
            "size": os.path.getsize("/etc/secrets/cookies.txt") if os.path.exists("/etc/secrets/cookies.txt") else 0
        },
        "env_vars": {
            "YOUTUBE_COOKIES": "Present" if os.getenv("YOUTUBE_COOKIES") else "Missing",
            "YOUTUBE_PO_TOKEN": "Present" if os.getenv("YOUTUBE_PO_TOKEN") else "Missing"
        }
    }

    if os.path.exists("cookies.txt"):
        try:
            size = os.path.getsize("cookies.txt")
            with open("cookies.txt", "r") as f:
                content = f.read(200) # Read first 200 chars to check format
            debug_info["cookies_file"] = {
                "exists": True,
                "size": size,
                "content_snippet": content 
            }
        except Exception as e:
            debug_info["cookies_file"]["error"] = str(e)
            
    return debug_info


class AnalyzeRequest(BaseModel):
    url: str
    options: List[str]  # "summary", "transcription_orig", "transcription_es", "guide"

@app.post("/analyze")
async def analyze_video(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    print(f"Received analysis request for URL: {request.url}")
    video_id = str(uuid.uuid4())[:8]
    
    try:
        # 1. Download Video/Audio (to base dir first to get metadata)
        try:
            video_data = download_audio_and_metadata(request.url, OUTPUT_DIR, video_id)
        except Exception as e:
            print(f"Download Error: {e}")
            raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

        
        # Create unique subdirectory
        safe_title = "".join([c for c in video_data.get('title', 'video') if c.isalnum() or c in (' ', '-', '_')]).strip().replace(' ', '_')
        video_output_dir = os.path.join(OUTPUT_DIR, f"{safe_title}_{video_id}")
        os.makedirs(video_output_dir, exist_ok=True)
        
        # Move audio file to subdirectory
        import shutil
        old_audio_path = video_data['audio_path']
        new_audio_path = os.path.join(video_output_dir, os.path.basename(old_audio_path))
        shutil.move(old_audio_path, new_audio_path)
        video_data['audio_path'] = new_audio_path
        
        # 2. Analyze with Gemini
        try:
            analysis_results = await analyze_content(video_data['audio_path'], request.options)
        except Exception as e:
            print(f"Analysis Error: {e}")
            raise HTTPException(status_code=500, detail=f"AI Analysis failed: {str(e)}")

        
        # 3. Generate Documents
        generated_files = generate_documents(analysis_results, video_data, video_output_dir, request.options)
        
        # 4. Update History
        entry = {
            "id": video_id,
            "title": video_data['title'],
            "url": request.url,
            "date": video_data['upload_date'],
            "report_date": datetime.now().strftime("%Y-%m-%d"),
            "dir_name": os.path.basename(video_output_dir), # Store dir name for frontend reconstruction
            "files": generated_files,
            "thumbnail": video_data['thumbnail']
        }
        history_log.append(entry)
        save_history(history_log)
        
        return entry

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def get_history():
    return history_log

@app.get("/clean_tmp")
def clean_tmp():
    # Helper to clean up audio files if needed
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
