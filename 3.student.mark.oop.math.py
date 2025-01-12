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

    # Function to input the number of students
    def input_num_of_std(self):
        while True:
            try:
                num_students = int(input("Enter the number of students: "))
                if num_students > 0:
                    self.num_students = num_students
                    break
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

    # Function to input student information
    def input_std_info(self):
        if self.num_students <= 0:
            print("Please input the number of students first.")
            return

        for _ in range(self.num_students):
            while True:
                student_id = input("Enter student ID: ")
                if any(student.id == student_id for student in self.student):
                    print("Student ID already exists. Please enter a unique ID.")
                else:
                    break

            while True:
                student_name = input("Enter student name: ")
                if re.match(r"^[A-Za-z\s]+$", student_name):
                    break
                else:
                    print("Invalid name. Please use letters only (no numbers or special characters).")

            while True:
                student_dob = input("Enter student date of birth (DD/MM/YYYY) (Example: 01/01/1111): ")
                if re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(\d{4})$", student_dob):
                    break
                else:
                    print("Invalid date format. Please use DD/MM/YYYY.")
            self.student.append(Student(student_id, student_name, student_dob))
        print("Student information successfully recorded.")

    # Function to input the number of courses
    def input_num_of_courses(self):
        while True:
            try:
                num_courses = int(input("Enter the number of courses: "))
                if num_courses > 0:
                    self.num_courses = num_courses
                    break
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

    # Function to input course information
    def input_course_info(self):
        if self.num_courses <= 0:
            print("Please input the number of courses first.")
            return
        for _ in range(self.num_courses):
            while True:
                course_id = input("Enter course ID: ")
                if any(course.id == course_id for course in self.course):
                    print("Course ID already exists. Please enter a unique ID.")
                else:
                    break
            course_name = input("Enter course name: ")
            course_credit = int(input("Enter course credits: "))
            self.course.append(Course(course_id, course_name, course_credit))
        print("Course information successfully recorded.")

    # Function to input marks
    def input_course_marks(self):
        if not self.course:
            print("No courses available. Please input course information first.")
            return
        if not self.student:
            print("No students available. Please input student information first.")
            return
        self.list_courses()
        course_id = input("Enter the course ID to input marks: ")
        course = next((c for c in self.course if c.id == course_id), None)
        if not course:
            print("Invalid course ID.")
        if course_id not in self.marks:
            self.marks[course_id] = {}
        for student in self.student:
            while True:
                try:
                    mark = float(input(f"Enter marks for {student.name} (ID: {student.id}): "))
                    if 0 <= mark <= 20:
                        self.marks[course_id][student.id] = math.floor(mark)
                        break
                    else:
                        print("Please enter a mark between 0 and 20.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        print("Marks successfully recorded.")

    # Function to list all students
    def list_students(self):
        if not self.student:
            print("No students available.")
        else:
            print("\nStudents:")
            for student in self.student:
                print(f"ID: {student.id}, Name: {student.name}, DOB: {student.dob}")

    # Function to list all name student and student id
    def list_id(self):
        if not self.student:
            print("No students available.")
        else:
            print("\nStudents:")
            for student in self.student:
                print(f"ID: {student.id}, Name: {student.name}")

    # Function to display course
    def list_courses(self):
        if not self.course:
            print("No courses available.")
        else:
            print("\nCourses: ")
            for course in self.course:
                print(f"Course ID: {course.id}, Course Name: {course.name}")

    # Function to show a student marks
    def show_std_marks(self):
        if not self.marks:
            print("No marks recorded.")
            return
        self.list_id()
        student_id = input("Enter student ID to view mark: ")
        student = next((s for s in self.student if s.id == student_id), None)
        if not student:
            print("Invalid student ID.")
            return
        print(f"\nMarks for Student: {student.name} (ID: {student.id})")
        found_marks = False
        for course_id, course_marks in self.marks.items():
            if student_id in course_marks:
                course = next((c for c in self.course if c.id == course_id), None)
                if course:
                    found_marks = True
                    print(f"Course: {course.name} - Mark: {course_marks[student_id]}")
        if not found_marks:
            print("No marks recorded for this student.")

    # Function to display and select the function
    def input_function(self):
        while True:
            print("\nChoose option to input:")
            print("1. Number of students in a class")
            print("2. Student information: id, name, DoB")
            print("3. Number of courses")
            print("4. Course information: id, name")
            print("5. Select a course, input marks for student")
            print("6. Return to main menu")

            option = input("Enter your option: ")
            if not option.isdigit():
                print("Invalid input. Please enter a number between 1 and 6.")
                continue
            if option == "1":
                self.input_num_of_std()
            elif option == "2":
                self.input_std_info()
            elif option == "3":
                self.input_num_of_courses()
            elif option == "4":
                self.input_course_info()
            elif option == "5":
                self.input_course_marks()
            elif option == "6":
                print("Returning to main menu...")
                break
            else:
                print("Invalid option. Please enter a number between 1 and 6.")

    def main(self):
        while True:
            print("\nWelcome to student mark management")
            print("Choose option:")
            print("1. Input function")
            print("2. List courses")
            print("3. List students")
            print("4. Show student marks")
            print("5. List student by GPA descending")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if not choice.isdigit():
                print("Invalid input. Please enter a number between 1 and 5.")
                continue

            choice = int(choice)

            if choice == 1:
                self.input_function()
            elif choice == 2:
                self.list_courses()
            elif choice == 3:
                self.list_students()
            elif choice == 4:
                self.show_std_marks()
            elif choice == 5:
                print("Student gpa list")
            elif choice == 6:
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

# Call the main function to start the program
if __name__ == "__main__":
    sms = StdManagement()
    sms.main()
