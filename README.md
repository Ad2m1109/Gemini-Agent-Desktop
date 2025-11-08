# ✨ Gemini Agent Desktop

A powerful, non-blocking desktop client for the Gemini CLI, featuring rich chat history, a code editor, and built-in version rollback.

## 🌟 Project Goal

The Gemini Agent Desktop elevates the command-line experience of the official Gemini CLI into a feature-rich, dedicated desktop application. It merges the functionality of a code editor with a state-aware AI chatbot, ensuring the user interface remains responsive and providing a robust mechanism to revert code changes made by the AI.

## 🚀 Key Features

- **⚡ Non-Blocking Performance:** Built on PySide6 and Qt's concurrency model (QProcess and signals/slots) to ensure the application UI never freezes while waiting for the Gemini CLI's network and computation latency.
- **💾 Conversation Persistence:** All user prompts and Gemini responses are stored in a local SQLite database, allowing you to save, reload, and continue conversations across sessions.
- **↩️ Version Rollback (The Safety Net):** Automatically creates a file snapshot before applying any Gemini-suggested code modifications. A simple "Revert" button in the chat history restores the file to its previous state, mitigating risks.
- **💻 Three-Panel UI:** A familiar layout featuring a File Navigator, a Code Editor, and the dedicated Agent Chat Panel.
- **🎨 Rich Chat Experience:** Renders Gemini's output (including code blocks and lists) using Markdown for maximum readability.

## 🛠️ Installation and Setup

### Prerequisites

- Python 3.8+
- Gemini CLI: You must have the official `gemini` command-line tool installed and authenticated on your system. Test this by running `gemini -p "hello"` in your terminal.

### Installation Steps

1. Clone the Repository:
    ```bash
    git clone https://github.com/ademyoussfi/Gemini-GUI-Agent.git
    cd Gemini-GUI-Agent
    ```

2. Create and Activate Virtual Environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    .\venv\Scripts\activate   # On Windows
    ```

3. Install Dependencies:
    ```bash
    pip install pyside6 markdown-it-py
    ```

4. Run the Application:
    ```bash
    python app.py
    ```

## 📂 Project Structure

```
Gemini-GUI-Agent/
├── app.py                  # Main application entry point (PySide6 GUI initialization)
├── agent_worker.py         # QProcess/QThread logic for non-blocking CLI communication
├── database.py            # SQLite functions for saving/loading sessions and turns
├── ui/
│   ├── main_window.py     # PySide6 layout and widget definitions (Three-Panel UI)
│   ├── chat_widget.py     # Custom widget for rendering markdown chat bubbles
│   └── file_navigator.py  # QTreeView logic for displaying the project structure
└── .gemini-versions/      # [AUTO-CREATED] Stores file snapshots for rollback
└── agent_data.db         # [AUTO-CREATED] SQLite database for history
```

## ⚙️ Usage Guide

### 1. Starting a Session

The application automatically starts a new Conversation Session when you open a project folder via the File -> Open Project menu. This session is tied to the project path and is where all history is saved.

### 2. Getting Code Assistance

1. Open or create a file in the Center Editor Panel
2. Highlight the code block you want to analyze, fix, or refactor
3. Right-click the selection and choose "Send to Gemini Chat" or simply type your prompt into the Right Panel Input Box

### 3. Using the Rollback Feature (The Safety Net)

When Gemini suggests a code fix and you click "Apply Changes" within the chat panel:

1. The system automatically saves the original file content to a snapshot in the `.gemini-versions/` directory
2. The chat history log will show a "File Modified" note with a clickable "Revert" button
3. If the change is faulty, click "Revert" to restore the file from the safe snapshot