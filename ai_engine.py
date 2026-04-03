import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GEMINI_API_KEY

# LLM SETUP
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.4
)

def analyze_and_generate(lead):
    try:
        prompt = f"""
Analyze this startup and write a cold email.

Name: {lead['name']}
Idea: {lead['idea']}

STRICT RULES:
- Return ONLY valid JSON
- No explanation, no markdown, no extra text

Output format:
{{
  "pain_point": "",
  "automation_idea": "",
  "generated_email": ""
}}
"""

        response = llm.invoke(prompt)

        content = response.content if hasattr(response, "content") else str(response)

        # 🔥 Extract JSON safely
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            return json.loads(match.group())

        raise ValueError("No JSON found")

    except Exception as e:
        print("ERROR:", e)
        return {
            "pain_point": "",
            "automation_idea": "",
            "generated_email": ""
        }