import re
import math
import numpy as np
import curses

# Class Student
class Student:
    def __init__(self, student_id, name, dob):
        self.id = student_id
        self.name = name
        self.dob = dob

# Class Course
class Course:
    def __init__(self, course_id,name,course_credit):
        self.id = course_id
        self.name = name
        self.credit = course_credit

# Class StudentManagement
class StdManagement:
    def __init__(self):
        self.num_students = 0
        self.student = []
        self.num_courses = 0
        self.course = []
        self.marks = {}
        self.gpa = {}

    def display_menu(self, window, prompt, options):
        while True:
            window.clear()
            window.addstr(f"{prompt}\n\n")
            for i, option in enumerate(options, 1):
                window.addstr(f"{i}. {option}\n")
            window.addstr("\nEnter your choice: ")
            window.refresh()

            try:
                curses.echo()
                choice = int(window.getstr().decode())
                curses.noecho()
                if 1 <= choice <= len(options):
                    return choice
                else:
                    window.addstr("\nInvalid choice. Press any key to try again.")
                    window.getch()
            except ValueError:
                window.addstr("\nInvalid input. Please enter a valid number. Press any key to try again.")
                window.getch()

    # Input a positive integer
    def input_positive_int(self, window, prompt):
        while True:
            window.clear()
            window.addstr(prompt)
            window.refresh()
            try:
                curses.echo()
                user_input = int(window.getstr().decode())
                curses.noecho()
                if user_input > 0:
                    return user_input
                else:
                    window.addstr("\nPlease enter a positive number. Press any key to retry.")
                    window.getch()
            except ValueError:
                window.addstr("\nInvalid input. Please enter an integer. Press any key to retry.")
                window.getch()

    # Input text with validation
    def input_text(self, window, prompt, validation=None):
        while True:
            window.clear()
            window.addstr(prompt)
            window.refresh()
            curses.echo()
            user_input = window.getstr().decode().strip()
            curses.noecho()
            if not validation or validation(user_input):
                return user_input
            window.addstr("\nInvalid input. Press any key to retry.")
            window.getch()

    # Function to input student information
    def input_std_info(self, window):
        # Check if the number of students is set and greater than 0
        if self.num_students <= 0:
            window.clear()
            window.addstr("Please input the number of students first.\n")
            window.addstr("Press any key to return to the previous menu.")
            window.refresh()
            window.getch()
            return

        for _ in range(self.num_students):
            while True:
                window.clear()
                window.addstr("Enter student information\n")
                window.addstr(f"Number of students left to input: {self.num_students - len(self.student)}\n\n")

                # Input Student ID
                while True:
                    window.addstr("Enter student ID: ")
                    window.refresh()
                    curses.echo()
                    student_id = window.getstr().decode().strip()
                    curses.noecho()
                    if any(s.id == student_id for s in self.student):
                        window.addstr("\nStudent ID already exists. Please try again.\n")
                    else:
                        break
                    window.getch()
                    window.clear()
                    window.addstr("Enter student information\n")

                # Input Student Name
                while True:
                    window.addstr("Enter student name: ")
                    window.refresh()
                    curses.echo()
                    student_name = window.getstr().decode().strip()
                    curses.noecho()
                    if not re.match(r"^[A-Za-z\s]+$", student_name):
                        window.addstr("\nInvalid name. Use only letters and spaces. Please try again.\n")
                    else:
                        break
                    window.getch()

                # Input Student Date of Birth
                while True:
                    window.addstr("Enter student date of birth (DD/MM/YYYY): ")
                    window.refresh()
                    curses.echo()
                    student_dob = window.getstr().decode().strip()
                    curses.noecho()
                    if not re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(\d{4})$", student_dob):
                        window.addstr("\nInvalid date format. Use DD/MM/YYYY. Please try again.\n")
                    else:
                        break
                    window.getch()
                # Add student to the list if all inputs are valid
                self.student.append(Student(student_id, student_name, student_dob))
                break
        window.addstr("\nAll student information successfully recorded. Press any key to continue.")
        window.refresh()
        window.getch()

    # Function to input course information
    def input_course_info(self, window):
        if self.num_courses <= 0:
            window.clear()
            window.addstr("Please input the number of courses first.\n")
            window.addstr("Press any key to return to the previous menu.\n")
            window.getch()
            return
        for _ in range(self.num_courses):
            while True:
                window.clear()
                window.addstr("Enter course information\n")
                window.addstr(f"Number of course left to input: {self.num_courses - len(self.course)}\n\n")
                while True:
                    window.addstr("Enter course ID: ")
                    window.refresh()
                    curses.echo()
                    course_id = window.getstr().decode().strip()
                    curses.noecho()
                    if any(course.id == course_id for course in self.course):
                        print("Course ID already exists. Please enter a unique ID.\n")
                    else:
                        break
                while True:
                    window.addstr("Enter course name: ")
                    window.refresh()
                    curses.echo()
                    course_name = window.getstr().decode().strip()
                    curses.noecho()
                    if course_name == "":
                        window.addstr("\nCourse name cannot be empty. Please try again.\n")
                        window.getch()
                    else:
                        break
                while True:
                    window.addstr("Enter course credits (integer): ")
                    window.refresh()
                    curses.echo()
                    try:
                        course_credit = int(window.getstr().decode().strip())
                        curses.noecho()
                        if course_credit <= 0:
                            window.addstr("\nCredits must be a positive integer. Please try again.\n")
                            window.getch()
                        else:
                            break
                    except ValueError:
                        curses.noecho()
                        window.addstr("\nInvalid input. Please enter a valid integer for credits.\n")
                        window.getch()
                self.course.append(Course(course_id, course_name, course_credit))
                break
        window.addstr("\nAll course information successfully recorded. Press any key to continue.")
        window.refresh()
        window.getch()

    # Function to list all students
    def list_students(self, window):
        window.clear()
        if not self.student:
            window.addstr("No students available.")
        else:
            window.addstr("Students:\n")
            for student in self.student:
                window.addstr(f"ID: {student.id}, Name: {student.name}, DOB: {student.dob}\n")
        window.addstr("\nPress any key to return.")
        window.getch()

    def list_id(self, window):
        window.clear()
        if not self.student:
            window.addstr("No students available.")
        else:
            window.addstr("Students:\n")
            for student in self.student:
                window.addstr(f"ID: {student.id}, Name: {student.name} \n")
        window.addstr("\nPress any key to return.")
        window.getch()

    # Function to display course
    def list_courses(self, window):
        window.clear()
        if not self.course:
            window.addstr("No courses available.")
        else:
            window.addstr("Courses:\n")
            for course in self.course:
                window.addstr(f"Course ID: {course.id}, Course Name: {course.name}\n")
        window.addstr("\nPress any key to return.")
        window.getch()

    # Function to input marks
    def input_course_marks(self, window):
        window.clear()
        if not self.course:
            window.addstr("No courses available. Press any key to return.")
            window.getch()
            return
        if not self.student:
            window.clear()
            window.addstr("No student available. Press any key to return.")
            window.getch()
            return
        self.list_courses(window)
        course_id = self.input_text(window,"Enter the course ID to input marks: ")
        course = next((c for c in self.course if c.id == course_id), None)
        if not course:
            window.addstr("\nInvalid course ID. Press any key to return.")
            window.getch()
            return
        # Initialize marks for the course if not already present
        if course_id not in self.marks:
            self.marks[course_id] = {}
        # Input marks for each student
        for student in self.student:
            mark = self.input_positive_int(window, f"Enter marks for {student.name} (ID: {student.id}): ")
            self.marks[course_id][student.id] = math.floor(mark)
        window.addstr("\nMarks successfully recorded. Press any key to continue.")
        window.getch()

    # Function to calculate gpa
    def cal_gpa(self, window):
        window.addstr("\nCalculating GPA for all students...\n")
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
                    window.addstr(f"{student.id:}{student.name}No GPA")
        window.addstr("GPA calculation complete.\n")

    # Function to sort desc GPA
    def sort_by_gpa_desc(self, window):
        window.clear()
        self.cal_gpa(window)
        student_gpa = np.array([self.gpa.get(student.id, 0) for student in self.student])
        sorted_gpa = np.argsort(-student_gpa)
        window.addstr("\nStudents sorted by GPA (descending): \n")
        for idx in sorted_gpa:
            student = self.student[idx]
            gpa = self.gpa.get(student.id, "No GPA")
            window.addstr(f"ID: {student.id}, Name: {student.name}, GPA: {gpa}\n")
        window.addstr("\nSorting completed. Press any key to return.")
        window.getch()
        return [self.student[idx] for idx in sorted_gpa]

    # Function to show a student marks
    def show_std_marks(self, window):
        window.clear()
        if not self.marks:
            window.addstr("No marks recorded. Press any key to return.")
            window.getch()
            return
        self.list_id(window)
        student_id = self.input_text(window, "Enter student ID to view mark: ")
        student = next((s for s in self.student if s.id == student_id), None)
        if not student:
            window.addstr("Invalid student ID. Press any key to return.")
            window.getch()
            return
        window.addstr(f"\nMarks for Student: {student.name} (ID: {student.id})\n")
        found_marks = False
        for course_id, course_marks in self.marks.items():
            if student_id in course_marks:
                course = next((c for c in self.course if c.id == course_id), None)
                if course:
                    found_marks = True
                    window.addstr(f"Course: {course.name} - Mark: {course_marks[student_id]}\n")
        if not found_marks:
            window.addstr("No marks recorded for this student.\n")
        window.addstr("\nPress any key to return.")
        window.getch()

    # Function to display and select the function
    def input_function(self, window):
        curses.curs_set(0)
        while True:
            input_options = [
                "Number of students in a class",
                "Student information: id, name, DoB",
                "Number of courses",
                "Course information: id, name",
                "Select a course, input marks for students",
                "Return to main menu"
            ]

            option = self.display_menu(window, "Input Menu", input_options)
            if option == 1:
                self.num_students = self.input_positive_int(window, "Enter the number of students: ")
            elif option == 2:
                self.input_std_info(window)
            elif option == 3:
                self.num_courses = self.input_positive_int(window, "Enter the number of courses: ")
            elif option == 4:
                self.input_course_info(window)
            elif option == 5:
                self.input_course_marks(window)
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
            choice = self.display_menu(window, "Main Menu", options)
            if choice == 1:
                self.input_function(window)
            elif choice == 2:
                self.list_courses(window)
            elif choice == 3:
                self.list_students(window)
            elif choice == 4:
                self.show_std_marks(window)
            elif choice == 5:
                self.sort_by_gpa_desc(window)
            elif choice == 6:
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

# Call the main function to start the program
if __name__ == "__main__":
    sms = StdManagement()
    curses.wrapper(sms.main)
