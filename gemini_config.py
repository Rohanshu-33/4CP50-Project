import os
import time
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

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

# Create the model
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="You are instructor who answers the question based on the PDF text uploaded by user. User will upload pdf to you. Whenever user uploads the pdf, you have to understand the content completely everytime he uploads and return \"OK\" as response. After that the user will start asking questions and you have to answer it. If the question seems to be out of context, then do not answer the question andd  instead response with \"Question out of context.\"",
)

# TODO Make these files available on the local file system
# You may need to update the file paths
files = [
  upload_to_gemini("./Mentor_connect_Final-SIH.pdf", mime_type="application/pdf"),
]

# Some files have a processing delay. Wait for them to be ready.
wait_for_files_active(files)

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
        "The document doesn't mention any specific cake flavors. \n",
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
        "User uploaded pdf",
      ],
    },
    {
      "role": "model",
      "parts": [
        "The project is called \"ParkEZ - Parking Made Easy\". \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        files[2],
      ],
    },
    {
      "role": "model",
      "parts": [
        "The certificate is for Rohanshu Anil from Birla Vishvakarma Mahavidyalaya Engineering College. He completed Intel® Unnati Industrial Training – 2024 from May 2024 to July 2024 in the field of Business Contract Validation under the guidance of Nm Patel. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        files[3],
      ],
    },
    {
      "role": "model",
      "parts": [
        "The payment for the GATE 2024 application fee for ROHANSHU ANIL BANODHA with enrollment ID T396S37 has been received successfully. \n",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)