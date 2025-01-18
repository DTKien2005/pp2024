import curses
import numpy as np

def display_menu(window, prompt, options):
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

# Function to list all students
def list_std(self, window):
    window.clear()
    if not self.student:
        window.addstr("No students available.")
    else:
        window.addstr("Students:\n")
        for student in self.student:
            window.addstr(f"ID: {student.id}, Name: {student.name}, DOB: {student.dob}\n")
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

# Function to calculate gpa
def cal_gpa(self, window):
    window.clear()
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
    if not self.student:
        window.addstr("No students available.\n")
        window.addstr("Press any key to return.")
        window.getch()
        return
    if not self.marks:
        window.addstr("No marks recorded. Press any key to return.")
        window.getch()
        return

    while True:
        window.clear()
        window.addstr("Students:\n")
        for student in self.student:
            window.addstr(f"ID: {student.id}, Name: {student.name}\n")
        window.addstr("\n\nEnter student ID to view marks (or press 'q' to quit): ")
        window.refresh()
        curses.echo()
        student_id = window.getstr().decode().strip()
        curses.noecho()
        if student_id.lower() == 'q':
            break

        student = next((s for s in self.student if s.id == student_id), None)
        if not student:
            window.addstr("Invalid student ID. Press any key to try again.")
            window.getch()
            continue

        window.clear()
        window.addstr(f"Marks for Student: {student.name} (ID: {student.id})\n")
        found_marks = False
        for course_id, course_marks in self.marks.items():
            if student_id in course_marks:
                course = next((c for c in self.course if c.id == course_id), None)
                if course:
                    found_marks = True
                    window.addstr(f"Course: {course.name} - Mark: {course_marks[student_id]}\n")
        if not found_marks:
            window.addstr("No marks recorded for this student.\n")
        window.addstr("\nPress any key to return to the main menu.")
        window.getch()