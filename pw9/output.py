import tkinter as tk
from tkinter import messagebox
import numpy as np

# Function to list all students
def list_std(self):
    if not self.student:
        messagebox.showwarning("Warning", "No students available.")
    else:
        student_info = "\n".join(f"ID: {student.id}, Name: {student.name}, DOB: {student.dob}" for student in self.student)
        messagebox.showinfo("Students", student_info)

# Function to display course
def list_courses(self):
    if not self.course:
        messagebox.showwarning("Warning","No courses available.")
    else:
        course_info = "\n".join(f"ID: {c.id}, Name: {c.name}, Credits: {c.credit}" for c in self.course)
        messagebox.showinfo("Courses", course_info)

# Function to calculate gpa
def cal_gpa(self):
    for student in self.student:
        credit = []
        marks = []
        for course in self.course:
            if student.id in self.marks.get(course.id, {}):
                credit.append(course.credit)
                marks.append(self.marks[course.id][student.id])
            if credit and marks:
                credits_array = np.array(credit)
                marks_array = np.array(marks)
                weight_sum = np.sum(credits_array * marks_array)
                total_credits = np.sum(credits_array)
                gpa = weight_sum / total_credits
                self.gpa[student.id] = gpa
            else:
                self.gpa[student.id] = 0
                messagebox.showinfo("Warning",f"{student.id:}{student.name}No GPA")
    messagebox.showinfo("GPA Calculation", "GPA calculation completed successfully!")

# Function to sort desc GPA
def sort_by_gpa_desc(self):
    # Convert student GPAs into a NumPy array and sort indices in descending order
    student_gpa_list = [(student, self.gpa.get(student.id, 0)) for student in self.student]

    # Sort students by GPA (descending order)
    sorted_students = sorted(student_gpa_list, key=lambda x: x[1], reverse=True)

    # Format sorted students for display
    sorted_info = "\n".join(f"ID: {student.id}, Name: {student.name}, GPA: {gpa}" for student, gpa in sorted_students)
    messagebox.showinfo("Sorted GPA", f"Students sorted by GPA (descending):\n\n{sorted_info}")
    return [student for student, _ in sorted_students]  # Return sorted student list

# Function to show a student marks
def show_std_marks(self):
    if not self.student:
        messagebox.showwarning("Warning", "No students available.")
        return
    if not self.marks:
        messagebox.showwarning("Warning", "No marks recorded.")
        return

    # Create a new window for student selection
    root = tk.Toplevel()
    root.title("Select a Student")
    root.geometry("400x300")

    tk.Label(root, text="Select a student to view marks:", font=("Arial", 12)).pack(pady=10)

    # Listbox to display students
    listbox = tk.Listbox(root, width=50, height=10)
    for student in self.student:
        listbox.insert(tk.END, f"{student.id} - {student.name}")
    listbox.pack(pady=10)

    def on_select():
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a student.")
            return

        selected_student = self.student[selected_index[0]]
        student_id = selected_student.id

        # Retrieve marks for the selected student
        marks_info = f"Marks for {selected_student.name} (ID: {student_id}):\n"
        found_marks = False

        for course_id, course_marks in self.marks.items():
            if student_id in course_marks:
                course = next((c for c in self.course if c.id == course_id), None)
                if course:
                    found_marks = True
                    marks_info += f" - {course.name}: {course_marks[student_id]}\n"

        if not found_marks:
            marks_info += "No marks recorded for this student."

        # Hide the window before showing the marks
        root.withdraw()

        messagebox.showinfo("Student Marks", marks_info)

        # Close the window after showing the marks
        root.destroy()

    # Button to confirm selection
    tk.Button(root, text="View Marks", command=on_select).pack(pady=10)

    root.mainloop()
