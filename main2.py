import tkinter as tk
from tkinter import filedialog, messagebox
from gemini_config import obtainAnswer, gemini_starting, upload_and_train

gemini_starting()

root = tk.Tk()
root.title("PDF to Gemini LLM Interface")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

session_history = []
uploaded_file = None
file_path = False

# Upload PDF function
def upload_pdf():
    global uploaded_file, file_path
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    
    if file_path:
        upload_and_train(file_path)
        uploaded_file = True
        # Upload PDF to Gemini using the imported function
        # uploaded_file = upload_to_gemini(file_path, mime_type="application/pdf")
        
        # Wait for file processing
        # wait_for_files_active([uploaded_file])
        
        messagebox.showinfo("Success", f"PDF uploaded and processed: {file_path}")
        ask_button.config(state=tk.NORMAL)  # Enable the question asking after PDF upload
    else:
        messagebox.showwarning("Error", "No PDF selected")

# Ask Gemini function
def ask_question():
    global uploaded_file, file_path
    question = question_entry.get()
    if not question:
        messagebox.showwarning("Input Error", "Please enter a question.")
        return

    if uploaded_file is None:
        messagebox.showwarning("File Error", "Please upload a PDF first.")
        return

    # Send the question to the Gemini model
    response = obtainAnswer(question)

    print("response is : ", response)
    
    # Update session history
    session_history.append({"question": question, "response": response})
    
    # Update session display
    update_session_display()
    
    # Clear the question entry field
    question_entry.delete(0, tk.END)

# Update the session display with the question and response history
def update_session_display():
    session_text.config(state=tk.NORMAL)
    session_text.delete(1.0, tk.END)
    for entry in session_history:
        session_text.insert(tk.END, f"Q: {entry['question']}\nA: {entry['response']}\n\n")
    session_text.config(state=tk.DISABLED)

# Save session history to a file
def save_session():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            for entry in session_history:
                file.write(f"Q: {entry['question']}\nA: {entry['response']}\n\n")
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
