"""
Main window for the Electrical Estimator application
"""

from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                            QHBoxLayout, QSplitter, QTextEdit, QListWidget,
                            QPushButton, QToolBar, QLabel, QFileDialog,
                            QStatusBar, QMenuBar, QMenu, QMessageBox, QDialog,
                            QStyle)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QPixmap, QColor

from gui.project_tab import ProjectTab
from gui.pricing_widget import PricingWidget
from gui.styles import get_dark_theme, get_light_theme
from controllers.project_controller import ProjectController


class MainWindow(QMainWindow):
    """Main window class for the application"""
    
    def __init__(self):
        super().__init__()

        self.project_controller = ProjectController()

        # Set theme (default to dark theme)
        self.dark_mode = True
        self.apply_theme()

        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        # Set window properties
        self.setWindowTitle("Electrical Estimator")
        self.setMinimumSize(1200, 800)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
        
        # Create the tab widget for projects
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        
        # Create a default tab
        self.create_new_project_tab("New Project")
        
        # Set the central widget
        self.setCentralWidget(self.tab_widget)
    
    def create_menu_bar(self):
        """Create the menu bar"""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        
        new_action = QAction("&New Project", self)
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open Project", self)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Save Project", self)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menu_bar.addMenu("&Edit")
        # Add edit actions here
        
        # View menu
        view_menu = menu_bar.addMenu("&View")
        # Add view actions here
        
        # Help menu
        help_menu = menu_bar.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Create the toolbar"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))  # Larger icons
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)  # Text under icon
        self.addToolBar(toolbar)

        # Add new project button with icon
        new_button = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon), "New", self)
        new_button.setStatusTip("Create a new project")
        new_button.triggered.connect(self.new_project)
        toolbar.addAction(new_button)

        # Add open project button with icon
        open_button = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton), "Open", self)
        open_button.setStatusTip("Open an existing project")
        open_button.triggered.connect(self.open_project)
        toolbar.addAction(open_button)

        # Add save project button with icon
        save_button = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton), "Save", self)
        save_button.setStatusTip("Save the current project")
        save_button.triggered.connect(self.save_project)
        toolbar.addAction(save_button)

        toolbar.addSeparator()

        # Add media import button with icon
        import_media_button = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_ToolBarHorizontalExtensionButton), "Import Media", self)
        import_media_button.setStatusTip("Import images or videos")
        import_media_button.triggered.connect(self.import_media)
        toolbar.addAction(import_media_button)

        # Add pricing button with icon (using $ symbol)
        pricing_icon = self._create_text_icon("$", QColor("#2196f3"))
        pricing_button = QAction(pricing_icon, "Pricing", self)
        pricing_button.setStatusTip("Set hourly rate and pricing options")
        pricing_button.triggered.connect(self.open_pricing_dialog)
        toolbar.addAction(pricing_button)

        # Add API toggle button with icon
        api_icon = self._create_text_icon("AI", QColor("#9c27b0"))
        self.api_toggle_button = QAction(api_icon, "Toggle API", self)
        self.api_toggle_button.setStatusTip("Switch between Claude and Google Vision APIs")
        self.api_toggle_button.triggered.connect(self.toggle_api)
        toolbar.addAction(self.api_toggle_button)

        # Add separator
        toolbar.addSeparator()

        # Add theme toggle button with icon
        theme_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DesktopIcon)
        self.theme_toggle_button = QAction(theme_icon, "Theme", self)
        self.theme_toggle_button.setStatusTip("Toggle between light and dark themes")
        self.theme_toggle_button.triggered.connect(self.toggle_theme)
        toolbar.addAction(self.theme_toggle_button)
    
    def create_new_project_tab(self, name):
        """Create a new project tab"""
        project_tab = ProjectTab(self)
        self.tab_widget.addTab(project_tab, name)
        self.tab_widget.setCurrentWidget(project_tab)
    
    def new_project(self):
        """Create a new project"""
        self.create_new_project_tab("New Project")
        self.statusBar.showMessage("New project created")
    
    def open_project(self):
        """Open an existing project"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "", "Electrical Estimator Projects (*.eep);;All Files (*)"
        )
        
        if file_path:
            # Use project controller to load the project
            project_data = self.project_controller.load_project(file_path)
            if project_data:
                self.create_new_project_tab(project_data.get("name", "Loaded Project"))
                self.statusBar.showMessage(f"Project loaded: {file_path}")
            else:
                QMessageBox.critical(self, "Error", f"Failed to load project: {file_path}")
    
    def save_project(self):
        """Save the current project"""
        current_tab = self.tab_widget.currentWidget()
        if not current_tab:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Project", "", "Electrical Estimator Projects (*.eep);;All Files (*)"
        )
        
        if file_path:
            # Get project data from the current tab
            project_data = current_tab.get_project_data()
            
            # Use project controller to save the project
            if self.project_controller.save_project(file_path, project_data):
                self.tab_widget.setTabText(self.tab_widget.currentIndex(), project_data.get("name", "Saved Project"))
                self.statusBar.showMessage(f"Project saved: {file_path}")
            else:
                QMessageBox.critical(self, "Error", f"Failed to save project: {file_path}")
    
    def close_tab(self, index):
        """Close a tab"""
        # Ask for confirmation before closing
        reply = QMessageBox.question(
            self, "Close Project", 
            "Are you sure you want to close this project? Unsaved changes will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.tab_widget.removeTab(index)
            
            # Create a new default tab if no tabs are left
            if self.tab_widget.count() == 0:
                self.create_new_project_tab("New Project")
    
    def import_media(self):
        """Import media (images/videos) into the current project with multiple file selection"""
        current_tab = self.tab_widget.currentWidget()
        if not current_tab:
            return

        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Import Media (Multiple Files Supported)", "",
            "Media Files (*.png *.jpg *.jpeg *.bmp *.mp4 *.avi *.mov);;All Files (*)"
        )

        if file_paths:
            # Import all selected files
            for file_path in file_paths:
                current_tab.import_media(file_path)

            # Update status bar with summary
            if len(file_paths) == 1:
                self.statusBar.showMessage(f"Media imported: {file_paths[0]}")
            else:
                self.statusBar.showMessage(f"Imported {len(file_paths)} media files")
                print(f"Imported {len(file_paths)} media files to current project")
    
    def show_about(self):
        """Show the about dialog"""
        QMessageBox.about(
            self, "About Electrical Estimator",
            "Electrical Estimator\nVersion 0.1\n\nA PyQt6 application for electrical estimations."
        )

    def open_pricing_dialog(self):
        """Open the pricing settings dialog"""
        current_tab = self.tab_widget.currentWidget()
        if not current_tab:
            return

        # Get current pricing data if it exists
        project_data = current_tab.get_project_data()
        pricing_data = project_data.get("pricing_data", {
            "hourly_rate": 75.00,
            "increment": 15
        })

        # Open pricing dialog
        pricing_dialog = PricingWidget(self, pricing_data)
        result = pricing_dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            # Get updated pricing data
            updated_pricing_data = pricing_dialog.get_pricing_data()

            # Update project data
            project_data["pricing_data"] = updated_pricing_data
            current_tab.set_pricing_data(updated_pricing_data)

            self.statusBar.showMessage(f"Pricing updated: ${updated_pricing_data['hourly_rate']}/hour with {updated_pricing_data['increment']}-minute increments")

    def toggle_api(self):
        """Toggle between Claude API and Google Vision API"""
        current_tab = self.tab_widget.currentWidget()
        if not current_tab or not hasattr(current_tab, "toggle_api"):
            return

        # Call the toggle_api method on the current tab
        is_using_vision = current_tab.toggle_api()

        # Update status bar
        api_name = "Google Vision API" if is_using_vision else "Claude API"
        self.statusBar.showMessage(f"Using {api_name} for image analysis")

    def apply_theme(self):
        """Apply the current theme (dark or light) to the application"""
        if self.dark_mode:
            self.setStyleSheet(get_dark_theme())
        else:
            self.setStyleSheet(get_light_theme())

    def toggle_theme(self):
        """Toggle between dark and light themes"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()

        # Update status bar
        theme_name = "Dark" if self.dark_mode else "Light"
        self.statusBar.showMessage(f"Switched to {theme_name} theme")

    def _create_text_icon(self, text, color, size=24):
        """Create an icon with text in it"""
        # Create a pixmap
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        # Set up painter
        from PyQt6.QtGui import QPainter, QFont, QPen
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw colored circle background
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(color)
        painter.drawEllipse(0, 0, size, size)

        # Draw text
        painter.setPen(QPen(Qt.GlobalColor.white))
        font = QFont("Arial", size // 2)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, text)

        painter.end()

        return QIcon(pixmap)