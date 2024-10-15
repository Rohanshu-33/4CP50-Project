import tkinter as tk
from tkinter import filedialog, messagebox
import json

# Initialize the main window
root = tk.Tk()
root.title("PDF to Gemini LLM Interface")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

# Global variables to store session history in the specified format
session_history = []

# Upload PDF function
def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        session_history.append({
            "role": "user",
            "parts": [f"User uploaded PDF: {file_path}"]
        })
        session_history.append({
            "role": "model",
            "parts": ["OK. \n"]
        })
        messagebox.showinfo("Success", f"PDF uploaded: {file_path}")
        ask_button.config(state=tk.NORMAL)  # Enable the question asking after PDF upload
        update_session_display()
    else:
        messagebox.showwarning("Error", "No PDF selected")

# Ask Gemini function
def ask_question():
    question = question_entry.get()
    if not question:
        messagebox.showwarning("Input Error", "Please enter a question.")
        return
    
    # Simulate API request to Gemini (replace with actual API call)
    response = simulate_gemini_response(question)
    
    # Update session history in the required format
    session_history.append({
        "role": "user",
        "parts": [question]
    })
    session_history.append({
        "role": "model",
        "parts": [response]
    })
    
    # Update session display
    update_session_display()
    
    # Clear the question entry field
    question_entry.delete(0, tk.END)

# Simulate Gemini LLM response (replace with actual API integration)
def simulate_gemini_response(question):
    if "team" in question:
        return "The team name is Team HackStack. \n"
    elif "cricket" in question:
        return "Question out of context. \n"
    else:
        return f"Response to the question: '{question}'\n"

# Update the session display with the formatted session history
def update_session_display():
    session_text.config(state=tk.NORMAL)
    session_text.delete(1.0, tk.END)
    for entry in session_history:
        role = entry["role"]
        parts = entry["parts"]
        for part in parts:
            session_text.insert(tk.END, f"{role.capitalize()}: {part}\n")
    session_text.config(state=tk.DISABLED)

# Save session history to a file in JSON format
def save_session():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, "w") as file:
            json.dump(session_history, file, indent=4)
        messagebox.showinfo("Success", f"Session saved: {file_path}")

# Header label
header_label = tk.Label(
    root, text="Gemini PDF Parsing and Question Answering", font=("Helvetica", 24, "bold"), bg="#f0f0f0"
)
header_label.grid(row=0, column=0, columnspan=3, pady=20)

# Upload PDF button
upload_button = tk.Button(
    root, text="Upload PDF", padx=20, pady=10, bg="#4CAF50", fg="white", font=("Helvetica", 16), command=upload_pdf
)
upload_button.grid(row=1, column=0, columnspan=3, padx=20, pady=10)

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
ask_button.grid(row=3, column=0, columnspan=3, pady=10)
ask_button.config(state=tk.DISABLED)  # Initially disabled until PDF is uploaded

# Session history display (non-editable text widget)
session_text = tk.Text(root, wrap="word", height=15, font=("Helvetica", 14), state=tk.DISABLED)
session_text.grid(row=4, column=0, columnspan=3, padx=20, pady=10)

# Save session button
save_button = tk.Button(
    root, text="Save Session", padx=20, pady=10, bg="#4CAF50", fg="white", font=("Helvetica", 16), command=save_session
)
save_button.grid(row=5, column=0, columnspan=3, pady=10)

# Configure grid layout for responsiveness
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=1)

# Start the main loop
root.mainloop()
