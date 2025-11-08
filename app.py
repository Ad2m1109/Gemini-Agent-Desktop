import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # If a project path is provided as argument, open it
    if len(sys.argv) > 1:
        project_path = Path(sys.argv[1]).absolute()
        if project_path.is_dir():
            window.open_project(str(project_path))

    # Start the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()