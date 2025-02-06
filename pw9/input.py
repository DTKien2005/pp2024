import re
import math
import pickle
import os
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
from domains.StudentInfo import StudentInfo
from domains.CourseInfo import CourseInfo

# Background thread
save_lock = threading.Lock()  # Define a global lock
def save_data_async(data, file_name):
    def save():
        with save_lock:  # Ensure only one thread writes at a time
            with open(file_name, "wb") as f:
                pickle.dump(data, f)
    thread = threading.Thread(target=save)
    thread.daemon = True
    thread.start()

# Class Student
class Student:
    def __init__(self):
        self.num_students = 0
        self.student = []

    # Function to input number of students
    def input_num(self):
        if self.num_students > 0:
            if not simpledialog.askstring("Input", "You have already input the number of students. Change it? (y/n)").lower() == 'y':
                return
        while True:
            try:
                num_students = int(simpledialog.askstring("Input", "Enter the number of students:"))
                if num_students > 0:
                    self.num_students = num_students
                    messagebox.showinfo("Success", "Number of students updated successfully.")
                    break
                else:
                    messagebox.showerror("Error", "Please enter a positive number.")
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter an integer.")


    # Function to input student information
    def input_std_info(self):
        if self.num_students <= 0:
            messagebox.showerror("Error", "Please input the number of students first.")
            return
        for _ in range(self.num_students):
            while True:
                student_id = simpledialog.askstring("Input", "Enter student ID:")
                if any(s.id == student_id for s in self.student):
                    messagebox.showerror("Error", "Student ID already exists. Please try again.")
                else:
                    break
            while True:
                student_name = simpledialog.askstring("Input", "Enter student name:")
                if not re.match(r"^[A-Za-z\s]+$", student_name):
                    messagebox.showerror("Error", "Invalid name. Use only letters and spaces.")
                else:
                    break
            while True:
                student_dob = simpledialog.askstring("Input", "Enter student date of birth (DD/MM/YYYY):")
                if not re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$", student_dob):
                    messagebox.showerror("Error", "Invalid date format. Use DD/MM/YYYY.")
                else:
                    break
            self.student.append(StudentInfo(student_id, student_name, student_dob))
        # Save students to a file
        file_name = "students.pkl"
        if os.path.exists(file_name):
            messagebox.showinfo("File Exists", f"\n{file_name} already exists. Overwriting...")
        else:
            messagebox.showinfo("File Not Found", f"\n{file_name} does not exist. Creating a new file...")
        save_data_async(self.student, file_name)
        messagebox.showinfo("Success", "Student information saved successfully.")


# Class Course
class Course(Student):
    def __init__(self):
        super().__init__()
        self.num_courses = 0
        self.course = []
        self.marks = {}
        self.gpa = {}

    # Function to input number of courses
    def input_num(self):
        if self.num_courses > 0:
            if not simpledialog.askstring("Input", "You have already input the number of courses. Change it? (y/n)").lower() == 'y':
                return
        while True:
            try:
                num_courses = int(simpledialog.askstring("Input", "Enter the number of courses:"))
                if num_courses > 0:
                    self.num_courses = num_courses
                    messagebox.showinfo("Success", "Number of courses updated successfully.")
                    break
                else:
                    messagebox.showerror("Error", "Please enter a positive number.")
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter an integer.")

    # Function to input course information
    def input_course_info(self):
        if self.num_courses <= 0:
            messagebox.showerror("Error", "Please input the number of courses first.")
            return
        for _ in range(self.num_courses):
            while True:
                course_id = simpledialog.askstring("Input", "Enter course ID:")
                if any(course.id == course_id for course in self.course):
                    messagebox.showerror("Error", "Course ID already exists. Please try again.")
                else:
                    break
            while True:
                course_name = simpledialog.askstring("Input", "Enter course name:")
                if course_name == "":
                    messagebox.showerror("Error", "Course name cannot be empty.")
                else:
                    break
            while True:
                try:
                    course_credit = int(simpledialog.askstring("Input", "Enter course credits (integer):"))
                    if course_credit > 0:
                        break
                    else:
                        messagebox.showerror("Error", "Credits must be a positive integer.")
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please enter an integer.")
            self.course.append(CourseInfo(course_id, course_name, course_credit))

        # Save courses to a file
        file_name = "courses.pkl"
        if os.path.exists(file_name):
            messagebox.showinfo("File Exists", f"\n{file_name} already exists. Overwriting...")
        else:
            messagebox.showinfo("File Not Found", f"\n{file_name} does not exist. Creating a new file...")
        save_data_async(self.course, file_name)
        messagebox.showinfo("Success", "Course information saved successfully.")

    # Function to input marks
    def input_course_marks(self):
        if not self.course:
            messagebox.showerror("Error", "No courses available. Press any key to return.")
            return
        if not self.student:
            messagebox.showerror("Error", "No student available. Press any key to return.")
            return
        # Create a new Tkinter window for course selection
        course_window = tk.Toplevel()
        course_window.title("Select a Course")
        course_window.geometry("400x300")

        tk.Label(course_window, text="Select a course to enter marks:", font=("Arial", 12)).pack(pady=10)

        # Listbox to display courses
        listbox = tk.Listbox(course_window, width=50, height=10)
        for course in self.course:
            listbox.insert(tk.END, f"{course.id} - {course.name}")
        listbox.pack(pady=10)

        def on_select():
            selected_index = listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "Please select a course.")
                return
            selected_course = self.course[selected_index[0]]

            course_window.destroy()  # Close the selection window

            # Initialize marks dictionary if not present
            course_id = selected_course.id
            if course_id not in self.marks:
                self.marks[course_id] = {}

            # Input marks for each student
            for student in self.student:
                while True:
                    try:
                        mark = simpledialog.askfloat("Input Marks", f"Enter marks for {student.name} (ID: {student.id}):")
                        if mark is None:
                            return
                        if 20 >= mark >= 0:
                            self.marks[course_id][student.id] = math.floor(mark)
                            break
                        else:
                            messagebox.showerror("Error", "Invalid input. Please enter an integer number between 20 and 0.\n")
                    except ValueError:
                        messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

            # Write marks to marks.pkl
            file_name = "marks.pkl"
            if not os.path.exists(file_name):
                messagebox.showinfo("File Not Found" ,f"\n{file_name} does not exist. A new file will be created.")
            else:
                messagebox.showinfo("File Not Found", f"\n{file_name} does not exist. Creating a new file...")
            save_data_async(self.marks, file_name)
            messagebox.showinfo("Success", "Marks successfully recorded and saved to marks.txt. Press any key to continue.")

        # Button to confirm selection
        tk.Button(course_window, text="Select Course", command=on_select).pack(pady=10)