import json
import os
from dotenv import load_dotenv

load_dotenv()

OUTPUT_PATH = os.getenv("OUTPUT_PATH")

def export_mcqs_to_json(mcqs, output_path=OUTPUT_PATH):
    try:
        with open(output_path, 'w') as f:
            json.dump(mcqs, f, indent=4)
        print(f"MCQs saved to {output_path}")
    except Exception as e:
        print(f"Error exporting MCQs to JSON: {e}")
