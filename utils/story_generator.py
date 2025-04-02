from transformers import pipeline

# Load GPT-Neo model
story_pipeline = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

def generate_story(prompt, age_group):
    """
    Generates a children's story based on the given prompt and age group.
    """
    age_modifiers = {
        "5-7": "Tell a simple and cheerful fairy tale about ",
        "8-10": "Create an adventurous and exciting story about ",
        "11-13": "Write a thrilling and mysterious tale about "
    }
    
    # Modify the prompt based on age group
    full_prompt = age_modifiers.get(age_group, "Tell a magical story about ") + prompt

    # Generate the story
    story = story_pipeline(full_prompt, max_length=500, do_sample=True, temperature=0.7)[0]['generated_text']
    
    return story
