import requests
import json

url = "http://localhost:8000/analyze"
data = {
    "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw", # Me at the zoo (Short, fast)
    "options": ["summary", "guide", "transcription_orig"]
}

try:
    print(f"Sending POST request to {url}...")
    response = requests.post(url, json=data, timeout=120) # Increased timeout for analysis
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("Analysis success!")
        print(json.dumps(result, indent=2))
        
        # Test download of the PDF Guide if available
        if "guide_pdf" in result["files"]:
            dl_url = f"http://localhost:8000{result['files']['guide_pdf']}"
            print(f"Testing download: {dl_url}")
            dl_res = requests.get(dl_url)
            print(f"Download Status: {dl_res.status_code}")
            print(f"File Size: {len(dl_res.content)} bytes")
    else:
        print(f"Response: {response.text}")

except Exception as e:
    print(f"Request failed: {e}")
