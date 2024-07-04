import requests
import json

# Localhost URL
base_url = 'http://127.0.0.1:5000/selectresumes'

# Sample data
data = {
    "urls": [
        "https://link-health-staff.s3.us-east-2.amazonaws.com/1719316386044louRHJohn_Physiotherapist_Resume.docx",
        "https://link-health-staff.s3.us-east-2.amazonaws.com/17193163860479WvoBJane_Doe_PhysicalTherapist_Resume.docx",
        "https://link-health-staff.s3.us-east-2.amazonaws.com/17193163860518u2goJAI_MALHOTRA_PHYSIOTHERAPIST_Resume.docx",
        "https://link-health-staff.s3.us-east-2.amazonaws.com/17193163860541tqD5Himanshi_Tiwari_PHYSIOTHERAPIST_Resume.docx",
        "https://link-health-staff.s3.us-east-2.amazonaws.com/1719379115130dqIoEANKIT_SHARMA_CV.pdf",
    ],
    "job_description": """The Physiotherapist will be responsible for assessing, diagnosing, and treating a variety of physical conditions to improve patient mobility, relieve pain, and prevent or limit physical disabilities. The role involves creating personalized treatment plans and collaborating with other healthcare professionals to ensure comprehensive patient care.
    Key Responsibilities: 1.Experience needed around 7 years 2. Patient Assessment: Conduct thorough physical assessments of patients, including medical history review and physical examinations. 3.Diagnosis: Analyze assessment results to diagnose the patient's condition and determine appropriate treatment plans. Treatment Planning: Develop individualized treatment plans that may include exercise, manual therapy, education, and other modalities."""
}

# Send POST request
response = requests.post(base_url, json=data)

# Check the response
if response.status_code == 200:
    print("Success!")
    print(json.dumps(response.json(), indent=2))
else:
    print("Failed!")
    print(response.text)
