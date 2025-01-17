import curses
from input import Student, Course
from output import display_menu, list_courses, list_std, show_std_marks, cal_gpa, sort_by_gpa_desc

# Class StudentManagement
class StdManagement(Course):
    def __init__(self):
        super().__init__()

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
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

# Call the main function to start the program
if __name__ == "__main__":
    sms = StdManagement()
    curses.wrapper(sms.main)

