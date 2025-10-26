import tkinter as tk
from tkinter import ttk, messagebox
import qrcode
from PIL import Image, ImageTk
import io
import random

# ---------------- QUIZ QUESTIONS ----------------
questions = [
    {"question": "Which language is known as the language of Artificial Intelligence?",
     "options": ["Python", "C++", "Java", "HTML"], "answer": "Python"},
    {"question": "Which data structure uses FIFO order?",
     "options": ["Stack", "Queue", "Tree", "Graph"], "answer": "Queue"},
    {"question": "Which company developed TensorFlow?",
     "options": ["Google", "Meta", "OpenAI", "Apple"], "answer": "Google"},
    {"question": "What does GUI stand for?",
     "options": ["General User Interface", "Graphical User Interface", "Graphic Utility Interface", "Global User Integration"],
     "answer": "Graphical User Interface"},
    {"question": "Which keyword is used to define a function in Python?",
     "options": ["func", "function", "define", "def"], "answer": "def"}
]

# ---------------- MAIN CLASS ----------------
class QuizifyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quizify - Smart Quiz App")
        self.root.geometry("800x550")
        self.root.configure(bg="#121212")

        self.score = 0
        self.q_no = 0
        self.time_left = 15
        self.timer_running = False
        self.user_answer = tk.StringVar()

        self.title_bar = tk.Label(self.root, text="🎯 QUIZIFY",
                                  font=("Segoe UI", 26, "bold"), bg="#00FFAB", fg="#121212")
        self.title_bar.pack(fill="x")

        self.frame = tk.Frame(self.root, bg="#121212")
        self.frame.pack(pady=40)

        self.question_label = tk.Label(self.frame, text="", wraplength=650, justify="center",
                                       font=("Segoe UI", 16), fg="white", bg="#121212")
        self.question_label.grid(row=0, column=0, columnspan=2, pady=20)

        self.radio_buttons = []
        for i in range(4):
            rb = ttk.Radiobutton(self.frame, text="", variable=self.user_answer, value="")
            rb.grid(row=i + 1, column=0, columnspan=2, pady=6)
            self.radio_buttons.append(rb)

        self.timer_label = tk.Label(self.root, text="⏱️ Time Left: 15s",
                                    font=("Segoe UI", 14), fg="#FF5555", bg="#121212")
        self.timer_label.pack(pady=10)

        self.score_label = tk.Label(self.root, text="Score: 0",
                                    font=("Segoe UI", 14, "bold"), fg="#00FFAB", bg="#121212")
        self.score_label.pack(pady=5)

        self.next_btn = ttk.Button(self.root, text="Next ➡️", command=self.next_question)
        self.next_btn.pack(pady=20)

        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 12), padding=6)

        self.load_question()

    # ---------------- LOAD QUESTIONS ----------------
    def load_question(self):
        if self.q_no < len(questions):
            self.time_left = 15
            self.timer_running = True
            self.update_timer()

            q = questions[self.q_no]
            self.question_label.config(text=f"Q{self.q_no + 1}. {q['question']}")
            self.user_answer.set(None)
            for i, opt in enumerate(q["options"]):
                self.radio_buttons[i].config(text=opt, value=opt)
        else:
            self.show_result()

    # ---------------- TIMER FUNCTION ----------------
    def update_timer(self):
        if self.timer_running:
            self.timer_label.config(text=f"⏱️ Time Left: {self.time_left}s")
            if self.time_left > 0:
                self.time_left -= 1
                self.root.after(1000, self.update_timer)
            else:
                messagebox.showwarning("Time’s up!", "You ran out of time!")
                self.q_no += 1
                self.load_question()

    # ---------------- NEXT BUTTON ----------------
    def next_question(self):
        if not self.user_answer.get():
            messagebox.showwarning("Warning", "Please select an answer!")
            return

        correct = questions[self.q_no]["answer"]
        if self.user_answer.get() == correct:
            self.score += 1
            messagebox.showinfo("Correct!", "✅ That’s the right answer!")
        else:
            messagebox.showinfo("Incorrect", f"❌ The correct answer was: {correct}")

        self.q_no += 1
        self.score_label.config(text=f"Score: {self.score}")
        self.load_question()

    # ---------------- RESULT & QR CODE ----------------
    def show_result(self):
        self.timer_running = False
        for widget in self.root.winfo_children():
            widget.destroy()

        final_msg = f"🏁 Quiz Completed!\n\nYour Final Score: {self.score}/{len(questions)}"
        label = tk.Label(self.root, text=final_msg, fg="#00FFAB", bg="#121212",
                         font=("Segoe UI", 18, "bold"))
        label.pack(pady=40)

        # Generate QR reward
        reward_text = f"🎓 Congratulations!\nYou completed Quizify.\nFinal Score: {self.score}/{len(questions)}"
        qr_img = qrcode.make(reward_text)
        bio = io.BytesIO()
        qr_img.save(bio, format="PNG")
        qr_img = Image.open(bio)
        qr_img = qr_img.resize((200, 200))
        qr_photo = ImageTk.PhotoImage(qr_img)

        qr_label = tk.Label(self.root, image=qr_photo, bg="#121212")
        qr_label.image = qr_photo
        qr_label.pack(pady=10)

        msg_label = tk.Label(self.root, text="📱 Scan the QR to view your reward!", fg="white",
                             bg="#121212", font=("Segoe UI", 12))
        msg_label.pack(pady=10)

        exit_btn = ttk.Button(self.root, text="Exit", command=self.root.destroy)
        exit_btn.pack(pady=20)


# ---------------- MAIN APP ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizifyApp(root)
    root.mainloop()