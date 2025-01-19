import curses
import os
import pickle
import zipfile
from domains.StudentInfo import StudentInfo
from domains.CourseInfo import CourseInfo
from input import Student, Course
from output import display_menu, list_courses, list_std, show_std_marks, cal_gpa, sort_by_gpa_desc

def compress_file(output_file="students.dat"):
    files_to_compress = ["student.pkl", "course.pkl", "marks.pkl"]
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
    def input_function(self, window):
        curses.curs_set(0)
        while True:
            input_options = [
                "Number of students in a class",
                "Student information: id, name, DoB",
                "Number of courses",
                "Course information: id, name, credits",
                "Select a course, input marks for students",
                "Return to main menu"
            ]

            option = display_menu(window, "Input Menu", input_options)
            if option == 1:
                Student.input_num(self, window, "Enter the number of students: ")
            elif option == 2:
                Student.input_std_info(self, window)
            elif option == 3:
                Course.input_num(self, window, "Enter the number of courses: ")
            elif option == 4:
                Course.input_course_info(self, window)
            elif option == 5:
                Course.input_course_marks(self, window)
            elif option == 6:
                window.addstr("To return to main menu press key.")
                window.getch()
                break
            else:
                window.addstr("Invalid option. Please enter a number between 1 and 6.")
                window.getch()

    def main(self, window):
        curses.curs_set(0)
        while True:
            options = [
                "Input function",
                "List courses",
                "List students",
                "Show student marks",
                "List students by GPA descending",
                "Exit"
            ]
            choice = display_menu(window, "Main Menu", options)
            if choice == 1:
                self.input_function(window)
            elif choice == 2:
                list_courses(self, window)
            elif choice == 3:
                list_std(self, window)
            elif choice == 4:
                show_std_marks(self, window)
            elif choice == 5:
                cal_gpa(self, window)
                sort_by_gpa_desc(self, window)
            elif choice == 6:
                compress_file()
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

# Call the main function to start the program
if __name__ == "__main__":
    sms = StdManagement()
    curses.wrapper(sms.main)

