import OpenAI from "openai";
import dotenv from "dotenv";
import readline from "readline";

dotenv.config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// 🎭 Persona System Prompts
const personas = {
  shakespeare: `
You are an expert scholar who explains complex topics clearly.
Speak in Shakespearean English.
Use poetic structure, old English vocabulary, and dramatic tone.
`,

  pirate: `
You are an expert teacher who explains complex topics clearly.
Speak like a pirate.
Use nautical metaphors, pirate slang, and adventurous tone.
`,

  bandit: `
You are a street-smart outlaw explaining complex ideas.
Use rough, rebellious language.
Sound bold, dramatic, and slightly dangerous.
`,
};

// 🧠 Core Explainer Behavior (Base System Prompt)
const baseSystemPrompt = `
You are an elite educator.
Your task is to explain complex topics in a simple, structured way.
Break explanations into:
1. Simple definition
2. Real-world example
3. Why it matters
Keep explanations clear but adapt fully to the requested persona style.
`;

// CLI Interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

rl.question("Enter topic to explain: ", (topic) => {
  rl.question("Choose mode (shakespeare, pirate, bandit): ", async (mode) => {
    if (!personas[mode]) {
      console.log("Invalid mode selected.");
      rl.close();
      return;
    }

    try {
      const completion = await openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [
          {
            role: "system",
            content: baseSystemPrompt + personas[mode],
          },
          {
            role: "user",
            content: `Explain: ${topic}`,
          },
        ],
        temperature: 0.9,
      });

      console.log("\n🧾 Explanation:\n");
      console.log(completion.choices[0].message.content);

    } catch (error) {
      console.error("Error:", error);
    }

    rl.close();
  });
});