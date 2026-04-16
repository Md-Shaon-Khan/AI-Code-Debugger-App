from google import genai
from dotenv import load_dotenv
import os
import io

load_dotenv()

api_key_gemini = os.getenv("CODE_DEBUGGER")

client = genai.Client(api_key=api_key_gemini)

def solution_master(images,selected_option):
  prompt = f"""
  You are an expert AI programming debugger assistant.

  A student has uploaded one or more screenshots of code containing errors.

  Your task is to carefully analyze the images and identify:
  - programming language
  - exact error or bug
  - reason of the error
  - how to fix it

  You must help the student learn, not just give answers.

  ---

  USER SELECTED OPTION: {selected_option}

  ---

  IMPORTANT INSTRUCTIONS:

  1. If the selected option is "Hints":
    - Do NOT provide full solution or full corrected code
    - Only give step-by-step hints to fix the error
    - Keep explanation simple and educational
    - Guide the student like a teacher

  2. If the selected option is "Solution":
    - Provide full explanation of the error
    - Provide corrected working code
    - Explain what was changed and why

  ---

  OUTPUT FORMAT (STRICT):

  ### Error Summary:
  (Brief description of the error)

  ### Reason:
  (Why this error is happening)

  ### {selected_option}:
  (According to selected option rules above)

  ---

  RULES:
  - Be clear and structured
  - Do not include unnecessary information
  - If code is present in image, analyze it carefully
  - If multiple images exist, combine context
  """
  
  response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents = [images,prompt]
  )
  return response.text
  