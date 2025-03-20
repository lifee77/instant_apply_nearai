from nearai.agents.environment import Environment
import json

# Function to store a resume provided by the user
def store_resume(env: Environment, resume_text: str) -> str:
    """Stores the user's resume in the agent's storage."""
    try:
        with env.open("resume.txt", "w") as f:
            f.write(resume_text)
        return "Resume stored successfully."
    except Exception as e:
        return f"Error storing resume: {str(e)}"

# Function to check and read the stored resume
def read_resume(env: Environment) -> str:
    """Checks if a resume exists and reads its contents."""
    try:
        if not env.file_exists("resume.txt"):
            return "No resume found. Please provide your resume first."
        with env.open("resume.txt", "r") as f:
            resume = f.read()
        return f"Here is the stored resume: {resume}"
    except Exception as e:
        return f"Error reading resume: {str(e)}"

# Function to extract application questions from a job description
def extract_questions(env: Environment, job_description: str) -> str:
    """Extracts application questions from a job description using the AI model."""
    try:
        prompt = f"Extract any application questions from this job description: {job_description}"
        return env.get_completion(prompt)
    except Exception as e:
        return f"Error extracting questions: {str(e)}"

# Function to generate responses to application questions
def generate_responses(env: Environment, questions: str) -> str:
    """Generates responses to application questions based on the stored resume."""
    try:
        if not env.file_exists("resume.txt"):
            return "No resume found. Please provide your resume first."
        with env.open("resume.txt", "r") as f:
            resume = f.read()
        prompt = f"Generate responses to these questions: {questions}, based on this resume: {resume}"
        return env.get_completion(prompt)
    except Exception as e:
        return f"Error generating responses: {str(e)}"

# Function to tailor a resume for a specific job
def tailor_resume(env: Environment, job_description: str) -> str:
    """Suggests edits to the resume to align with a job description."""
    try:
        if not env.file_exists("resume.txt"):
            return "No resume found. Please provide your resume first."
        with env.open("resume.txt", "r") as f:
            resume = f.read()
        prompt = f"Suggest edits to this resume: {resume}, to align with this job description: {job_description}. Include recommended keywords."
        return env.get_completion(prompt)
    except Exception as e:
        return f"Error tailoring resume: {str(e)}"

# Function to track an application
def track_application(env: Environment, job_id: str, status: str) -> str:
    """Tracks the status of a job application in storage."""
    try:
        data = load_user_data(env)
        data["applications"].append({"job_id": job_id, "status": status})
        save_user_data(env, data)
        return f"Application {job_id} tracked with status: {status}"
    except Exception as e:
        return f"Error tracking application: {str(e)}"

# Helper functions for data management
def load_user_data(env: Environment) -> dict:
    try:
        if env.file_exists("applications.json"):
            with env.open("applications.json", "r") as f:
                return json.load(f)
        return {"resume": None, "applications": []}
    except Exception as e:
        return {"resume": None, "applications": [], "error": str(e)}

def save_user_data(env: Environment, data: dict):
    try:
        with env.open("applications.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        raise Exception(f"Error saving data: {str(e)}")

def run(env: Environment):
    # System prompt defining the agent's role and behavior
    system_prompt = {
        "role": "system",
        "content": (
            "You are an AI assistant for InstantApply, a platform that automates job applications by personalizing resumes and autofilling forms. "
            "Your goal is to help users efficiently customize and submit applications. Assist with tailoring resumes and cover letters by suggesting edits based on job postings, "
            "guide users through providing their resume or job details, and provide feedback to boost their materials' impact. "
            "You have the following capabilities: "
            "- Store a resume if the user provides one (e.g., a block of text with education, skills, or experience). "
            "- Read and display the stored resume if asked (e.g., 'Can you read the resume?'). "
            "- Extract application questions from a job description if provided. "
            "- Generate responses to application questions based on the stored resume. "
            "- Tailor the resume for a specific job description, suggesting edits and keywords. "
            "- Track job applications with a job ID and status. "
            "Keep your tone professional and supportive, offering tips like, 'Want me to adjust this for a sales role?' "
            "Assume today is March 19, 2025, for timely advice."
        )
    }

    # Combine system prompt with conversation history
    messages = [system_prompt] + env.list_messages()

    # Check the latest user message to detect resume submission or specific requests
    latest_message = messages[-1]["content"].lower() if messages and len(messages) > 1 else ""
    
    # Heuristic to detect resume submission
    if "resume" in latest_message and len(latest_message.split()) > 20:
        try:
            result = store_resume(env, messages[-1]["content"])
            env.add_reply(result)
        except Exception as e:
            env.add_reply(f"Error processing your resume: {str(e)}. Please try again.")
    
    # Handle specific user requests
    elif "read the resume" in latest_message:
        try:
            result = read_resume(env)
            env.add_reply(result)
        except Exception as e:
            env.add_reply(f"Error reading resume: {str(e)}. Please try again.")
    
    elif "extract questions" in latest_message or "job description" in latest_message:
        try:
            result = extract_questions(env, messages[-1]["content"])
            env.add_reply(result)
        except Exception as e:
            env.add_reply(f"Error extracting questions: {str(e)}. Please try again.")
    
    elif "generate responses" in latest_message or "answer these questions" in latest_message:
        try:
            result = generate_responses(env, messages[-1]["content"])
            env.add_reply(result)
        except Exception as e:
            env.add_reply(f"Error generating responses: {str(e)}. Please try again.")
    
    elif "tailor my resume" in latest_message or "adjust my resume" in latest_message:
        try:
            result = tailor_resume(env, messages[-1]["content"])
            env.add_reply(result)
        except Exception as e:
            env.add_reply(f"Error tailoring resume: {str(e)}. Please try again.")
    
    elif "track application" in latest_message or "status" in latest_message:
        try:
            # Parse job_id and status from the message (simplified for now)
            job_id = "job_" + str(len(load_user_data(env)["applications"]) + 1)
            status = "applied"  # Default status; could be parsed from message
            result = track_application(env, job_id, status)
            env.add_reply(result)
        except Exception as e:
            env.add_reply(f"Error tracking application: {str(e)}. Please try again.")
    
    else:
        try:
            # Fallback to AI completion for general queries
            result = env.completion(messages)
            if not result:
                result = "I'm here to help with your job applications! What would you like to do next? You can provide a job description, ask me to tailor your resume, or track an application."
            env.add_reply(result)
        except Exception as e:
            env.add_reply(f"An error occurred: {str(e)}. Please try again or let me know how to proceed.")

    # Request user input to continue the conversation
    env.request_user_input()

run(env)