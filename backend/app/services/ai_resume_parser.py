import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def parse_resume_with_ai(resume_text):

    prompt = f"""
Extract resume details.

Return ONLY valid JSON.

{{
  "name": "",
  "location": "",
  "skills": [],
  "experience_years": 0,
  "domain": "",
  "email": "",
  "phone": ""
}}

Resume:
{resume_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    return json.loads(content)
