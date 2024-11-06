import os
from openai import OpenAI
from dotenv import load_dotenv
from .prompt_manager import load_prompt

# Load environment variables
load_dotenv()

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

NUM_MCQS_PER_SUBTOPIC = int(os.getenv("NUM_MCQS_PER_SUBTOPIC", 3))
DIFFICULTY_LEVEL = os.getenv("DIFFICULTY_LEVEL", "medium")

# Paths to prompt templates
SYSTEM_MESSAGE_PATH = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'system_message.txt')
MCQ_PROMPT_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'generate_mcq_prompt.txt')

# check if the SYSTEM_MESSAGE_PATH and MCQ_PROMPT_TEMPLATE_PATH are not empty
if not SYSTEM_MESSAGE_PATH or not MCQ_PROMPT_TEMPLATE_PATH:
    raise ValueError("Prompt template paths are not set.")
else:
    print(f"Prompt template paths are set. '{SYSTEM_MESSAGE_PATH}'")

def generate_mcq(text, num_questions, difficulty):
    """Generate multiple-choice questions based on the provided text."""
    try:
        # Load prompts from files
        system_message = load_prompt(SYSTEM_MESSAGE_PATH)
        user_prompt = load_prompt(MCQ_PROMPT_TEMPLATE_PATH, num_questions=num_questions, difficulty=difficulty, text=text)
        
        if not system_message or not user_prompt:
            raise ValueError ("Prompt templates are empty.")
        
        # Call the OpenAI API with the prompts using client.chat.completions.create
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        # Return the generated content
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error generating MCQs: {e}")
        return ""

def create_mcqs_for_subtopics(subtopics, num_questions=NUM_MCQS_PER_SUBTOPIC, difficulty=DIFFICULTY_LEVEL):
    """Generate MCQs for each subtopic in the text."""
    mcqs = {}
    for header, content in subtopics.items():
        mcqs[header] = generate_mcq(content, num_questions, difficulty)
    return mcqs
