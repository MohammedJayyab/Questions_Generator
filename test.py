import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def test_openai_api():
    try:
        response = openai.client.chat.completions   .create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Generate a sample question"}
            ]
        )
        print("Response:", response.choices[0].message['content'].strip())
    except Exception as e:
        print("Error:", e)

# Run the test function
test_openai_api()