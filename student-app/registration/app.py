from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage (no database needed for demo)
students = []

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "registration"})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate required fields
    if not data.get('name'):
        return jsonify({"error": "Name is required"}), 400
    if not data.get('email'):
        return jsonify({"error": "Email is required"}), 400
    if not data.get('phone'):
        return jsonify({"error": "Phone is required"}), 400

    # Check duplicate email
    for student in students:
        if student['email'] == data['email']:
            return jsonify({"error": "Email already registered"}), 409

    # Save student
    student = {
        "id": len(students) + 1,
        "name": data['name'],
        "email": data['email'],
        "phone": data['phone'],
        "course": data.get('course', 'Not specified')
    }
    students.append(student)

    return jsonify({
        "message": "Student registered successfully",
        "student": student
    }), 201

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({
        "total": len(students),
        "students": students
    })

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    for student in students:
        if student['id'] == student_id:
            return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)