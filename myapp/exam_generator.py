import json
import re
from django.conf import settings
from groq import Groq


def generate_exam_questions(text: str):
    """
    Generates long-answer exam questions with structured answer outlines.

    Returns:
    [
        {
            "question": "...",
            "outline": ["point 1", "point 2", "point 3"]
        }
    ]
    """

    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt = f"""
You are ScholarShield AI.

Generate EXACTLY 5 university-level long-answer exam questions
based strictly on the study notes below.

Rules:
- Questions must be analytical (Explain, Discuss, Compare, Evaluate).
- Each question must include:
    - "question": the full question text
    - "outline": a structured list of bullet points students should cover
- Do NOT write full essays.
- Provide only structured outlines.
- Return ONLY valid JSON.
- No markdown.
- No commentary.

Format:

[
  {{
    "question": "Explain the two stages of photosynthesis.",
    "outline": [
      "Definition of photosynthesis",
      "Light-dependent reactions",
      "Calvin cycle",
      "Connection between stages"
    ]
  }}
]

Study Notes:
{text[:4000]}
"""

    try:
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

    except Exception as e:
        print("Exam Question Generation Error:", str(e))
        return []