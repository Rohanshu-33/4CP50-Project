import tkinter as tk
from tkinter import filedialog, messagebox
import requests

# Initialize the main window
root = tk.Tk()
root.title("PDF to Gemini LLM Interface")
root.geometry("800x600")  # Set a large window size for better UI on big screens
root.configure(bg="#f0f0f0")  # Light background color

# Define the API endpoints (replace with actual URLs)
GEMINI_PDF_UPLOAD_URL = "http://gemini-api/upload"  # Replace with your Gemini upload endpoint
GEMINI_QUESTION_URL = "http://gemini-api/question"  # Replace with your Gemini question endpoint

# Function to upload PDF and parse with Gemini
def upload_pdf():
    filepath = filedialog.askopenfilename(
        initialdir="/", title="Select PDF File", filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*"))
    )
    if filepath:
        try:
            with open(filepath, 'rb') as file:
                # Send the PDF to Gemini API
                response = requests.post(GEMINI_PDF_UPLOAD_URL, files={'file': file})
                
                if response.status_code == 200 and response.text == "OK":
                    messagebox.showinfo("Success", "PDF successfully parsed by Gemini!")
                else:
                    messagebox.showerror("Error", "Failed to parse PDF with Gemini")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to send a question to the Gemini LLM and get a response
def ask_question():
    question = question_entry.get()
    if question:
        try:
            # Send the question to the Gemini API
            response = requests.post(GEMINI_QUESTION_URL, json={'question': question})
            if response.status_code == 200:
                response_text = response.json().get("answer", "No answer returned")
                response_label.config(text=f"Response: {response_text}")
            else:
                messagebox.showerror("Error", "Failed to get a response from Gemini")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Header label
header_label = tk.Label(
    root, text="Gemini PDF Parsing and Question Answering", font=("Helvetica", 24, "bold"), bg="#f0f0f0"
)
header_label.grid(row=0, column=0, columnspan=2, pady=20)

# Upload PDF button
upload_button = tk.Button(
    root, text="Upload PDF", padx=20, pady=10, bg="#4CAF50", fg="white", font=("Helvetica", 16), command=upload_pdf
)
upload_button.grid(row=1, column=0, padx=20, pady=10)

# Question label
question_label = tk.Label(
    root, text="Enter your question:", font=("Helvetica", 18), bg="#f0f0f0"
)
question_label.grid(row=2, column=0, padx=20, pady=20)

# Question entry field
question_entry = tk.Entry(root, width=50, font=("Helvetica", 16))
question_entry.grid(row=2, column=1, padx=20, pady=20)

# Ask button
ask_button = tk.Button(
    root, text="Ask Gemini", padx=20, pady=10, bg="#008CBA", fg="white", font=("Helvetica", 16), command=ask_question
)
ask_button.grid(row=3, column=0, columnspan=2, pady=10)

# Response label
response_label = tk.Label(root, text="Response: ", font=("Helvetica", 18), bg="#f0f0f0", wraplength=700)
response_label.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

# Configure grid layout for responsiveness
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)

# Start the main loop
root.mainloop()
