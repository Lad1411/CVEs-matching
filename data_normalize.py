import json
from google import genai
import os
from dotenv import load_dotenv
from utils import read_content, to_native_python
from google.genai import types

def get_normalize_data(cve_list_path):

    load_dotenv()
    API_KEY = os.getenv("API_KEY")

    cve_list = read_content(cve_list_path)

    client = genai.Client(api_key=API_KEY)
    tools = [
        {'google_search': {}}
    ]


    prompt = f"""
    You are a cybersecurity expert. I have a list of CVEs below.
    Your task is to:
    1. Use Google Search to find the affected Major versions.
    2. For each Major version, find the EXACT **Release Date** of the vulnerable range and the fixed version.
    3. Normalize the data into the structure defined below.
    4. Return result as text
    
    Input CVE List:
    {cve_list}
    
    ---
    Required JSON Structure:
    {{
      "CVE-ID": {{
        "Dependency name": {{
          "Major_Version_Number": {{
            "vulnerable_range": {{
                 "start_date": "YYYY-MM-DD (Release date of first affected version or 'UNKNOWN')",
                 "end_date": "YYYY-MM-DD (Release date of last affected version)"
            }},
            "safe_min_version": {{
                 "version": "Fixed Version Number (or None)",
                 "release_date": "YYYY-MM-DD (Release date of the fixed version)"
            }}
          }}
        }}
      }}
    }}
    
    Constraint:
    - Date format MUST be YYYY-MM-DD.
    - If you cannot find the exact date after searching, write "UNKNOWN".
    - Do not make up dates.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=tools,
            automatic_function_calling={"disable": False}
        ),
    )

    return response.text