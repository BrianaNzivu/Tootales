from transformers import pipeline

# Initialize the text-to-text generation pipeline using flan-t5-small
story_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    trust_remote_code=True,
    device=-1  # Use CPU, change to 0 for GPU if available
)

def generate_story(prompt, age_group):
    """
    Generates a child-friendly story based on the given prompt and age group.
    The story output is targeted to be roughly 400-600 words long.
    
    Parameters:
      - prompt (str): The base idea for the story.
      - age_group (str): One of "5-7", "8-10", or "11-13". 
    
    Returns:
      - str: The generated story.
    """
    # Age-specific instructions for tone and language
    age_instructions = {
        "5-7": (
            "Write a very simple, cheerful, and imaginative story in plain language for children aged 5-7. "
            "Use very short sentences and extremely easy words. "
        ),
        "8-10": (
            "Write an adventurous and engaging story in plain language for children aged 8-10. "
            "Ensure the narrative has a clear beginning, middle, and end, and use clear, simple sentences. "
        ),
        "11-13": (
            "Write a creative and engaging story in plain language for children aged 11-13. "
            "Keep the narrative interesting and smooth, with a clear structure and accessible vocabulary. "
        )
    }
    
    instruction = age_instructions.get(age_group, age_instructions["8-10"])
    
    # Construct the full prompt with desired output length instructions
    full_prompt = (
        instruction +
        "The story should be between 400 and 600 words long. " +
        "Avoid repetitive phrases and ensure the narrative flows naturally. " +
        "Now, write a complete story about " + prompt + "."
    )

    # Generate the story with adjusted max_length and sampling settings for better coherence
    generated = story_pipeline(
        full_prompt,
        max_length=600,  # Increase to 600 for a longer story
        do_sample=True,
        temperature=0.75,
        top_p=0.95,
        repetition_penalty=1.3,
        no_repeat_ngram_size=3,
        num_return_sequences=1,
        truncation=True
    )

    story = generated[0]["generated_text"]

    # Clean up the response to remove the prompt repetition
    if story.startswith(full_prompt):
        story = story[len(full_prompt):].strip()

    return story

# For testing the module by itself.
if __name__ == "__main__":
    test_prompt = "a brave fox named Finn who embarks on a journey to find a hidden treasure in an enchanted forest"
    test_age_group = "8-10"
    generated_story = generate_story(test_prompt, test_age_group)
    print("Generated Story:\n")
    print(generated_story)
