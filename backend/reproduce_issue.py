import os
import sys
import traceback
import asyncio
from dotenv import load_dotenv

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.youtube import download_audio_and_metadata
from services.gemini import analyze_content
from services.document_generator import generate_documents

load_dotenv()

async def reproduce():
    print("--- Starting Reproduction Script ---")
    
    # 1. Check Environment
    print("\n[1] Checking Environment...")
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY not found in env.")
        return
    print("GOOGLE_API_KEY found.")
    
    import shutil
    if not shutil.which("ffmpeg"):
        print("ERROR: FFmpeg not found in PATH.")
        return
    print("FFmpeg found.")

    # 2. Mock Request
    print("\n[2] Mocking Request...")
    # Use a short, known video for testing
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw" # Me at the zoo
    test_options = ["summary", "keywords"]
    output_dir = "../output"
    os.makedirs(output_dir, exist_ok=True)
    video_id = "test_debug"

    try:
        # 3. Download
        print(f"\n[3] Testing Download for {test_url}...")
        video_data = download_audio_and_metadata(test_url, output_dir, video_id)
        print("Download successful.")
        print(f"Metadata: {video_data.keys()}")

        # 4. Analyze
        print(f"\n[4] Testing Gemini Analysis with audio: {video_data['audio_path']}...")
        analysis_results = await analyze_content(video_data['audio_path'], test_options)
        print("Analysis successful.")
        print(f"Results keys: {analysis_results.keys()}")

        # 5. Generate Docs
        print("\n[5] Testing Document Generation...")
        safe_title = "debug_test"
        video_output_dir = os.path.join(output_dir, f"{safe_title}_{video_id}")
        os.makedirs(video_output_dir, exist_ok=True)
        
        generated_files = generate_documents(analysis_results, video_data, video_output_dir, test_options)
        print(f"Generation successful. Files: {generated_files}")
        
        print("\n--- Reproduction Complete: SUCCESS ---")

    except Exception as e:
        print(f"\n--- Reproduction Complete: FAILED ---")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(reproduce())
