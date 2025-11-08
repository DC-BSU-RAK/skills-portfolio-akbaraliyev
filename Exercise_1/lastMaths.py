import tkinter as tk
from tkinter import messagebox
import random
from PIL import ImageTk, Image

current_score = 0
question_number = 0
difficulty_level = ''
current_answer = 0
attempts_left = 0

def randomInt(level):
    if level == 'easy':
        return random.randint(1, 9)
    elif level == 'moderate':
        return random.randint(10, 99)
    else:
        return random.randint(1000, 9999)

def decideOperation():
    if random.randint(0, 1) == 0:
        return '+'
    else:
        return '-'

def start_quiz(difficulty):
    global current_score, question_number, difficulty_level
    current_score = 0
    question_number = 1
    difficulty_level = difficulty
    
    displayProblem()
    quiz_frame.tkraise()

def displayProblem():
    global question_number, current_answer, attempts_left, difficulty_level
    
    if question_number > 10:
        displayResults()
        return

    attempts_left = 2
    answer_entry.delete(0, tk.END)
    question_counter_label.configure(text=f"Question {question_number}/10")

    num1 = randomInt(difficulty_level)
    num2 = randomInt(difficulty_level)
    op = decideOperation()

    if op == '+':
        current_answer = num1 + num2
    else:
        current_answer = num1 - num2
        
    question_label.configure(text=f"{num1} {op} {num2} =")

def isCorrect():
    global current_score, attempts_left, question_number, current_answer

    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        feedback_label.configure(text="PLEASE ENTER VALID NUMBER")
        return

    if user_answer == current_answer:
        feedback_label.configure(text="")
        if attempts_left == 2:
            current_score += 10
            feedback_label.configure(text="Correct! +10 points")
        else:
            current_score += 5
            feedback_label.configure(text="Correct! +5 points")
        question_number += 1
        displayProblem()    
    else:
        attempts_left -= 1
        if attempts_left == 1:
            feedback_label.configure(text="Incorrect. Try again.")
            answer_entry.delete(0, tk.END)
        else:
            feedback_label.configure(text=f"Incorrect. The answer was {current_answer}.")
            question_number += 1
            displayProblem()

def displayResults():
    global current_score
    
    if current_score >= 90:
        grade = "A+"
    elif current_score >= 80:
        grade = "A"
    elif current_score >= 70:
        grade = "B"
    elif current_score >= 60:
        grade = "C"
    elif current_score >= 50:
        grade = "D"
    else:
        grade = "F"
        
    results_label.configure(text=f"Your final score is: {current_score} / 100")
    grade_label.configure(text=f"GRADE: {grade}")

    results_frame.tkraise()

def play_again():
    menu_frame.tkraise()

def return_to_menu():
    answer = messagebox.askyesno("Return to Menu", 
                               "Are you sure you want to quit this quiz?\n"
                               "YOUR CURRENT PROGRESS WILL BE LOST")
    
    if answer:
        menu_frame.tkraise()


root = tk.Tk()
root.title("Maths Quiz")
root.geometry("800x750")
root.iconphoto(True, ImageTk.PhotoImage(file="img/icon.png"))


try:
    button_size = (340, 94)

    img_easy_original = Image.open("img/easy.png")
    img_easy_resized = img_easy_original.resize(button_size)
    root.easy_img = ImageTk.PhotoImage(img_easy_resized)

    img_moderate_original = Image.open("img/moderate.png")
    img_moderate_resized = img_moderate_original.resize(button_size)
    root.moderate_img = ImageTk.PhotoImage(img_moderate_resized)

    img_advanced_original = Image.open("img/advanced.png")
    img_advanced_resized = img_advanced_original.resize(button_size)
    root.advanced_img = ImageTk.PhotoImage(img_advanced_resized)

    img_submit_original = Image.open("img/submit.png")
    img_submit_resized = img_submit_original.resize(button_size)
    root.submit_img = ImageTk.PhotoImage(img_submit_resized)

    img_return_original = Image.open("img/main_menu.png")
    img_return_resized = img_return_original.resize(button_size)
    root.return_menu_img = ImageTk.PhotoImage(img_return_resized)

    img_play_again_original = Image.open("img/play_again.png")
    img_play_again_resized = img_play_again_original.resize(button_size)
    root.play_again_img = ImageTk.PhotoImage(img_play_again_resized)

except Exception as e:
    print(f"Error loading or resizing images: {e}")
    root.destroy()
    exit()

menu_frame = tk.Frame(root)
menu_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

quiz_frame = tk.Frame(root)
quiz_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

results_frame = tk.Frame(root)
results_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

menu_title = tk.Label(menu_frame, text="DIFFICULTY LEVEL", font=("Terminal", 38))
menu_title.place(relx=0.5, rely=0.2, anchor='center')


easy_button = tk.Button(menu_frame, image=root.easy_img, bd=0,
                        command=lambda: start_quiz('easy'))
easy_button.place(relx=0.5, rely=0.4, anchor='center')

moderate_button = tk.Button(menu_frame, image=root.moderate_img, bd=0,
                            command=lambda: start_quiz('moderate'))
moderate_button.place(relx=0.5, rely=0.55, anchor='center')

advanced_button = tk.Button(menu_frame, image=root.advanced_img, bd=0,
                            command=lambda: start_quiz('advanced'))
advanced_button.place(relx=0.5, rely=0.7, anchor='center')

question_counter_label = tk.Label(quiz_frame, text="Question 1/10", font=("Terminal", 38))
question_counter_label.place(relx=0.5, rely=0.2, anchor='center')

question_label = tk.Label(quiz_frame, text="", font=("Terminal", 34))
question_label.place(relx=0.5, rely=0.35, anchor='center')

answer_entry = tk.Entry(quiz_frame, font=("Terminal", 40), width=11, borderwidth=0, highlightthickness=5, justify='center')
answer_entry.place(relx=0.5, rely=0.45, anchor='center')

feedback_label = tk.Label(quiz_frame, text="", font=("Terminal", 12, "bold"), fg='red')
feedback_label.place(relx=0.5, rely=0.52, anchor='center')

submit_button = tk.Button(quiz_frame, image=root.submit_img, bd=0, command=isCorrect)
submit_button.place(relx=0.5, rely=0.62, anchor='center')

menu_return_button = tk.Button(quiz_frame, image=root.return_menu_img, bd=0, 
                             command=return_to_menu)
menu_return_button.place(relx=0.5, rely=0.78, anchor='center')

final_title = tk.Label(results_frame, text="Quiz Completed!", font=("Terminal", 38))
final_title.place(relx=0.5, rely=0.2, anchor='center')

results_label = tk.Label(results_frame, text="", font=("Terminal", 26))
results_label.place(relx=0.5, rely=0.4, anchor='center')

grade_label = tk.Label(results_frame, text="", font=("Terminal", 26))
grade_label.place(relx=0.5, rely=0.55, anchor='center')

play_again_button = tk.Button(results_frame, image=root.play_again_img, bd=0, command=play_again)
play_again_button.place(relx=0.5, rely=0.75, anchor='center')


menu_frame.tkraise()
root.mainloop()