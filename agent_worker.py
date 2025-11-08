from PySide6.QtCore import QObject, Signal, QProcess
import json

class AgentWorker(QObject):
    """
    Handles asynchronous communication with the Gemini CLI using QProcess
    """
    response_ready = Signal(str)  # Emitted when Gemini response is ready
    error_occurred = Signal(str)  # Emitted when an error occurs

    def __init__(self):
        super().__init__()
        self.process = None

    def send_prompt(self, prompt: str):
        """
        Sends a prompt to Gemini CLI asynchronously
        """
        if self.process is not None and self.process.state() == QProcess.Running:
            self.process.kill()

        self.process = QProcess()
        self.process.finished.connect(self._handle_response)
        self.process.errorOccurred.connect(self._handle_error)
        
        # Start Gemini CLI process
        self.process.start("gemini", ["-p", prompt])

    def _handle_response(self):
        """
        Handles the response from Gemini CLI
        """
        if self.process is None:
            return

        exit_code = self.process.exitCode()
        if exit_code == 0:
            response = self.process.readAllStandardOutput().data().decode().strip()
            self.response_ready.emit(response)
        else:
            error = self.process.readAllStandardError().data().decode().strip()
            self.error_occurred.emit(f"Gemini CLI Error (Exit code: {exit_code}): {error}")

    def _handle_error(self, error: QProcess.ProcessError):
        """
        Handles QProcess errors
        """
        error_messages = {
            QProcess.FailedToStart: "Failed to start Gemini CLI. Is it installed and in PATH?",
            QProcess.Crashed: "Gemini CLI process crashed",
            QProcess.Timedout: "Operation timed out",
            QProcess.WriteError: "Failed to write to Gemini CLI process",
            QProcess.ReadError: "Failed to read from Gemini CLI process",
            QProcess.UnknownError: "An unknown error occurred"
        }
        self.error_occurred.emit(error_messages.get(error, "An unknown error occurred"))