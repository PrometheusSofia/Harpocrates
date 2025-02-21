from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel,
    QPushButton, QMessageBox, QHBoxLayout, QTabWidget, QLineEdit, QApplication, QInputDialog  
)
from PyQt5.QtGui import QClipboard, QIcon
from password_manager import load_passwords, save_password, generate_password, check_password_strength, delete_password
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem



class RunWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Password Manager")
        self.setGeometry(100, 100, 800, 400)

        self.setWindowIcon(QIcon("data/secret.ico"))

        layout = QVBoxLayout()

        # Create a horizontal layout for top-left buttons
        button_layout = QHBoxLayout()

        # Create Folder Button
        create_folder_button = QPushButton("Create Folder")
        create_folder_button.clicked.connect(self.create_folder_action)
        button_layout.addWidget(create_folder_button)

        # Delete Folder Button
        delete_folder_button = QPushButton("Delete Folder")
        delete_folder_button.clicked.connect(self.delete_folder_action)
        button_layout.addWidget(delete_folder_button)

        # Add button layout at the top
        layout.addLayout(button_layout)

        # Tab Widget
        self.tab_widget = QTabWidget()

        # Tabs
        self.init_password_table_tab()
        self.init_password_creation_tab()

        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

    def init_password_table_tab(self):
        password_tab = QWidget()
        tab_layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Stored Passwords")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        tab_layout.addWidget(title_label)

        # Replace QTableWidget with QTreeWidget
        self.password_tree = QTreeWidget()
        self.password_tree.setColumnCount(4)  # Folder, Source, Username, Password
        self.password_tree.setHeaderLabels(["Strength", "Source", "Username", "Password"])
        self.password_tree.itemSelectionChanged.connect(self.update_copy_button_state)

        # Expand and collapse functionality
        self.password_tree.setExpandsOnDoubleClick(True)

        self.refresh_password_table()
        tab_layout.addWidget(self.password_tree)

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
        expand_button = QPushButton("Expand All")
        expand_button.clicked.connect(lambda: self.password_tree.expandAll())

        collapse_button = QPushButton("Collapse All")
        collapse_button.clicked.connect(lambda: self.password_tree.collapseAll())

        button_layout.addWidget(expand_button)
        button_layout.addWidget(collapse_button)

        tab_layout.addLayout(button_layout)
        password_tab.setLayout(tab_layout)
        self.tab_widget.addTab(password_tab, "View Passwords")

    def refresh_password_table(self):
        self.password_tree.clear()  # Clear existing data

        passwords = load_passwords()  # Load saved passwords
        folder_dict = {}  # Store folder items

        for entry in passwords:
            folder_name = entry.get("Folder", "Default")  # Default if no folder
            source = entry.get("Source", "")
            username = entry.get("Username", "")
            password = entry.get("Password", "")

            # If the folder doesn't exist in the tree, create it
            if folder_name not in folder_dict:
                folder_item = QTreeWidgetItem(self.password_tree, [folder_name])
                folder_item.setExpanded(True)  # Expand folders by default
                folder_dict[folder_name] = folder_item

            # Add password as a child of the folder
            child_item = QTreeWidgetItem(folder_dict[folder_name], ["🔍", source, username, password])
            folder_dict[folder_name].addChild(child_item)

        self.password_tree.expandAll()  # Expand all folders initially

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

    def create_folder_action(self):
        folder_name, ok = QInputDialog.getText(self, "Create Folder", "Enter folder name:")

        if ok and folder_name.strip():
            folder_name = folder_name.strip()

            # Check if the folder already exists
            for i in range(self.password_tree.topLevelItemCount()):
                if self.password_tree.topLevelItem(i).text(0) == folder_name:
                    QMessageBox.warning(self, "Error", "Folder already exists.")
                    return

            # Add the folder to the tree
            folder_item = QTreeWidgetItem(self.password_tree, [folder_name])
            folder_item.setExpanded(True)

    def delete_folder_action(self):
        selected_items = self.password_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "No folder selected.")
            return

        selected_item = selected_items[0]

        if selected_item.parent() is not None:  # Ensure it's a folder
            QMessageBox.warning(self, "Error", "You must select a folder to delete.")
            return

        # Confirm deletion
        confirm = QMessageBox.question(self, "Delete Folder",
                                       f"Are you sure you want to delete the folder '{selected_item.text(0)}'?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirm == QMessageBox.Yes:
            if selected_item.childCount() > 0:
                QMessageBox.warning(self, "Error", "Folder is not empty.")
                return

            index = self.password_tree.indexOfTopLevelItem(selected_item)
            self.password_tree.takeTopLevelItem(index)


    def delete_selected_password(self):
        selected_items = self.password_tree.selectedItems()
        if not selected_items:
            return

        selected_item = selected_items[0]
        if selected_item.parent() is None:  # Skip folders
            return

        source = selected_item.text(1)  # Column 1 = Source
        username = selected_item.text(2)  # Column 2 = Username

        confirm = QMessageBox.question(self, "Delete Password",
                                    f"Are you sure you want to delete the password for {source} ({username})?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirm == QMessageBox.Yes:
            success = delete_password(source, username)
            if success:
                QMessageBox.information(self, "Success", "Password deleted successfully.")
                self.refresh_password_table()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete password.")

    def update_copy_button_state(self):
        selected_items = self.password_tree.selectedItems()
        
        # Ensure we have a selection and it's not a folder
        has_selection = bool(selected_items) and selected_items[0].parent() is not None  

        self.copy_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)

    def copy_password_to_clipboard(self):
        selected_items = self.password_tree.selectedItems()
        if not selected_items:
            return

        selected_item = selected_items[0]  # Get selected item
        if selected_item.parent() is None:  # Skip folders
            return

        password = selected_item.text(3)  # Column 3 = Password
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

        # Folder Input
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Enter folder (optional)")
        tab_layout.addWidget(QLabel("Folder:"))
        tab_layout.addWidget(self.folder_input)


        creation_tab.setLayout(tab_layout)
        self.tab_widget.addTab(creation_tab, "Password Creation")

    def generate_password_action(self):
        try:
            source = self.source_input.text().strip()
            username = self.username_input.text().strip()
            length = self.length_input.text().strip() or "14"  # Default to "14" if empty
            folder = self.folder_input.text().strip() or "Default"  # Default to "Default"

            if not source or not username:
                QMessageBox.warning(self, "Error", "Source and Username fields cannot be empty.")
                return

            if not length.isdigit():  # Ensure it's a valid number
                QMessageBox.warning(self, "Error", "Password length must be a number.")
                return
            
            length = int(length)  # Convert to int
            password = generate_password(length)  # Generate password

            save_password({
                "Folder": folder,
                "Source": source,
                "Username": username,
                "Password": password
            })

            self.refresh_password_table()  # Refresh UI
            QMessageBox.information(self, "Password Generated", f"Generated Password: {password}")

            # Clear input fields after saving
            self.source_input.clear()
            self.username_input.clear()
            self.length_input.clear()
            self.folder_input.clear()

        except Exception as e:
            print(f"Error in generate_password_action: {e}")  # Debugging log
            QMessageBox.critical(self, "Error", f"Unexpected error: {e}")
