import os
import re
import sys
from functools import lru_cache
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, 
    QFileDialog, QLineEdit, QMessageBox, QCheckBox, QHBoxLayout, 
    QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect
from PyQt6.QtGui import QIcon

"""
File Renaming Tool
Created by GuptaAman777
Copyright © 2025 GuptaAman777. All rights reserved.
"""

class RenameTool(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.rename_history = []
        self.last_directory = None
        self.setup_ui()
        self.connect_signals()
        
        # Developer signature
        self._developer = "GuptaAman777"
        self._copyright = "Copyright © 2025 GuptaAman777"
        
    def connect_signals(self):
        # Connect all signals in one place for better organization
        self.prefix_checkbox.stateChanged.connect(self.update_preview)
        self.suffix_checkbox.stateChanged.connect(self.update_preview)
        self.prefix_entry.textChanged.connect(self.update_preview)
        self.suffix_entry.textChanged.connect(self.update_preview)
        self.digit_entry.textChanged.connect(self.validate_inputs)
        
    def setup_ui(self):
        self.setWindowTitle("File Renaming Tool")
        self.setGeometry(100, 100, 850, 550)
        
        # Set application icon - using the correct path for PyInstaller
        icon_path = self.get_resource_path("icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        
        self.setup_theme()
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Left panel (Input controls)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 2)
        
        # Right panel (File list and actions)
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 3)
        
        # Final layout assembly
        final_layout = QVBoxLayout(self)
        final_layout.addLayout(main_layout)
        
        # Add GitHub repository button and copyright info
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 5, 0, 0)
        
        # GitHub repository button
        github_button = QPushButton("🔗 GitHub Repository")
        github_button.setStyleSheet("""
            QPushButton {
                background-color: #2d2d3f;
                color: #ffffff;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 9pt;
                max-width: 150px;
            }
            QPushButton:hover {
                background-color: #3d3d4f;
            }
            QPushButton:pressed {
                background-color: #007AFF;
            }
        """)
        github_button.clicked.connect(lambda: self.open_github_repo("https://github.com/GuptaAman777/Rename-Tool"))
        footer_layout.addWidget(github_button)
        
        # Add spacer to push copyright to the right
        footer_layout.addStretch()
        
        # Copyright text
        copyright_text = "Copyright © 2025 GuptaAman777 | For personal use only | For commercial contact: "
        copyright_label = QLabel(copyright_text)
        copyright_label.setStyleSheet("""
            color: #555555;
            font-size: 8pt;
            padding: 2px;
            background-color: transparent;
        """)
        footer_layout.addWidget(copyright_label)
        
        # Create clickable link
        github_link = QLabel('<a href="https://github.com/GuptaAman777" style="color: #007AFF; text-decoration: none;">github.com/GuptaAman777</a>')
        github_link.setOpenExternalLinks(True)
        github_link.setStyleSheet("""
            color: #555555;
            font-size: 8pt;
            padding: 2px;
            background-color: transparent;
        """)
        footer_layout.addWidget(github_link)
        
        # Add the footer layout to the main layout
        final_layout.addLayout(footer_layout)
        
        self.setLayout(final_layout)
        
        self.animate_window()
    
    def get_resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)

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
        """)
        
    def create_left_panel(self):
        panel = QFrame()
        panel.setStyleSheet("background-color: #2d2d3f; border-radius: 10px;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Title for the panel
        title = QLabel("Rename Settings")
        title.setStyleSheet("font-size: 14pt; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Digits input
        digits_group = self.create_input_group("Number Format", "Enter digits (e.g., 3)")
        self.digit_entry = digits_group.findChild(QLineEdit)
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
        
        # Help text
        help_text = QLabel("Enter the number of digits for file numbering.\nOptionally add prefix/suffix to the filenames.")
        help_text.setStyleSheet("color: #aaaaaa; font-size: 9pt; margin-top: 10px;")
        layout.addWidget(help_text)
        
        layout.addStretch()
        return panel

    def create_right_panel(self):
        panel = QFrame()
        panel.setStyleSheet("background-color: #2d2d3f; border-radius: 10px;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Title for the panel
        title = QLabel("File Selection & Preview")
        title.setStyleSheet("font-size: 14pt; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Action buttons
        self.create_action_buttons(layout)
        
        # File list header
        file_header = QLabel("Selected Files:")
        file_header.setStyleSheet("font-weight: bold; font-size: 11pt; margin-top: 5px;")
        layout.addWidget(file_header)
        
        # File list scroll area with improved styling
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #252535;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background-color: #4d4d5f;
                border-radius: 5px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background-color: #2d2d3f;
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
        
        # Add preview section with scroll area
        preview_header = QLabel("Preview:")
        preview_header.setStyleSheet("font-weight: bold; font-size: 11pt; margin-top: 5px;")
        layout.addWidget(preview_header)
        
        # Preview scroll area with improved styling
        preview_scroll = QScrollArea()
        preview_scroll.setWidgetResizable(True)
        preview_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #252535;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background-color: #4d4d5f;
                border-radius: 5px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background-color: #2d2d3f;
            }
        """)
        
        preview_container = QWidget()
        preview_container.setStyleSheet("background-color: #1e1e2e; border-radius: 5px;")
        preview_layout = QVBoxLayout(preview_container)
        
        self.preview_list = QLabel("No preview available")
        self.preview_list.setWordWrap(True)
        self.preview_list.setStyleSheet("color: #888888; padding: 10px;")
        preview_layout.addWidget(self.preview_list)
        
        preview_scroll.setWidget(preview_container)
        layout.addWidget(preview_scroll)
        
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
        self.update_preview()

    def update_preview(self):
        if not self.selected_files or not self.digit_entry.text().strip().isdigit():
            self.preview_list.setText("No preview available")
            self.preview_list.setStyleSheet("color: #888888;")
            return

        try:
            digit_format = int(self.digit_entry.text().strip())
            files = self.get_sorted_files(self.selected_files)[:5]  # Preview first 5 files
            
            if not files:
                self.preview_list.setText("No numbered files found")
                return

            prefix = self.prefix_entry.text() if self.prefix_checkbox.isChecked() else ""
            suffix = self.suffix_entry.text() if self.suffix_checkbox.isChecked() else ""
            
            preview_text = "Preview of first 5 files:\n\n"
            for idx, (old_path, _, ext) in enumerate(files, 1):
                old_name = os.path.basename(old_path)
                new_name = f"{prefix}{str(idx).zfill(digit_format)}{suffix}{ext}"
                preview_text += f"{old_name} → {new_name}\n"
                
            if len(self.selected_files) > 5:
                preview_text += f"\n... and {len(self.selected_files)-5} more files"
                
            self.preview_list.setText(preview_text)
            self.preview_list.setStyleSheet("color: #ffffff;")
            
        except Exception as e:
            self.preview_list.setText(f"Preview error: {str(e)}")
            self.preview_list.setStyleSheet("color: #ff6b6b;")

    def start_rename(self):
        if not self.selected_files:
            QMessageBox.warning(self, "No Files", "Please select files first.")
            return
            
        if not (digit_format := self.digit_entry.text()).isdigit():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number of digits.")
            return

        # Create a custom dialog with better styled buttons
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Confirm Rename")
        dialog.setText(f"Are you sure you want to rename {len(self.selected_files)} files?")
        
        # Fix: Use standard buttons instead of custom buttons for better compatibility
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        yes_btn = dialog.button(QMessageBox.StandardButton.Yes)
        no_btn = dialog.button(QMessageBox.StandardButton.No)
        
        # Apply styling to standard buttons
        yes_btn.setText("✓ Yes, Rename Files")
        yes_btn.setStyleSheet("""
            QPushButton {
                background-color: #34c759;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover { background-color: #2ea94e; }
            QPushButton:pressed { background-color: #27963f; }
        """)
        
        no_btn.setText("✗ No, Cancel")
        no_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF3B30;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover { background-color: #E0352B; }
            QPushButton:pressed { background-color: #C02D25; }
        """)
        
        # Check the result directly
        if dialog.exec() == QMessageBox.StandardButton.Yes:
            self.process_rename(self.selected_files)

    def process_rename(self, files):
        digit_format = int(self.digit_entry.text().strip())
        files = self.get_sorted_files(files)
        
        if not files:
            QMessageBox.warning(self, "No Files", "No numbered files found.")
            return

        prefix = self.prefix_entry.text() if self.prefix_checkbox.isChecked() else ""
        suffix = self.suffix_entry.text() if self.suffix_checkbox.isChecked() else ""
        
        # Clear previous history
        self.rename_history.clear()
        
        # Process files
        for idx, (old_path, _, ext) in enumerate(files, 1):
            new_name = f"{prefix}{str(idx).zfill(digit_format)}{suffix}{ext}"
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            try:
                os.rename(old_path, new_path)
                self.rename_history.append((new_path, old_path))
            except OSError as e:
                QMessageBox.warning(self, "Error", f"Failed to rename {os.path.basename(old_path)}: {str(e)}")
                continue
        
        # Show styled success message with centered button
        if self.rename_history:
            success_dialog = QMessageBox(self)
            success_dialog.setWindowTitle("Success")
            success_dialog.setText(f"✅ Successfully renamed {len(self.rename_history)} files!")
            success_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
            
            # Get the OK button and style it
            ok_btn = success_dialog.button(QMessageBox.StandardButton.Ok)
            ok_btn.setText("OK")
            ok_btn.setStyleSheet("""
                QPushButton {
                    background-color: #34c759;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 6px;
                    font-weight: bold;
                    min-width: 100px;
                }
                QPushButton:hover { background-color: #2ea94e; }
                QPushButton:pressed { background-color: #27963f; }
            """)
            
            # Set dialog layout to center the button
            success_dialog.setStyleSheet("""
                QDialogButtonBox {
                    alignment: center;
                }
                QMessageBox {
                    background-color: #1e1e2e;
                }
                QMessageBox QLabel {
                    color: white;
                    font-size: 12pt;
                }
            """)
            
            success_dialog.exec()
            self.undo_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "No Changes", "No files were renamed.")

    def undo_rename(self):
        if not self.rename_history:
            QMessageBox.warning(self, "Nothing to Undo", "No previous renames to undo.")
            return
        
        # Undo renames in reverse order
        for new_path, old_path in reversed(self.rename_history):
            try:
                if os.path.exists(new_path):
                    os.rename(new_path, old_path)
            except OSError:
                continue
        
        # Show styled undo success message with centered button
        undo_dialog = QMessageBox(self)
        undo_dialog.setWindowTitle("Undo Success")
        undo_dialog.setText("↩️ Renaming has been undone.")
        undo_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Get the OK button and style it
        ok_btn = undo_dialog.button(QMessageBox.StandardButton.Ok)
        ok_btn.setText("OK")
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #34c759;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover { background-color: #2ea94e; }
            QPushButton:pressed { background-color: #27963f; }
        """)
        
        # Set dialog layout to center the button
        undo_dialog.setStyleSheet("""
            QDialogButtonBox {
                alignment: center;
            }
            QMessageBox {
                background-color: #1e1e2e;
            }
            QMessageBox QLabel {
                color: white;
                font-size: 12pt;
            }
        """)
        
        undo_dialog.exec()
        
        self.rename_history.clear()
        self.undo_button.setEnabled(False)
        
    def open_github_repo(self, url):
        """Open the GitHub repository in the default web browser"""
        import webbrowser
        webbrowser.open(url)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RenameTool()
    window.show()
    sys.exit(app.exec())
