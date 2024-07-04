import json
from flask import Flask, request, jsonify
import docx
import PyPDF2
import ollama
import requests
from io import BytesIO

# Initialize the Flask application
app = Flask(__name__)


# Function to extract text from a docx file
def extract_text_from_docx(file):
    # Load the .docx file
    doc = docx.Document(file)
    # Extract and join paragraphs
    return "\n".join([para.text for para in doc.paragraphs])


# Function to extract text from a PDF file
def extract_text_from_pdf(file):
    # Load the PDF file
    reader = PyPDF2.PdfReader(file)
    # Initialize text variable
    text = ""
    # Iterate through each page
    for page_num in range(len(reader.pages)):
        # Extract text from each page and append
        text += reader.pages[page_num].extract_text()
    # Return the extracted text
    return text


# Initialize Ollama client
api_client = ollama.Client("http://localhost:11434")  # Create Ollama client instance with server address
# Model Name of ollama
model_name = "llama3"


# Function to generate similarity score and summary
def generate_similarity_score_and_summary(job_description, resume_text):
    # Create a prompt with job description and resume text
    prompt = (
        f"Job Description: {job_description}\n\n"
        f"Resume: {resume_text}\n\n"
        f"Please evaluate the similarity between the job description and the resume on a scale from 0 to 100. "
        f"Provide a single numerical similarity score.\n\n"
        f"Additionally, explain why the resume is a good fit or not.Your response must include both the similarity "
        f"percentage and the summary.\n\n"
        f"Format your response in JSON as follows:\n\n"
        f"{{\n"
        f"  \"similarity_percentage\": numerical_score,\n"
        f"  \"summary\": \"brief summary of why the resume is a good fit or not\"\n"
        f"}}"
    )
    # Generate response from API
    response = api_client.generate(model=model_name, prompt=prompt, format='json')
    print(response['response'])

    # Parse the response text as JSON
    try:
        # Load response as JSON
        response_data = json.loads(response['response'])
    except (KeyError, json.JSONDecodeError):  # Handle possible errors
        # Raise an error for unexpected format
        raise ValueError("Unexpected response format from Ollama API")

    # Extract similarity percentage from the response_data
    similarity_percentage = response_data.get('similarity_percentage', 0)
    # Extract summary from the response_data
    summary = response_data.get('summary', "Summary not available")

    # Return similarity percentage and summary
    return similarity_percentage, summary


# Define route to calculate similarity for resumes
@app.route('/selectresumes', methods=['GET', 'POST'])
def calculate_similarity_for_resumes():
    # Get JSON data from the request
    data = request.json
    # Extract job description text
    job_description_text = data.get('job_description')
    # Extract resume URLs
    resume_urls = data.get('urls')

    # Check if job description and resume URLs are provided
    if not job_description_text or not resume_urls:
        # Return error response
        return jsonify({"error": "Job description text and resume URLs are required"}), 400

    # Extract and process each resume
    results = []  # Initialize results list
    for resume_url in resume_urls:  # Iterate over each resume URL
        # Make a GET request to the resume URL
        response = requests.get(resume_url)
        # Load the response content into a BytesIO object
        file = BytesIO(response.content)
        # Check if file is a .docx
        if resume_url.endswith('.docx'):
            # Extract text from .docx
            resume_text = extract_text_from_docx(file)
        # Check if file is a PDF
        elif resume_url.endswith('.pdf'):
            # Extract text from PDF
            resume_text = extract_text_from_pdf(file)
        # If file format is unsupported
        else:
            # Return error response
            return jsonify({"error": "Unsupported file format for resume"}), 400

        # Try to generate similarity score and summary
        try:
            # Generate score and summary
            score, summary = generate_similarity_score_and_summary(job_description_text, resume_text)
            # Store the analysis result at the results dictionary index at the given index
            results.append({
                "resume_url": resume_url,
                "similarity_percentage": score,
                "summary": summary
            })
        # Prints and returns the exception if the error during the processing
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Returns the matched resumes as a JSON Response
    return jsonify({"matched_resumes": results})


# Main function where flask is run and debug is set to True
if __name__ == '__main__':
    app.run(debug=True)
