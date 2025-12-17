import google.generativeai as genai
import os
from dotenv import load_dotenv
from utils import read_content, save_result_to_file
from data_normalize import get_normalize_data
import argparse
load_dotenv()

API_KEY =  os.getenv('API_KEY')

def get_args():
    parser = argparse.ArgumentParser(description= "CVEs matching")
    parser.add_argument("--input_cve", "-c", type= str, help= "Path of cve list", required=True)
    parser.add_argument("--input_asset", "-a", type= str, help= "Path of asset list", required=True)
    parser.add_argument("--save_file", "-s", type=str, help="Save result to this path", required=True)
    args = parser.parse_args()
    return args

args = get_args()

input_cve = get_normalize_data(args.input_cve)
input_asset = read_content(args.input_asset)

genai.configure(api_key=API_KEY)
generation_config = {
    "temperature": 0.2,
}
tool = [save_result_to_file]
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    generation_config=generation_config,
    tools = tool
)

chat = model.start_chat(enable_automatic_function_calling=True)

prompt = f'''
INPUT CVE: 
<cve_list>
{input_cve}
</cve_list>
INPUT ASSET: 
<assets>
{input_asset}
</assets>

For each item in my input asset, match it with my input cve
If it is not in my cve list it is SAFE
If it is in my cve list:
1. Use Google search to find the release date of my current version
2. If release date in vulnerable_range: it is UNSAFE
3. If release date >= safe_min_version date: it is SAFE
4. Result is a list of dictinonaries:'dependency name': 'SAFE or UNSAFE'
5. Finally, call the function `save_result_to_file` with the content argument containing ONLY the valid JSON string of the results to save content to {args.save_file}.
'''

response = chat.send_message(prompt)
print(response.text)
