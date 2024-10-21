import tkinter as tk
from tkinter import filedialog, messagebox
from gemini_config import obtainAnswer, gemini_starting, upload_and_train

gemini_starting()

root = tk.Tk()
root.title("PDF Explorer")
root.geometry("1000x800")

session_history = []

# Upload PDF function
def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    
    if file_path:
        signal = upload_and_train(file_path)

        print("Signal is : ", signal)
        
        if signal == "red":
            messagebox.showerror("Error", "Please check your internet connection")
            return
        
        messagebox.showinfo("Success", f"PDF uploaded and processed: {file_path}")
        ask_button.config(state=tk.NORMAL) 
    else:
        messagebox.showwarning("Error", "No PDF selected")

# Ask Gemini function
def ask_question():
    question = question_entry.get()
    if not question:
        messagebox.showwarning("Input Error", "Please enter a question.")
        return

    # Send the question to the Gemini model
    response = obtainAnswer(question)

    print("response is : ", response)
    
    # Update history
    session_history.append({"question": question, "response": response})
    
    # Update display
    update_history()
    
    # Clear the question entry field
    question_entry.delete(0, tk.END)

# Update the display with the question and response history
def update_history():
    history.config(state=tk.NORMAL)
    last_entry = session_history[-1]
    history.insert(tk.END, f"Q: {last_entry['question']}\nA: {last_entry['response']}\n\n")
    history.config(state=tk.DISABLED)

# Savehistory to a file
def save_session():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            for entry in session_history:
                file.write(f"Q: {entry['question']}\nA: {entry['response']}\n\n")
        messagebox.showinfo("Success", f"Session saved: {file_path}")

# Header
header = tk.Label(
    root, text="PDF Explorer", font=("", 24, "bold"), bg="#f0f0f0"
)
header.grid(row=0, column=0, columnspan=3, pady=20)

# Upload PDF button
upload_button = tk.Button(
    root, text="Upload PDF", padx=20, pady=10, bg="#4CAF50", fg="white", font=("", 16), command=upload_pdf
)
upload_button.grid(row=1, column=0, columnspan=3, padx=20, pady=10)

# Question label
question_label = tk.Label(
    root, text="Enter your question:", font=("", 18), bg="#f0f0f0"
)
question_label.grid(row=2, column=0, padx=20, pady=20)

# Question entry field
question_entry = tk.Entry(root, width=50, font=("", 16))
question_entry.grid(row=2, column=1, padx=20, pady=20)

# Ask button
ask_button = tk.Button(
    root, text="Ask Question", padx=20, pady=10, bg="#008CBA", fg="white", font=("", 16), command=ask_question
)
ask_button.grid(row=3, column=0, columnspan=3, pady=10)
ask_button.config(state=tk.DISABLED) 

#history
history = tk.Text(root, wrap="word", height=13, font=("", 14), state=tk.DISABLED)
history.grid(row=4, column=0, columnspan=3, padx=20, pady=10)

# Savebutton
save_button = tk.Button(
    root, text="Save history", padx=20, pady=10, bg="#4CAF50", fg="white", font=("", 16), command=save_session
)
save_button.grid(row=5, column=0, columnspan=3, pady=10)

# Configure grid layout for responsiveness
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=1)

# Start the main loop
root.mainloop()
