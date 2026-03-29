"""
story_generator.py
------------------
AI-powered story generator using Groq (LLaMA 3).
Responsibility: Friend 2 (Model Development)

Given a FLAMES outcome and two names, generates a short, fun
personalised story about the relationship between the two people.

Design notes:
- Uses Groq for fast LLaMA 3 inference
- Falls back to a template-based story if API call fails
- Prompt is carefully tuned for fun, concise, non-cringe output
- Async to not block the FastAPI event loop
"""

import os
import asyncio
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

# ─── Config ──────────────────────────────────────────────────────────────────

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME = "llama-3.1-8b-instant"   # Fast, free-tier friendly

OUTCOME_CONTEXT = {
    "Friends":   "they are great friends who enjoy each other's company",
    "Loves":     "one of them has romantic feelings for the other",
    "Affection": "there is a warm, caring affection between them",
    "Marriage":  "they are destined to get married someday",
    "Enemies":   "they are rivals or enemies who clash often",
    "Siblings":  "they share a sibling-like bond — protective and playful",
}

FALLBACK_STORIES = {
    "Friends":   "{name1} and {name2} make an amazing duo — always there for each other through thick and thin. Their friendship is the kind that lasts a lifetime. 🤝",
    "Loves":     "There's something special between {name1} and {name2}. Every glance, every smile — it all adds up to something neither of them can ignore. ❤️",
    "Affection": "{name1} and {name2} share a quiet, warm bond. It's not loud or dramatic — it's the kind of connection that feels safe and real. 🥰",
    "Marriage":  "The stars have spoken! {name1} and {name2} are written in the same chapter of life's big story. 💐",
    "Enemies":   "{name1} and {name2} can't seem to agree on anything — but hey, even rivals push each other to be better. 😬",
    "Siblings":  "{name1} and {name2} feel like family. They tease, support, and look out for each other like only siblings can. 😊",
}

SYSTEM_PROMPT = """You are a fun, witty storyteller for a relationship prediction game called FLAMES.
When given two names and a relationship outcome, you write a short 2-3 sentence story (60-80 words max).
Rules:
- Keep it light, fun, and age-appropriate
- Be creative and specific to the names given
- End with a relevant emoji
- Do NOT mention the word FLAMES or that this is a game
- Do NOT use asterisks or markdown formatting
- Write as a narrator, not as the characters
"""


# ─── Main Generator ──────────────────────────────────────────────────────────

async def generate_story(name1: str, name2: str, outcome: str, emoji: str) -> str:
    """
    Generate a personalised story for the FLAMES outcome.

    Args:
        name1   (str): First person's name
        name2   (str): Second person's name
        outcome (str): FLAMES outcome label (e.g. "Loves", "Friends")
        emoji   (str): Emoji for the outcome

    Returns:
        str: A short fun story about the two people
    """
    if not GROQ_API_KEY:
        return _fallback_story(name1, name2, outcome)

    context = OUTCOME_CONTEXT.get(outcome, f"they share a '{outcome}' relationship")

    user_prompt = (
        f"Names: {name1} and {name2}\n"
        f"Relationship: {outcome} {emoji}\n"
        f"Context: {context}\n\n"
        f"Write a short, fun story about {name1} and {name2} given this relationship."
    )

    try:
        client = AsyncGroq(api_key=GROQ_API_KEY)
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=120,
            temperature=0.85,
        )
        story = response.choices[0].message.content.strip()
        return story

    except Exception as e:
        print(f"[StoryGenerator] Groq API error: {e}")
        return _fallback_story(name1, name2, outcome)


def _fallback_story(name1: str, name2: str, outcome: str) -> str:
    """Return a template-based story when AI is unavailable."""
    template = FALLBACK_STORIES.get(outcome, "{name1} and {name2} share a special bond.")
    return template.format(name1=name1, name2=name2)


# ─── CLI test ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    async def test():
        story = await generate_story("Akash", "Priya", "Marriage", "💐")
        print("Generated story:\n", story)

    asyncio.run(test())
