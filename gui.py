from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel,
    QPushButton, QMessageBox, QHBoxLayout, QTabWidget, QLineEdit, QApplication, 
)
from PyQt5.QtGui import QClipboard, QIcon
from password_manager import load_passwords, save_password, generate_password, check_password_strength, delete_password


class RunWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Password Manager")
        self.setGeometry(100, 100, 800, 400)

            # Set the window icon from the "data" folder
        self.setWindowIcon(QIcon("data/secret.ico"))  

        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        # Tab 1: View Stored Passwords
        self.init_password_table_tab()

        # Tab 2: Password Creation
        self.init_password_creation_tab()

        # Add tab widget to the main layout
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

    def init_password_table_tab(self):
        password_tab = QWidget()
        tab_layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Stored Passwords")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        tab_layout.addWidget(title_label)

        # Password Table
        self.password_table = QTableWidget()
        self.password_table.setColumnCount(4)  # 4 columns (Strength, Source, Username, Password)
        self.password_table.setHorizontalHeaderLabels(["Strength", "Source", "Username", "Password"])
        self.password_table.horizontalHeader().setStretchLastSection(True)
        self.password_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.password_table.setSelectionMode(QTableWidget.SingleSelection)
        self.password_table.itemSelectionChanged.connect(self.update_button_states)

        self.refresh_password_table()
        tab_layout.addWidget(self.password_table)

        # Button Layout (Copy + Delete)
        button_layout = QHBoxLayout()

        # Copy Password Button
        self.copy_button = QPushButton("Copy Password")
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copy_password_to_clipboard)
        button_layout.addWidget(self.copy_button)

        # Delete Password Button
        self.delete_button = QPushButton("Delete Password")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_selected_password)
        button_layout.addWidget(self.delete_button)

        button_layout.addStretch(1)  # Align buttons properly

        tab_layout.addLayout(button_layout)
        password_tab.setLayout(tab_layout)
        self.tab_widget.addTab(password_tab, "View Passwords")

    def refresh_password_table(self):
        passwords = load_passwords()
        self.password_table.setRowCount(len(passwords))
        self.password_table.setColumnCount(4)  # Ensure there are 4 columns

        # Update column headers to reflect the new order
        self.password_table.setHorizontalHeaderLabels(["Strength", "Source", "Username", "Password"])

        for row, entry in enumerate(passwords):
            # Create Strength button inside the table (Column 0)
            strength_button = QPushButton("🔍")  
            strength_button.setFixedSize(40, 25)  
            strength_button.clicked.connect(lambda _, r=row: self.check_password_strength(r))

            self.password_table.setCellWidget(row, 0, strength_button)  

            # Populate the remaining columns
            self.password_table.setItem(row, 1, QTableWidgetItem(entry.get("Source", "")))
            self.password_table.setItem(row, 2, QTableWidgetItem(entry.get("Username", "")))
            self.password_table.setItem(row, 3, QTableWidgetItem(entry.get("Password", "")))

        # Adjust column widths (Strength first, then Source, Username, Password)
        self.password_table.setColumnWidth(0, 60)   # Strength column (smaller)
        self.password_table.setColumnWidth(1, 200)  # Source column
        self.password_table.setColumnWidth(2, 200)  # Username column
        self.password_table.setColumnWidth(3, 250)  # Password column

    def check_password_strength(self, row):
        password_item = self.password_table.item(row, 3)  # Column 3 is Password

        if not password_item:
            QMessageBox.warning(self, "Error", "No password found in this row.")
            return

        password = password_item.text()
        strength = check_password_strength(password)  # Calls function from password_manager.py

        strength_message = (
            f"Lowercase: {'✔' if strength['lowercase'] else '❌'}\n"
            f"Uppercase: {'✔' if strength['uppercase'] else '❌'}\n"
            f"Numbers: {'✔' if strength['numbers'] else '❌'}\n"
            f"Special Characters: {'✔' if strength['special'] else '❌'}"
        )

        QMessageBox.information(self, "Password Strength", strength_message)
    
    def update_button_states(self):
        selected_rows = self.password_table.selectionModel().selectedRows()
        has_selection = bool(selected_rows)
        
        self.copy_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)

    def delete_selected_password(self):
        selected_rows = self.password_table.selectionModel().selectedRows()
        if not selected_rows:
            return

        selected_row = selected_rows[0].row()
        source_item = self.password_table.item(selected_row, 1)  
        username_item = self.password_table.item(selected_row, 2)  

        if not source_item or not username_item:
            QMessageBox.warning(self, "Error", "Could not retrieve Source and Username.")
            return

        source = source_item.text()
        username = username_item.text()

        # Confirm deletion
        confirm = QMessageBox.question(self, "Delete Password", 
                                    f"Are you sure you want to delete the password for {source} ({username})?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirm == QMessageBox.Yes:
            success = delete_password(source, username)

            if success:
                QMessageBox.information(self, "Success", "Password deleted successfully.")
                self.refresh_password_table()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete password. Entry not found.")

    def update_copy_button_state(self):
        selected_rows = self.password_table.selectionModel().selectedRows()
        self.copy_button.setEnabled(bool(selected_rows))  # Enable if a row is selected

    def copy_password_to_clipboard(self):
        selected_rows = self.password_table.selectionModel().selectedRows()
        if not selected_rows:
            return

        selected_row = selected_rows[0].row()  # Get the first selected row
        password_item = self.password_table.item(selected_row, 3)  # Column 3 is the Password column

        if password_item:
            password = password_item.text()
            clipboard = QApplication.clipboard()
            clipboard.setText(password, QClipboard.Clipboard)
            QMessageBox.information(self, "Password Copied", "The password has been copied to the clipboard.")

    def init_password_creation_tab(self):
        creation_tab = QWidget()
        tab_layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Password Creation")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        tab_layout.addWidget(title_label)

        # Input Fields
        self.source_input = QLineEdit()
        self.source_input.setPlaceholderText("Enter source (e.g., Gmail)")
        tab_layout.addWidget(QLabel("Source:"))
        tab_layout.addWidget(self.source_input)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        tab_layout.addWidget(QLabel("Username:"))
        tab_layout.addWidget(self.username_input)

        self.length_input = QLineEdit()
        self.length_input.setPlaceholderText("Enter password length (default: 14)")
        tab_layout.addWidget(QLabel("Password Length:"))
        tab_layout.addWidget(self.length_input)

        # Generate Password Button
        generate_password_button = QPushButton("Generate Password")
        generate_password_button.clicked.connect(self.generate_password_action)  
        tab_layout.addWidget(generate_password_button)

        creation_tab.setLayout(tab_layout)
        self.tab_widget.addTab(creation_tab, "Password Creation")

    def generate_password_action(self):
        try:
            source = self.source_input.text().strip()
            username = self.username_input.text().strip()
            length = self.length_input.text().strip()

            if not source or not username:
                QMessageBox.warning(self, "Error", "Source and Username fields cannot be empty.")
                return

            length = int(length) if length else 14  # Convert length to integer

            print(f"Generating password of length {length}")  # Debugging log

            password = generate_password(length)  # Call the function
            print(f"Generated password: {password}")  # Debugging log

            save_password({"Source": source, "Username": username, "Password": password})

            QMessageBox.information(self, "Password Generated", f"Generated Password: {password}")

            # Refresh table in the first tab
            self.refresh_password_table()
            self.source_input.clear()
            self.username_input.clear()
            self.length_input.clear()

        except Exception as e:
            print(f"Error in generate_password_action: {e}")  # Log any exceptions
            QMessageBox.critical(self, "Error", f"Unexpected error: {e}")
