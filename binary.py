# Text to binary
def encrypt(text):
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

# Binary back to text
def decrypt(text):
    if len(text) % 8 != 0:
        raise ValueError("String Is Not A Multiple of 8")
    chars = [chr(int(text[i : i + 8], 2)) for i in range(0, len(text), 8)]
    return ''.join(chars)