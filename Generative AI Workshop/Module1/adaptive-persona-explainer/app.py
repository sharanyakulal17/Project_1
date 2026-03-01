import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

# GROQ CLIENT (IMPORTANT CHANGE)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = """
You are an expert educator AI.

Explain complex topics clearly and accurately.
Adapt explanation style based on persona:
- Shakespeare
- Pirate
- Bandit (Western outlaw)

Never sacrifice accuracy for style.
Keep explanations structured and educational.
"""

STYLE_GUIDE = {
    "shakespeare": "Use archaic English, poetic tone, dramatic phrasing.",
    "pirate": "Use pirate slang, nautical metaphors, energetic tone.",
    "bandit": "Use western outlaw slang, rugged frontier metaphors."
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/explain", methods=["POST"])
def explain():
    data = request.json
    topic = data.get("topic")
    style = data.get("style")

    style_instruction = STYLE_GUIDE.get(style.lower(), "")

    user_prompt = f"""
Explain the following topic: {topic}

Style requirement:
{style_instruction}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # GROQ MODEL
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8
        )

        explanation = response.choices[0].message.content
        return jsonify({"explanation": explanation})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)