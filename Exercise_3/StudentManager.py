import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

filename = "resource/studentMarks.txt"
nav_bg = "#22263d"
btn_bg = "white"
btn_fg = "black"

students = []

def load_data():
    global students
    students = []

    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            start_index = 0
            first_line = lines[0].strip()
            if first_line.isdigit():
                start_index = 1

            for line in lines[start_index:]:
                parts = line.strip().split(',')
                if len(parts) == 6:
                    try:
                        students.append({
                            "id": parts[0],
                            "name": parts[1],
                            "c1": int(parts[2]),
                            "c2": int(parts[3]),
                            "c3": int(parts[4]),
                            "exam": int(parts[5])
                        })
                    except ValueError:
                        continue
    except FileNotFoundError:
        messagebox.showwarning("Warning!!", f"{filename} file not found")
    except Exception as e:
        messagebox.showerror("Warning!!", f"Read Error: {e}")

def save_data():
    try:
        with open(filename, "w") as file:
            file.write(f"{len(students)}\n")
            for s in students:
                line = f"{s['id']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n"
    except Exception as e:
        messagebox.showerror("Writing ERROR")

def calculate_stats(s):
    total_course = s['c1'] + s['c2'] + s['c3']
    total_score = total_course + s['exam']
    percentage = (total_score / 160) *100

    if percentage >= 70:
        grade='A'
    elif percentage >=60: 
        grade='B'
    elif percentage >=50:
        grade='C'
    elif percentage >= 40:
        grade='D'
    else:
        grade='F'

    return total_course, total_score, percentage, grade

#**********     GUI     **********

class StudentManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BSU Student Manager System")
        self.geometry("1920x1080")
        icon = ImageTk.PhotoImage(Image.open("resource/icon.png"))
        self.iconphoto(False, icon)
        load_data()

        self.nav_frame = tk.Frame(self, width=300, bg=nav_bg)
        self.nav_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.nav_frame.pack_propagate(False)

        self.load_images()
        self.logo_label = tk.Label(self.nav_frame, image=self.logo_img, bg=nav_bg)
        self.logo_label.pack(pady=(0,40))

        menu_items = [
            ("View All Records", self.view_all),
            ("View Individual", self.view_individual),
            ("Highest Overall", self.show_highest),
            ("Lowest Overall", self.show_lowest),
            ("Sort Records", self.sort_records),
            ("Add Student", self.add_student),
            ("Delete Student", self.delete_student),
            ("Update Student", self.update_student)
        ]

        for text, command in menu_items:
            btn = tk.Button(self.nav_frame, text=text, command=command, bg=btn_bg, fg=btn_fg, font=("Arial", 15, "bold"), bd=0, pady=10)
            btn.pack(fill=tk.X, padx=20, pady=10)

        self.right_frame = tk.Frame(self, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.bg_label = tk.Label(self.right_frame, image=self.bg_img)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.overlay = None
        self.show_overlay("Welcome", "Please select option from menu")

    def load_images(self):
        logo = Image.open("resource/logo.jpg")
        self.logo_img = ImageTk.PhotoImage(logo)

        background_img = Image.open("resource/bg.jpg").resize((1920, 1080))
        self.bg_img = ImageTk.PhotoImage(background_img)

    def show_overlay(self, title, msg=None):
        if self.overlay:
            self.overlay.destroy()
        
        self.overlay = tk.Frame(self.right_frame, bg="white", bd=2, relief="groove")
        self.overlay.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        tk.Label(self.overlay, text=title, font=("Helvetica", 24, "bold"), bg="white", fg=nav_bg).pack(pady=20)

        if msg:
            tk.Label(self.overlay, text=msg, font=("Arial", 14), bg="white").pack()

        return self.overlay
    
    def view_all(self):
        frame = self.show_overlay("All Student Records")
        cols = ("Name", "ID", "Coursework", "Exam", "%", "Grade")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=25)

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
            if col == "Name":
                tree.column(col, width=250, anchor="w")
        
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(40,0), pady=20)
        scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,40), pady=20)

        total_p = 0
        for s in students:
            tc, ts, p, g =calculate_stats(s)
            total_p +=p
            tree.insert("", tk.END, values=(s['name'], s['id'], tc, s['exam'], f"{p:.1f}%", g))

        if students:
            avg = total_p / len(students)
            tk.Label(frame, text=f"Total: {len(students)} | Average: {avg:.2f}%", bg="white", font=("Arial", 14, "bold")).place(x=40, y=650)
    
    def view_individual(self):
        frame = self.show_overlay("View Individual Record")

        fr = tk.Frame(frame, bg="white")
        fr.pack(pady=20)
        tk.Label(fr, text="Student Name/ID:", bg="white", font=("Arial", 14)).pack(side=tk.LEFT, padx=10)

        entry = tk.Entry(fr, font=("Arial", 14))
        entry.pack(side=tk.LEFT, padx=10)

        lbl_res = tk.Label(frame, text="", bg="white", font=("Arial", 16), justify="left")
        lbl_res.pack(pady=20)

        def search():
            q = entry.get().lower()
            for s in students:
                if q in s['id'].lower() or q in s['name'].lower():
                    tc, ts, p, g = calculate_stats(s)
                    lbl_res.config(text=f"Name: {s['name']}\nID: {s['id']}\nScore: {p:.2f}% ({g})", fg="black")
                    return
            lbl_res.config(text="Not Found", fg="red")
        
        tk.Button(fr, text="Search", command=search, bg=nav_bg, fg="white", font=("Arial", 12)).pack(side=tk.LEFT)

    def show_highest(self):
        frame = self.show_overlay("Highest Score")
        if not students: return
        best=max(students, key=lambda s: s['c1'] + s['c2'] + s['c3'] + s['exam'])
        tc, ts, p, g = calculate_stats(best)
        tk.Label(frame, text=f"{best['name']}", font=("Arial", 36), bg="white", fg="gold").pack(pady=40)
        tk.Label(frame, text=f"{p:.2f}% (Grade {g})", font=("Arial", 24), bg="white").pack()

    def show_lowest(self):
        frame = self.show_overlay("Lowest Score")
        if not students: return
        worst = min(students, key=lambda s: s['c1'] + s['c2'] + s['c3'] + s['exam'])
        tc, ts, p, g = calculate_stats(worst)
        tk.Label(frame, text=f"{worst['name']}", font=("Arial", 36), bg="white", fg="red").pack(pady=40)
        tk.Label(frame, text=f"{p:.2f}% (Grade {g})", font=("Arial", 24), bg="white").pack()

    def sort_records(self):
        students.sort(key=lambda s: s['c1'] + s['c2'] + s['c3'] + s['exam'], reverse=True)
        messagebox.showinfo("Done", "Sorted by score (Descending)")
        self.view_all()

    def add_student(self):
        frame= self.show_overlay("Add New Student")
        form = tk.Frame(frame, bg="white")
        form.pack(pady=20)
        entries={}
        fields=[("ID", "id"), ("Name", "name"), ("C1", "c1"), ("C2", "c2"), ("C3", "c3"), ("Exam", "exam")]

        for i, (lbl, k) in enumerate(fields):
            tk.Label(form, text=lbl, bg="white", font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            e = tk.Entry(form, font=("Arial", 12))
            e.grid(row=i, column=1, padx=10, pady=5)
            entries[k] = e
        
        def save():
            try:
                new_s = {
                    "id": entries["id"].get(),
                    "name": entries["name"].get(),
                    "c1": int(entries["c1"].get()), 
                    "c2": int(entries["c2"].get()),
                    "c3": int(entries["c3"].get()),
                    "exam": int(entries["exam"].get())
                }
                students.append(new_s)
                save_data()
                messagebox.showinfo("SUCCESSFULLY ADDED")
                self.view_all()
            except:
                messagebox.showerror("INVALID INPUT")

        tk.Button(frame, text="SAVE", command=save, bg="green", fg="white", font=("Arial", 14)).pack(pady=20)

    def delete_student(self):
        frame = self.show_overlay("Delete Student")
        tk.Label(frame, text="ID to Delete:", bg="white", font=("Arial", 14)).pack(pady=10)
        e = tk.Entry(frame, font=("Arial", 14))
        e.pack(pady=5)

        def delete():
            tid = e.get()
            for i, s in enumerate(students):
                if s['id'] == tid:
                    if messagebox.askyesno("Confirm", "Delete record?"):
                        del students[i]
                        save_data()
                        messagebox.showinfo("DELETED")
                        self.view_all()
                    return
            messagebox.showerror("Not Found")
        
        tk.Button(frame, text="DELETE", command=delete, bg="red", fg="white", font=("Arial", 12)).pack(pady=10)

    def update_student(self):
        frame = self.show_overlay("Update Student")
        
        search_fr = tk.Frame(frame, bg="white")
        search_fr.pack(pady=10)
        tk.Label(search_fr, text="ID:", bg="white", font=("Arial", 14)).pack(side=tk.LEFT)
        e_id = tk.Entry(search_fr, font=("Arial", 14))
        e_id.pack(side=tk.LEFT, padx=5)

        form = tk.Frame(frame, bg="white")
        entries = {}
        target = {}

        def fetch():
            for w in form.winfo_children(): w.destroy()
            tid = e_id.get()
            found = None
            for s in students:
                if s['id'] == tid: found = s; break

            if found:
                target['ref'] = found
                form.pack(pady=20)
                fields = ["name", "c1", "c2", "c3", "exam"]
                for i, k in enumerate(fields):
                    tk.Label(form, text=k.upper(), bg="white", font=("Arial", 12)).grid(row=i, column=0, sticky="e", pady=5)
                    e = tk.Entry(form, font=("Arial", 12))
                    e.insert(0, str(found[k]))
                    e.grid(row=i, column=1,pady=5)
                    entries[k] = e

                def update():
                    try:
                        s = target['ref']
                        s['name'] = entries['name'].get()
                        s['c1'] = int(entries['c1'].get())
                        s['c2'] = int(entries['c2'].get())
                        s['c3'] = int(entries['c3'].get())
                        s['exam'] = int(entries['exam'].get())
                        save_data()
                        messagebox.showinfo("UPDATED")
                        self.view_all()
                    except:
                        messagebox.showerror("Invalid Date")

                tk.Button(form, text="UPDATE", command=update, bg="orange", font=("Arial", 12)).grid(row=5, columnspan=2, pady=20)
            else:
                messagebox.showerror("ERROR", "Not Found")

        tk.Button(search_fr, text="Find", command=fetch, bg=nav_bg, fg="white", font=("Arial", 14)).pack(side=tk.LEFT)

if __name__ == "__main__":
    app = StudentManager()
    app.mainloop()