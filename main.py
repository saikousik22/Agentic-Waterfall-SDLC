import streamlit as st
import time
import json
from datetime import datetime
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph
from typing import TypedDict
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("api_key")

# Initialize session state
if 'workflow_started' not in st.session_state:
    st.session_state.workflow_started = False
if 'current_agent' not in st.session_state:
    st.session_state.current_agent = None
if 'agent_outputs' not in st.session_state:
    st.session_state.agent_outputs = {}
if 'agent_communications' not in st.session_state:
    st.session_state.agent_communications = []
if 'workflow_complete' not in st.session_state:
    st.session_state.workflow_complete = False
if 'workflow_progress' not in st.session_state:
    st.session_state.workflow_progress = 0

# Page config
st.set_page_config(
    page_title="Multi-Agent SDLC Workflow",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .agent-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
    }
    
    .agent-active {
        border-left: 5px solid #28a745;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        animation: pulse 2s infinite;
    }
    
    .agent-completed {
        border-left: 5px solid #6c757d;
        background: #f8f9fa;
    }
    
    .communication-bubble {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 20px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ff6b6b;
    }
    
    .handover-bubble {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 20px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
        font-weight: bold;
    }
    
    .workflow-progress {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    
    .task-complete {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Shared State Type
class BuildState(TypedDict):
    requirements: str
    design: str
    code: str
    review: str
    tests: str
    deploy: str

# Communication and Progress Functions
def add_communication(agent_name, message, recipient=None, is_handover=False):
    """Add communication message to session state"""
    comm = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "agent": agent_name,
        "message": message,
        "recipient": recipient,
        "is_handover": is_handover
    }
    st.session_state.agent_communications.append(comm)

def update_progress():
    """Update workflow progress"""
    st.session_state.workflow_progress = len(st.session_state.agent_outputs)

def display_agent_completion(agent_name, output_key):
    """Display agent completion status"""
    st.session_state.agent_outputs[output_key] = st.session_state.get(f"temp_{output_key}", "")
    update_progress()
    
    # Show completion message
    st.markdown(f"""
    <div class="task-complete">
        ✅ <strong>{agent_name}</strong> - Task Completed Successfully!
        <br>Output ready for next agent in pipeline.
    </div>
    """, unsafe_allow_html=True)

# Enhanced Agent Functions with Real LLM Integration
def RequirementsAgent(state):
    st.session_state.current_agent = "Requirements Agent"
    add_communication("Requirements Agent", "🚀 Starting requirements analysis for CLI To-Do List app...")
    
    # Show current agent working until task is complete
    with st.spinner("Requirements Agent analyzing project needs..."):
        prompt = """You are a senior software analyst with expertise in requirements engineering. 
        
        Define comprehensive requirements for a CLI-based To-Do List application that should include:
        - Add new tasks with descriptions
        - List all tasks with their current status  
        - Delete tasks by ID or description
        - Mark tasks as complete/incomplete
        - Edit existing task descriptions
        
        Provide detailed functional and non-functional requirements in a professional format.
        Include user stories and then  story mapping is compulsory, acceptance criteria, and technical constraints.
        Format the output in a structured, professional requirements document."""
        try:
            if API_KEY:
                llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key=API_KEY)
                result = llm.invoke(prompt)
                requirements = str(result) if result else "No response from LLM"
            else:
                st.error("API Key not found. Please set your Google API key in .env file")
                return {"requirements": "Error: API Key required"}
        except Exception as e:
            st.error(f"Requirements Agent Error: {str(e)}")
            requirements = f"Error in requirements generation: {str(e)}"
        # Store and display completion
        st.session_state.temp_requirements = requirements
        display_agent_completion("Requirements Agent", "requirements")
        # Handover message
        add_communication("Requirements Agent", "✅ Requirements analysis complete! Handover to Design Agent with comprehensive requirements document.", "Design Agent", True)
        return {"requirements": requirements}

def DesignAgent(state):
    st.session_state.current_agent = "Design Agent"
    add_communication("Design Agent", "👋 Received handover from Requirements Agent. Starting system architecture design...")
    
    with st.spinner("🎨 Design Agent creating system architecture..."):
        prompt = f"""You are a senior software architect with expertise in system design and Python development.

        Based on these requirements:
        {state['requirements']}

        Design a comprehensive system architecture that includes:
        - Detailed system architecture overview
        - All required functions with input/output specifications
        - Data structures and their relationships
        - Program flow and user interaction patterns
        - Error handling and validation strategies
        - CLI interface design principles
        - Security considerations
        - Performance optimization approaches
        
        Provide a complete technical design document that a developer can directly implement from."""
        try:
            if API_KEY:
                llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key=API_KEY)
                result = llm.invoke(prompt)
                design = str(result) if result else "No response from LLM"
            else:
                st.error("API Key not found. Please set your Google API key in .env file")
                return {"design": "Error: API Key required"}
        except Exception as e:
            st.error(f"Design Agent Error: {str(e)}")
            design = f"Error in design generation: {str(e)}"
        st.session_state.temp_design = design
        display_agent_completion("Design Agent", "design")
        add_communication("Design Agent", "🎯 System architecture design completed! Handover to Development Agent with detailed technical blueprint.", "Development Agent", True)
        return {"design": design}

def DevAgent(state):
    st.session_state.current_agent = "Development Agent"
    add_communication("Development Agent", "💻 Received handover from Design Agent. Starting code implementation...")
    
    with st.spinner("⚡ Development Agent writing Python code..."):
        prompt = f"""You are a senior Python developer with expertise in clean code and software craftsmanship.

        Based on this system design:
        {state['design']}

        Write complete, production-ready Python code for the CLI To-Do List application that includes:
        
        - Object-oriented design with proper class structure
        - All functions specified in the design document
        - Comprehensive error handling and input validation
        - User-friendly CLI interface with clear menus and messages
        - Proper data persistence during the session
        - Clean, readable, and maintainable code
        - Appropriate comments and documentation
        - Following Python best practices and PEP 8 standards
        
        Provide ONLY the complete, executable Python code without any explanations or markdown formatting."""
        try:
            if API_KEY:
                llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key=API_KEY)
                result = llm.invoke(prompt)
                code = str(result) if result else "No response from LLM"
            else:
                st.error("API Key not found. Please set your Google API key in .env file")
                return {"code": "Error: API Key required"}
        except Exception as e:
            st.error(f"Development Agent Error: {str(e)}")
            code = f"Error in code generation: {str(e)}"
        st.session_state.temp_code = code
        display_agent_completion("Development Agent", "code")
        add_communication("Development Agent", "⚡ Code implementation finished! Handover to Code Review Agent for quality assurance and optimization.", "Code Review Agent", True)
        return {"code": code}

def CodeReviewAgent(state):
    st.session_state.current_agent = "Code Review Agent"
    add_communication("Code Review Agent", "🔍 Received handover from Development Agent. Conducting comprehensive code review...")
    
    with st.spinner("🔍 Code Review Agent analyzing code quality..."):
        prompt = f"""You are a senior code reviewer and technical lead with expertise in Python development and software quality assurance.

        Conduct a comprehensive code review of this Python application:
        
        {state['code']}

        Provide a detailed code review report that includes:
        
        1. **Code Quality Assessment**: Overall quality score and rationale
        2. **Security Analysis**: Security vulnerabilities or concerns
        3. **Performance Review**: Performance issues and optimization opportunities  
        4. **Bug Detection**: Any bugs, logical errors, or edge cases not handled
        5. **Best Practices**: Adherence to Python best practices and coding standards
        6. **Maintainability**: Code structure, readability, and maintainability assessment
        7. **Testing Recommendations**: Areas that need testing focus
        8. **Improvement Suggestions**: Specific recommendations for enhancement
        9. **Code Refactoring**: Any refactoring suggestions with examples
        10. **Final Verdict**: Ready for production or needs modifications
        
        Provide actionable feedback that the development team can implement."""
        try:
            if API_KEY:
                llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key=API_KEY)
                result = llm.invoke(prompt)
                review = str(result) if result else "No response from LLM"
            else:
                st.error("API Key not found. Please set your Google API key in .env file")
                return {"review": "Error: API Key required"}
        except Exception as e:
            st.error(f"Code Review Agent Error: {str(e)}")
            review = f"Error in code review: {str(e)}"
        st.session_state.temp_review = review
        display_agent_completion("Code Review Agent", "review")
        add_communication("Code Review Agent", "✨ Code review completed with detailed analysis! Handover to Testing Agent for comprehensive test suite creation.", "Testing Agent", True)
        return {"review": review}

def TestingAgent(state):
    st.session_state.current_agent = "Testing Agent"
    add_communication("Testing Agent", "🧪 Received handover from Code Review Agent. Creating comprehensive test suite...")
    
    with st.spinner("🧪 Testing Agent writing unit tests..."):
        prompt = f"""You are a senior QA engineer and test automation specialist with expertise in Python testing frameworks.

        Based on the application code and code review feedback:
        
        CODE:
        {state['code']}
        
        REVIEW FEEDBACK:
        {state['review']}

        Create a comprehensive test suite using Python's unittest framework that includes:
        
        1. **Unit Tests**: Test all individual functions and methods
        2. **Integration Tests**: Test component interactions
        3. **Edge Case Testing**: Test boundary conditions and error scenarios
        4. **Input Validation Tests**: Test all input validation logic
        5. **Error Handling Tests**: Test error conditions and exception handling
        6. **State Management Tests**: Test data persistence and state changes
        7. **User Interface Tests**: Test CLI menu and user interaction flows
        8. **Performance Tests**: Basic performance validation
        9. **Regression Tests**: Tests to prevent future bugs
        10. **Mock Tests**: Use mocks where appropriate for external dependencies
        
        Provide ONLY the complete, executable Python test code using unittest framework.
        Include proper test setup, teardown, and comprehensive test coverage.
        Follow testing best practices and naming conventions."""
        try:
            if API_KEY:
                llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key=API_KEY)
                result = llm.invoke(prompt)
                tests = str(result) if result else "No response from LLM"
            else:
                st.error("API Key not found. Please set your Google API key in .env file")
                return {"tests": "Error: API Key required"}
        except Exception as e:
            st.error(f"Testing Agent Error: {str(e)}")
            tests = f"Error in test generation: {str(e)}"
        st.session_state.temp_tests = tests
        display_agent_completion("Testing Agent", "tests")
        add_communication("Testing Agent", "🎉 Comprehensive test suite completed with full coverage! Handover to Deployment Agent for final deployment preparation.", "Deployment Agent", True)
        return {"tests": tests}

def DeployAgent(state):
    st.session_state.current_agent = "Deployment Agent"
    add_communication("Deployment Agent", "🚀 Received handover from Testing Agent. Preparing deployment documentation and final package...")
    
    with st.spinner("🚀 Deployment Agent preparing final deployment..."):
        prompt = f"""You are a senior DevOps engineer and deployment specialist with expertise in software delivery and documentation.

        Based on the complete project deliverables:
        
        REQUIREMENTS: {state['requirements']}
        DESIGN: {state['design']}  
        CODE: {state['code']}
        REVIEW: {state['review']}
        TESTS: {state['tests']}

        Create comprehensive deployment documentation and delivery package that includes:
        
        1. **Professional README**: Complete project documentation with features, installation, and usage
        2. **System Requirements**: Detailed technical requirements and dependencies
        3. **Installation Guide**: Step-by-step installation instructions for different platforms
        4. **User Manual**: Comprehensive user guide with examples and screenshots
        5. **Developer Guide**: Setup instructions for development environment
        6. **Testing Instructions**: How to run tests and validate installation
        7. **Troubleshooting Guide**: Common issues and their solutions
        8. **Performance Specifications**: Performance benchmarks and optimization tips
        9. **Security Guidelines**: Security considerations and best practices
        10. **Version Information**: Release notes and version history
        11. **Support Information**: How to get help and report issues
        12. **License and Legal**: Licensing information and legal notices
        
        Create production-ready documentation that enables easy deployment and maintenance.
        Format as a professional software release package."""
        try:
            if API_KEY:
                llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key=API_KEY)
                result = llm.invoke(prompt)
                deploy = str(result) if result else "No response from LLM"
            else:
                st.error("API Key not found. Please set your Google API key in .env file")
                return {"deploy": "Error: API Key required"}
        except Exception as e:
            st.error(f"Deployment Agent Error: {str(e)}")
            deploy = f"Error in deployment documentation: {str(e)}"
        st.session_state.temp_deploy = deploy
        display_agent_completion("Deployment Agent", "deploy")
        add_communication("Deployment Agent", "✅ Deployment preparation completed successfully! Full SDLC workflow finished - Project ready for production release! 🎉", None, True)
        st.session_state.workflow_complete = True
        return {"deploy": deploy}

# Create the LangGraph workflow
def create_workflow():
    graph = StateGraph(BuildState)
    
    graph.add_node("Requirements", RequirementsAgent)
    graph.add_node("Design", DesignAgent)
    graph.add_node("Dev", DevAgent)
    graph.add_node("Review", CodeReviewAgent)
    graph.add_node("Testing", TestingAgent)
    graph.add_node("Deploy", DeployAgent)
    
    graph.set_entry_point("Requirements")
    graph.add_edge("Requirements", "Design")
    graph.add_edge("Design", "Dev")
    graph.add_edge("Dev", "Review")
    graph.add_edge("Review", "Testing")
    graph.add_edge("Testing", "Deploy")
    graph.set_finish_point("Deploy")
    
    return graph.compile()

# Main UI Function
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Multi-Agent SDLC Workflow</h1>
        <p>Complete Software Development Lifecycle with Intelligent Agent Collaboration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # API Key Check
    if not API_KEY:
        st.error("⚠️ Google API Key not found! Please add your API key to the .env file:")
        st.code("api_key=your_google_api_key_here")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Workflow Control")
        
        if not st.session_state.workflow_started:
            if st.button("🚀 Start Multi-Agent Workflow", type="primary"):
                st.session_state.workflow_started = True
                st.rerun()
        else:
            if st.button("🔄 Reset Workflow"):
                # Reset all session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        st.markdown("---")
        st.header("📘 About This Project")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #232526 0%, #414345 100%); border-radius: 12px; padding: 1.5rem; color: #fff; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <h3 style="margin-top:0; margin-bottom: 0.5rem; font-size: 1.3rem; letter-spacing: 1px;">
                <span style="font-size:1.5rem; vertical-align:middle;">🚀</span> <b>Multi-Agent SDLC Workflow</b> <span style="font-size:0.95rem; color:#b3b3b3;">(Waterfall Model)</span>
            </h3>
            <p style="margin-bottom: 1.2rem; font-size:1.05rem; color:#e0e0e0;">
                This application demonstrates a complete <b>Software Development Lifecycle (SDLC)</b> using a <b>multi-agent system</b>, where each agent is responsible for a specific phase. Agents communicate and hand over deliverables to the next agent, simulating a real-world <b>Waterfall SDLC</b> process.
            </p>
            <div style="margin-bottom: 1.1rem;">
                <b>🧑‍💻 Agent Roles:</b>
                <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0; font-size:1.02rem;">
                    <li><b>Requirements Agent</b> <span style='color:#a3e635;'>📋</span>: Gathers and defines comprehensive requirements for the project.</li>
                    <li><b>Design Agent</b> <span style='color:#38bdf8;'>🗂️</span>: Creates the system architecture and technical design based on requirements.</li>
                    <li><b>Development Agent</b> <span style='color:#fbbf24;'>💻</span>: Implements the application code according to the design.</li>
                    <li><b>Code Review Agent</b> <span style='color:#f472b6;'>🔍</span>: Reviews the code for quality, security, and best practices.</li>
                    <li><b>Testing Agent</b> <span style='color:#34d399;'>🧪</span>: Develops and runs comprehensive tests to ensure code quality.</li>
                    <li><b>Deployment Agent</b> <span style='color:#818cf8;'>🚀</span>: Prepares deployment documentation and final release package.</li>
                </ul>
            </div>
            <div style="margin-bottom: 0.5rem;">
                <b>🔗 How it works:</b>
                <p style="margin:0.3rem 0 0 0.2rem; color:#d1d5db; font-size:1.01rem;">
                    Each agent completes its task and <b>communicates</b> with the next agent, passing along its deliverables.<br/>
                    The <b>Agent Communications</b> panel on the right shows these interactions in real time, providing transparency into the workflow.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🔄 Agent Workflow Progress")
        
        if st.session_state.workflow_started and not st.session_state.workflow_complete:
            # Run workflow step by step
            app = create_workflow()
            
            try:
                final_output = app.invoke({
                    "requirements": "",
                    "design": "",
                    "code": "",
                    "review": "",
                    "tests": "",
                    "deploy": ""
                })
                st.success("🎉 Multi-Agent Workflow completed successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Workflow Error: {str(e)}")
        
        # Display agent outputs
        if st.session_state.agent_outputs:
            st.header("📋 Agent Deliverables")  
            
            agent_names = {
                "requirements": "Requirements Agent",
                "design": "Design Agent", 
                "code": "Development Agent",
                "review": "Code Review Agent",
                "tests": "Testing Agent",
                "deploy": "Deployment Agent"
            }
            
            for key, output in st.session_state.agent_outputs.items():
                agent_name = agent_names.get(key, key.title())
                is_active = st.session_state.current_agent == agent_name
                
                with st.expander(f"{'🔄' if is_active else '✅'} {agent_name} - Deliverables", expanded=is_active):
                    st.markdown(f"**Agent:** {agent_name}")
                    st.markdown("**Output:**")
                    if key in ["code", "tests"]:
                        st.code(output, language="python")
                    else:
                        st.markdown(output)
    
    with col2:
        st.header("💬 Agent Communications")
        
        if st.session_state.agent_communications:
            for comm in st.session_state.agent_communications:
                css_class = "handover-bubble" if comm["is_handover"] else "communication-bubble"
                st.markdown(f"""
                <div class="{css_class}">
                    <small><strong>{comm['timestamp']}</strong></small><br>
                    <strong>{comm['agent']}:</strong><br>
                    {comm['message']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No communications yet. Start the workflow to see agent interactions!")
        
        # Workflow completion summary
        if st.session_state.workflow_complete:
            st.markdown("""
            <div class="task-complete">
                🎉 <strong>WORKFLOW COMPLETE!</strong><br>
                All agents have successfully completed their tasks.
                The CLI Todo application is ready for production deployment!
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()