# 🚀 Multi-Agent SDLC Workflow (Waterfall Model)

A modern, interactive Streamlit application that demonstrates a complete **Software Development Lifecycle (Waterfall Model)** using a multi-agent system. Each agent is responsible for a specific phase, communicating and handing over deliverables to the next, simulating a real-world Waterfall SDLC process.

---

## 📂 Folder Structure

```
ai/
│
├── main.py                # Main Streamlit app with multi-agent workflow
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project metadata and dependencies
├── uv.lock                # Poetry/virtualenv lock file
├── .python-version        # Python version file
├── README.md              # (You are here!)
├── .venv/                 # (Optional) Virtual environment
└── __pycache__/           # Python cache
```
*Other folders in the repo (e.g., RAG/, summarizer/) are not required for this app.*

---

## 🌟 Features

- **Full SDLC Simulation:** From requirements to deployment, each phase is handled by a specialized agent.
- **Agent Communication:** Real-time, transparent handover and communication between agents.
- **Modern UI:** Beautiful, responsive Streamlit interface with clear workflow visualization.
- **LLM-Powered:** Uses Google Gemini (via LangChain) for realistic, high-quality agent outputs.
- **Extensible:** Easily adapt or extend agent logic for other SDLC models or projects.

---

## 🧑‍💻 Tech Stack

- **Frontend/UI:** [Streamlit](https://streamlit.io/)
- **AI/Agents:** [LangChain](https://python.langchain.com/), [LangGraph](https://github.com/langchain-ai/langgraph), [Google Generative AI (Gemini)](https://ai.google.dev/)
- **Environment:** Python 3.12+, [python-dotenv](https://pypi.org/project/python-dotenv/)
- **Other:** Modern CSS for custom styling

---

## 🛠️ How to Run

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd ai
   ```

2. **Set up Python Environment (Recommended: [uv](https://github.com/astral-sh/uv))**
   - If you don't have uv, install it: https://github.com/astral-sh/uv
   ```bash
   uv init  # Initializes pyproject.toml and lock files if not present
   uv venv  # Creates a virtual environment ('.venv' by default)
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv add -r requirements.txt  # Installs all dependencies from requirements.txt
   ```

   **Alternatively, use pip:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up Google API Key**
   - Create a `.env` file in the project root:
     ```
     api_key=your_google_gemini_api_key_here
     ```

4. **Run the App**
   ```bash
   streamlit run main.py
   ```

---

## 🧩 Agent Roles & Workflow

| Agent                | Role & Responsibilities                                                                 |
|----------------------|----------------------------------------------------------------------------------------|
| **Requirements Agent**  📋 | Gathers and defines comprehensive requirements, user stories, and constraints.         |
| **Design Agent**        🗂️ | Creates system architecture, technical design, and data structures.                   |
| **Development Agent**   💻 | Implements the application code according to the design.                              |
| **Code Review Agent**   🔍 | Reviews code for quality, security, and best practices.                               |
| **Testing Agent**       🧪 | Develops and runs comprehensive tests to ensure code quality.                         |
| **Deployment Agent**    🚀 | Prepares deployment documentation and the final release package.                       |

**Workflow:**  
Each agent completes its task and communicates with the next agent, passing along its deliverables. The "Agent Communications" panel in the app shows these interactions in real time, providing transparency into the workflow.

---

## ✨ Project Highlights

- **Educational:** Great for learning about SDLC, agent-based systems, and LLM integration.
- **Customizable:** Swap out agents, change prompts, or adapt to Agile/other SDLC models.
- **Beautiful UI:** Custom CSS and Streamlit components for a delightful user experience.

---

## 👤 Author & Contributions

- **Author:** [Padarthi Sai Kousik]
- **Contact:** [psaikousik@gmail.com]
- **GitHub:** [your-github-profile-link]

**Contributions are welcome!**  
Feel free to open issues or submit pull requests for improvements, new features, or bug fixes.

---

## 🤝 Last Contributions

- Sidebar redesign with static project info and beautiful formatting.
- Robust progress tracking and agent communication improvements.
- Enhanced requirements prompt with story mapping and acceptance criteria.

---

## 📜 License

This project is licensed under the MIT License.

---

> **Enjoy exploring the Multi-Agent SDLC Workflow!**  
> For questions, suggestions, or collaboration, please reach out via GitHub or email.
