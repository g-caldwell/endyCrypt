
# EnD-Crypt

EnD-Crypt is a text encryption and decryption tool that supports RSA, Caesar Cipher, and Binary methods. This project provides both a command-line interface and a PyQt6 GUI for encryption and decryption tasks. It also includes key management, allowing users to securely store encryption keys between sessions.

## Features

- **RSA**: Utilizes the RSA algorithm for secure public-key encryption.
- **Caesar Cipher**: A form of cipher that uses a shift key for text obfuscation.
- **Binary**: Converts text into binary format and back for secure transmission.
- **Persistent Key Storage**: Saves RSA and Caesar Cipher keys between sessions for easy retrieval.
- **GUI**: A clean and intuitive PyQt6 GUI for user tasks.

## Installation

To get started with EnD-Crypt, first install the required dependencies:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/g-caldwell/EnD-Crypt
   cd EnD-Crypt
   ```

2. **Install the dependencies:**

   ```bash
   pip install sympy
   pip install PyQt6
   ```

## Usage

### Command-Line Interface (CLI)

You can encrypt and decrypt messages using the various encryption methods through the Python scripts.

1. **RSA Example:**

   - To generate keys:
     ```python
     from rsa import generateKeys
     e, d, n = generateKeys()
     ```

   - To encrypt a message:
     ```python
     encrypted_message = encrypt_text("Hello World", e, n)
     ```

   - To decrypt a message:
     ```python
     decrypted_message = decrypt_text(encrypted_message, d, n)
     ```

2. **Caesar Cipher Example:**

   - To encrypt:
     ```python
     encrypted_text, key = encrypt("Hello World")
     ```

   - To decrypt:
     ```python
     decrypted_text = decrypt(encrypted_text, key)
     ```

3. **Binary Encoding Example:**

   - To encrypt (convert text to binary):
     ```python
     binary_text = encrypt("Hello World")
     ```

   - To decrypt (convert binary back to text):
     ```python
     decrypted_text = decrypt(binary_text)
     ```

### PyQt6 GUI

For users who prefer a GUI, you can run the application using the following:

```bash
python src/qtGUI.py
```

The GUI provides a user-friendly interface to:

- Select encryption methods (RSA, Caesar Cipher, Binary).
- Enter text for encryption and decryption.
- View the encryption keys and manage them between sessions.

### Key Management

Keys for RSA and Caesar Cipher are stored persistently in `keys.txt` for easy access and retrieval between sessions.

## File Structure

```
EnD-Crypt/
├── dist/
│   ├── EnD-Crypt-2.0.0-py3-none-any.whl
│   └── EnD-Crypt-2.0.0.tar.gz
├── src/
│   ├── binary.py              # Binary encoding/decoding
│   ├── caesarCypher.py        # Caesar Cipher logic
│   ├── rsa.py                 # RSA key generation, encryption, decryption
│   ├── qtGUI.py               # Main PyQt6 GUI application
│   ├── data.txt               # Input/output text file
│   └── keys.txt               # Persistent storage of encryption keys
├── LICENSE
├── README.md                 # Project documentation
└── pyproject.toml            # Project metadata and dependencies
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **PyQt6** for the GUI framework.
- **SymPy** for the RSA implementation.
