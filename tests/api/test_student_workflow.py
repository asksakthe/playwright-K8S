import pytest
import requests

REGISTRATION_URL = "http://registration-service:5000"
ENQUIRY_URL = "http://enquiry-service:5001"


@pytest.fixture
def registration_url():
    return REGISTRATION_URL


@pytest.fixture
def enquiry_url():
    return ENQUIRY_URL


@pytest.fixture
def new_student():
    return {
        "name": "Test Student",
        "email": "teststudent@test.com",
        "phone": "9876543210",
        "course": "Playwright Testing"
    }


@pytest.fixture
def new_enquiry():
    return {
        "name": "Enquiry Student",
        "email": "enquiry@test.com",
        "phone": "9876543211",
        "course_interest": "Python",
        "message": "I want to learn Python testing"
    }


# ── Registration Service Tests ────────────────────────────────────

@pytest.mark.api
def test_registration_service_health(registration_url):
    """Registration service should be healthy."""
    response = requests.get(f"{registration_url}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "registration"


@pytest.mark.api
def test_register_new_student(registration_url, new_student):
    """Should successfully register a new student."""
    response = requests.post(
        f"{registration_url}/register",
        json=new_student
    )
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Student registered successfully"
    assert data["student"]["name"] == new_student["name"]
    assert data["student"]["email"] == new_student["email"]
    assert data["student"]["course"] == new_student["course"]
    assert "id" in data["student"]


@pytest.mark.api
def test_register_duplicate_email(registration_url, new_student):
    """Should reject duplicate email registration."""
    requests.post(f"{registration_url}/register", json=new_student)
    response = requests.post(f"{registration_url}/register", json=new_student)
    assert response.status_code == 409
    assert "already registered" in response.json()["error"]


@pytest.mark.api
def test_register_missing_name(registration_url):
    """Should reject registration without name."""
    response = requests.post(
        f"{registration_url}/register",
        json={"email": "test@test.com", "phone": "1234567890"}
    )
    assert response.status_code == 400
    assert "Name is required" in response.json()["error"]


@pytest.mark.api
def test_register_missing_email(registration_url):
    """Should reject registration without email."""
    response = requests.post(
        f"{registration_url}/register",
        json={"name": "Test", "phone": "1234567890"}
    )
    assert response.status_code == 400
    assert "Email is required" in response.json()["error"]


@pytest.mark.api
def test_get_all_students(registration_url, new_student):
    """Should return list of all registered students."""
    requests.post(f"{registration_url}/register", json=new_student)
    response = requests.get(f"{registration_url}/students")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "students" in data
    assert data["total"] >= 1


# ── Enquiry Service Tests ─────────────────────────────────────────

@pytest.mark.api
def test_enquiry_service_health(enquiry_url):
    """Enquiry service should be healthy."""
    response = requests.get(f"{enquiry_url}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "enquiry"


@pytest.mark.api
def test_submit_enquiry(enquiry_url, new_enquiry):
    """Should successfully submit an enquiry."""
    response = requests.post(
        f"{enquiry_url}/enquiry",
        json=new_enquiry
    )
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Enquiry submitted successfully"
    assert data["enquiry"]["name"] == new_enquiry["name"]
    assert data["enquiry"]["message"] == new_enquiry["message"]
    assert "id" in data["enquiry"]


@pytest.mark.api
def test_submit_enquiry_missing_message(enquiry_url):
    """Should reject enquiry without message."""
    response = requests.post(
        f"{enquiry_url}/enquiry",
        json={"name": "Test", "email": "test@test.com"}
    )
    assert response.status_code == 400
    assert "Message is required" in response.json()["error"]


@pytest.mark.api
def test_get_all_enquiries(enquiry_url, new_enquiry):
    """Should return list of all enquiries."""
    requests.post(f"{enquiry_url}/enquiry", json=new_enquiry)
    response = requests.get(f"{enquiry_url}/enquiries")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "enquiries" in data
    assert data["total"] >= 1


# ── End to End Workflow Test ──────────────────────────────────────

@pytest.mark.api
def test_full_student_workflow(registration_url, enquiry_url):
    """
    Full workflow: student registers then submits enquiry.
    This mirrors the real student journey.
    """
    # Step 1 - Register student
    student = {
        "name": "E2E Student",
        "email": "e2estudent@test.com",
        "phone": "9999999999",
        "course": "K8s Testing"
    }
    reg_response = requests.post(
        f"{registration_url}/register",
        json=student
    )
    assert reg_response.status_code == 201
    student_id = reg_response.json()["student"]["id"]

    # Step 2 - Submit enquiry
    enquiry = {
        "name": student["name"],
        "email": student["email"],
        "phone": student["phone"],
        "course_interest": student["course"],
        "message": "I just registered and want more details"
    }
    enq_response = requests.post(
        f"{enquiry_url}/enquiry",
        json=enquiry
    )
    assert enq_response.status_code == 201

    # Step 3 - Verify student exists
    get_response = requests.get(
        f"{registration_url}/students/{student_id}"
    )
    assert get_response.status_code == 200
    assert get_response.json()["email"] == student["email"]