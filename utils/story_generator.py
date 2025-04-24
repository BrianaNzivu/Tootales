from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model_name = "EleutherAI/gpt-neo-125M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

story_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)  # Use device=0 for GPU

def generate_story(prompt):
    """
    Generates a story using GPT-Neo 125M.

    Args:
        prompt (str): The user's input prompt.

    Returns:
        str: The generated story.
    """
    # Add a child-friendly instruction to guide the model
    instruction = (
        "Write a detailed, child-friendly story based on the following prompt. "
        "The story should be imaginative, engaging, and around 400 words long. "
        "Avoid repetition and ensure the story is suitable for children. "
        "Prompt: "
    )
    full_prompt = instruction + prompt

    generated = story_pipeline(
        full_prompt,
        max_length=600, 
        do_sample=True,
        temperature=0.7,  
        top_p=0.9,  
        repetition_penalty=1.2, 
        num_return_sequences=1,
        truncation=True  
    )
    return generated[0]["generated_text"]