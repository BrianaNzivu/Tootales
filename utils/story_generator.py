import random

def generate_story(prompt):
    """Generate a simple story based on user input."""
    story_templates = [
        f"One magical day, {prompt} discovered a secret door leading to a world of enchanted creatures.",
        f"In a faraway kingdom, {prompt} embarked on an adventure full of mystical lands and treasures.",
        f"Deep in the forest, {prompt} found a mysterious book that unlocked a realm of wonder."
    ]
    return random.choice(story_templates)
