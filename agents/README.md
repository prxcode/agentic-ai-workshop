CREATE a .env file with a field API_KEY, further for one of the programs you will need a TAVILY_API_KEY. For the API_KEY go to groq, and create one and set it to the variable in your environment file.

# Project Setup

## 1. Creating and Activating a Python Virtual Environment

### Windows (Command Prompt or PowerShell)

1. **Navigate to your project folder**:

   ```bat
   cd C:\path\to\your\project
   ```
2. **Create a virtual environment**:

   ```bat
   python -m venv venv
   ```
3. **Activate the virtual environment**:

   ```bat
   .\venv\Scripts\activate
   ```
4. **You should see** `(venv)` **prepended to your prompt**.

### macOS / Linux (bash/zsh)

1. **Navigate to your project folder**:

   ```bash
   cd /path/to/your/project
   ```
2. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   ```
3. **Activate the virtual environment**:

   ```bash
   source venv/bin/activate
   ```
4. **You should see** `(venv)` **prepended to your prompt**.

---

## 2. Installing Required Python Libraries

Once your virtual environment is active, install the libraries used in this project:

```bash
pip install langchain langgraph langchain_groq python-dotenv pydantic requests
```

* **langchain**: Core agent and chain framework
* **langgraph**: Core agent and chain framework
* **langchain\_groq**: Groq-hosted model integration
* **python-dotenv**: Loading environment variables from `.env`
* **pydantic**: Structured tool schemas
* **requests**: HTTP calls (if you use manual API wrappers)

---


