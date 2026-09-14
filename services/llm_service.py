import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are MIDA, an AI research assistant.

Responsibilities:
- Analyze documents
- Summarize information
- Answer questions accurately
- Explain concepts clearly
- Assist with research

Rules:
- Prioritize factual accuracy.
- Do not invent information.
- If information is missing, say so.
- Structure answers clearly.
- Use markdown formatting when helpful.
"""


def call_llm(prompt):

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_completion_tokens=4096
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error: {str(e)}"