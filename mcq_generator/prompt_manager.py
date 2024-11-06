import os

def load_prompt(template_path, **kwargs):
    """Loads a prompt template from a file and formats it with provided kwargs."""
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            prompt = file.read()
        return prompt.format(**kwargs)
    except Exception as e:
        print(f"Error loading prompt from {template_path}: {e}")
        return ""
