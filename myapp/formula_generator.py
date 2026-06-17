import json
import re
from django.conf import settings
from groq import Groq


def generate_formulas(text: str):
    """
    Extract important formulas and mathematical expressions
    from academic notes.

    Returns:
    [
        {
            "formula": "E = mc^2",
            "explanation": "Energy equals mass times the speed of light squared."
        }
    ]
    """

    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt = f"""
You are ScholarShield AI.

Extract all important mathematical formulas, equations, or scientific expressions
from the study notes below.

Rules:
- Only extract real formulas or equations.
- If none exist, return an empty JSON list.
- For each formula include:
    - "formula": the exact formula
    - "explanation": short explanation (1-2 sentences)
- Return ONLY valid JSON.
- No markdown.
- No commentary.

Format:

[
  {{
    "formula": "F = ma",
    "explanation": "Force equals mass multiplied by acceleration."
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
            max_tokens=1000,
        )

        raw_output = completion.choices[0].message.content.strip()

        match = re.search(r"\[.*\]", raw_output, re.DOTALL)

        if match:
            return json.loads(match.group())

        return []

    except Exception as e:
        print("Formula Extraction Error:", str(e))
        return []