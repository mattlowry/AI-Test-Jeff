"""
Estimation widget for displaying and managing electrical estimates
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget,
                            QPushButton, QHeaderView, QHBoxLayout, QTableWidgetItem,
                            QDialog, QFormLayout, QLineEdit, QDoubleSpinBox,
                            QSpinBox, QComboBox, QMessageBox, QTextEdit)
from PyQt6.QtCore import Qt


class EstimationWidget(QWidget):
    """Widget for managing electrical estimates"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.estimation_data = {
            "items": [],
            "total": 0.0,
            "notes": "",
            "scope_of_work": "",
            "labor_hours": 1.0,
            "labor_cost": 75.00
        }
        self.pricing_data = {
            "hourly_rate": 75.00,
            "increment": 15
        }
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Estimation Details")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Scope of Work section
        scope_label = QLabel("Scope of Work:")
        scope_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(scope_label)

        self.scope_edit = QTextEdit()
        self.scope_edit.setPlaceholderText("Enter the scope of work for this estimation...")
        self.scope_edit.setMinimumHeight(80)
        layout.addWidget(self.scope_edit)

        # Labor Hours section
        labor_layout = QHBoxLayout()

        labor_label = QLabel("Labor Hours:")
        labor_label.setStyleSheet("font-weight: bold;")
        labor_layout.addWidget(labor_label)

        self.labor_hours = QDoubleSpinBox()
        self.labor_hours.setRange(0.25, 1000.00)
        self.labor_hours.setSingleStep(0.25)  # 15-minute increments
        self.labor_hours.setValue(1.0)
        self.labor_hours.valueChanged.connect(self.update_labor_cost)
        labor_layout.addWidget(self.labor_hours)

        self.labor_cost_label = QLabel("Cost: $75.00")
        self.labor_cost_label.setStyleSheet("font-weight: bold;")
        labor_layout.addWidget(self.labor_cost_label)

        labor_layout.addStretch()
        layout.addLayout(labor_layout)

        # Estimation table
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Item", "Quantity", "Unit", "Unit Price", "Total"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.table)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Add item button
        add_button = QPushButton("Add Item")
        add_button.clicked.connect(self.add_item)
        button_layout.addWidget(add_button)
        
        # Edit item button
        edit_button = QPushButton("Edit Item")
        edit_button.clicked.connect(self.edit_item)
        button_layout.addWidget(edit_button)
        
        # Remove item button
        remove_button = QPushButton("Remove Item")
        remove_button.clicked.connect(self.remove_item)
        button_layout.addWidget(remove_button)
        
        # Clear all button
        clear_button = QPushButton("Clear All")
        clear_button.clicked.connect(self.clear_all_items)
        button_layout.addWidget(clear_button)
        
        layout.addLayout(button_layout)
        
        # Total layout
        total_layout = QHBoxLayout()
        
        # Spacer
        total_layout.addStretch()
        
        # Total label
        self.total_label = QLabel("Total: $0.00")
        self.total_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        total_layout.addWidget(self.total_label)
        
        layout.addLayout(total_layout)
        
        # Notes
        notes_label = QLabel("Notes:")
        layout.addWidget(notes_label)
        
        self.notes_edit = QLineEdit()
        self.notes_edit.setPlaceholderText("Enter notes about this estimate...")
        layout.addWidget(self.notes_edit)
        
    def add_item_to_table(self, item_data):
        """Add an item to the table"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # Set item values
        self.table.setItem(row, 0, QTableWidgetItem(item_data["item"]))
        self.table.setItem(row, 1, QTableWidgetItem(str(item_data["quantity"])))
        self.table.setItem(row, 2, QTableWidgetItem(item_data["unit"]))
        self.table.setItem(row, 3, QTableWidgetItem(f"${item_data['unit_price']:.2f}"))
        
        # Calculate total
        total = item_data["quantity"] * item_data["unit_price"]
        self.table.setItem(row, 4, QTableWidgetItem(f"${total:.2f}"))
            
    def add_item(self):
        """Open dialog to add a new item"""
        dialog = ItemDialog(self)
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            item_data = dialog.get_item_data()
            self.add_item_to_table(item_data)
            self.estimation_data["items"].append(item_data)
            self.update_total()
            
    def add_item_from_ai(self, item_data):
        """Add an item from AI response"""
        # Check if a similar item already exists
        for existing_item in self.estimation_data["items"]:
            if (existing_item["item"].lower() == item_data["item"].lower() and 
                existing_item["unit"] == item_data["unit"]):
                
                # Ask the user if they want to update the existing item
                reply = QMessageBox.question(
                    self, 
                    "Similar Item Found", 
                    f"A similar item '{existing_item['item']}' already exists. Update it with the new quantity and price?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    # Find the index of the existing item
                    index = self.estimation_data["items"].index(existing_item)
                    
                    # Update the item
                    self.estimation_data["items"][index] = item_data
                    
                    # Update the table
                    self.table.setItem(index, 0, QTableWidgetItem(item_data["item"]))
                    self.table.setItem(index, 1, QTableWidgetItem(str(item_data["quantity"])))
                    self.table.setItem(index, 2, QTableWidgetItem(item_data["unit"]))
                    self.table.setItem(index, 3, QTableWidgetItem(f"${item_data['unit_price']:.2f}"))
                    
                    # Calculate total
                    total = item_data["quantity"] * item_data["unit_price"]
                    self.table.setItem(index, 4, QTableWidgetItem(f"${total:.2f}"))
                    
                    # Update total
                    self.update_total()
                    return
        
        # No similar item or user chose not to update, add as new
        self.add_item_to_table(item_data)
        self.estimation_data["items"].append(item_data)
        self.update_total()
            
    def edit_item(self):
        """Edit the selected item"""
        current_row = self.table.currentRow()
        if current_row < 0:
            return
            
        # Get current item data
        current_item = self.estimation_data["items"][current_row]
        
        # Open dialog with current values
        dialog = ItemDialog(self, current_item)
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            # Get updated item data
            item_data = dialog.get_item_data()
            
            # Update table
            self.table.setItem(current_row, 0, QTableWidgetItem(item_data["item"]))
            self.table.setItem(current_row, 1, QTableWidgetItem(str(item_data["quantity"])))
            self.table.setItem(current_row, 2, QTableWidgetItem(item_data["unit"]))
            self.table.setItem(current_row, 3, QTableWidgetItem(f"${item_data['unit_price']:.2f}"))
            
            # Calculate total
            total = item_data["quantity"] * item_data["unit_price"]
            self.table.setItem(current_row, 4, QTableWidgetItem(f"${total:.2f}"))
            
            # Update estimation data
            self.estimation_data["items"][current_row] = item_data
            self.update_total()
            
    def remove_item(self):
        """Remove the selected item"""
        current_row = self.table.currentRow()
        if current_row < 0:
            return
            
        # Remove from table
        self.table.removeRow(current_row)
        
        # Remove from data
        self.estimation_data["items"].pop(current_row)
        self.update_total()
    
    def clear_all_items(self):
        """Clear all items from the estimate"""
        # Ask for confirmation
        reply = QMessageBox.question(
            self, 
            "Clear All Items", 
            "Are you sure you want to clear all items from the estimate?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Clear the table
            self.table.setRowCount(0)
            
            # Clear the data
            self.estimation_data["items"] = []
            self.update_total()
            
    def update_labor_cost(self):
        """Update the labor cost based on hours and hourly rate"""
        # Round to nearest increment (e.g., 15 minutes)
        increment_decimal = self.pricing_data["increment"] / 60.0  # Convert minutes to hours
        hours = round(self.labor_hours.value() / increment_decimal) * increment_decimal

        # Set the value back to ensure it's exactly on the increment
        self.labor_hours.setValue(hours)

        # Calculate labor cost
        labor_cost = hours * self.pricing_data["hourly_rate"]
        self.estimation_data["labor_hours"] = hours
        self.estimation_data["labor_cost"] = labor_cost

        # Update the display
        self.labor_cost_label.setText(f"Cost: ${labor_cost:.2f}")

        # Update the total
        self.update_total()

    def update_total(self):
        """Update the total estimate amount"""
        # Sum of items
        items_total = sum(item["quantity"] * item["unit_price"] for item in self.estimation_data["items"])

        # Add labor cost
        total = items_total + self.estimation_data["labor_cost"]

        self.total_label.setText(f"Total: ${total:.2f}")
        self.estimation_data["total"] = total
        
    def update_pricing(self, pricing_data):
        """Update the pricing settings"""
        self.pricing_data = pricing_data

        # Update labor cost based on new hourly rate
        self.update_labor_cost()

        # If any item has a unit of "hour", update its unit price
        for i, item in enumerate(self.estimation_data["items"]):
            if item["unit"] == "hour":
                item["unit_price"] = pricing_data["hourly_rate"]

                # Update the table display
                self.table.setItem(i, 3, QTableWidgetItem(f"${item['unit_price']:.2f}"))

                # Calculate and update total
                total = item["quantity"] * item["unit_price"]
                self.table.setItem(i, 4, QTableWidgetItem(f"${total:.2f}"))

        # Update the overall total
        self.update_total()

    def get_estimation_data(self):
        """Get the current estimation data"""
        self.estimation_data["notes"] = self.notes_edit.text()
        self.estimation_data["scope_of_work"] = self.scope_edit.toPlainText()
        return self.estimation_data


class ItemDialog(QDialog):
    """Dialog for adding or editing an estimation item"""
    
    def __init__(self, parent=None, item_data=None):
        super().__init__(parent)
        self.item_data = item_data
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        # Set dialog properties
        self.setWindowTitle("Estimation Item")
        self.setMinimumWidth(300)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Item input
        self.item_input = QLineEdit()
        form_layout.addRow("Item:", self.item_input)
        
        # Quantity input
        self.quantity_input = QDoubleSpinBox()  # Changed to QDoubleSpinBox to support fractional quantities
        self.quantity_input.setRange(0.01, 10000.00)
        self.quantity_input.setDecimals(2)
        form_layout.addRow("Quantity:", self.quantity_input)
        
        # Unit input
        self.unit_input = QComboBox()
        self.unit_input.addItems(["ea", "ft", "m", "sq ft", "sq m", "hour", "lot"])

        # Connect unit change to update price if "hour" is selected
        self.unit_input.currentTextChanged.connect(self.on_unit_changed)
        self.unit_input.setEditable(True)
        form_layout.addRow("Unit:", self.unit_input)
        
        # Unit price input
        self.unit_price_input = QDoubleSpinBox()
        self.unit_price_input.setRange(0.01, 100000.00)
        self.unit_price_input.setPrefix("$")
        self.unit_price_input.setDecimals(2)
        form_layout.addRow("Unit Price:", self.unit_price_input)
        
        layout.addLayout(form_layout)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        # OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        layout.addLayout(button_layout)
        
        # If editing an item, fill in existing values
        if self.item_data:
            self.item_input.setText(self.item_data["item"])
            self.quantity_input.setValue(self.item_data["quantity"])
            self.unit_input.setCurrentText(self.item_data["unit"])
            self.unit_price_input.setValue(self.item_data["unit_price"])
        
    def on_unit_changed(self, text):
        """Update the unit price based on the selected unit"""
        if text == "hour":
            # Get hourly rate from parent widget's pricing data
            parent = self.parent()
            if parent and hasattr(parent, "pricing_data"):
                hourly_rate = parent.pricing_data.get("hourly_rate", 75.00)
                self.unit_price_input.setValue(hourly_rate)

    def get_item_data(self):
        """Get the item data from the dialog"""
        return {
            "item": self.item_input.text(),
            "quantity": self.quantity_input.value(),
            "unit": self.unit_input.currentText(),
            "unit_price": self.unit_price_input.value()
        }