"""
Modern stylesheet for the Electrical Estimator application
"""

def get_dark_theme():
    """
    Returns a dark theme stylesheet for the application
    """
    return """
    /* Global application style */
    QMainWindow, QDialog {
        background-color: #2d2d2d;
        color: #e0e0e0;
    }
    
    QWidget {
        color: #e0e0e0;
        background-color: #2d2d2d;
    }
    
    /* Toolbar and menu */
    QToolBar {
        background-color: #3a3a3a;
        border-bottom: 1px solid #505050;
        spacing: 8px;
        padding: 4px;
    }
    
    QToolBar QToolButton {
        background-color: #3a3a3a;
        color: #e0e0e0;
        border: none;
        border-radius: 4px;
        padding: 4px;
    }
    
    QToolBar QToolButton:hover {
        background-color: #505050;
    }
    
    QToolBar QToolButton:pressed {
        background-color: #1e88e5;
    }
    
    QMenuBar {
        background-color: #3a3a3a;
        color: #e0e0e0;
    }
    
    QMenuBar::item:selected {
        background-color: #505050;
    }
    
    QMenu {
        background-color: #3a3a3a;
        border: 1px solid #505050;
    }
    
    QMenu::item {
        padding: 5px 18px 5px 15px;
    }
    
    QMenu::item:selected {
        background-color: #505050;
        color: #ffffff;
    }
    
    /* Tabs */
    QTabWidget::pane {
        border: 1px solid #505050;
        top: -1px;
    }
    
    QTabBar::tab {
        background-color: #3a3a3a;
        color: #e0e0e0;
        padding: 6px 12px;
        border: 1px solid #505050;
        border-bottom: none;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
    
    QTabBar::tab:selected {
        background-color: #2d2d2d;
        border-bottom: none;
    }
    
    QTabBar::tab:!selected {
        margin-top: 2px;
    }
    
    /* Buttons */
    QPushButton {
        background-color: #1e88e5;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 6px 16px;
        font-weight: bold;
        transition: background-color 0.2s;
    }

    QPushButton:hover {
        background-color: #42a5f5;
        border-color: #64b5f6;
    }

    QPushButton:pressed {
        background-color: #0d47a1;
        padding: 7px 15px 5px 17px; /* Slight shift effect */
    }

    QPushButton:focus {
        outline: none;
        border: 1px solid #bbdefb;
    }
    
    QPushButton:disabled {
        background-color: #505050;
        color: #9e9e9e;
    }
    
    /* Input fields */
    QLineEdit, QTextEdit, QPlainTextEdit {
        background-color: #3a3a3a;
        color: #e0e0e0;
        border: 1px solid #505050;
        border-radius: 4px;
        padding: 5px;
        selection-background-color: #1e88e5;
    }
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 1px solid #1e88e5;
    }
    
    /* Table */
    QTableWidget {
        gridline-color: #505050;
        background-color: #2d2d2d;
        border: 1px solid #505050;
        border-radius: 4px;
    }
    
    QTableWidget::item {
        padding: 5px;
    }
    
    QTableWidget::item:selected {
        background-color: #1e88e5;
        color: white;
    }
    
    QHeaderView::section {
        background-color: #3a3a3a;
        color: #e0e0e0;
        padding: 5px;
        border: 1px solid #505050;
    }
    
    /* Scrollbars */
    QScrollBar:vertical {
        border: none;
        background-color: #3a3a3a;
        width: 10px;
        margin: 16px 0 16px 0;
    }
    
    QScrollBar::handle:vertical {
        background-color: #606060;
        border-radius: 5px;
        min-height: 30px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #808080;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
        height: 0px;
    }
    
    QScrollBar:horizontal {
        border: none;
        background-color: #3a3a3a;
        height: 10px;
        margin: 0 16px 0 16px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #606060;
        border-radius: 5px;
        min-width: 30px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #808080;
    }
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        border: none;
        background: none;
        width: 0px;
    }
    
    /* Splitter */
    QSplitter::handle {
        background-color: #505050;
    }
    
    QSplitter::handle:horizontal {
        width: 2px;
    }
    
    QSplitter::handle:vertical {
        height: 2px;
    }
    
    /* Other elements */
    QLabel {
        color: #e0e0e0;
    }
    
    QStatusBar {
        background-color: #3a3a3a;
        color: #e0e0e0;
    }
    
    QSpinBox, QDoubleSpinBox, QComboBox {
        background-color: #3a3a3a;
        color: #e0e0e0;
        border: 1px solid #505050;
        border-radius: 4px;
        padding: 4px;
    }
    
    QSpinBox::up-button, QDoubleSpinBox::up-button {
        subcontrol-origin: border;
        subcontrol-position: top right;
        width: 16px;
        border-left: 1px solid #505050;
        border-bottom: 1px solid #505050;
    }
    
    QSpinBox::down-button, QDoubleSpinBox::down-button {
        subcontrol-origin: border;
        subcontrol-position: bottom right;
        width: 16px;
        border-left: 1px solid #505050;
        border-top: 1px solid #505050;
    }
    
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 15px;
        border-left: none;
    }
    
    /* Media viewer */
    QScrollArea {
        border: 1px solid #505050;
        border-radius: 4px;
    }
    
    /* Message frames in chat */
    QFrame[frameShape="6"] {  /* StyledPanel */
        border: 1px solid #505050;
        border-radius: 8px;
        padding: 8px;
    }
    """

def get_light_theme():
    """
    Returns a light theme stylesheet for the application
    """
    return """
    /* Global application style */
    QMainWindow, QDialog {
        background-color: #fafafa;
        color: #212121;
    }
    
    QWidget {
        color: #212121;
        background-color: #fafafa;
    }
    
    /* Toolbar and menu */
    QToolBar {
        background-color: #f0f0f0;
        border-bottom: 1px solid #e0e0e0;
        spacing: 8px;
        padding: 4px;
    }
    
    QToolBar QToolButton {
        background-color: #f0f0f0;
        color: #212121;
        border: none;
        border-radius: 4px;
        padding: 4px;
    }
    
    QToolBar QToolButton:hover {
        background-color: #e0e0e0;
    }
    
    QToolBar QToolButton:pressed {
        background-color: #2196f3;
        color: white;
    }
    
    QMenuBar {
        background-color: #f0f0f0;
        color: #212121;
    }
    
    QMenuBar::item:selected {
        background-color: #e0e0e0;
    }
    
    QMenu {
        background-color: #fafafa;
        border: 1px solid #e0e0e0;
    }
    
    QMenu::item {
        padding: 5px 18px 5px 15px;
    }
    
    QMenu::item:selected {
        background-color: #e0e0e0;
        color: #212121;
    }
    
    /* Tabs */
    QTabWidget::pane {
        border: 1px solid #e0e0e0;
        top: -1px;
    }
    
    QTabBar::tab {
        background-color: #f0f0f0;
        color: #212121;
        padding: 6px 12px;
        border: 1px solid #e0e0e0;
        border-bottom: none;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
    
    QTabBar::tab:selected {
        background-color: #fafafa;
        border-bottom: none;
    }
    
    QTabBar::tab:!selected {
        margin-top: 2px;
    }
    
    /* Buttons */
    QPushButton {
        background-color: #2196f3;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 6px 16px;
        font-weight: bold;
        transition: background-color 0.2s;
    }

    QPushButton:hover {
        background-color: #42a5f5;
        border-color: #64b5f6;
    }

    QPushButton:pressed {
        background-color: #1976d2;
        padding: 7px 15px 5px 17px; /* Slight shift effect */
    }

    QPushButton:focus {
        outline: none;
        border: 1px solid #bbdefb;
    }
    
    QPushButton:disabled {
        background-color: #e0e0e0;
        color: #9e9e9e;
    }
    
    /* Input fields */
    QLineEdit, QTextEdit, QPlainTextEdit {
        background-color: white;
        color: #212121;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 5px;
        selection-background-color: #2196f3;
    }
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 1px solid #2196f3;
    }
    
    /* Table */
    QTableWidget {
        gridline-color: #e0e0e0;
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
    }
    
    QTableWidget::item {
        padding: 5px;
    }
    
    QTableWidget::item:selected {
        background-color: #2196f3;
        color: white;
    }
    
    QHeaderView::section {
        background-color: #f0f0f0;
        color: #212121;
        padding: 5px;
        border: 1px solid #e0e0e0;
    }
    
    /* Scrollbars */
    QScrollBar:vertical {
        border: none;
        background-color: #f0f0f0;
        width: 10px;
        margin: 16px 0 16px 0;
    }
    
    QScrollBar::handle:vertical {
        background-color: #bdbdbd;
        border-radius: 5px;
        min-height: 30px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #9e9e9e;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
        height: 0px;
    }
    
    QScrollBar:horizontal {
        border: none;
        background-color: #f0f0f0;
        height: 10px;
        margin: 0 16px 0 16px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #bdbdbd;
        border-radius: 5px;
        min-width: 30px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #9e9e9e;
    }
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        border: none;
        background: none;
        width: 0px;
    }
    
    /* Splitter */
    QSplitter::handle {
        background-color: #e0e0e0;
    }
    
    QSplitter::handle:horizontal {
        width: 2px;
    }
    
    QSplitter::handle:vertical {
        height: 2px;
    }
    
    /* Other elements */
    QLabel {
        color: #212121;
    }
    
    QStatusBar {
        background-color: #f0f0f0;
        color: #212121;
    }
    
    QSpinBox, QDoubleSpinBox, QComboBox {
        background-color: white;
        color: #212121;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 4px;
    }
    
    QSpinBox::up-button, QDoubleSpinBox::up-button {
        subcontrol-origin: border;
        subcontrol-position: top right;
        width: 16px;
        border-left: 1px solid #e0e0e0;
        border-bottom: 1px solid #e0e0e0;
    }
    
    QSpinBox::down-button, QDoubleSpinBox::down-button {
        subcontrol-origin: border;
        subcontrol-position: bottom right;
        width: 16px;
        border-left: 1px solid #e0e0e0;
        border-top: 1px solid #e0e0e0;
    }
    
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 15px;
        border-left: none;
    }
    
    /* Media viewer */
    QScrollArea {
        border: 1px solid #e0e0e0;
        border-radius: 4px;
    }
    
    /* Message frames in chat */
    QFrame[frameShape="6"] {  /* StyledPanel */
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 8px;
    }
    """