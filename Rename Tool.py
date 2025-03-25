import os
import re
from functools import lru_cache
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, 
    QFileDialog, QLineEdit, QMessageBox, QCheckBox, QHBoxLayout, 
    QFrame, QScrollArea, QProgressBar
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PyQt6.QtGui import QIcon, QFont

class RenameTool(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.rename_history = []
        self.last_directory = None
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("File Renaming Tool")
        self.setGeometry(100, 100, 800, 500)  # Increased window size for better layout
        
        # Add window icon
        self.setWindowIcon(QIcon("Rename Tool.ico"))
        
        self.setup_theme()
        
        # Main layout with better spacing
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Left panel (Input controls)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 2)
        
        # Right panel (File list and actions)
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 3)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #2d2d3f;
                border-radius: 5px;
                text-align: center;
                background-color: #1e1e2e;
            }
            QProgressBar::chunk {
                background-color: #007AFF;
                border-radius: 3px;
            }
        """)
        
        # Final layout assembly
        final_layout = QVBoxLayout(self)
        final_layout.addLayout(main_layout)
        final_layout.addWidget(self.progress_bar)
        self.setLayout(final_layout)
        
        self.animate_window()

    def setup_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #ffffff;
                border-radius: 10px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                background-color: transparent;
                padding: 2px;
            }
            QFrame {
                padding: 2px;
            }
            QScrollArea {
                padding: 1px;
            }
            QProgressBar {
                min-height: 20px;
                max-height: 20px;
            }
        """)
        
    def create_left_panel(self):
        panel = QFrame()
        panel.setStyleSheet("background-color: #2d2d3f; border-radius: 10px;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Digits input
        digits_group = self.create_input_group("Number Format", "Enter digits (e.g., 3)")
        self.digit_entry = digits_group.findChild(QLineEdit)
        self.digit_entry.textChanged.connect(self.validate_inputs)
        layout.addWidget(digits_group)
        
        # Prefix input
        prefix_group = self.create_input_group("Prefix", "Enter prefix (optional)")
        self.prefix_checkbox = prefix_group.findChild(QCheckBox)
        self.prefix_entry = prefix_group.findChild(QLineEdit)
        layout.addWidget(prefix_group)
        
        # Suffix input
        suffix_group = self.create_input_group("Suffix", "Enter suffix (optional)")
        self.suffix_checkbox = suffix_group.findChild(QCheckBox)
        self.suffix_entry = suffix_group.findChild(QLineEdit)
        layout.addWidget(suffix_group)
        
        layout.addStretch()
        return panel

    def create_right_panel(self):
        panel = QFrame()
        panel.setStyleSheet("background-color: #2d2d3f; border-radius: 10px;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Action buttons
        self.create_action_buttons(layout)
        
        # File list header
        file_header = QLabel("Selected Files:")
        file_header.setStyleSheet("font-weight: bold; font-size: 11pt; margin-top: 10px;")
        layout.addWidget(file_header)
        
        # File list
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar {
                background-color: #1e1e2e;
                width: 10px;
            }
            QScrollBar::handle {
                background-color: #3d3d4f;
                border-radius: 5px;
            }
        """)
        
        file_container = QWidget()
        file_container.setStyleSheet("background-color: #1e1e2e; border-radius: 5px;")
        file_layout = QVBoxLayout(file_container)
        
        self.file_list = QLabel("No files selected")
        self.file_list.setWordWrap(True)
        self.file_list.setStyleSheet("color: #888888; padding: 10px;")
        file_layout.addWidget(self.file_list)
        
        scroll_area.setWidget(file_container)
        layout.addWidget(scroll_area)
        
        return panel

    def create_input_group(self, title, placeholder):
        group = QFrame()
        group.setStyleSheet("""
            QFrame {
                background-color: #1e1e2e;
                border-radius: 8px;
                padding: 12px;
                margin: 2px;
            }
        """)
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Header with better spacing
        header = QHBoxLayout()
        header.setSpacing(10)
        
        label = QLabel(title)
        label.setStyleSheet("font-weight: bold; font-size: 10pt; padding: 2px;")
        
        if title != "Number Format":
            checkbox = QCheckBox("Enable")
            checkbox.setStyleSheet("""
                QCheckBox {
                    padding: 4px;
                    spacing: 8px;
                    color: #888888;
                }
                QCheckBox:checked {
                    color: #34c759;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                    border-radius: 4px;
                    background-color: #2d2d3f;
                    border: 2px solid #444444;
                }
                QCheckBox::indicator:checked {
                    background-color: #34c759;
                    border-color: #34c759;
                    image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>');
                }
                QCheckBox::indicator:hover {
                    border-color: #555555;
                    background-color: #3d3d4f;
                }
                QCheckBox::indicator:checked:hover {
                    background-color: #2ea94e;
                    border-color: #2ea94e;
                }
            """)
            
            header.addWidget(label)
            header.addStretch()
            header.addWidget(checkbox, 0, Qt.AlignmentFlag.AlignRight)
        else:
            header.addWidget(label)
            header.addStretch()
        
        layout.addLayout(header)
        
        # Input field with better styling
        entry = QLineEdit()
        entry.setPlaceholderText(placeholder)
        entry.setEnabled(title == "Number Format" or False)
        entry.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border-radius: 6px;
                background-color: #2d2d3f;
                border: 1px solid #3d3d4f;
                margin-top: 4px;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border: 2px solid #007AFF;
            }
            QLineEdit:disabled {
                background-color: #252535;
                color: #666666;
                border: 1px solid #333333;
            }
        """)
        layout.addWidget(entry)
        
        if title != "Number Format":
            checkbox.stateChanged.connect(lambda state: entry.setEnabled(state == Qt.CheckState.Checked.value))
            
        return group

    def create_action_buttons(self, layout):
        button_style = """
            QPushButton {
                background-color: #007AFF;
                color: white;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover { background-color: #0064D1; }
            QPushButton:pressed { background-color: #0056B3; }
            QPushButton:disabled { background-color: #2d2d3f; color: #666666; }
        """
        
        buttons_layout = QHBoxLayout()
        
        self.folder_button = QPushButton("📁 Select Folder")
        self.files_button = QPushButton("📄 Select Files")
        
        for btn in [self.folder_button, self.files_button]:
            btn.setStyleSheet(button_style)
            buttons_layout.addWidget(btn)
            
        layout.addLayout(buttons_layout)
        
        self.rename_button = QPushButton("✨ Process Rename")
        self.rename_button.setStyleSheet(button_style)
        self.rename_button.setEnabled(False)
        layout.addWidget(self.rename_button)
        
        self.undo_button = QPushButton("↩ Undo")
        self.undo_button.setStyleSheet(button_style.replace("#007AFF", "#FF3B30"))
        self.undo_button.setEnabled(False)
        layout.addWidget(self.undo_button)
        
        # Connect signals
        self.folder_button.clicked.connect(self.select_folder)
        self.files_button.clicked.connect(self.select_files)
        self.rename_button.clicked.connect(self.start_rename)
        self.undo_button.clicked.connect(self.undo_rename)

    def animate_window(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setStartValue(QRect(self.x(), self.y() - 20, self.width(), self.height()))
        self.animation.setEndValue(QRect(self.x(), self.y(), self.width(), self.height()))
        self.animation.start()

    @lru_cache(maxsize=128)
    def extract_number(self, filename):
        match = re.search(r'\d+', os.path.basename(filename))
        return int(match.group(0)) if match else 0

    def get_sorted_files(self, files):
        return sorted(
            [(f, self.extract_number(f), os.path.splitext(f)[1]) 
            for f in files if os.path.isfile(f)],
            key=lambda x: x[1]
        )

    def select_folder(self):
        if folder := QFileDialog.getExistingDirectory(self, "Select Folder"):
            self.selected_files = [entry.path for entry in os.scandir(folder) if entry.is_file()]
            self.last_directory = folder
            if self.selected_files:
                self.file_list.setText(f"📁 Folder: {folder}\n\nTotal files: {len(self.selected_files)}")
                self.file_list.setStyleSheet("color: #ffffff; font-size: 9pt;")
                self.validate_inputs()
            else:
                self.file_list.setText("⚠️ No files found in selected folder")
                self.file_list.setStyleSheet("color: #ff6b6b; font-size: 9pt;")
                self.selected_files = []
                self.validate_inputs()

    def select_files(self):
        start_dir = self.last_directory if self.last_directory else ""
        if files := QFileDialog.getOpenFileNames(self, "Select Files", start_dir)[0]:
            self.selected_files = files
            if files:
                self.last_directory = os.path.dirname(files[0])
            
            file_names = [os.path.basename(f) for f in files[:5]]
            display_text = f"📄 Selected {len(files)} files:\n\n" + "\n".join(file_names)
            if len(files) > 5:
                display_text += f"\n\n... and {len(files)-5} more files"
            self.file_list.setText(display_text)
            self.file_list.setStyleSheet("color: #ffffff; font-size: 9pt;")
            self.validate_inputs()

    def validate_inputs(self):
        is_valid = self.digit_entry.text().strip().isdigit()
        self.rename_button.setEnabled(is_valid and bool(self.selected_files))

    def start_rename(self):
        if not self.selected_files:
            QMessageBox.warning(self, "No Files", "Please select files first.")
            return
            
        if not (digit_format := self.digit_entry.text()).isdigit():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number of digits.")
            return

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Rename")
        msg_box.setText(f"Are you sure you want to rename {len(self.selected_files)} files?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes)
        
        if msg_box.exec() == QMessageBox.StandardButton.No:
            return
            
        self.process_rename(self.selected_files)

    def process_rename(self, files):
        digit_format = int(self.digit_entry.text().strip())
        files = self.get_sorted_files(files)
        
        if not files:
            QMessageBox.warning(self, "No Files", "No numbered files found.")
            return

        prefix = self.prefix_entry.text() if self.prefix_checkbox.isChecked() else ""
        suffix = self.suffix_entry.text() if self.suffix_checkbox.isChecked() else ""
        
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, len(files))
        self.progress_bar.setValue(0)
        
        # Clear previous history
        self.rename_history.clear()
        
        # Process files
        for idx, (old_path, _, ext) in enumerate(files, 1):
            new_name = f"{prefix}{str(idx).zfill(digit_format)}{suffix}{ext}"
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            try:
                os.rename(old_path, new_path)
                self.rename_history.append((new_path, old_path))
                self.progress_bar.setValue(idx)
                QApplication.processEvents()  # Update UI
            except OSError as e:
                QMessageBox.warning(self, "Error", f"Failed to rename {os.path.basename(old_path)}: {str(e)}")
                continue

        # Hide progress bar after completion
        QTimer.singleShot(1000, lambda: self.progress_bar.setVisible(False))
        
        # Show success message
        if self.rename_history:
            QMessageBox.information(self, "Success", f"Successfully renamed {len(self.rename_history)} files!")
            self.undo_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "No Changes", "No files were renamed.")

    def undo_rename(self):
        if not self.rename_history:
            QMessageBox.warning(self, "Nothing to Undo", "No previous renames to undo.")
            return
            
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, len(self.rename_history))
        self.progress_bar.setValue(0)
        
        # Undo renames in reverse order
        for idx, (new_path, old_path) in enumerate(reversed(self.rename_history)):
            try:
                if os.path.exists(new_path):
                    os.rename(new_path, old_path)
                self.progress_bar.setValue(idx + 1)
                QApplication.processEvents()  # Update UI
            except OSError:
                continue
                
        # Hide progress bar after completion
        QTimer.singleShot(1000, lambda: self.progress_bar.setVisible(False))
        
        QMessageBox.information(self, "Undo Success", "Renaming has been undone.")
        self.rename_history.clear()
        self.undo_button.setEnabled(False)


if __name__ == "__main__":
    app = QApplication([])
    window = RenameTool()
    window.show()
    app.exec()

# Remove everything after this line
def update_toggle(self, state, circle, text):
        if state == Qt.CheckState.Checked.value:
            circle.setStyleSheet("""
                background-color: white;
                border-radius: 9px;
                margin: 3px;
                margin-left: 25px;
            """)
            text.setText("ON")
            text.setStyleSheet("color: white; font-size: 10px; font-weight: bold; margin-right: 10px;")
        else:
            circle.setStyleSheet("""
                background-color: white;
                border-radius: 9px;
                margin: 3px;
                margin-left: 3px;
            """)
            text.setText("OFF")
            text.setStyleSheet("color: white; font-size: 10px; font-weight: bold; margin-left: 5px;")
        
        # Also update the entry field
        entry = self.sender().parent().findChild(QLineEdit)
        if entry:
            entry.setEnabled(state == Qt.CheckState.Checked.value)