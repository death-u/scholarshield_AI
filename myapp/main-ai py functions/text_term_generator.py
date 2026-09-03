import json
import re
from django.conf import settings
from groq import Groq


def generate_keyterms(text: str):
    """
    Generates structured academic key terms and definitions
    from extracted note text.

    Returns:
        List of dict:
        [
            {
                "term": "...",
                "definition": "..."
            }
        ]
    """

    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt = f"""
You are ScholarShield AI.

Your task:
Extract the most important academic key terms from the study notes below.

Rules:
- Extract between 8 and 15 key terms.
- Each term must have:
    - "term": short concept name
    - "definition": clear, concise academic explanation
- Definitions must be 1–3 sentences.
- Only use information from the notes.
- Return ONLY valid JSON.
- No markdown.
- No explanations.
- No extra commentary.

Required JSON format:

[
  {{
    "term": "Concept Name",
    "definition": "Clear explanation."
  }}
]

Study Notes:
{text[:4000]}
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1200,
        )

        raw_output = completion.choices[0].message.content.strip()

        # ✅ Safely extract JSON block
        match = re.search(r"\[.*\]", raw_output, re.DOTALL)

        if match:
            return json.loads(match.group())

        # Fallback if AI misbehaves
        return []

    except Exception as e:
        print("KeyTerm Generation Error:", str(e))
        return []