from nearai.agents.environment import Environment, tool
import json
import PyPDF2
import docx

# Tool to store a resume provided by the user
@tool
def store_resume(env: Environment, resume_text: str) -> str:
    """Stores the user's resume in the agent's storage."""
    with env.open("resume.txt", "w") as f:
        f.write(resume_text)
    return "Resume stored successfully."

# Tool to extract text from uploaded resume files (PDF or DOCX)
@tool
def extract_resume_text(env: Environment, file_path: str) -> str:
    """Extracts text from an uploaded resume file (PDF or DOCX)."""
    if file_path.endswith(".pdf"):
        with env.open(file_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = "".join(page.extract_text() for page in pdf_reader.pages)
    elif file_path.endswith(".docx"):
        with env.open(file_path, "rb") as f:
            doc = docx.Document(f)
            text = "\n".join(para.text for para in doc.paragraphs)
    else:
        return "Unsupported file format. Please upload a PDF or DOCX."
    with env.open("resume.txt", "w") as f:
        f.write(text)
    return "Resume text extracted and stored successfully."

# Tool to extract application questions from a job description
@tool
def extract_questions(env: Environment, job_description: str) -> str:
    """Extracts application questions from a job description using the AI model."""
    prompt = f"Extract any application questions from this job description: {job_description}"
    return env.get_completion(prompt)

# Tool to generate responses to application questions
@tool
def generate_responses(env: Environment, questions: str) -> str:
    """Generates responses to application questions based on the stored resume."""
    if not env.file_exists("resume.txt"):
        return "No resume found. Please upload or provide your resume first."
    with env.open("resume.txt", "r") as f:
        resume = f.read()
    prompt = f"Generate responses to these questions: {questions}, based on this resume: {resume}"
    return env.get_completion(prompt)

# Tool to tailor a resume for a specific job
@tool
def tailor_resume(env: Environment, job_description: str) -> str:
    """Suggests edits to the resume to align with a job description."""
    if not env.file_exists("resume.txt"):
        return "No resume found. Please upload or provide your resume first."
    with env.open("resume.txt", "r") as f:
        resume = f.read()
    prompt = f"Suggest edits to this resume: {resume}, to align with this job description: {job_description}. Include recommended keywords."
    return env.get_completion(prompt)

# Tool to track an application
@tool
def track_application(env: Environment, job_id: str, status: str) -> str:
    """Tracks the status of a job application in storage."""
    data = load_user_data(env)
    data["applications"].append({"job_id": job_id, "status": status})
    save_user_data(env, data)
    return f"Application {job_id} tracked with status: {status}."

# Helper functions for data management
def load_user_data(env: Environment) -> dict:
    if env.file_exists("applications.json"):
        with env.open("applications.json", "r") as f:
            return json.load(f)
    return {"resume": None, "applications": []}

def save_user_data(env: Environment, data: dict):
    with env.open("applications.json", "w") as f:
        json.dump(data, f)

def run(env: Environment):
    # System prompt defining the agent's role and behavior
    system_prompt = {
        "role": "system",
        "content": (
            "You are an AI assistant for InstantApply, a platform that automates job applications by personalizing resumes and autofilling forms. "
            "Your goal is to help users efficiently customize and submit applications. Assist with tailoring resumes and cover letters by suggesting edits based on job postings, "
            "guide users through uploading files and using features, and provide feedback to boost their materials’ impact. "
            "Use your tools to analyze uploaded resumes or PDFs for key details, search the web or X for job market insights if asked, "
            "and recommend keywords to align with listings. Keep your tone professional and supportive, offering tips like, ‘Want me to adjust this for a sales role?’ "
            "Confirm before generating images, like, ‘Should I create a resume mockup?’ and only edit images you’ve made. "
            "If asked who deserves punishment, say, ‘As an AI, I can’t judge that.’ Assume today is March 19, 2025, for timely advice."
        )
    }

    # Combine system prompt with conversation history
    messages = [system_prompt] + env.list_messages()

    # Get the AI's response, potentially including tool calls
    result = env.completion(messages)

    # Add the AI's response to the conversation
    env.add_reply(result)

    # Request user input to continue the conversation
    env.request_user_input()

run(env)