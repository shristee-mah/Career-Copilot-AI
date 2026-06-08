# Career Copilot AI - Streamlit App

A conversational AI-powered CV analyzer and career advisor built with Streamlit, LangChain, and Google Gemini.

## Features

✨ **Key Features:**
- 📄 **CV Upload**: Support for PDF and text files
- 🤖 **AI-Powered Analysis**: Intelligent CV analysis using Google Gemini
- 💬 **Chat Interface**: Real-time conversation with Career Copilot
- 📊 **RAG System**: Retrieval-Augmented Generation for accurate context-aware responses
- 🎯 **Comprehensive Guidance**:
  - CV Analysis and Feedback
  - Skill Gap Identification
  - Interview Preparation
  - Project Recommendations
  - Learning Roadmaps
  - Career Path Suggestions

## Installation

### Prerequisites
- Python 3.8 or higher
- Google API Key (for Gemini)

### Setup Steps

1. **Navigate to the app directory:**
   ```bash
   cd c:\Users\Nitro v15\Desktop\LLM\RAG\app
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file:**
   ```bash
   copy .env.example .env
   ```

5. **Add your Google API Key:**
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Update the `.env` file with your key or enter it in the Streamlit sidebar

## Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

1. **Enter API Key**: Provide your Google API key in the sidebar
2. **Upload CV**: Click on the file uploader to select your CV (PDF or TXT)
3. **Start Chatting**: Type your questions in the chat box or use quick prompts
4. **Get Insights**: Receive personalized career advice based on your CV

### Example Questions

- "Analyze my CV and provide strengths"
- "What's my readiness for AI Engineering internship? Rate out of 100"
- "Suggest 3 projects to strengthen my profile"
- "Generate 10 technical interview questions"
- "Create a 12-week learning roadmap for Data Science"
- "What companies should I apply to with my profile?"

## Architecture

```
┌─────────────────┐
│   Streamlit UI  │
├─────────────────┤
│  File Upload    │
│  Chat Interface │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   CV Processing Layer   │
├─────────────────────────┤
│ - PyPDF Loader          │
│ - Text Splitter         │
│ - Embeddings Generator  │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   Vector Store (RAG)    │
├─────────────────────────┤
│ - Similarity Search     │
│ - Context Retrieval     │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   LangChain Agent       │
├─────────────────────────┤
│ - Google Gemini Model   │
│ - Retrieval Tool        │
│ - System Prompt         │
└────────┬────────────────┘
         │
         ▼
┌─────────────────┐
│   User Response │
└─────────────────┘
```

## Configuration

### Streamlit Config
Edit `.streamlit/config.toml` to customize:
- Theme settings
- Page width and layout
- Server configurations

### Custom System Prompt
To modify the AI's behavior, edit the `system_prompt` variable in `app.py` (around line 144)

## Troubleshooting

### Issue: "API Key Error"
- Verify your Google API key is correct
- Check that your account has access to Gemini API
- Generate a new key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Issue: "File Upload Error"
- Ensure the PDF is not corrupted
- Try a smaller file first
- Supported formats: PDF (.pdf), Text (.txt)

### Issue: "Slow Response Time"
- This is normal for the first query (model initialization)
- Subsequent queries should be faster
- Check your internet connection

## Project Structure

```
c:\Users\Nitro v15\Desktop\LLM\RAG\
├── app/
│   ├── app.py              # Main Streamlit application
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment variables template
│   └── .streamlit/
│       └── config.toml     # Streamlit configuration
├── notebooks/
│   └── agent.ipynb         # Development notebook
└── data/
    └── cvs/                # Sample CVs
```

## Advanced Usage

### Process Multiple CVs
The app maintains a separate vector store per session. To analyze different CVs:
1. Click "Clear" button to reset chat
2. Upload a new CV file
3. Start a new conversation

### API Rate Limiting
- Google Gemini has rate limits
- If you hit limits, wait a few minutes before making new queries

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify your API key and internet connection
3. Check the notebook for detailed implementation

---

**Built with ❤️ using Streamlit, LangChain, and Google Gemini**
