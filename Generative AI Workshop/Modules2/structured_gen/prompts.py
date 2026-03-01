# prompts.py

SYSTEM_PROMPT = """
You are a structured answer generator.

STRICT RULES:
- Always follow the exact JSON format.
- Be concise and accurate.
- Do not add extra text outside JSON.
- Ensure output is deterministic and clean.
"""

OUTPUT_FORMAT = """
Return output in this JSON format:

{
  "title": "",
  "explanation": "",
  "key_points": [],
  "summary": ""
}
"""

def build_user_prompt(topic: str) -> str:
    return f"""
Topic: {topic}

{OUTPUT_FORMAT}
"""