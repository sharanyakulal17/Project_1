import os
import json
from dotenv import load_dotenv
import litellm

from prompts import SYSTEM_PROMPT, build_user_prompt
from config import MODEL_NAME, TEMPERATURE, MAX_TOKENS

# Load environment variables
load_dotenv()

# Set Groq key for LiteLLM
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


def generate_structured_answer(topic: str):
    try:
        response = litellm.completion(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(topic)},
            ],
        )

        content = response.choices[0].message.content

        # Try to parse JSON (production safety)
        try:
            parsed = json.loads(content)
            return parsed
        except json.JSONDecodeError:
            return {"error": "Invalid JSON returned", "raw_output": content}

    except Exception as e:
        return {"error": str(e)}


def main():
    print("\n📊 Structured Answer Generator (LiteLLM + Groq)")
    print("--------------------------------------------------")

    topic = input("Enter topic: ")

    print("\n⏳ Generating structured response...\n")

    result = generate_structured_answer(topic)

    print("✅ Output:\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()