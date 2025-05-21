"""
Chat widget for interaction with the AI estimator
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QLineEdit,
                            QPushButton, QHBoxLayout, QLabel, QScrollArea,
                            QFrame, QStyle, QGraphicsOpacityEffect)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QPalette, QKeyEvent, QIcon


class MessageFrame(QFrame):
    """Frame for displaying a single chat message"""

    def __init__(self, text, role="assistant", parent=None):
        super().__init__(parent)

        self.role = role
        self.content = text

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        # Add more modern styling based on role
        if role == "user":
            # User message style - aligned right
            self.setStyleSheet("""
                QFrame {
                    background-color: #e3f2fd;
                    border: none;
                    border-radius: 12px;
                    margin-left: 50px;
                    margin-right: 10px;
                }
            """)
        elif role == "thinking":
            # Thinking message style
            self.setStyleSheet("""
                QFrame {
                    background-color: #fff8e1;
                    border: none;
                    border-radius: 12px;
                    margin-left: 10px;
                    margin-right: 10px;
                }
            """)
        else:
            # Assistant message style - aligned left
            self.setStyleSheet("""
                QFrame {
                    background-color: #f5f5f5;
                    border: none;
                    border-radius: 12px;
                    margin-left: 10px;
                    margin-right: 50px;
                }
            """)

        # Create layout with better padding
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)

        # Add sender label with better styling
        sender_label = QLabel(self.get_sender_label())
        sender_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(sender_label)

        # Add message text with better styling
        self.message_text = QLabel(text)
        self.message_text.setWordWrap(True)
        self.message_text.setStyleSheet("font-size: 13px; line-height: 1.4;")
        self.message_text.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(self.message_text)

        # Add timestamp if not a thinking message
        if role != "thinking":
            from datetime import datetime
            timestamp = QLabel(datetime.now().strftime("%H:%M"))
            timestamp.setStyleSheet("color: #757575; font-size: 10px;")
            timestamp.setAlignment(Qt.AlignmentFlag.AlignRight)
            layout.addWidget(timestamp)

        # Set minimum width
        self.setMinimumWidth(250)
    
    def get_sender_label(self):
        """Get the sender label based on role"""
        if self.role == "user":
            return "You"
        elif self.role == "thinking":
            return "Assistant (thinking)"
        else:
            return "Assistant"


class ChatWidget(QWidget):
    """Widget for chat interaction with the AI estimator"""

    # Signal emitted when the user sends a message
    message_sent = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.chat_history = []  # List to store chat history
        self.message_frames = []  # List to store message frames
        self.thinking_timer = None  # Timer for thinking animation
        self.thinking_dots = 0  # Counter for thinking animation
        self.thinking_frame = None  # Reference to the thinking message frame
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout with better spacing and margins
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Title with better styling
        title_label = QLabel("AI Estimator Chat")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(title_label)

        # Scroll area for chat messages with improved styling
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(250)  # Increased height
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)  # Remove frame for cleaner look

        # Chat content widget with improved spacing
        self.chat_content = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(12)  # Increased spacing between messages
        self.chat_layout.setContentsMargins(5, 5, 5, 5)  # Add some padding

        self.scroll_area.setWidget(self.chat_content)
        layout.addWidget(self.scroll_area)

        # Message count indicator
        self.message_count = QLabel("0 messages")
        self.message_count.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.message_count.setStyleSheet("color: #808080; font-size: 11px; margin-top: 5px;")
        layout.addWidget(self.message_count)

        # Input area with improved styling
        input_section = QWidget()
        input_section.setStyleSheet("background-color: rgba(0, 0, 0, 0.02); border-radius: 8px; padding: 5px;")
        input_layout = QHBoxLayout(input_section)
        input_layout.setContentsMargins(8, 8, 8, 8)
        input_layout.setSpacing(10)

        # Message input with better styling
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Type your message here... (Press Ctrl+Enter to send)")
        self.message_input.setMinimumHeight(70)  # Make it bigger vertically
        self.message_input.setMaximumHeight(100)  # But not too big
        self.message_input.setStyleSheet("border-radius: 4px; padding: 8px;")

        # Setup keyboard shortcut for Ctrl+Enter to send message
        self.message_input.keyPressEvent = self.handle_input_key_press

        input_layout.addWidget(self.message_input)

        # Send button with better styling and icon
        send_button = QPushButton("Send")
        send_button.setMinimumWidth(80)
        send_button.setMinimumHeight(40)
        send_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_CommandLink))
        send_button.setIconSize(QSize(20, 20))
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                border-radius: 4px;
                padding: 4px 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #42a5f5;
            }
            QPushButton:pressed {
                background-color: #1976d2;
            }
        """)
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)

        layout.addWidget(input_section)
        
        # Initialize with a welcome message
        self.add_assistant_message("Welcome to the Electrical Estimator. Upload media files and ask questions about the electrical work you need.")
        
    def send_message(self):
        """Handle sending a message"""
        # Make sure QTimer is available
        from PyQt6.QtCore import QTimer

        message = self.message_input.toPlainText().strip()
        if not message:
            # Visual feedback for empty message with animation
            self.show_input_error("Please enter a message")
            return

        # Add visual feedback for sending (subtle flash)
        self.add_send_animation()

        # Add user message to chat
        self.add_user_message(message)

        # Clear input field
        self.message_input.clear()

        # Reset style
        self._reset_input_style()

        # Set focus back to input
        self.message_input.setFocus()

        # Show thinking animation
        self.start_thinking_animation()

        # Emit signal with message
        self.message_sent.emit(message)

    def _reset_input_style(self):
        """Reset the input field style"""
        self.message_input.setStyleSheet("border-radius: 4px; padding: 8px;")

    def show_input_error(self, message):
        """Show error animation and tooltip for input field"""
        # Make sure QTimer is available
        from PyQt6.QtCore import QTimer

        # Visual feedback with red border
        self.message_input.setStyleSheet("border: 2px solid #f44336; background-color: rgba(244, 67, 54, 0.05); border-radius: 4px; padding: 8px;")

        # Shake animation for error
        self.shake_widget(self.message_input)

        # Show tooltip with error message
        self.message_input.setToolTip(message)

        # Reset style after delay
        QTimer.singleShot(1500, self._reset_input_style)

    def add_send_animation(self):
        """Add a subtle flash animation when sending a message"""
        # Make sure QTimer is available
        from PyQt6.QtCore import QTimer

        # Store original style
        original_style = self.message_input.styleSheet()

        # Set flash style (light blue highlight)
        self.message_input.setStyleSheet("border: 1px solid #2196f3; background-color: rgba(33, 150, 243, 0.1); border-radius: 4px; padding: 8px;")

        # Reset after very short delay
        QTimer.singleShot(200, lambda: self.message_input.setStyleSheet(original_style))

    def shake_widget(self, widget, duration=500, amplitude=5, steps=5):
        """Add a shake animation to indicate error"""
        # Make sure QTimer is available
        from PyQt6.QtCore import QTimer
        # Starting position
        start_pos = widget.pos()

        # Setup timer for shake steps
        shake_steps = 0
        shake_direction = 1
        shake_timer = QTimer(self)

        def shake_step():
            nonlocal shake_steps, shake_direction
            if shake_steps >= steps * 2:
                shake_timer.stop()
                widget.move(start_pos)  # Reset to original position
                return

            # Calculate offset and convert to integer
            offset = int(amplitude * shake_direction * (steps - shake_steps//2) / steps)

            # Move widget with integer coordinates
            widget.move(start_pos.x() + offset, start_pos.y())

            # Update for next step
            shake_direction *= -1
            shake_steps += 1

        # Connect and start timer
        shake_timer.timeout.connect(shake_step)
        shake_timer.start(duration // (steps * 2))
        
    def add_user_message(self, message):
        """Add a user message to the chat with animation"""
        self.chat_history.append({"role": "user", "content": message})

        # Create message frame with animation
        message_frame = MessageFrame(message, role="user")

        # Add fade-in animation
        opacity_effect = QGraphicsOpacityEffect(message_frame)
        message_frame.setGraphicsEffect(opacity_effect)

        # Add to layout
        self.chat_layout.addWidget(message_frame)
        self.message_frames.append(message_frame)

        # Start animation with slide-in effect
        self.fade_in_widget(message_frame, 200)  # Faster animation for user messages

        # Update message count
        self._update_message_count()

        # Scroll to bottom
        self.scroll_to_bottom()

    def add_assistant_message(self, message):
        """Add an assistant message to the chat"""
        # If there's a thinking animation active, stop it and remove the message
        if self.thinking_timer and self.thinking_timer.isActive():
            self.stop_thinking_animation()

        # Check if this is a thinking message
        role = "thinking" if message == "Thinking..." else "assistant"

        # If this is a thinking message, start animation instead of normal display
        if role == "thinking":
            self.start_thinking_animation()
            return

        self.chat_history.append({"role": "assistant", "content": message})

        # Create and add message frame with animation
        message_frame = MessageFrame(message, role="assistant")

        # Add fade-in animation
        opacity_effect = QGraphicsOpacityEffect(message_frame)
        message_frame.setGraphicsEffect(opacity_effect)

        # Add to layout
        self.chat_layout.addWidget(message_frame)
        self.message_frames.append(message_frame)

        # Start animation
        self.fade_in_widget(message_frame)

        # Update message count
        self._update_message_count()

        # Scroll to bottom
        self.scroll_to_bottom()

    def _update_message_count(self):
        """Update the message counter"""
        # Don't count thinking messages
        count = sum(1 for msg in self.chat_history if msg["role"] != "thinking")
        self.message_count.setText(f"{count} messages")
        
    def remove_last_message(self):
        """Remove the last message from the chat"""
        if self.message_frames:
            # Get the last frame
            last_frame = self.message_frames.pop()
            
            # Remove from layout and delete
            self.chat_layout.removeWidget(last_frame)
            last_frame.deleteLater()
            
            # Remove from history
            if self.chat_history:
                self.chat_history.pop()
    
    def scroll_to_bottom(self):
        """Scroll to the bottom of the chat"""
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )
        
    def handle_input_key_press(self, event):
        """Handle key press events in the message input"""
        # Check for Ctrl+Enter
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Return:
            self.send_message()
        else:
            # Call the parent class implementation for other key presses
            QTextEdit.keyPressEvent(self.message_input, event)

    def get_chat_history(self):
        """Get the current chat history"""
        return self.chat_history

    def start_thinking_animation(self):
        """Start the thinking animation with dots"""
        # Make sure QTimer is available
        from PyQt6.QtCore import QTimer
        # Create the thinking message if it doesn't exist
        if not self.thinking_frame:
            self.thinking_frame = MessageFrame("Thinking...", role="thinking")
            self.chat_layout.addWidget(self.thinking_frame)

            # Add fade-in animation
            opacity_effect = QGraphicsOpacityEffect(self.thinking_frame)
            self.thinking_frame.setGraphicsEffect(opacity_effect)
            self.fade_in_widget(self.thinking_frame)

            # Scroll to bottom to show the message
            self.scroll_to_bottom()

        # Start the timer for dot animation
        self.thinking_dots = 0
        if not self.thinking_timer:
            self.thinking_timer = QTimer(self)
            self.thinking_timer.timeout.connect(self.update_thinking_animation)
        self.thinking_timer.start(500)  # Update every 500ms

    def update_thinking_animation(self):
        """Update the thinking animation dots"""
        if self.thinking_frame:
            # Update dots (cycle between 1-3 dots)
            self.thinking_dots = (self.thinking_dots + 1) % 4
            dots = "." * self.thinking_dots if self.thinking_dots > 0 else "..."

            # Update the message text
            self.thinking_frame.message_text.setText(f"Thinking{dots}")

    def stop_thinking_animation(self):
        """Stop the thinking animation and remove the message"""
        if self.thinking_timer:
            self.thinking_timer.stop()

        if self.thinking_frame:
            # Remove from layout with fade-out
            self.fade_out_widget(self.thinking_frame, self._remove_thinking_frame)

    def _remove_thinking_frame(self):
        """Remove the thinking frame after animation"""
        if self.thinking_frame:
            self.chat_layout.removeWidget(self.thinking_frame)
            self.thinking_frame.deleteLater()
            self.thinking_frame = None

    def fade_in_widget(self, widget, duration=300):
        """Add fade-in animation to widget"""
        # Make sure QPropertyAnimation is available
        from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
        if hasattr(widget, 'graphicsEffect') and widget.graphicsEffect():
            effect = widget.graphicsEffect()
            # Start completely transparent
            effect.setOpacity(0)

            # Create animation
            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(duration)
            animation.setStartValue(0)
            animation.setEndValue(1)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    def fade_out_widget(self, widget, callback=None, duration=300):
        """Add fade-out animation to widget"""
        # Make sure QPropertyAnimation is available
        from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
        if hasattr(widget, 'graphicsEffect') and widget.graphicsEffect():
            effect = widget.graphicsEffect()

            # Create animation
            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(duration)
            animation.setStartValue(1)
            animation.setEndValue(0)
            animation.setEasingCurve(QEasingCurve.Type.InCubic)

            # Connect finished signal if callback provided
            if callback:
                animation.finished.connect(callback)

            animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)