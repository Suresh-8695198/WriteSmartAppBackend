# firebase_auth.py

from firebase_admin import firestore

def verify_student(register_number, dob):
    db = firestore.client()  # Initialize Firestore
    try:
        # Query the Firestore collection for both register_number and dob
        students_ref = db.collection('students')
        query = students_ref.where('register_number', '==', register_number).where('dob', '==', dob)
        results = query.stream()

        # Debug: Check and print results
        found = False
        for student in results:
            student_data = student.to_dict()
            if student_data.get("register_number") == register_number and student_data.get("dob") == dob:
                found = True
                break

        if found:
            return True
        else:
            print("No matching document found with both register_number and dob.")
            return False
    except Exception as e:
        print(f"Error fetching data from Firestore: {e}")
        return False
