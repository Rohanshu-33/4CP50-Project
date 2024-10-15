import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API = os.getenv("GEMINI_API")

genai.configure(api_key=GEMINI_API)

model = ""
chat_session = ""

def gemini_starting():
  # Create the model
  generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }

  global model
  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction="You are instructor who answers the question based on the PDF text uploaded by user. User will upload pdf to you. Whenever user uploads the pdf, you have to understand the content completely everytime he uploads and return \"OK\" as response. After that the user will start asking questions and you have to answer it. If the question seems to be out of context, then do not answer the question andd  instead response with \"Question out of context.\"",
  )


def upload_to_gemini(path, mime_type=None):
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file


def wait_for_files_active(files):
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()


def upload_and_train(pdf_path):
  global files

  files = [
    upload_to_gemini("./static/Mentor_connect_Final-SIH.pdf", mime_type="application/pdf"),
    upload_to_gemini("./static/Certificate.pdf", mime_type="application/pdf"),
  ]

  files.append(upload_to_gemini(pdf_path))
  print("Uploaded files : ", files)
  wait_for_files_active(files)
  global chat_session
  chat_session = model.start_chat(
    history=[
      {
        "role": "user",
        "parts": [
          files[0],
        ],
      },
      {
        "role": "model",
        "parts": [
          "OK. \n",
        ],
      },
      {
        "role": "user",
        "parts": [
          "how to bake a cake?",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Question out of context. \n",
        ],
      },
      {
        "role": "user",
        "parts": [
          "flavors of cake",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Question out of context. \n",
        ],
      },
      {
        "role": "user",
        "parts": [
          "name of team",
        ],
      },
      {
        "role": "model",
        "parts": [
          "The team name is Team HackStack. \n",
        ],
      },
      {
        "role": "user",
        "parts": [
          "name of cricket team",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Question out of context. \n",
        ],
      },
      {
        "role": "user",
        "parts": [
          files[1],
        ],
      },
      {
        "role": "model",
        "parts": [
          "OK. \n",
        ],
      },
      {
        "role": "user",
        "parts": [
          "name of team",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Question out of context. \n",
        ],
      },
      {
        "role": "user",
        "parts": [
          "summarize the pdf.",
        ],
      },
      {
        "role": "model",
        "parts": [
          "The certificate is for Rohanshu Anil from Birla Vishvakarma Mahavidyalaya Engineering College. He completed Intel® Unnati Industrial Training - 2024 from May 2024 to July 2024 in the field of Business Contract Validation under the guidance of Nm Patel. \n",
        ],
      },
      {
        "role": "user",
        "parts": [
          files[-1],
        ],
      },
      {
        "role": "model",
        "parts": [
          "OK. \n",
        ],
      },
    ]
  )



def obtainAnswer(question):

  # # Create the model
  # generation_config = {
  #   "temperature": 0,
  #   "top_p": 0.95,
  #   "top_k": 64,
  #   "max_output_tokens": 8192,
  #   "response_mime_type": "text/plain",
  # }

  # model = genai.GenerativeModel(
  #   model_name="gemini-1.5-flash",
  #   generation_config=generation_config,
  #   # safety_settings = Adjust safety settings
  #   # See https://ai.google.dev/gemini-api/docs/safety-settings
  #   system_instruction="You are instructor who answers the question based on the PDF text uploaded by user. User will upload pdf to you. Whenever user uploads the pdf, you have to understand the content completely everytime he uploads and return \"OK\" as response. After that the user will start asking questions and you have to answer it. If the question seems to be out of context, then do not answer the question andd  instead response with \"Question out of context.\"",
  # )

  

  response = chat_session.send_message(question)

  print(response.text)
  return response.text