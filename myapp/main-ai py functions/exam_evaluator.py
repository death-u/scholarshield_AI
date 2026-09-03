import json
import re
from django.conf import settings
from groq import Groq


def evaluate_exam_answer(note_text: str, question: str, student_answer: str):

    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt = f"""
You are an academic examiner.

You are given:
1. Study Notes
2. An Exam Question
3. A Student's Answer

Your task:
- Grade the answer from 0 to 10.
- Provide:
    - "score": integer (0–10)
    - "strengths": list of strong points
    - "weaknesses": list of missing or incorrect points
    - "suggestions": list of improvements
    - "model_outline": structured bullet points showing the ideal answer structure
    - "model_answer": a short but complete model answer (maximum 150 words)

Rules:
- "model_answer" must be clear, accurate, and based strictly on the study notes but also you should be flexable to the student answer as far it also generally correct not only strictly following the note.
- Do NOT write more than 150 words for the model answer.
- Grade strictly based on the study notes but also be flexible with the student answer.
- Return ONLY valid JSON.
- No markdown.
- No commentary.
- also note be flexable.

Format:

{{
  "score": 7,
  "strengths": ["..."],
  "weaknesses": ["..."],
  "suggestions": ["..."],
  "model_outline": ["point 1", "point 2", "point 3"],
  "model_answer": "Short model answer here."
}}

Study Notes:
{note_text[:3000]}

Question:
{question}

Student Answer:
{student_answer}
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1200,
        )

        raw_output = completion.choices[0].message.content.strip()

        match = re.search(r"\{.*\}", raw_output, re.DOTALL)

        if match:
            return json.loads(match.group())

        return {
            "score": 0,
            "strengths": [],
            "weaknesses": ["Evaluation failed."],
            "suggestions": [],
            "model_outline": [],
            "model_answer": "Could not generate model answer."
        }

    except Exception as e:
        print("Exam Evaluation Error:", str(e))
        return {
            "score": 0,
            "strengths": [],
            "weaknesses": ["Evaluation failed."],
            "suggestions": [],
            "model_outline": [],
            "model_answer": "Could not generate model answer."
        }