from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QFileDialog
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QTextCharFormat, QSyntaxHighlighter, QColor, QTextCursor
import re

class PythonHighlighter(QSyntaxHighlighter):
    """Simple Python syntax highlighter"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.highlight_rules = []
        
        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FF6B68"))
        keywords = [
            "and", "as", "assert", "break", "class", "continue", "def",
            "del", "elif", "else", "except", "False", "finally", "for",
            "from", "global", "if", "import", "in", "is", "lambda", "None",
            "nonlocal", "not", "or", "pass", "raise", "return", "True",
            "try", "while", "with", "yield"
        ]
        for word in keywords:
            pattern = re.compile(r"\b" + re.escape(word) + r"\b")
            self.highlight_rules.append((pattern, keyword_format))
        
        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#6A8759"))
        self.highlight_rules.append((re.compile(r'".*?"'), string_format))
        self.highlight_rules.append((re.compile(r"'.*?'") , string_format))
        
        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#808080"))
        self.highlight_rules.append((re.compile(r"#[^\n]*"), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlight_rules:
            for m in pattern.finditer(text):
                start = m.start()
                length = m.end() - m.start()
                self.setFormat(start, length, fmt)

class CodeEditor(QWidget):
    text_changed = Signal()  # Emitted when editor content changes
    file_saved = Signal(str)  # Emitted when file is saved, passes file path

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.current_file = None

    def setup_ui(self):
        """Initialize the code editor UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create and configure editor
        self.editor = QPlainTextEdit()
        self.setup_editor()
        layout.addWidget(self.editor)

        # Connect signals
        self.editor.textChanged.connect(self.text_changed.emit)

    def setup_editor(self):
        """Configure the editor instance"""
        # Set the default font
        self.editor.setFont("Consolas")
        
        # Enable line numbers
        self.editor.setLineWrapMode(QPlainTextEdit.NoWrap)
        
        # Set tab settings
        self.editor.setTabStopDistance(40)  # 4 spaces
        
        # Enable syntax highlighting
        self.highlighter = PythonHighlighter(self.editor.document())

    def open_file(self):
        """Open a file in the editor"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Python Files (*.py);;All Files (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.editor.setPlainText(content)
                    self.current_file = file_path
                    return True
            except Exception as e:
                print(f"Error opening file: {e}")
                return False
        return False

    def save_file(self):
        """Save the current file"""
        if not self.current_file:
            return self.save_file_as()
            
        try:
            with open(self.current_file, 'w', encoding='utf-8') as file:
                file.write(self.editor.toPlainText())
            self.file_saved.emit(self.current_file)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False

    def save_file_as(self):
        """Save the current file with a new name"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "Python Files (*.py);;All Files (*.*)"
        )
        
        if file_path:
            self.current_file = file_path
            return self.save_file()
        return False

    def get_selected_text(self) -> str:
        """Get the currently selected text"""
        return self.editor.textCursor().selectedText()

    def get_current_line(self) -> str:
        """Get the text of the current line"""
        cursor = self.editor.textCursor()
        cursor.select(QTextCursor.LineUnderCursor)
        return cursor.selectedText()

    def set_text(self, text: str):
        """Set the editor's text content"""
        self.editor.setPlainText(text)

    def insert_text(self, text: str):
        """Insert text at the current cursor position"""
        self.editor.insertPlainText(text)

    def replace_selection(self, text: str):
        """Replace the current selection with new text"""
        cursor = self.editor.textCursor()
        cursor.insertText(text)