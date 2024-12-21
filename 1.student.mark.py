import re

#Function to input the number of students
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

#Function to input student information
def input_std_info(data):
    num_students = data.get("num_students", 0)
    if num_students <= 0:
        print("Please input the number of students first.")
        return

    for _ in range(num_students):
        student_id = input("Enter student ID: ")
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

# Function to list all students
def list_students(data):
    if not data["students"]:
        print("No students available.")
    else:
        print("\nStudents:")
        for student in data["students"]:
            print(f"ID: {student['id']}, Name: {student['name']}, DOB: {student['dob']}")

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
            print("Input number of courses")
        elif option == "4":
            print("Input course information: id, name")
        elif option == "5":
            print("Select a course, input marks for student in this course")
        elif option == "6":
            print("Returning to main menu...")
            break  # Exit the loop and return to the main menu
        else:
            print("Invalid option. Please enter a number between 1 and 6.")

def main():
    data = {
        "num_student": 0,
        "students": [],
        "num_course": 0,
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
            print("Listing courses...")
        elif choice == 3:
            list_students(data)
        elif choice == 4:
            print("Showing student marks...")
        elif choice == 5:
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# Call the main function to start the program
main()
