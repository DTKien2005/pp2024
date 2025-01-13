import re

# Function to input the number of students
def input_num_of_std():
    while True:
        try:
            num_students = int(input("Enter the number of students: "))
            if num_students > 0:
                return num_students
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

# Function to input student information
def input_std_info(data):
    num_students = data.get("num_students", 0)
    if num_students <= 0:
        print("Please input the number of students first.")
        return
    for _ in range(num_students):
        while True:
            student_id = input("Enter student ID: ")
            if any(students["id"] == student_id for students in data["students"]):
                print("Student ID already exists. Please enter a unique ID.")
            else:
                break
        while True:
            student_name = input("Enter student name: ")
            if re.match(r"^[A-Za-z\s]+$", student_name):  # Only allows letters and spaces
                break
            else:
                print("Invalid name. Please use letters only (no numbers or special characters).")
        while True:
            student_dob = input("Enter student date of birth (DD/MM/YYYY) (Example: 01/01/1111): ")
            if re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(\d{4})$", student_dob):
                break
            else:
                print("Invalid date format. Please use DD/MM/YYYY.")
        data["students"].append({"id": student_id, "name": student_name, "dob": student_dob})
    print("Student information successfully recorded.")

# Function to input the number of courses
def input_num_of_courses():
    while True:
        try:
            num_courses = int(input("Enter the number of courses: "))
            if num_courses > 0:
                return num_courses
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

# Function to input course information
def input_course_info(data):
    num_courses = data.get("num_courses", 0)
    if num_courses <= 0:
        print("Please input the number of courses first.")
        return
    for _ in range(num_courses):
        while True:
            course_id = input("Enter course ID: ")
            if any(courses["id"] == course_id for courses in data["courses"]):
                print("Course ID already exists. Please enter a unique ID.")
            else:
                break
        course_name = input("Enter course name: ")
        data["courses"].append({"id": course_id, "name": course_name})
    print("Course information successfully recorded.")

# Function to input marks
def input_course_marks(data):
    if not data["courses"]:
        print("No courses available. Please input course information first.")
        return
    if not data["students"]:
        print("No students available. Please input student information first.")
        return
    list_courses(data)
    course_id = input("Enter the course ID to input marks: ")
    course = next((c for c in data["courses"] if c["id"] == course_id), None)
    if not course:
        print("Invalid course ID.")
    if course_id not in data["marks"]:
        data["marks"][course_id] = {}
    for students in data["students"]:
        while True:
            try:
                mark = float(input(f"Enter marks for {students['name']} (ID: {students['id']}): "))
                if 0 <= mark <= 20:
                    data["marks"][course_id][students["id"]] = mark
                    break
                else:
                    print("Please enter a mark between 0 and 20.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    print("Marks successfully recorded.")

# Function to list all students
def list_students(data):
    if not data["students"]:
        print("No students available.")
    else:
        print("\nStudents:")
        for student in data["students"]:
            print(f"ID: {student['id']}, Name: {student['name']}, DOB: {student['dob']}")

# Function to list all name student and student id
def list_id(data):
    if not data["students"]:
        print("No students available.")
    else:
        print("\nStudents:")
        for student in data["students"]:
            print(f"ID: {student['id']}, Name: {student['name']}")

# Function to display course
def list_courses(data):
    if not data['courses']:
        print("No courses available.")
    else:
        print("\nCourses: ")
        for courses in data["courses"]:
            print(f"Course ID: {courses['id']}, Course Name: {courses['name']}")

# Function to show a student marks
def show_std_marks(data):
    if not data["marks"]:
        print("No marks recorded.")
        return
    list_id(data)
    student_id = input("Enter student ID to view mark: ")
    student = next((s for s in data["students"] if s["id"] == student_id), None)
    if not student:
        print("Invalid student ID.")
        return
    print(f"\nMarks for Student: {student['name']} (ID: {student['id']})")
    found_marks = False
    for course_id, marks in data["marks"].items():
        if student_id in marks:
            found_marks = True
            print(f"Course: {next(c['name'] for c in data['courses'] if c['id'] == course_id)} - Mark: {marks[student_id]}")
    if not found_marks:
        print("No marks recorded for this student.")

# Function to display and select the function
def input_function(data):
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
            data["num_students"] = input_num_of_std()
        elif option == "2":
            input_std_info(data)
        elif option == "3":
            data["num_courses"] = input_num_of_courses()
        elif option == "4":
            input_course_info(data)
        elif option == "5":
            input_course_marks(data)
        elif option == "6":
            print("Returning to main menu...")
            break  # Exit the loop and return to the main menu
        else:
            print("Invalid option. Please enter a number between 1 and 6.")

def main():
    data = {
        "num_student": 0,
        "students": [],
        "num_courses": 0,
        "courses": [],
        "marks": {}
    }
    while True:
        print("\nWelcome to student mark management")
        print("Choose option:")
        print("1. Input function")
        print("2. List courses")
        print("3. List students")
        print("4. Show student marks")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if not choice.isdigit():
            print("Invalid input. Please enter a number between 1 and 5.")
            continue
        choice = int(choice)
        if choice == 1:
            input_function(data)
        elif choice == 2:
            list_courses(data)
        elif choice == 3:
            list_students(data)
        elif choice == 4:
            show_std_marks(data)
        elif choice == 5:
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# Call the main function to start the program
main()
