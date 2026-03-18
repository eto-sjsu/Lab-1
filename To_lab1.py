import csv
import time
import sys
import os
import unittest



courses_dict = {}
professors_dict = {}
logins_dict = {}

class LoginUser:

    def __init__(self, emailID, password, role):
        self.emailID = emailID
        self.password = password
        self.role = role
        self.is_logged_in = False
 
    def Login(self, entered_password):
        decrypted = self.decrypt_password(self.password)
        if decrypted == entered_password:
            self.is_logged_in = True
            print(f"You are now logged in as {self.emailID}.")
            return True
        else:
            print("Incorrect password. Try again.")
            return False
 
    def Logout(self):
            self.is_logged_in = False
            print(f"{self.emailID} has been logged out.")

    def change_password(self, old_password, new_password):
        if self.decrypt_password(self.password) == old_password:
            self.password = self.encrypt_password(new_password)
            print("Password updated successfully.")
        else:
            print("Old password is incorrect, password not changed.")
 
    def encrypt_password(self, unencrypted_pass):
        shift = 8
        encoded = ""
        for char in unencrypted_pass:
            new_char = chr(ord(char) + shift)
            encoded += new_char
        return encoded
 
    def decrypt_password(self, encrypted_pass):
        shift = 8
        decoded = ""
        for char in encrypted_pass:
            original_char = chr(ord(char) - shift)
            decoded += original_char
        return decoded



class Grades:

    def __init__(self, gradeID, grade, marks_range):
        self.gradeID = gradeID
        self.grade = grade
        self.marks_range = marks_range

    def display_grade_report(self):
        print(f"Grade ID: {self.gradeID} | Grade: {self.grade} | Marks Range: {self.marks_range}")


    def add_grade(self, gradeID, grade, marks_range):
        self.gradeID = gradeID
        self.grade = grade
        self.marks_range = marks_range
        print(f"Grade {grade} has been added.")

    def delete_grade(self):
        print(f'Removed grade {self.grade}')
        self.gradeID = None
        self.grade = None
        self.marks_range = None
        

    def modify_grade(self,new_grade=None, new_range=None):
        if new_grade:
            self.grade = new_grade
        if new_range:
            self.marks_range = new_range
        print(f'Updated Grade:{self.grade} and Range:{self.marks_range}')

class Course:

    def __init__(self, courseID, credits, course_name):
        self.courseID = courseID
        self.credits = credits
        self.course_name = course_name

    def display_courses(self):
        print(f'ID: {self.courseID} | Name: {self.course_name} | Credits: {self.credits}')
 
    def add_new_course(self, courseID, credits, course_name):
        self.courseID = courseID
        self.credits = credits
        self.course_name = course_name
        print(f"{course_name} (ID: {courseID}) added.")
 
    def delete_new_course(self):
        print(f"{self.course_name} (ID: {self.courseID}) deleted.")
        self.courseID = None
        self.credits = None
        self.course_name = None

    def calc_average_marks(self):
        marks_list = []
        current = Student.head
        while current:
            if current.courseID == self.courseID:
                try:
                    marks_list.append(float(current.marks))
                except ValueError:
                    pass
            current = current.next

        if len(marks_list) == 0:
            print(f"No marks found for {self.course_name}.")
            return

        total = 0
        for m in marks_list:
            total += m
        count = len(marks_list)
        avg = total / count
        print(f"Course: {self.course_name} | Students: {count} | Average: {avg:.2f}")

    def calc_median_marks(self):
        marks_list = []
        current = Student.head
        while current:
            if current.courseID == self.courseID:
                try:
                    marks_list.append(float(current.marks))
                except ValueError:
                    pass
            current = current.next

        if len(marks_list) == 0:
            print(f"No student marks found for {self.course_name}.")
            return

        n = len(marks_list)
        for i in range(n):
            for j in range(0, n - i - 1):
                if marks_list[j] > marks_list[j + 1]:
                    temp = marks_list[j]
                    marks_list[j] = marks_list[j + 1]
                    marks_list[j + 1] = temp

        mid = n // 2
        if n % 2 == 0:
            median = (marks_list[mid - 1] + marks_list[mid]) / 2
        else:
            median = marks_list[mid]

        print(f"Course: {self.course_name} | Students: {n} | Median Marks: {median:.2f}")

class Person:

    def __init__(self, email, firstname, lastname, role):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.role = role

class Professor(Person):

    def __init__(self,email ,firstname, lastname, rank, courseID=None):
        super().__init__(email, firstname, lastname, "professor")
        self.rank = rank
        self.courseID = courseID if courseID else ""

    def professors_details(self):
        cid = self.courseID if self.courseID else "None"
        print(f'Email:{self.email} | {self.firstname} {self.lastname} | Rank:{self.rank} | CourseID: {cid}')

    def add_new_professor(self,email, firstname,lastname,rank, courseID=None):

        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.rank = rank
        self.courseID = courseID if courseID else ""
        print(f"Professor {self.firstname} {self.lastname} added successfully.")

    def delete_professor(self):
        if self.email in professors_dict:
            del professors_dict[self.email]
        print(f"Professor {self.email} | {self.firstname} {self.lastname} deleted.")
        self.email = None
        self.firstname = None
        self.lastname = None
        self.rank = None
        self.courseID = "" 

    def modify_professor_details(self, firstname=None, lastname=None, email=None, rank=None, courseID=None):
        if firstname:
            self.firstname = firstname
        if lastname:
            self.lastname = lastname
        if email:
            self.email = email
        if rank:
            self.rank = rank
        if courseID is not None:
            self.courseID = courseID 
        print(f"Details updated for: {self.email} {self.firstname} {self.lastname}")

    def show_course_details_by_professor(self):
        print("\n--- Courses by Professor ---")
        if not professors_dict:
            print("No professors found.")
            return
        for email, p in professors_dict.items():
            print(f"\nProfessor: {p.firstname} {p.lastname} | Rank: {p.rank}")
            if not p.courseID:
                print("No course found.")
            else:
                if p.courseID in courses_dict:
                    c = courses_dict[p.courseID]
                    print(f"ID: {c.courseID} | {c.course_name} | Credits: {c.credits}")
                else:
                    print(f"Course {p.courseID} not found in course list")


class Student(Person):

    head = None

    def __init__(self, email, firstname, lastname, courseID, grades, marks):
        super().__init__(email, firstname, lastname, "student")
        self.courseID = courseID
        self.grades = grades
        self.marks = marks
        self.next = None

    def display_records(self):
        print(f'ID: {self.email} | {self.firstname} {self.lastname} | CourseID:{self.courseID} | Grade: {self.grades} | Marks:{self.marks}')

    def check_my_grades(self):
        print(f"{self.firstname} {self.lastname}  |  Course: {self.courseID}  |  Grade: {self.grades}")

    def check_my_marks(self):
        print(f"{self.firstname} {self.lastname}  |  Course: {self.courseID}  |  Marks: {self.marks}")


    def update_student_record(self, firstname=None, lastname=None, email=None, grades=None, marks=None):
        if firstname:
            self.firstname = firstname
        if lastname:
            self.lastname = lastname
        if email:
            self.email = email
        if grades:
            self.grades = grades
        if marks is not None:
            self.marks = marks
        print(f"Updated {self.firstname} {self.lastname} ID: {self.email}")

    @classmethod
    def add_new_student(cls, student):
        if not student.email or student.email.strip() == "":
            print("Student email cannot be empty.")
            return False
        if cls.search_student(student.email):
            print(f"A student with email {student.email} already exists.")
            return False
        student.next = None
        if cls.head is None:
            cls.head = student
            return True
        c1 = cls.head
        while c1.next:
            c1 = c1.next
        c1.next = student
        return True
    
    @classmethod
    def delete_student(cls, email):
        c1 = cls.head
        previous = None
        while c1:
            if c1.email == email:
                if previous is None:
                    cls.head = c1.next
                else:
                    previous.next = c1.next
                c1.next = None
                return c1
            previous = c1
            c1 = c1.next
        return None

    @classmethod
    def search_student(cls, email):

        c1 = cls.head
        while c1:
            if c1.email == email:
                return c1
            c1 = c1.next
        return None
    
    @classmethod
    def sort_students(cls, key='lastname', descending=False, silent=False):
        arr = []
        current = cls.head
        while current:
            arr.append(current)
            current = current.next
#bubble sorting
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if key == 'marks':
                    try:
                        val_a = float(arr[j].marks)
                        val_b = float(arr[j + 1].marks)
                    except ValueError:
                        val_a = 0.0
                        val_b = 0.0
                elif key == 'email':
                    val_a = arr[j].email
                    val_b = arr[j + 1].email
                else:
                    val_a = arr[j].lastname
                    val_b = arr[j + 1].lastname

                if (val_a > val_b) if not descending else (val_a < val_b):
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

# only added this to not bloat terminal
        if not silent:
            print("\n--- Sorted Students ---")
            for s in arr:
                s.display_records()

    @classmethod
    def clear_all(cls):
        cls.head = None
        



def load_all_csv_data():
    # load courses first
    try:
        with open('Course.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader) 
            for row in reader:
                courses_dict[row[0]] = Course(row[0], row[1], row[2])
        print("Courses loaded.")
    except FileNotFoundError:
        print("File not found. No Courses.")

    try:
        with open('Professor.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                cid = row[4] if len(row) > 4 else ""
                professors_dict[row[0]] = Professor(row[0], row[1], row[2], row[3], cid)
        print("Professors loaded.")
    except FileNotFoundError:
        print("File not found. New Professor file.")

    try:
        with open('Student.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                new_student = Student(row[0], row[1], row[2], row[3], row[4], row[5])
                Student.add_new_student(new_student)
        print("Students loaded.")
    except FileNotFoundError:
        print("File not found. New Student file.")

    try:
        with open('Login.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                logins_dict[row[0]] = LoginUser(row[0], row[1], row[2])
        print("Logins loaded.")
    except FileNotFoundError:
        print("File not found. No logins.")


def save_all_csv_data():
    with open('Course.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Course_id', 'Credits', 'Course_name'])
        for c_id, course in courses_dict.items():
            writer.writerow([course.courseID, course.credits, course.course_name])

    with open('Professor.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Email', 'First_name', 'Last_name', 'Rank', 'CourseID'])
        for p_id, prof in professors_dict.items():
            writer.writerow([prof.email, prof.firstname, prof.lastname, prof.rank, prof.courseID])


    with open('Student.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Email', 'First_name', 'Last_name', 'Course_id', 'Grades', 'Marks'])
        c1 = Student.head
        while c1:
            writer.writerow([c1.email, c1.firstname, c1.lastname,
                             c1.courseID, c1.grades, c1.marks])
            c1 = c1.next

    with open('Login.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['User_id', 'Password', 'Role'])
        for u_id, user in logins_dict.items():
            writer.writerow([user.emailID, user.password, user.role])

    print("\nAll data saved to CSV files.")


# menu and operations
def checkmygrade():
    load_all_csv_data()
    while True:
        print("\n-- Welcome to the Grade Checker --")
        print("1. Login")
        print("2. Exit")
        user_input = input("Enter value 1 or 2: ")
        if user_input == "1":
            print("-- Welcome --")
            email = input("Email: ")
            password = input("Password: ")
            if email in logins_dict:
                current_user = logins_dict[email]
                if current_user.Login(password):
                    if current_user.role == "professor":
                        professor_role(current_user) 
                    elif current_user.role == "student":
                        student_role(current_user)
                    else:
                        print("Credentials not recognized.")
            else:
                print("Email not found in the system.")
                
        elif user_input == "2":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

def student_role(user):
    student_log = Student.search_student(user.emailID)
    if not student_log:
        print("Credentials not found.")
        return

    while True:
        print("\n-- Grade Management --")
        print("1. Check Grades")
        print("2. Check Marks")
        print("3. View Courses by Profesor")
        print("4. Change Password")
        print("5. Logout")
        choice = input("Enter Choice 1-5: ")

        if choice == "1":
            student_log.check_my_grades()
        elif choice == "2":
            student_log.check_my_marks()
        elif choice == "3":
            if professors_dict:
                prof_list = next(iter(professors_dict.values()))
                prof_list.show_course_details_by_professor()
            else:
                print("No professors found.")
        elif choice == "4":
            old_pw = input("Enter Old Password: ")
            new_pw = input("Enter New Password: ")
            user.change_password(old_pw,new_pw)
        elif choice == "5":
            user.Logout()
            save_all_csv_data()
            break
        else:
            print("Invalid option, choose 1-5")




def professor_role(user):
    while True:
        print("\n-- Professor Menu --")
        print("1. Professor Management")
        print("2. Course Management")
        print("3. Student Management")
        print("4. Grade Management")
        print("5. Show All Courses by Professor")
        print("6. Change My Password")
        print("7. Logout")

        choice = input("Enter Input 1-8: ")

        if choice == "1":
            professor_management()
        elif choice == "2":
            course_management()
        elif choice == "3":
            student_management()
        elif choice == "4":
            grade_management()
        elif choice == "5":
            if professors_dict:
                any_prof = next(iter(professors_dict.values()))
                any_prof.show_course_details_by_professor()
            else:
                print("No professors in the system.")
        elif choice == "6":
            old_pw = input("Enter current password: ")
            new_pw = input("Enter new password: ")
            user.change_password(old_pw, new_pw)
        elif choice == "7":
            user.Logout()
            save_all_csv_data()
            break
        else:
            print("Invalid option. Choose 1-7.")
            


def student_management():
    while True:
        print("\n-- Student Management --")
        print("1. Display Students")
        print("2. Search Student")
        print("3. Add Student")
        print("4. Delete Student")
        print("5. Update Student Record")
        print("6. Exit")
        
        choice = input("Enter Input 1-6: ")

        if choice == "1":
            print("Sort by: (1) Last Name  (2) Marks  (3) Email")
            key_pick = input("Enter 1, 2 or 3: ")
            if key_pick == "2":
                sort_key = "marks"
            elif key_pick == "3":
                sort_key = "email"
            else:
                sort_key = "lastname"
            order = input("Sort Ascending (A) or Descending (D)? ").upper()
            Student.sort_students(key=sort_key, descending=(order == "D"))

        elif choice == "2":
            email = input("Enter Student Email to search: ")
            found = Student.search_student(email)
            if found:
                found.display_records()
            else:
                print("Student not found.")

        elif choice == "3":
            email = input("Email: ")
            if not email or email.strip() == "":
                print("Email cannot be empty.")
                continue
            if Student.search_student(email):
                print("Email already exists.")
                continue
            fname = input("First Name: ")
            lname = input("Last Name: ")
            cid = input("Course ID: ")
            grade = input("Grade: ")
            marks = input("Marks: ")
            new_s = Student(email, fname, lname, cid, grade, marks)
            Student.add_new_student(new_s)
            print("Student added.")

        elif choice == "4":
            email = input("Enter Email of student to delete: ")
            deleted = Student.delete_student(email)
            if deleted:
                print(f"Deleted student: {deleted.firstname} {deleted.lastname}")
            else:
                print("Student not found.")

        elif choice == "5":
            email = input("Enter Email to update: ")
            found = Student.search_student(email)
            if found:
                print("Leave blank to keep current value.")
                fname = input(f"New First Name ({found.firstname}): ")
                lname = input(f"New Last Name ({found.lastname}): ")
                grade = input(f"New Grade ({found.grades}): ")
                marks = input(f"New Marks ({found.marks}): ")
                
                found.update_student_record(
                    firstname=fname if fname != "" else None,
                    lastname=lname if lname != "" else None,
                    grades=grade if grade != "" else None,
                    marks=marks if marks != "" else None
                )
            else:
                print("Student not found.")

        elif choice == "6":
            break
        else:
            print("Invalid option.")

def professor_management():
    while True:
        print("\n-- Professor Management --")
        print("1. Display Details")
        print("2. Add Professor")
        print("3. Delete Professor")
        print("4. Update Professr Record")
        print("5. Exit")
        
        choice = input("Enter Input 1-5: ")

        if choice == "1":
            professor = input("Email: ")
            if professor in professors_dict:
                professors_dict[professor].professors_details()
            else:
                print("Professor not found.")
        elif choice == "2":
            professor = input("Email: ")
            if not professor or professor.strip() == "":
                print("Email cannot be empty.")
                continue
            if professor in professors_dict:
                print("Email already exists.")
                continue
            fname = input("First Name: ")
            lname = input("Last Name: ")
            rank = input("Rank: ")
            cid = input("Course ID: ")
            if not cid or cid.strip() == "":
                print("Course ID cannot be empty.")
                continue
            professors_dict[professor] = Professor(professor, fname, lname, rank, cid)
            print("Professor added.")

        elif choice == "3":
            professor = input("Enter Professor Email to delete: ")
            if professor in professors_dict:
                professors_dict[professor].delete_professor()
            else:
                print("Professor not found.")

        elif choice == "4":
            professor = input("Enter Professor Email to update: ")
            if professor in professors_dict:
                found = professors_dict[professor]
                print("Leave blank to keep current value.")
                fname = input(f"New First Name ({found.firstname}): ")
                lname = input(f"New Last Name ({found.lastname}): ")
                rank = input(f"New Rank ({found.rank}): ")
                cid = input(f"New Course ID ({found.courseID}): ")
                found.modify_professor_details(
                    firstname=fname if fname != "" else None,
                    lastname=lname if lname != "" else None,
                    rank=rank if rank != "" else None,
                    courseID=cid if cid != "" else None
                )
            else:
                print("Professor not found.")
        elif choice == "5":
            break
        else:
            print("Invalid option. Input 1-5")




def course_management():
    while True:
        print("\n-- Course Management --")
        print("1. Display Courses")
        print("2. Add Course")
        print("3. Delete Course")
        print("4. Update Course")
        print("5. Marks Average by Course")
        print("6. Median Marks by Course")
        print("7. Exit")

        choice = input("Enter Input 1-7: ")

        if choice == "1":
            if len(courses_dict) == 0:
                print("No courses found.")
            else:
                print("\n--- All Courses ---")
                for courseid, course in courses_dict.items():
                    course.display_courses()

        elif choice == "2":
            cid = input("Course ID: ")
            if not cid or cid.strip() == "":
                print("Course ID cannot be empty.")
                continue
            if cid in courses_dict:
                print("Course already exists.")
                continue
            cname = input("Course Name: ")
            credits = input("Credits: ")
            courses_dict[cid] = Course(cid, credits, cname)
            print(f"Course '{cname}' added.")

        elif choice == "3":
            cid = input("Enter Course ID to delete: ")
            if cid in courses_dict:
                deleted_course = courses_dict[cid]
                del courses_dict[cid]
                print(f"Deleted: {deleted_course.course_name}")
            else:
                print("Course not found.")

        elif choice == "4":
            cid = input("Enter Course ID to update: ")
            if cid in courses_dict:
                found = courses_dict[cid]
                print("Leave blank to keep current value.")
                cname = input(f"New Course Name ({found.course_name}): ")
                credits = input(f"New Credits ({found.credits}): ")
                if cname != "":
                    found.course_name = cname
                if credits != "":
                    found.credits = credits
                print(f"Course {found.courseID} updated.")
            else:
                print("Course not found.")

        elif choice == "5":
            cid = input("Enter Course ID: ")
            if cid in courses_dict:
                courses_dict[cid].calc_average_marks()
            else:
                print("Course not found.")

        elif choice == "6":
            cid = input("Enter Course ID: ")
            if cid in courses_dict:
                courses_dict[cid].calc_median_marks()
            else:
                print("Course not found.")

        elif choice == "7":
            break
        else:
            print("Invalid option. Please try again.")
            

def grade_management():
    while True:
        print("\n-- Grade Management --")
        print("1. Display Grades")
        print("2. Add Grades")
        print("3. Update Grades")
        print("4. Remove Grades")
        print("5. Exit")

        choice = input("Enter Input 1-5: ")

        if choice == "1":
            email = input("Enter Student Email: ")
            found = Student.search_student(email)
            if found:
                found.check_my_grades()
                found.check_my_marks()
            else:
                print("Student not found.")

        elif choice == "2":
            email = input("Enter Student Email: ")
            found = Student.search_student(email)
            if found:
                grade = input("Enter Grade (e.g. A, B, C): ")
                marks = input("Enter Marks: ")
                found.update_student_record(grades=grade, marks=marks)
                print(f"Grade assigned to {found.firstname} {found.lastname}.")
            else:
                print("Student not found.")

        elif choice == "3":
            email = input("Enter Student Email: ")
            found = Student.search_student(email)
            if found:
                print(f"Current Grade: {found.grades} | Current Marks: {found.marks}")
                grade = input("New Grade (leave blank to keep): ")
                marks = input("New Marks (leave blank to keep): ")
                found.update_student_record(
                    grades=grade if grade != "" else None,
                    marks=marks if marks != "" else None
                )
            else:
                print("Student not found.")

        elif choice == "4":
            email = input("Enter Student Email: ")
            found = Student.search_student(email)
            if found:
                found.grades = "N/A"
                found.marks = "0"
                print(f"Grade removed for {found.firstname} {found.lastname}.")
            else:
                print("Student not found.")

        elif choice == "5":
            break
        else:
            print("Invalid option. Please try again.")
            
            
# Unit Testing 


class TestStudent(unittest.TestCase):

    def setUp(self):
        Student.clear_all()
        courses_dict.clear()
        professors_dict.clear()
        logins_dict.clear()
        load_all_csv_data()

    def test_add(self):
        s = Student("newstudent@sjsu.edu", "Test", "Student", "DATA200", "A", "90")
        result = Student.add_new_student(s)
        self.assertTrue(result)
        found = Student.search_student("newstudent@sjsu.edu")
        self.assertIsNotNone(found)
        self.assertEqual(found.firstname, "Test")

    def test_delete(self):
        deleted = Student.delete_student("sofia.patel@sjsu.edu")
        self.assertIsNotNone(deleted)
        self.assertIsNone(Student.search_student("sofia.patel@sjsu.edu"))

    def test_modify(self):
        found = Student.search_student("sofia.patel@sjsu.edu")
        self.assertIsNotNone(found)
        found.update_student_record(grades="B", marks="80")
        self.assertEqual(found.grades, "B")
        self.assertEqual(found.marks, "80")

    def test_search(self):

        targets = [
            "paul.lopez@sjsu.edu",
            "grace.harris@sjsu.edu",
            "andre.reed@sjsu.edu",
            "jayden.patel@sjsu.edu"
        ]

        start = time.perf_counter()
        for email in targets:
            Student.search_student(email)
        total = time.perf_counter() - start

        print(f"\nSearch time across {len(targets)} rows: {total:.2f}s")
        for email in targets:
            self.assertIsNotNone(Student.search_student(email))

    def test_sort_students(self):
        start = time.perf_counter()
        Student.sort_students(key='lastname', descending=False,silent=True)
        elapsed = time.perf_counter() - start
        print(f"\nlastname ascending:  {elapsed:.3f}s")

        start = time.perf_counter()
        Student.sort_students(key='lastname', descending=True,silent=True)
        elapsed = time.perf_counter() - start
        print(f"lastname descending: {elapsed:.3f}s")


        start = time.perf_counter()
        Student.sort_students(key='marks', descending=False,silent=True)
        elapsed = time.perf_counter() - start
        print(f"marks ascending:     {elapsed:.3f}s")

        start = time.perf_counter()
        Student.sort_students(key='marks', descending=True,silent=True)
        elapsed = time.perf_counter() - start
        print(f"marks descending:    {elapsed:.3f}s")

        start = time.perf_counter()
        Student.sort_students(key='email', descending=False,silent=True)
        elapsed = time.perf_counter() - start
        print(f"email ascending:     {elapsed:.3f}s")

        start = time.perf_counter()
        Student.sort_students(key='email', descending=True,silent=True)
        elapsed = time.perf_counter() - start
        print(f"email descending:    {elapsed:.3f}s")

class TestCourse(unittest.TestCase):

    def setUp(self):
        Student.clear_all()
        courses_dict.clear()
        professors_dict.clear()
        logins_dict.clear()
        load_all_csv_data()

    def test_add(self):
        courses_dict["CSTEST"] = Course("CSTEST", "4", "Test Course")
        self.assertIn("CSTEST", courses_dict)

    def test_delete(self):
        del courses_dict["CS101"]
        self.assertNotIn("CS101", courses_dict)

    def test_modify(self):
        courses_dict["CS101"].course_name = "Updated CS"
        courses_dict["CS101"].credits = "4"
        self.assertEqual(courses_dict["CS101"].course_name, "Updated CS")
        self.assertEqual(courses_dict["CS101"].credits, "4")

class TestProfessor(unittest.TestCase):

    def setUp(self):
        Student.clear_all()
        courses_dict.clear()
        professors_dict.clear()
        logins_dict.clear()
        load_all_csv_data()

    def test_add(self):
        p = Professor("testprof@sjsu.edu", "TEST", "PROF", "Janitor", "CS101")
        professors_dict["testprof@sjsu.edu"] = p
        self.assertIn("testprof@sjsu.edu", professors_dict)

    def test_delete(self):
        email = "sierra.kennedy@sjsu.edu"
        professors_dict[email].delete_professor()
        self.assertNotIn(email, professors_dict)

    def test_modify(self):
        email = "sierra.kennedy@sjsu.edu"
        professors_dict[email].modify_professor_details(rank="Test Professor")
        self.assertEqual(professors_dict[email].rank, "Test Professor")


if __name__ == "__main__":
    unittest.main(verbosity=2)


# if __name__ == "__main__":
#     checkmygrade()