import sys
import os
import asyncio
from fastapi import HTTPException

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app, health_check, analyze_video, AnalyzeRequest

def test_health_metrics():
    print("\n[Testing health_check logic]...")
    try:
        status = health_check()
        print(f"Status: {status}")
        if status["status"] == "healthy":
            print("PASS: System is healthy.")
        else:
            print("FAIL: System is unhealthy.")
    except Exception as e:
        print(f"FAIL: health_check error. {e}")

async def test_download_error_logic():
    print("\n[Testing analyze_video error logic]...")
    # Invalid URL to trigger yt-dlp error
    req = AnalyzeRequest(url="https://www.youtube.com/watch?v=INVALID_VIDEO_ID_12345", options=["summary"])
    
    try:
        await analyze_video(req, None)
        print("FAIL: Should have raised HTTPException")
    except HTTPException as e:
        print(f"Caught expected HTTPException: {e.detail}")
        if e.status_code == 500 and "Download failed" in e.detail:
            print("PASS: Correctly caught download error.")
        else:
            print(f"FAIL: Unexpected error details: {e.detail}")
    except Exception as e:
        print(f"FAIL: Unexpected exception type: {type(e)}")

if __name__ == "__main__":
    test_health_metrics()
    asyncio.run(test_download_error_logic())
