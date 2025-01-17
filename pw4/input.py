import re
import curses
import math
from domains.StudentInfo import StudentInfo
from domains.CourseInfo import CourseInfo

# Class Student
class Student:
    def __init__(self):
        self.num_students = 0
        self.student = []

    # Function to input number of students
    def input_num(self, window, prompt):
        if getattr(self, "num_students", 0) > 0:
            window.clear()
            window.addstr("You have already input the number of students.\n")
            window.addstr("Do you want to change it? (y/n): ")
            window.refresh()
            curses.echo()
            change = window.getstr().decode().strip().lower()
            curses.noecho()
            if change != 'y':
                return

        while True:
            try:
                window.clear()
                window.addstr("Enter the number of students: ")
                window.refresh()
                curses.echo()
                num_students = int(window.getstr().decode().strip())
                curses.noecho()
                if num_students > 0:
                    self.num_students = num_students
                    window.addstr("\nNumber of students updated successfully. Press any key to continue.")
                    window.getch()
                    break
                else:
                    window.addstr("\nPlease enter a positive number. Press any key to retry.")
                    window.getch()
            except ValueError:
                window.addstr("\nInvalid input. Please enter an integer. Press any key to retry.")
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
                self.student.append(StudentInfo(student_id, student_name, student_dob))
                break
        window.addstr("\nAll student information successfully recorded. Press any key to continue.")
        window.refresh()
        window.getch()

# Class Course
class Course(Student):
    def __init__(self):
        super().__init__()
        self.num_courses = 0
        self.course = []
        self.marks = {}
        self.gpa = {}

    # Function to input number of courses
    def input_num(self, window, prompt):
        if getattr(self, "num_courses", 0) > 0:
            window.clear()
            window.addstr("You have already input the number of courses.\n")
            window.addstr("Do you want to change it? (y/n): ")
            window.refresh()
            curses.echo()
            change = window.getstr().decode().strip().lower()
            curses.noecho()
            if change != 'y':
                return

        while True:
            try:
                window.clear()
                window.addstr("Enter the number of courses: ")
                window.refresh()
                curses.echo()
                num_courses = int(window.getstr().decode().strip())
                curses.noecho()
                if num_courses > 0:
                    self.num_courses = num_courses
                    window.addstr("\nNumber of courses updated successfully. Press any key to continue.")
                    window.getch()
                    break
                else:
                    window.addstr("\nPlease enter a positive number. Press any key to retry.")
                    window.getch()
            except ValueError:
                window.addstr("\nInvalid input. Please enter an integer. Press any key to retry.")
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
                self.course.append(CourseInfo(course_id, course_name, course_credit))
                break
        window.addstr("\nAll course information successfully recorded. Press any key to continue.")
        window.refresh()
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
        while True:
            window.clear()
            window.addstr("Courses:\n")
            for course in self.course:
                window.addstr(f"Course ID: {course.id}, Course Name: {course.name}\n")
            window.addstr("\n\nEnter the course ID to input marks (or press 'q' to quit): ")
            window.refresh()
            curses.echo()
            course_id = window.getstr().decode().strip()
            curses.noecho()
            if course_id.lower() == 'q':
                break

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
                while True:
                    window.addstr(f"Enter marks for {student.name} (ID: {student.id}): ")
                    curses.echo()
                    mark = float(window.getstr().decode().strip())
                    curses.noecho()
                    if 20 >= mark >= 0:
                        self.marks[course_id][student.id] = math.floor(mark)
                        break
                    else:
                        window.addstr("Invalid input. Please enter an integer number between 20 and 0.\n")
                        window.refresh()
            window.addstr("\nMarks successfully recorded. Press any key to continue.")
            window.getch()