from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("CODE_DEBUGGER"))

def solution_master(images, selected_option):

    prompt = f"""
You are an expert AI programming debugger.

Analyze the uploaded code screenshot(s) carefully.

USER OPTION: {selected_option}

If "Hints":
- Give only step-by-step hints
- No full code

If "Solution":
- Give full fixed code + explanation

FORMAT:
### Error Summary
### Reason
### Response
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[prompt, *images]
    )

    return response.text