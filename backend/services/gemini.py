import os
import google.generativeai as genai
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    # Just a warning, might crash later if not set
    print("WARNING: GOOGLE_API_KEY not found in environment variables.")

genai.configure(api_key=API_KEY)

async def analyze_content(audio_path: str, options: list) -> dict:
    """
    Uploads audio to Gemini and performs analysis based on options.
    """
    
    print(f"Uploading file: {audio_path}")
    audio_file = genai.upload_file(path=audio_path)
    
    # Wait for file to be active
    while audio_file.state.name == "PROCESSING":
        print("Waiting for audio processing...")
        time.sleep(2)
        audio_file = genai.get_file(audio_file.name)
        
    if audio_file.state.name == "FAILED":
        raise Exception("Audio processing failed.")

    print("Audio processing complete. Generating content...")

    model = genai.GenerativeModel('gemini-flash-latest')
    
    # Construct the prompt based on options
    prompt_parts = [
        "You are an expert video analyst and educational content creator.",
        "Analyze the provided audio from a YouTube video and generate the following outputs based on the requested sections.",
        "Please separate your response clearly with headers like '### SECTION_NAME'."
    ]

    prompt_parts.append("""
    Please include a section ### KEYWORDS at the beginning with a list of 5-10 relevant keywords/tags for this video.
    """)

    if "summary" in options:
        prompt_parts.append("""
        ### SUMMARY
        Generate an EXTENSIVE and DETAILED summary of the video content in Spanish.
        - Go deep into the details, arguments, and examples provided.
        - Do not be brief. Aim for a comprehensive overview that covers all aspects of the video.
        - Structure it with clear subheadings.
        """)
        
    if "transcription_orig" in options:
        prompt_parts.append("""
        ### TRANSCRIPTION_ORIG
        Provide a transcription of the video in its original language. 
        Identify different speakers (e.g., 'Speaker A', 'Speaker B') if possible. 
        Do not include timestamps.
        """)

    if "transcription_es" in options:
        prompt_parts.append("""
        ### TRANSCRIPTION_ES
        Provide a transcription of the video translated to Spanish.
        Identify different speakers.
        Do not include timestamps.
        """)
        
    if "guide" in options:
        prompt_parts.append("""
        ### GUIDE
        Create a comprehensive Didactic Guide (in Spanish) for the content.
        - Structure it as a professional course script or tutorial.
        - Section 1: Introduction & Learning Objectives.
        - Section 2: Detailed Content Modules (break down the video into logical lessons).
          - For each module, provide a detailed explanation and a text-based schema or infographic description.
        - Section 3: Key Takeaways & Conclusion.
        - Section 4: Quiz/Self-assessment questions.
        """)

    prompt_parts.append("Using the provided audio file, generate the response.")

    response = model.generate_content([audio_file, "\n".join(prompt_parts)])
    
    # Clean up file after generation (optional, but good practice if not needed anymore)
    # genai.delete_file(audio_file.name) 
    
    # Parse the response (Simple parsing by splitting headers)
    # This is a basic implementation. Ideally, we ask for JSON or robust delimiters.
    try:
        text_content = response.text
    except ValueError:
        print(f"Safety Feedback: {response.prompt_feedback}")
        raise Exception(f"Gemini refused to generate content. Safety feedback: {response.prompt_feedback}")
    
    results = {}
    
    # Very naive parsing, assuming the model follows instructions perfectly
    # A better way would be to ask for JSON output
    
    current_section = None
    buffer = []
    
    for line in text_content.split('\n'):
        if line.strip().startswith("### SUMMARY"):
            current_section = "summary"
            buffer = []
        elif line.strip().startswith("### TRANSCRIPTION_ORIG"):
            if current_section: results[current_section] = "\n".join(buffer).strip()
            current_section = "transcription_orig"
            buffer = []
        elif line.strip().startswith("### TRANSCRIPTION_ES"):
            if current_section: results[current_section] = "\n".join(buffer).strip()
            current_section = "transcription_es"
            buffer = []
        elif line.strip().startswith("### KEYWORDS"):
            if current_section: results[current_section] = "\n".join(buffer).strip()
            current_section = "keywords"
            buffer = []
        elif line.strip().startswith("### GUIDE"):
            if current_section: results[current_section] = "\n".join(buffer).strip()
            current_section = "guide"
            buffer = []
        else:
            if current_section:
                buffer.append(line)
    
    if current_section:
        results[current_section] = "\n".join(buffer).strip()

    return results
