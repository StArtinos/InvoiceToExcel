from ai import ClaudeMF
from prompts import FELIPACK_PROMPT
import os
import PyPDF2
import re
import json
import pandas as pd
import datetime


felipack = ClaudeMF(sys_prompt=FELIPACK_PROMPT)
directory = 'Input'
output_directory = 'Output'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

all_data = []

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        with open(os.path.join(directory, filename), 'r') as file:
            content = file.read()
    elif filename.endswith(".pdf"):
        with open(os.path.join(directory, filename), 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content = " ".join([page.extract_text() for page in reader.pages])
    else:
        continue  # Skip files that are neither .txt nor .pdf
    response = felipack.chat(content)
    json_pattern = re.compile(r'<json>(.*?)</json>', re.DOTALL)
    json_match = json_pattern.search(response)


    if json_match:
        json_str = json_match.group(1)
        print("Extracted JSON string:", json_str)  # For debugging

        # Write raw JSON string to a file for debugging
        with open('raw_json.txt', 'w', encoding='utf-8') as f:
            f.write(json_str)

        try:
            # Replace single quotes with double quotes
            json_str = json_str.replace("'", '"')

            # Parse the JSON string
            json_data = json.loads('[' + json_str + ']')

            # Convert to DataFrame
            df = pd.DataFrame(json_data)

            # Generate filename with current date and time
            current_time = datetime.datetime.now()
            filename = f"invoice_{current_time.strftime('%Y%m%d_%H%M%S')}.xlsx"

            # Ensure the Output directory exists
            os.makedirs('Output', exist_ok=True)

            # Write to Excel with the new filename
            output_path = os.path.join('Output', filename)
            df.to_excel(output_path, index=False)
            print(f"Excel file '{output_path}' has been created successfully.")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print("Please check the 'raw_json.txt' file for the raw JSON string.")
    else:
        print("No JSON data found in the response.")