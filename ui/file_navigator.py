from PySide6.QtWidgets import QTreeView, QFileSystemModel
from PySide6.QtCore import Qt, QDir

class FileNavigator(QTreeView):
    def __init__(self):
        super().__init__()
        self.setup_model()
        self.setup_view()

    def setup_model(self):
        """Initialize the file system model"""
        self.model = QFileSystemModel()
        self.model.setRootPath("")  # Will be set when opening a project
        self.model.setNameFilters(["*.py", "*.md", "*.txt", "*.json"])
        self.model.setNameFilterDisables(False)  # Hide filtered files
        self.setModel(self.model)

    def setup_view(self):
        """Configure the tree view appearance and behavior"""
        # Hide size, type, and date columns
        self.setHeaderHidden(True)
        for i in range(1, 4):  # Columns 1-3
            self.hideColumn(i)
        
        # Enable selection and drag-drop
        self.setSelectionMode(QTreeView.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def set_root_path(self, path: str):
        """Set the root directory for the file navigator"""
        root_index = self.model.setRootPath(path)
        self.setRootIndex(root_index)

    def get_selected_path(self) -> str:
        """Get the absolute path of the selected file/directory"""
        indexes = self.selectedIndexes()
        if not indexes:
            return ""
        return self.model.filePath(indexes[0])