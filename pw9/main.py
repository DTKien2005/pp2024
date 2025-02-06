import tkinter as tk
import os
import pickle
import zipfile
from domains.StudentInfo import StudentInfo
from domains.CourseInfo import CourseInfo
from input import Student, Course
from output import list_courses, list_std, show_std_marks, cal_gpa, sort_by_gpa_desc

def compress_file(output_file="students.dat"):
    files_to_compress = ["students.pkl", "courses.pkl", "marks.pkl"]
    with zipfile.ZipFile(output_file, "w") as z:
        for file in files_to_compress:
            if os.path.exists(file):
                z.write(file, arcname=os.path.basename(file))
    print("Files compressed successfully into students.dat.")

def decompress_file(input_file="students.dat"):
    if not os.path.exists(input_file):
        print(f"{input_file} not found. Starting with empty data.")
        return None, None, None

    # Extract the ZIP file
    with zipfile.ZipFile(input_file, "r") as z:
        z.extractall()  # This will extract all files in the current directory
        print("Files decompressed successfully.")

# Class StudentManagement
class StdManagement(Course):
    def __init__(self):
        super().__init__()
        decompress_file()  # Load data from students.dat
        # Ensure the in-memory data matches the decompressed files
        if os.path.exists("students.pkl"):
            with open("students.pkl", "rb") as f:
                self.student = pickle.load(f)

        if os.path.exists("courses.pkl"):
            with open("courses.pkl", "rb") as f:
                self.course = pickle.load(f)

        if os.path.exists("marks.pkl"):
            with open("marks.pkl", "rb") as f:
                self.marks = pickle.load(f)

    # Function to display and select the function
    def input_function(self, main_window):
        # Hide the main window
        main_window.withdraw()

        # Create a new top-level window (Input Menu)
        input_window = tk.Toplevel()
        input_window.title("Input Menu")
        input_window.geometry("500x400")  # Adjust size as needed

        # Function to close input window and show the main window again
        def close_input_window():
            input_window.destroy()
            main_window.deiconify()  # Show main window again

        input_options = [
            "Number of students in a class",
            "Student information: id, name, DoB",
            "Number of courses",
            "Course information: id, name, credits",
            "Select a course, input marks for students",
            "Return to main menu"
        ]

        radio_value = tk.IntVar()
        radio_value.set(1)  # Default selection

        for i, option in enumerate(input_options, start=1):
            tk.Radiobutton(input_window,
                           variable=radio_value,
                           text=option,
                           value=i,
                           anchor="w").pack(anchor="w",padx=20, pady=5)

        def submit_choice():
            option = radio_value.get()

            if option == 1:
                Student.input_num(self)
            elif option == 2:
                Student.input_std_info(self)
            elif option == 3:
                Course.input_num(self)
            elif option == 4:
                Course.input_course_info(self)
            elif option == 5:
                Course.input_course_marks(self)
            elif option == 6:
                close_input_window()  # Hide input window and show main window again

        submit_button = tk.Button(input_window, text="Submit", command=submit_choice)
        submit_button.pack(pady=10)

        # Button to return without selection
        close_button = tk.Button(input_window, text="Return to Main Menu", command=close_input_window)
        close_button.pack(pady=10)

        input_window.protocol("WM_DELETE_WINDOW", close_input_window)  # Handle window close event

    def main(self):
        window = tk.Tk()
        window.title("Student Information System")
        window.geometry("400x300")

        options = [
            "Input function",
            "List courses",
            "List students",
            "Show student marks",
            "List students by GPA descending",
            "Exit"
        ]
        frame = tk.Frame(window)
        frame.pack(expand=True)  # Center the frame in the window

        radioValue = tk.IntVar()
        radioValue.set(1)

        for i, option in enumerate(options, start=1):
            tk.Radiobutton(
                frame,
                variable=radioValue,
                text=option,
                value=i,
                anchor="w",  # Left-align text inside the button
                justify="left",
                width=30  # Set a fixed width to make all buttons the same size
            ).pack(anchor="center", pady=5)  # Center buttons inside the frame

        def submit_choice():
            choice = radioValue.get()
            if choice == 1:
                self.input_function(window)
            elif choice == 2:
                list_courses(self)
            elif choice == 3:
                list_std(self)
            elif choice == 4:
                show_std_marks(self)
            elif choice == 5:
                cal_gpa(self)
                sort_by_gpa_desc(self)
            elif choice == 6:
                compress_file()
                print("Exiting the program.")
                window.destroy()

        submit_button = tk.Button(window, text="Submit", command=submit_choice)
        submit_button.pack()

        window.mainloop()

if __name__ == "__main__":
    sms = StdManagement()
    sms.main()

