from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QScrollArea
from PySide6.QtCore import Qt, Signal
from markdown_it import MarkdownIt

from agent_worker import AgentWorker

class ChatWidget(QWidget):
    prompt_submitted = Signal(str)  # Emitted when user submits a prompt

    def __init__(self, agent_worker: AgentWorker):
        super().__init__()
        self.agent_worker = agent_worker
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Initialize the chat widget UI components"""
        layout = QVBoxLayout(self)
        
        # Chat history scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Chat history content widget
        self.chat_content = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_layout.addStretch()
        self.scroll_area.setWidget(self.chat_content)
        
        # Input area
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Type your prompt here...")
        self.input_text.setMaximumHeight(100)
        
        # Submit button
        self.submit_button = QPushButton("Send")
        self.submit_button.clicked.connect(self.submit_prompt)
        
        # Add widgets to layout
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.input_text)
        layout.addWidget(self.submit_button)

        # Initialize markdown parser
        self.md = MarkdownIt()

    def connect_signals(self):
        """Connect agent worker signals"""
        self.agent_worker.response_ready.connect(self.handle_response)
        self.agent_worker.error_occurred.connect(self.handle_error)

    def submit_prompt(self):
        """Handle prompt submission"""
        prompt = self.input_text.toPlainText().strip()
        if not prompt:
            return
            
        # Clear input and add prompt to chat
        self.input_text.clear()
        self.add_message(prompt, is_user=True)
        
        # Send to agent worker
        self.agent_worker.send_prompt(prompt)
        self.prompt_submitted.emit(prompt)

    def handle_response(self, response: str):
        """Handle response from agent worker"""
        self.add_message(response, is_user=False)

    def handle_error(self, error: str):
        """Handle error from agent worker"""
        self.add_message(f"Error: {error}", is_user=False, is_error=True)

    def add_message(self, text: str, is_user: bool, is_error: bool = False):
        """Add a new message to the chat history"""
        # Create message widget
        message = QTextEdit()
        message.setReadOnly(True)
        
        # Style based on message type
        style = """
            QTextEdit {
                background-color: %s;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
            }
        """ % (
            "#e3f2fd" if is_user else  # Light blue for user
            "#ffebee" if is_error else  # Light red for errors
            "#f5f5f5"                   # Light gray for agent
        )
        message.setStyleSheet(style)
        
        # Convert markdown to HTML if it's an agent message
        if not is_user:
            html = self.md.render(text)
            message.setHtml(html)
        else:
            message.setPlainText(text)
        
        # Add to layout and scroll to bottom
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, message)
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )