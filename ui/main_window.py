from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt

from ui.file_navigator import FileNavigator
from ui.chat_widget import ChatWidget
from agent_worker import AgentWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gemini Agent Desktop")
        self.resize(1200, 800)

        # Initialize the agent worker
        self.agent_worker = AgentWorker()
        
        # Create the central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create the main splitter
        self.main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.main_splitter)
        
        # Add the file navigator (left panel)
        self.file_navigator = FileNavigator()
        self.main_splitter.addWidget(self.file_navigator)
        
        # Create a second splitter for editor and chat
        self.editor_chat_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.addWidget(self.editor_chat_splitter)
        
        # Add code editor placeholder (middle panel)
        # TODO: Replace with actual code editor implementation
        self.code_editor = QWidget()  
        self.editor_chat_splitter.addWidget(self.code_editor)
        
        # Add chat widget (right panel)
        self.chat_widget = ChatWidget(self.agent_worker)
        self.editor_chat_splitter.addWidget(self.chat_widget)
        
        # Set initial splitter sizes (ratios: 1:2:1)
        self.main_splitter.setSizes([200, 800])
        self.editor_chat_splitter.setSizes([500, 300])

    def open_project(self, project_path: str):
        """
        Opens a project directory and initializes the UI components
        """
        self.file_navigator.set_root_path(project_path)
        # TODO: Initialize database session
        # TODO: Load recent files in editor