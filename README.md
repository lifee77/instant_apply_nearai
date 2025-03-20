# InstantApply - Automate Your Job Applications! 🚀

**InstantApply** is an AI-powered agent built on the [NearAI platform](https://app.near.ai/) to help you streamline your job application process. It automates tasks like storing your resume, tailoring it for specific job postings, generating responses to application questions, and tracking your applications. Whether you're applying for a software engineering role or a project management position, InstantApply provides professional guidance and feedback to boost your application materials.

Try it out now: [InstantApply on NearAI](https://app.near.ai/agents/kindyak1075.near/InstantApply/latest)

---

## Features

- **Resume Storage**: Store your resume as text for easy access and use.
- **Resume Tailoring**: Customize your resume for specific job postings with suggested edits and keywords.
- **Application Question Responses**: Generate answers to job application questions based on your resume.
- **Application Tracking**: Keep track of your job applications with job IDs and statuses.
- **Professional Guidance**: Get supportive tips to improve your application materials.

---

## Getting Started

When you start the agent on NearAI, InstantApply will greet you with:

**InstantApply, Your Job Application Wizard! 🚀**  
Hey there! I’m InstantApply, here to make your job hunt a breeze. I can store your resume, tailor it for your dream job, answer application questions, and track your progress. Try saying: 'store my resume', 'tailor my resume for a software engineer role', 'answer these application questions', or 'track my application for Job ID 123'. What can I help you with today?

### Prerequisites

- A NearAI account to interact with the agent.
- A resume in text format (you can copy-paste it into the chat).

### How to Use

1. **Access the Agent**:
   - Visit the deployed agent: [InstantApply on NearAI](https://app.near.ai/agents/kindyak1075.near/InstantApply/latest).

2. **Interact with InstantApply**:
   - Follow the welcome message’s examples to get started.
   - Use natural language commands to interact with the agent.

3. **Example Commands**:
   - **Store Your Resume**:
     ```
     store my resume: JEEVAN BHATTA | EDUCATION: MINERVA UNIVERSITY...
     ```
     *Response*: "Resume stored successfully."
   - **Read Your Resume**:
     ```
     Can you read the resume?
     ```
     *Response*: "Here is the stored resume: JEEVAN BHATTA | EDUCATION: MINERVA UNIVERSITY..."
   - **Tailor Your Resume**:
     ```
     tailor my resume for a software engineer role
     ```
     *Response*: "Here’s a tailored version of your resume: [suggested edits]. I recommend adding keywords like 'Python' and 'software development' to align with the posting. Want me to adjust it further?"
   - **Answer Application Questions**:
     ```
     answer these application questions: Why are you interested in this role? What are your strengths?
     ```
     *Response*: "Here are the responses: [generated answers based on your resume]."
   - **Track an Application**:
     ```
     track my application for Job ID 123
     ```
     *Response*: "Application job_1 tracked with status: applied."

---

## Project Structure

- **`agent.py`**: The main script for the InstantApply agent, handling user interactions, resume management, and application tracking.
- **`metadata.json`**: Configuration file defining the agent’s name, description, welcome message, and capabilities.
- **`README.md`**: This file, providing an overview and usage instructions.

---

## Setup for Development

If you’d like to modify or run the agent locally before deploying it to NearAI, follow these steps:

### Prerequisites

- A NearAI account

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/lifee77/instant_apply_nearai.git
   cd instant_apply_nearai
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   - The agent primarily relies on the `nearai` package. Install it using:
     ```bash
     pip install nearai
     ```
   - Note: The `nearai` package is specific to the NearAI platform and may require authentication or access to deploy agents.

4. **Modify the Agent**:
   - Edit `agent.py` to add new features or adjust the system prompt.
   - Update `metadata.json` to change the welcome message, model settings, or capabilities.

5. **Deploy the Agent**:
   - Use the NearAI CLI to deploy the agent:
     ```bash
     nearai agent deploy
     ```
   - Follow the prompts to authenticate and deploy to your NearAI account.

---

## Limitations

- **File Uploads**: Currently, the agent only supports text-based resume input (copy-paste). File uploads (e.g., PDF, DOCX) are not supported due to NearAI environment constraints.
- **Web Automation**: Features like browsing job postings or filling forms online are not supported in the NearAI environment.
- **Error Handling**: While the agent includes basic error handling, complex user inputs might require additional validation.

---

## Contributing

Contributions are welcome! If you’d like to improve InstantApply, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request with a description of your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- Powered by the [NearAI platform](https://app.near.ai/).
- Inspired by the NearAI agent ecosystem and the need for efficient job application automation.

---

## Contact

For questions or feedback, feel free to open an issue on GitHub or reach out via the [NearAI platform](https://app.near.ai/agents/kindyak1075.near/InstantApply/latest).
```
