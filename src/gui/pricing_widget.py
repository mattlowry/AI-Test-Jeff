"""
Pricing widget for setting and managing hourly rates
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFormLayout, QDoubleSpinBox, 
                            QComboBox, QGroupBox)
from PyQt6.QtCore import Qt


class PricingWidget(QDialog):
    """Dialog for setting hourly rates for electrical estimation"""
    
    def __init__(self, parent=None, pricing_data=None):
        super().__init__(parent)
        self.pricing_data = pricing_data or {
            "hourly_rate": 75.00,
            "increment": 15  # minutes
        }
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        # Set dialog properties
        self.setWindowTitle("Pricing Settings")
        self.setMinimumWidth(350)
        self.setMinimumHeight(200)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Hourly rate group
        rate_group = QGroupBox("Hourly Rate Settings")
        rate_layout = QFormLayout()
        
        # Hourly rate input
        self.hourly_rate_input = QDoubleSpinBox()
        self.hourly_rate_input.setRange(0.00, 1000.00)
        self.hourly_rate_input.setPrefix("$")
        self.hourly_rate_input.setDecimals(2)
        self.hourly_rate_input.setValue(self.pricing_data["hourly_rate"])
        self.hourly_rate_input.setSingleStep(5.00)  # Step by $5
        rate_layout.addRow("Hourly Rate:", self.hourly_rate_input)
        
        # Time increment selector
        self.increment_selector = QComboBox()
        self.increment_selector.addItems(["15 minutes", "30 minutes", "60 minutes"])
        
        # Set current increment based on data
        current_increment = self.pricing_data["increment"]
        if current_increment == 15:
            self.increment_selector.setCurrentIndex(0)
        elif current_increment == 30:
            self.increment_selector.setCurrentIndex(1)
        else:
            self.increment_selector.setCurrentIndex(2)
            
        rate_layout.addRow("Time Increment:", self.increment_selector)
        
        rate_group.setLayout(rate_layout)
        layout.addWidget(rate_group)
        
        # Information label
        info_label = QLabel("Time will be rounded to the nearest increment when calculating costs.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(info_label)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        save_button.setDefault(True)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
        
    def get_pricing_data(self):
        """Get the pricing data from the dialog"""
        # Get increment in minutes from the selector
        increment_index = self.increment_selector.currentIndex()
        if increment_index == 0:
            increment = 15
        elif increment_index == 1:
            increment = 30
        else:
            increment = 60
            
        return {
            "hourly_rate": self.hourly_rate_input.value(),
            "increment": increment
        }