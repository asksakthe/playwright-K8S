from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
enquiries = []

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "enquiry"})

@app.route('/enquiry', methods=['POST'])
def submit_enquiry():
    data = request.get_json()

    # Validate required fields
    if not data.get('name'):
        return jsonify({"error": "Name is required"}), 400
    if not data.get('email'):
        return jsonify({"error": "Email is required"}), 400
    if not data.get('message'):
        return jsonify({"error": "Message is required"}), 400

    # Save enquiry
    enquiry = {
        "id": len(enquiries) + 1,
        "name": data['name'],
        "email": data['email'],
        "phone": data.get('phone', 'Not provided'),
        "course_interest": data.get('course_interest', 'General'),
        "message": data['message']
    }
    enquiries.append(enquiry)

    return jsonify({
        "message": "Enquiry submitted successfully",
        "enquiry": enquiry
    }), 201

@app.route('/enquiries', methods=['GET'])
def get_enquiries():
    return jsonify({
        "total": len(enquiries),
        "enquiries": enquiries
    })

@app.route('/enquiries/<int:enquiry_id>', methods=['GET'])
def get_enquiry(enquiry_id):
    for enquiry in enquiries:
        if enquiry['id'] == enquiry_id:
            return jsonify(enquiry)
    return jsonify({"error": "Enquiry not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)