import os
import re
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit, QMessageBox, QCheckBox, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect
from PyQt6.QtGui import QIcon

class RenameTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.rename_history = []  # Stores renaming history for undo

    def initUI(self):
        self.setWindowTitle("Bulk Renaming Tool By GuptaAman777")
        self.setGeometry(100, 100, 400, 350)
        self.setStyleSheet("background-color: rgba(30, 30, 30, 0.9); color: white; border-radius: 10px;")
        self.setWindowIcon(QIcon("Rename Tool.ico"))

        layout = QVBoxLayout()
        self.label = QLabel("Enter Digits Format (e.g., 1, 2, 3):", self)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.digit_entry = QLineEdit(self)
        self.digit_entry.setPlaceholderText("Enter digits")
        self.digit_entry.setStyleSheet("background-color: rgba(50, 50, 50, 0.8); color: white; padding: 10px; border-radius: 10px;")
        layout.addWidget(self.digit_entry, alignment=Qt.AlignmentFlag.AlignCenter)

        self.prefix_checkbox = QCheckBox("Enable Prefix", self)
        self.prefix_checkbox.setStyleSheet("color: white;")
        self.prefix_checkbox.stateChanged.connect(self.toggle_prefix)
        layout.addWidget(self.prefix_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.prefix_entry = QLineEdit(self)
        self.prefix_entry.setPlaceholderText("Enter prefix")
        self.prefix_entry.setStyleSheet("background-color: rgba(80, 80, 80, 0.5); color: gray; padding: 10px; border-radius: 10px;")
        self.prefix_entry.setEnabled(False)
        layout.addWidget(self.prefix_entry, alignment=Qt.AlignmentFlag.AlignCenter)

        self.suffix_checkbox = QCheckBox("Enable Suffix", self)
        self.suffix_checkbox.setStyleSheet("color: white;")
        self.suffix_checkbox.stateChanged.connect(self.toggle_suffix)
        layout.addWidget(self.suffix_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)

        self.suffix_entry = QLineEdit(self)
        self.suffix_entry.setPlaceholderText("Enter suffix")
        self.suffix_entry.setStyleSheet("background-color: rgba(80, 80, 80, 0.5); color: gray; padding: 10px; border-radius: 10px;")
        self.suffix_entry.setEnabled(False)
        layout.addWidget(self.suffix_entry, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(20)

        self.folder_button = QPushButton("Select a Folder to Rename", self)
        self.folder_button.setStyleSheet("background-color: #007AFF; color: white; padding: 10px; border-radius: 8px;"
            "min-width: 200px; min-height: 30px;")
        self.folder_button.clicked.connect(self.rename_files)
        layout.addWidget(self.folder_button, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(10)

        self.files_button = QPushButton("Select Files of a Folder to Rename", self)
        self.files_button.setStyleSheet("background-color: #007AFF; color: white; padding: 10px; border-radius: 8px;"
            "min-width: 200px; min-height: 30px;")
        self.files_button.clicked.connect(self.rename_selected_files)
        layout.addWidget(self.files_button, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(20)

        self.undo_button = QPushButton("Undo Last Rename", self)
        self.undo_button.setStyleSheet("background-color: #FF3B30; color: white; padding: 10px; border-radius: 8px;")
        self.undo_button.setEnabled(False)  # Initially disabled
        self.undo_button.clicked.connect(self.undo_rename)
        layout.addWidget(self.undo_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.animate_window()

    def animate_window(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(500)
        self.animation.setStartValue(QRect(self.x(), self.y() - 20, self.width(), self.height()))
        self.animation.setEndValue(QRect(self.x(), self.y(), self.width(), self.height()))
        self.animation.start()

    def toggle_prefix(self, state):
        self.prefix_entry.setEnabled(state == Qt.CheckState.Checked.value)
        color = "white" if state == Qt.CheckState.Checked.value else "gray"
        self.prefix_entry.setStyleSheet(f"background-color: rgba(50, 50, 50, 0.8); color: {color}; padding: 10px; border-radius: 10px;")

    def toggle_suffix(self, state):
        self.suffix_entry.setEnabled(state == Qt.CheckState.Checked.value)
        color = "white" if state == Qt.CheckState.Checked.value else "gray"
        self.suffix_entry.setStyleSheet(f"background-color: rgba(50, 50, 50, 0.8); color: {color}; padding: 10px; border-radius: 10px;")

    def get_sorted_files(self, files):
        numbered_files = []
        for file in files:
            match = re.search(r'\d+', os.path.basename(file))
            if match:
                number = int(match.group(0))
                ext = os.path.splitext(file)[1]
                numbered_files.append((file, number, ext))
        return sorted(numbered_files, key=lambda x: x[1])

    def rename_files(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if not folder:
            return
        files = [os.path.join(folder, f) for f in os.listdir(folder)]
        self.process_rename(files)

    def rename_selected_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if not files:
            return
        self.process_rename(files)

    def process_rename(self, files):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Rename")
        msg_box.setText("Are you sure you want to rename the selected files?")

        # Remove default buttons and add them manually
        msg_box.setStandardButtons(QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes)

        # Get the buttons
        yes_button = msg_box.button(QMessageBox.StandardButton.Yes)
        no_button = msg_box.button(QMessageBox.StandardButton.No)

        # Adjust styles for proper alignment
        yes_button.setStyleSheet("padding: 10px 30px; margin-right: 20px;")  # Push left
        no_button.setStyleSheet("padding: 10px 30px; margin-left: 20px;")  # Push right

        response = msg_box.exec()

        if response == QMessageBox.StandardButton.No:
            return


        digit_format = self.digit_entry.text()
        if not digit_format.isdigit():
            QMessageBox.critical(self, "Invalid Input", "Please enter a valid number of digits.")
            return

        digit_format = int(digit_format)
        prefix = self.prefix_entry.text() if self.prefix_checkbox.isChecked() else ""
        suffix = self.suffix_entry.text() if self.suffix_checkbox.isChecked() else ""
        files = self.get_sorted_files(files)

        if not files:
            QMessageBox.warning(self, "No Numbered Files", "No files with numbers found.")
            return

        self.rename_history.clear()  # Clear previous history
        for index, (old_path, _, ext) in enumerate(files, start=1):
            new_name = f"{prefix}{str(index).zfill(digit_format)}{suffix}{ext}"
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            os.rename(old_path, new_path)
            self.rename_history.append((new_path, old_path))  # Store renaming history for undo

        QMessageBox.information(self, "Success", "Files renamed successfully!")
        self.undo_button.setEnabled(True)  # Enable Undo button

    def undo_rename(self):
        if not self.rename_history:
            QMessageBox.warning(self, "Nothing to Undo", "No previous renames to undo.")
            return

        for new_path, old_path in reversed(self.rename_history):
            if os.path.exists(new_path):
                os.rename(new_path, old_path)

        QMessageBox.information(self, "Undo Success", "Renaming has been undone.")
        self.rename_history.clear()
        self.undo_button.setEnabled(False)  # Disable Undo button after undoing


if __name__ == "__main__":
    app = QApplication([])
    window = RenameTool()
    window.show()
    app.exec()
