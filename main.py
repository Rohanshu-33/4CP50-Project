import tkinter as tk
from tkinter import filedialog, messagebox
import requests

# Initialize the main window
root = tk.Tk()
root.title("PDF to Gemini LLM Interface")
root.geometry("800x600")  # Set a large window size for better UI on big screens
root.configure(bg="#f0f0f0")  # Light background color

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
