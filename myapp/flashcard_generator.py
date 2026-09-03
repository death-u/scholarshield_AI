import json
import re
from django.conf import settings
from groq import Groq


def generate_flashcards(text: str):

    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt = f"""
You are ScholarShield AI.

Generate EXACTLY 10 academic flashcards
from the study notes below.

Rules:
- Each flashcard must have:
  - "front": question or concept
  - "back": clear academic explanation
- Return ONLY valid JSON
- No markdown
- No commentary

Format:

[
  {{
    "front": "Question or concept",
    "back": "Explanation"
  }}
]

Study Notes:
{text[:4000]}
"""

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=1200,
    )

    raw_output = completion.choices[0].message.content.strip()

    match = re.search(r"\[.*\]", raw_output, re.DOTALL)
    if match:
        return json.loads(match.group())

    return []