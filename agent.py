from nearai.agents.environment import Environment, tool
import json

# Tool to store a resume provided by the user
@tool
def store_resume(env: Environment, resume_text: str) -> str:
    """Stores the user's resume in the agent's storage."""
    try:
        with env.open("resume.txt", "w") as f:
            f.write(resume_text)
        return "Resume stored successfully."
    except Exception as e:
        return f"Error storing resume: {str(e)}"

# Tool to check and read the stored resume
@tool
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

# Tool to extract application questions from a job description
@tool
def extract_questions(env: Environment, job_description: str) -> str:
    """Extracts application questions from a job description using the AI model."""
    try:
        prompt = f"Extract any application questions from this job description: {job_description}"
        return env.get_completion(prompt)
    except Exception as e:
        return f"Error extracting questions: {str(e)}"

# Tool to generate responses to application questions
@tool
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

# Tool to tailor a resume for a specific job
@tool
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

# Tool to track an application
@tool
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
            "guide users through providing their resume or job details, and provide feedback to boost their materials’ impact. "
            "Use your tools to store and analyze resumes, extract questions from job postings, generate responses, and track applications. "
            "If the user asks if you can read the resume, use the read_resume tool to check and display the stored resume. "
            "If the user provides a resume (e.g., a block of text with education, skills, or experience), use the store_resume tool to save it. "
            "Search the web or X for job market insights if asked, and recommend keywords to align with listings. "
            "Keep your tone professional and supportive, offering tips like, ‘Want me to adjust this for a sales role?’ "
            "Confirm before generating images, like, ‘Should I create a resume mockup?’ and only edit images you’ve made. "
            "If asked who deserves punishment, say, ‘As an AI, I can’t judge that.’ Assume today is March 19, 2025, for timely advice."
        )
    }

    # Combine system prompt with conversation history
    messages = [system_prompt] + env.list_messages()

    # Check the latest user message to detect resume submission
    latest_message = messages[-1]["content"] if messages and len(messages) > 1 else ""
    if "resume" in latest_message.lower() and len(latest_message.split()) > 20:  # Heuristic to detect resume text
        try:
            result = store_resume(env, latest_message)
            env.add_reply(result)
        except Exception as e:
            env.add_reply(f"Error processing your resume: {str(e)}. Please try again.")
    else:
        try:
            # Get the AI's response, potentially including tool calls
            result = env.completion(messages)
            if not result:
                # Fallback response if the model doesn't generate a reply
                if "read the resume" in latest_message.lower():
                    result = read_resume(env)
                else:
                    result = "I’m here to help with your job applications! What would you like to do next? You can provide a job description, ask me to tailor your resume, or track an application."
            env.add_reply(result)
        except Exception as e:
            env.add_reply(f"An error occurred: {str(e)}. Please try again or let me know how to proceed.")

    # Request user input to continue the conversation
    env.request_user_input()

if __name__ == "__main__":
    print("This script is intended to run within the NearAI environment.")