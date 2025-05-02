import random

def encrypt(text):
    key = random.randint(1, 25)
    encrypt = ''
    for char in text:
        if char.isupper():
            encrypt += chr((ord(char) - ord('A') + key) % 26 + ord('A'))
        elif char.islower():
            encrypt += chr((ord(char) - ord('a') + key) % 26 + ord('a'))
        else:
            encrypt += char

    print(f"Your Caesar Cypher Key Is: {key}")  # Print the key
    return encrypt, key  # Return both encrypted text and the key

def decrypt(text, key):
    decrypt = ""
    for char in text:
        if char.isalpha():
            shift = key % 26  # Apply the shift to the character
            char_code = ord(char)
            if char.islower():
                decrypt += chr((char_code - ord('a') - shift) % 26 + ord('a'))
            else:
                decrypt += chr((char_code - ord('A') - shift) % 26 + ord('A'))
        else:
            decrypt += char
    return decrypt