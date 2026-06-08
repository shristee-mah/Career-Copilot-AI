# pyrefly: ignore [missing-import]
import streamlit as st
import os
from pathlib import Path
from io import BytesIO
import tempfile

# LangChain imports
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.tools import tool
from langchain.agents import create_agent
import getpass

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Career Copilot AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .chat-message {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .user-message {
        border-left: 4px solid #2196F3;
    }
    .ai-message {
        border-left: 4px solid #9c27b0;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # API Key Input
    api_key = st.text_input(
        "🔑 Google API Key",
        type="password",
        help="Enter your Google Generative AI API key"
    )
    
    st.divider()
    st.markdown("### 📄 About")
    st.info(
        "Career Copilot AI is an intelligent advisor that analyzes CVs and helps "
        "with career planning, internship preparation, and skill development."
    )

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================
if "cv_loaded" not in st.session_state:
    st.session_state.cv_loaded = False
    st.session_state.cv_content = ""
    st.session_state.vector_store = None
    st.session_state.agent = None
    st.session_state.chat_history = []
    st.session_state.embeddings = None
    st.session_state.docs = []

# ============================================================================
# MAIN HEADER
# ============================================================================
st.markdown(
    """
    <div class="header">
    <h1>🤖 Career Copilot AI</h1>
    <p>Your Intelligent Career, University & Internship Advisor</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================================
# SETUP RAG SYSTEM
# ============================================================================
def setup_rag_system(api_key):
    """Initialize the RAG system with embeddings and agent"""
    try:
        # Set up embeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=api_key
        )
        
        # Initialize vector store
        vector_store = InMemoryVectorStore(embeddings)
        
        # Initialize LLM
        model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key
        )
        
        # Create retrieval tool
        @tool(response_format="content_and_artifact")
        def retrieve_context(query: str):
            """Retrieve information to help answer a query."""
            retrieved_docs = vector_store.similarity_search(query, k=3)
            serialized = "\n\n".join(
                (f"Source: {doc.metadata}\nContent: {doc.page_content}")
                for doc in retrieved_docs
            )
            return serialized, retrieved_docs
        
        # Create agent with system prompt
        system_prompt = """You are Career Copilot AI, an intelligent career, university, and internship advisor.

Your purpose is to help students, graduates, and professionals evaluate their current profile, identify skill gaps, prepare for internships, jobs, higher studies, and create actionable improvement plans.

You have expertise in:
- Resume and CV analysis
- Internship and job preparation
- AI/ML, Data Science, Software Engineering, and Technology careers
- University admission preparation
- Technical interview preparation
- Learning roadmap generation
- Project recommendations
- Skill gap analysis

## Core Responsibilities
When analyzing a CV or profile:
1. Analyze the provided information thoroughly
2. Identify strengths and weaknesses
3. Identify missing skills and qualifications
4. Recommend improvements
5. Suggest suitable job roles
6. Suggest suitable internships
7. Suggest projects that strengthen the profile
8. Generate interview questions
9. Generate practice MCQs
10. Create a personalized learning roadmap
11. Research and explain company or university expectations when information is available

## Response Style
- Be specific and actionable
- Avoid generic advice
- Explain reasoning
- Prioritize practical recommendations
- Tailor all recommendations to the user's background and goals
- If information is missing, ask focused follow-up questions before making assumptions
- Use clear formatting with headings and bullet points

Your goal is to function as a personalized AI mentor that helps users become competitive candidates for their desired jobs, internships, or university programs."""
        
        agent = create_agent(model, [retrieve_context], system_prompt=system_prompt)
        
        return embeddings, vector_store, agent, retrieve_context
    
    except Exception as e:
        st.error(f"Error setting up RAG system: {str(e)}")
        return None, None, None, None

# ============================================================================
# LOAD AND PROCESS CV
# ============================================================================
def load_and_process_cv(uploaded_file, api_key):
    """Load CV file and populate vector store"""
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name
        
        # Load document
        if uploaded_file.type == "application/pdf":
            loader = PyPDFLoader(tmp_path)
        else:
            loader = TextLoader(tmp_path)
        
        docs = loader.load()
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )
        all_splits = text_splitter.split_documents(docs)
        
        # Add to vector store
        document_ids = st.session_state.vector_store.add_documents(documents=all_splits)
        
        # Store metadata
        st.session_state.docs = docs
        st.session_state.cv_content = "\n\n".join([doc.page_content for doc in docs])
        
        # Cleanup
        os.unlink(tmp_path)
        
        return len(all_splits), len(document_ids)
    
    except Exception as e:
        st.error(f"Error processing CV: {str(e)}")
        return None, None

# ============================================================================
# MAIN INTERFACE
# ============================================================================

# Check if API key is provided
if not api_key:
    st.warning("⚠️ Please enter your Google API Key in the sidebar to get started")
    st.stop()

# Setup RAG system on first load or when API key changes
if st.session_state.agent is None:
    with st.spinner("Initializing Career Copilot AI..."):
        embeddings, vector_store, agent, retrieve_context = setup_rag_system(api_key)
        if agent:
            st.session_state.embeddings = embeddings
            st.session_state.vector_store = vector_store
            st.session_state.agent = agent
            st.session_state.retrieve_context = retrieve_context
            st.success("✓ Career Copilot AI initialized successfully!")
        else:
            st.error("Failed to initialize the system")
            st.stop()

# Two-column layout
col1, col2 = st.columns([1, 2])

# ============================================================================
# LEFT COLUMN: CV UPLOAD
# ============================================================================
with col1:
    st.subheader("📂 Upload Your CV")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF or Text file",
        type=["pdf", "txt"],
        help="Upload your CV in PDF or TXT format"
    )
    
    if uploaded_file:
        with st.spinner("Processing your CV..."):
            chunks, doc_ids = load_and_process_cv(uploaded_file, api_key)
            if chunks:
                st.session_state.cv_loaded = True
                st.success(f"✓ CV loaded successfully!")
                st.info(f"📊 Processed into {chunks} chunks for analysis")
                
                # Show file info
                st.markdown("### 📋 File Information")
                st.write(f"**File Name:** {uploaded_file.name}")
                st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")
                st.write(f"**Pages/Sections:** {len(st.session_state.docs)}")
    
    st.divider()
    
    # Quick start prompts
    st.subheader("💡 Quick Prompts")
    quick_prompts = [
        "Analyze my CV and provide strengths",
        "What's my readiness for AI internship?",
        "Suggest projects to improve my profile",
        "Generate interview questions for me",
        "Create a learning roadmap",
    ]
    
    for prompt in quick_prompts:
        if st.button(prompt, key=prompt, use_container_width=True):
            st.session_state.user_input = prompt

# ============================================================================
# RIGHT COLUMN: CHAT INTERFACE
# ============================================================================
with col2:
    st.subheader("💬 Chat with Career Copilot")
    
    if not st.session_state.cv_loaded:
        st.info("👆 Please upload your CV in the left panel to start the conversation")
    
    # Display chat history
    chat_container = st.container(height=400, border=True)
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(
                    f'<div class="chat-message user-message"><b>You:</b> {message["content"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="chat-message ai-message"><b>Career Copilot:</b> {message["content"]}</div>',
                    unsafe_allow_html=True
                )
    
    # Chat input
    st.divider()
    
    user_input = st.text_area(
        "Your message:",
        placeholder="Ask me anything about your career, CV, internships, or skill development...",
        height=80,
        key="user_input"
    )
    
    col_send, col_clear = st.columns([4, 1])
    
    with col_send:
        send_button = st.button("📤 Send", use_container_width=True, type="primary")
    
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Process user message
    if send_button and user_input:
        if not st.session_state.cv_loaded:
            st.error("Please upload your CV first!")
        else:
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Get CV context
            with st.spinner("Analyzing your CV and generating response..."):
                try:
                    # Fetch full CV content directly
                    cv_context = st.session_state.cv_content
                    
                    # Create prompt with context
                    prompt_with_context = f"""Here is the CV content:

{cv_context}

Based on this CV, please respond to the following:

{user_input}

Provide specific, actionable advice based on the CV content."""
                    
                    # Get agent response
                    response = st.session_state.agent.invoke(
                        {"messages": [{"role": "user", "content": prompt_with_context}]}
                    )
                    
                    ai_message = response["messages"][-1].content
                    
                    # Add AI message to history
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_message})
                    
                    st.rerun()
                
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
    
    # Display tips
    st.divider()
    with st.expander("💡 Tips for Better Results"):
        st.markdown("""
        - **Be specific**: Ask questions about particular skills or roles
        - **Use examples**: Mention specific internships or companies
        - **Ask for details**: Request actionable steps and timelines
        - **Follow up**: Ask follow-up questions to dive deeper
        - **Get templates**: Ask for interview questions or project ideas
        """)

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.markdown("""
    <center>
    <p style="color: gray; font-size: 12px;">
    Career Copilot AI | Powered by Google Gemini & LangChain<br>
    Built with ❤️ for your career success
    </p>
    </center>
""", unsafe_allow_html=True)
