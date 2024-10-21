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
    try:
        # Creating the model
        generation_config = {
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 20000,
            "response_mime_type": "text/plain",
        }

        global model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="You are an instructor who answers the question based on the PDF text uploaded by user. User will upload pdf to you. Whenever user uploads the pdf, you have to understand the content completely every time they upload and return 'OK' as response. After that, the user will start asking questions, and you have to answer them. If the question seems to be out of context, then do not answer the question, and instead respond with 'Question out of context.'",
        )
        print("Gemini model initialized successfully.")
    except Exception as e:
        print(f"Error in gemini_starting: {str(e)}")


def upload_to_gemini(path, mime_type=None):
    try:
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file
    except Exception as e:
        print(f"Error in upload_to_gemini: {str(e)}")


def wait_for_files_active(files):
    try:
        print("Waiting for file processing...")
        for name in (file.name for file in files):
            file = genai.get_file(name)
            while file.state.name == "PROCESSING":
                print(".", end="", flush=True)
                time.sleep(2)
                file = genai.get_file(name)
            if file.state.name != "ACTIVE":
                raise Exception(f"File {file.name} failed to process")
        print("Files are ready.")
        print()
    except Exception as e:
        print(f"Error in wait_for_files_active: {str(e)}")


def upload_and_train(pdf_path):
    try:
        global files
        files = []
        files.append(upload_to_gemini(pdf_path))
        print("Uploaded files:", files)
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
                }]
        )
        print("Chat session started successfully.")
        return "green"
    except Exception as e:
        print(f"Error in upload_and_train: {str(e)}")
        return "red"


def obtainAnswer(question):
    try:
        response = chat_session.send_message(question)
        print(response.text)
        return response.text
    except Exception as e:
        print(f"Error in obtainAnswer: {str(e)}")
