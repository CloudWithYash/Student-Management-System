import json
import os

DATA_FILE = "students.json"

class StudentManagementSystem:
    def __init__(self):
        self.students = []
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    self.students = json.load(f)
            except Exception as e:
                print(f"Error loading data from file: {e}")
                self.students = []
        else:
            self.students = []

    def save_data(self):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(self.students, f, indent=4)
        except Exception as e:
            print(f"Error saving data to file: {e}")

    def generate_student_id(self):
        if not self.students:
            return 1
        else:
            max_id = max(student["id"] for student in self.students)
            return max_id + 1

    def add_student(self):
        print("\nAdd New Student")
        name = input("Enter student name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        try:
            age = int(input("Enter age: "))
        except ValueError:
            print("Invalid age.")
            return
        email = input("Enter email: ").strip()
        course = input("Enter course: ").strip()
        if not course:
            print("Course cannot be empty.")
            return

        student_id = self.generate_student_id()
        new_student = {
            "id": student_id,
            "name": name,
            "age": age,
            "email": email,
            "course": course
        }
        self.students.append(new_student)
        self.save_data()
        print(f"Student '{name}' added with ID: {student_id}")

    def list_students(self):
        if not self.students:
            print("\nNo students found.\n")
            return
        print("\nList of Students:\n")
        print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Email':<30} {'Course':<20}")
        print("-" * 80)
        for s in self.students:
            print(f"{s['id']:<5} {s['name']:<20} {s['age']:<5} {s['email']:<30} {s['course']:<20}")
        print("")

    def search_students(self):
        keyword = input("\nEnter name or ID to search: ").strip()
        if not keyword:
            print("Input cannot be empty.")
            return
        results = []
        if keyword.isdigit():
            # Search by ID
            sid = int(keyword)
            results = [s for s in self.students if s["id"] == sid]
        else:
            # Search by name case-insensitive substring match
            results = [s for s in self.students if keyword.lower() in s["name"].lower()]

        if not results:
            print("No matching students found.")
            return
        print(f"\nFound {len(results)} student(s):\n")
        print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Email':<30} {'Course':<20}")
        print("-" * 80)
        for s in results:
            print(f"{s['id']:<5} {s['name']:<20} {s['age']:<5} {s['email']:<30} {s['course']:<20}")
        print("")

    def update_student(self):
        try:
            sid = int(input("\nEnter student ID to update: "))
        except ValueError:
            print("Invalid ID.")
            return
        student = next((s for s in self.students if s["id"] == sid), None)
        if not student:
            print("Student not found.")
            return

        print(f"Updating student '{student['name']}' (ID: {sid}). Press enter to keep current value.")
        new_name = input(f"New name [{student['name']}]: ").strip()
        if new_name:
            student['name'] = new_name
        new_age = input(f"New age [{student['age']}]: ").strip()
        if new_age:
            try:
                student['age'] = int(new_age)
            except ValueError:
                print("Invalid age entered; keeping previous age.")
        new_email = input(f"New email [{student['email']}]: ").strip()
        if new_email:
            student['email'] = new_email
        new_course = input(f"New course [{student['course']}]: ").strip()
        if new_course:
            student['course'] = new_course

        self.save_data()
        print("Student updated successfully.")

    def delete_student(self):
        try:
            sid = int(input("\nEnter student ID to delete: "))
        except ValueError:
            print("Invalid ID.")
            return
        index = next((i for i,s in enumerate(self.students) if s["id"] == sid), None)
        if index is None:
            print("Student not found.")
            return
        confirm = input(f"Are you sure you want to delete student '{self.students[index]['name']}'? (y/n): ").lower()
        if confirm == "y":
            del self.students[index]
            self.save_data()
            print("Student deleted.")
        else:
            print("Deletion cancelled.")

    def menu(self):
        while True:
            print("\n--- Student Management System ---")
            print("1. Add Student")
            print("2. List Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Exit")
            choice = input("Choose an option (1-6): ").strip()
            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.list_students()
            elif choice == "3":
                self.search_students()
            elif choice == "4":
                self.update_student()
            elif choice == "5":
                self.delete_student()
            elif choice == "6":
                print("Exiting Student Management System. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    sms = StudentManagementSystem()
    sms.menu()
