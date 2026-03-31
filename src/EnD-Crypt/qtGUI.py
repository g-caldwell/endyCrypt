import os
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QApplication, QWidget, QTabWidget, QVBoxLayout, QPlainTextEdit, QPushButton, QLineEdit, QLabel, QComboBox, QListWidget, QInputDialog, QHBoxLayout)
from PyQt6.QtCore import Qt
import rsa
import caesarCypher
import binary

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data.txt')
KEYS_FILE = os.path.join(BASE_DIR, 'keys.txt')

# Main App Window
class EncryptionDecryptionApp(QWidget):
    def __init__(self):
        super().__init__()

        # Window Settings
        self.setWindowTitle("endyCrypt.exe")  # Window Name
        self.setGeometry(100, 100, 900, 650)  # Window Size And Location
        self.setStyleSheet("""
            QWidget {
                background-color: #3f3f3f;
                color: #121212;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 500;
            }
            QPlainTextEdit, QLineEdit {
                background-color: #282828;
                border: 1px solid #4C4C4C;
                padding: 8px;
                color: white;
                font-weight: 500;
            }
            QPushButton {
                background-color: #7b6bd7;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 15px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #4b45ca;
            }
            QComboBox {
                background-color: #383838;
                color: white;
                border: 1px solid #4C4C4C;
                padding: 8px;
                border-radius: 6px;
                font-weight: 500;
            }
            QListWidget {
                background-color: #383838;
                color: white;
                border: 1px solid #4C4C4C;
                padding: 8px;
                border-radius: 6px;
                font-weight: 500;
            }
            QLabel {
                font-weight: 600;
            }
        """)

        # Tab Initialization: Encryption, Decryption, Key
        self.tabs = QTabWidget(self)
        self.tabs.addTab(self.createEncryptTab(), "Encrypt")
        self.tabs.addTab(self.createDecryptTab(), "Decrypt")
        self.tabs.addTab(self.createKeyTab(), "Keys")
        self.tabs.currentChanged.connect(self.loadData)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.tabs)
        self.setLayout(mainLayout)

        self.loadData()

    # Encrypt Tab Setup
    def createEncryptTab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Text Box
        self.dataTextEdit = QPlainTextEdit(tab)
        self.dataTextEdit.setPlaceholderText("Enter text to encrypt...")  # Placeholder text to guide users
        self.dataTextEdit.setFixedHeight(525)
        layout.addWidget(self.dataTextEdit)

        # Dropdown
        self.encryptionMethodCombo = QComboBox(tab)
        self.encryptionMethodCombo.addItems(["Binary", "Caesar Cypher", "RSA"])
        layout.addWidget(self.encryptionMethodCombo)

        # Encrypt Button
        encryptButton = QPushButton("Encrypt", tab)
        encryptButton.clicked.connect(self.encryptData)
        layout.addWidget(encryptButton)

        tab.setLayout(layout)
        return tab

    # Decrypt Tab Setup
    def createDecryptTab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Text Box
        self.decryptTextEdit = QPlainTextEdit(tab)
        self.decryptTextEdit.setPlaceholderText("Enter encrypted text...")  # Placeholder for decryption input
        self.decryptTextEdit.setFixedHeight(525)
        layout.addWidget(self.decryptTextEdit)

        # Method Dropdown
        self.decryptionMethodCombo = QComboBox(tab)
        self.decryptionMethodCombo.addItems(["Binary", "Caesar Cypher", "RSA"])
        self.decryptionMethodCombo.currentTextChanged.connect(self.toggleDecryptKeyVisibility)
        layout.addWidget(self.decryptionMethodCombo)

        # Caesar Key Dropdown
        self.caesarKeySelect = QComboBox(tab)
        self.caesarKeySelect.setPlaceholderText("Select Caesar Key")
        layout.addWidget(self.caesarKeySelect)

        # RSA Key Dropdown
        self.rsaKeySelect = QComboBox(tab)
        self.rsaKeySelect.setPlaceholderText("Select RSA Key")
        layout.addWidget(self.rsaKeySelect)

        # Decrypt Button
        decryptButton = QPushButton("Decrypt", tab)
        decryptButton.clicked.connect(self.decryptData)
        layout.addWidget(decryptButton)

        tab.setLayout(layout)
        return tab

    # Toggle Visibility Of Dropdowns Based On Decryption Method
    def toggleDecryptKeyVisibility(self):
        method = self.decryptionMethodCombo.currentText()
        self.caesarKeySelect.setVisible(method == "Caesar Cypher")
        self.rsaKeySelect.setVisible(method == "RSA")

    # Key Tab Setup: Manage Stored Keys
    def createKeyTab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("My Keys:", tab))  # Key List Title
        self.keyListWidget = QListWidget(tab)
        layout.addWidget(self.keyListWidget)

        # Delete Button For Removing Keys
        deleteButton = QPushButton("Delete Selected Key", tab)
        deleteButton.clicked.connect(self.deleteKey)
        layout.addWidget(deleteButton)

        # Rename Button For Key Names
        renameButton = QPushButton("Rename Selected Key", tab)
        renameButton.clicked.connect(self.renameKey)
        layout.addWidget(renameButton)

        tab.setLayout(layout)
        return tab

    # Encrypt Data Based Selected Method
    def encryptData(self):
        text = self.dataTextEdit.toPlainText()
        method = self.encryptionMethodCombo.currentText()
        encryptedText = ""

        try:
            if method == "Binary":
                encryptedText = binary.encrypt(text)

            elif method == "Caesar Cypher":
                encryptedText, caesarKey = caesarCypher.encrypt(text)
                label, ok = QInputDialog.getText(self, "Save Key", "Enter a label for this Caesar key:")
                if ok and label:
                    with open(KEYS_FILE, "a") as f:
                        f.write(f"{label} | Caesar | {caesarKey}\n")

            elif method == "RSA":
                rsaE, rsaD, rsaN = rsa.generateKeys()
                encryptedBlocks = rsa.encrypt_text(text, rsaE, rsaN)
                encryptedText = ' '.join(map(str, encryptedBlocks))
                label, ok = QInputDialog.getText(self, "Save Key", "Enter a label for this RSA key:")
                if ok and label:
                    with open(KEYS_FILE, "a") as f:
                        f.write(f"{label} | RSA | d: {rsaD} , n: {rsaN}\n")

            with open(DATA_FILE, "w") as f:
                f.write(encryptedText)

            self.loadData()
        except Exception as e:
            print(f"An error occurred during encryption: {e}")

    # Decrypt Data Based Selected Method
    def decryptData(self):
        encryptedText = self.decryptTextEdit.toPlainText()
        method = self.decryptionMethodCombo.currentText()
        decryptedText = ""

        try:
            if method == "Binary":
                decryptedText = binary.decrypt(encryptedText)

            elif method == "Caesar Cypher":
                selectedLabel = self.caesarKeySelect.currentText()
                keyLine = self.getKeyByLabel(selectedLabel, "Caesar")
                if keyLine:
                    key = int(keyLine.split("|")[2].strip())
                    decryptedText = caesarCypher.decrypt(encryptedText, key)

            elif method == "RSA":
                selectedLabel = self.rsaKeySelect.currentText()
                keyLine = self.getKeyByLabel(selectedLabel, "RSA")
                if keyLine:
                    d, n = self.getRsaKeyValues(keyLine)
                    blocks = list(map(int, encryptedText.strip().split()))
                    decryptedText = rsa.decrypt_text(blocks, d, n)

            with open(DATA_FILE, "w") as f:
                f.write(decryptedText)

            self.loadData()
        except Exception as e:
            print(f"Decryption failed: {e}")

    # Helper To Search Keys Based On Label
    def getKeyByLabel(self, labelTypeText, keyType):
        if os.path.exists(KEYS_FILE):
            with open(KEYS_FILE, "r") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) >= 3 and parts[1].strip() == keyType:
                        label = parts[0].strip()
                        if f"{label} ({keyType})" == labelTypeText:
                            return line.strip()
        return None

    # Helper To Extract RSA Key Values
    def getRsaKeyValues(self, keyLine):
        try:
            valuePart = keyLine.split("|", 2)[2].strip()
            parts = valuePart.split(",")
            d = int(parts[0].split(":")[1].strip())
            n = int(parts[1].split(":")[1].strip())
            return d, n
        except Exception as e:
            print(f"Error parsing RSA key values: {e}")
            return None, None

    # Load Data from data.txt
    def loadData(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                content = f.read()
            if self.tabs.currentIndex() == 0:
                self.dataTextEdit.setPlainText(content)
            elif self.tabs.currentIndex() == 1:
                self.decryptTextEdit.setPlainText(content)

        self.updateCaesarKeySelection()
        self.updateRsaKeySelection()
        self.updateKeysList()
        self.toggleDecryptKeyVisibility()

    # Update Caesar Key Dropdown
    def updateCaesarKeySelection(self):
        self.caesarKeySelect.clear()
        if os.path.exists(KEYS_FILE):
            with open(KEYS_FILE, "r") as f:
                for line in f:
                    if "| Caesar |" in line:
                        label = line.split("|")[0].strip()
                        self.caesarKeySelect.addItem(f"{label} (Caesar)")

    # Update RSA Key Dropdown
    def updateRsaKeySelection(self):
        self.rsaKeySelect.clear()
        if os.path.exists(KEYS_FILE):
            with open(KEYS_FILE, "r") as f:
                for line in f:
                    if "| RSA |" in line:
                        label = line.split("|")[0].strip()
                        self.rsaKeySelect.addItem(f"{label} (RSA)")

    # Update Keys List Widget
    def updateKeysList(self):
        self.keyListWidget.clear()
        if os.path.exists(KEYS_FILE):
            with open(KEYS_FILE, "r") as f:
                for line in f:
                    self.keyListWidget.addItem(line.strip())

    # Delete Selected Key
    def deleteKey(self):
        selectedItem = self.keyListWidget.currentItem()
        if selectedItem:
            keyToDelete = selectedItem.text()
            if os.path.exists(KEYS_FILE):
                with open(KEYS_FILE, "r") as f:
                    keys = f.readlines()
                with open(KEYS_FILE, "w") as f:
                    for key in keys:
                        if key.strip() != keyToDelete:
                            f.write(key)
            self.updateKeysList()

    # Rename Selected Key
    def renameKey(self):
        selectedItem = self.keyListWidget.currentItem()
        if selectedItem:
            oldLine = selectedItem.text()
            parts = oldLine.split("|")
            if len(parts) >= 3:
                oldLabel = parts[0].strip()
                keyType = parts[1].strip()
                value = parts[2].strip()
                newLabel, ok = QInputDialog.getText(self, "Rename Key", "Enter new key label:", text=oldLabel)
                if ok and newLabel:
                    newLine = f"{newLabel} | {keyType} | {value}\n"
                    if os.path.exists(KEYS_FILE):
                        with open(KEYS_FILE, "r") as f:
                            keys = f.readlines()
                        with open(KEYS_FILE, "w") as f:
                            for key in keys:
                                if key.strip() == oldLine.strip():
                                    f.write(newLine)
                                else:
                                    f.write(key)
                    self.updateKeysList()

# Running the App
if __name__ == '__main__':
    app = QApplication([])  # Start PyQt application
    window = EncryptionDecryptionApp()  # Create main window
    window.show()  # Show window
    app.exec()  # Execute application loop