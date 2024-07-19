#Student management system


#blank dictonary
students = {}

#student function for add data
def add_student():
    student_id = int(input("Enter student id: "))
    if student_id in students:
        print("Student ID already exists!")
        print("*************************************************************")
        return False
    else:
        student_fname = input("Enter student first name: ")
        student_lname = input("Enter student last name: ")
        student_contact = input("Enter contact number: ")
        subject = input("Enter a subject: ")
        marks = int(input("Enter marks: "))
        fees = int(input("Enter fees: "))
        students[student_id] = {
            "first_name": student_fname,
            "last_name": student_lname,
            "contact": student_contact,
            "subjects": {
                subject: {
                    "marks": marks,
                    "fees": fees
                }
            }
        }
        print("Student added successfully!")
        print("*************************************************************")
        return True

#student function for remove data
def remove(student_id):
    if student_id in students:
        del students[student_id]
        print("Student removed successfully!")
        print("*************************************************************")
    else:
        print("Student ID not found!")
        print("*************************************************************")

#student function for specific students data
def specific_student(student_id):
    if student_id in students:
        student_info = students[student_id]
        student_data = {
            "student_id": student_id,
            "first_name": student_info["first_name"],
            "last_name": student_info["last_name"],
            "contact": student_info["contact"],
            "subjects": student_info["subjects"]
        }
        print("Student Details:")
        print(student_data)
        print("*************************************************************")
    else:
        print("Student ID not found!")
        print("*************************************************************")

#student function for view all students data    
def view_all_students():
    if not students:
        print("No students registered yet!")
        print("*************************************************************")
    else:
        for student_id, student_info in students.items():
            student_data = {
                "student_id": student_id,
                "first_name": student_info["first_name"],
                "last_name": student_info["last_name"],
                "contact": student_info["contact"],
                "subjects": student_info["subjects"]
            }
            print(student_data)


#counseller function
def counseller():
    while True:
        print("1. Add student")
        print("2. Remove student")
        print("3. View all students")
        print("4. View specific student")
        print("5. Exit")
        print("*************************************************************")
        choice = int(input("Enter your choice: "))
        print("*************************************************************")
        if choice == 1:
            add_student()
        elif choice == 2:
            student_id = int(input("Enter student ID to remove: "))
            remove(student_id)
        elif choice == 3:
            view_all_students()
        elif choice == 4:
            student_id = int(input("Enter student ID to view details: "))
            specific_student(student_id)
        elif choice == 5:
            break
        else:
            print("Invalid choice!")

#add marks faculty for students
def student_faculty(student_id):
    if student_id in students:
        subject = input("Enter subject: ")
        marks = int(input("Enter marks: "))
        students[student_id]["subjects"][subject] = {
            "marks": marks
        }
        print("Marks added successfully!")
        print("*************************************************************")
    else:
        print("Student ID not found!")
        print("*************************************************************")

#faculty student     
def faculty():
    while True:
        print("1.add mark to student")
        print("2.view all students")
        print("3.exit")
        print("*************************************************************")
        choice=int(input("choce what You want : "))
         print("*************************************************************")

        if choice == 1:
            student_id = int(input("Enter student ID to add marks : "))
            student_faculty(student_id)
        elif choice == 2:
            view_all_students()
        else:
            print("invalid choice!!")
            print("*************************************************************")
            break



while True:
    print("Press 1 for counsellor")
    print("Press 2 for faculty")
    print("Press 3 for student")
    print("*************************************************************")
    role = int(input("Enter your role: "))
    print("*************************************************************")
    if role == 1:
        counseller()
    elif role == 2:
        faculty()
    elif role == 3:
        student_id = int(input("Enter student ID to view details: "))
        specific_student(student_id)
    else:
        print("Invalid role!")
        print("*************************************************************")
        break    
