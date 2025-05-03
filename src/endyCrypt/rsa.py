import math
import random
import sympy

# Generates a random prime within range
def random_prime(min_val, max_val):
    return sympy.randprime(min_val, max_val)

def power(base, expo, m):
    res = 1
    base = base % m
    while expo > 0:
        if expo & 1:
            res = (res * base) % m
        base = (base * base) % m
        expo = expo // 2
    return res

# Function to find modular inverse of e modulo phi(n)
def modInverse(e, phi):
    return pow(e, -1, phi)

# RSA Key Generation
def generateKeys():
    p = random_prime(2**512, 2**1024)
    q = random_prime(2**512, 2**1024)
    
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    d = modInverse(e, phi)

    return e, d, n

# Convert text to integer
def text_to_int(text):
    return int.from_bytes(text.encode(), 'big')

# Convert integer back to text
def int_to_text(number):
    try:
        return number.to_bytes((number.bit_length() + 7) // 8, 'big').decode('utf-8', errors='ignore')
    except Exception as e:
        return f"Decoding Error: {e}"

# Encrypt integer message using public key (e, n)
def encrypt_integer(message, e, n):
    return power(message, e, n)

# Encrypt text message in blocks using public key (e, n)
def encrypt_text(message, e, n):
    block_size = (n.bit_length() // 8) - 1
    encrypted_blocks = []

    for i in range(0, len(message), block_size):
        chunk = message[i:i+block_size]
        chunk_int = text_to_int(chunk)
        encrypted_blocks.append(encrypt_integer(chunk_int, e, n))
    return encrypted_blocks

# Decrypt integer message using private key (d, n)
def decrypt_integer(message, d, n):
    return power(message, d, n)

# Decrypt text message in blocks using private key (d, n)
def decrypt_text(encrypted_blocks, d, n):
    decrypted_text = ""
    
    for i in encrypted_blocks:
        decrypted_chunk_int = decrypt_integer(i, d, n)
        decrypted_text += int_to_text(decrypted_chunk_int)
    return decrypted_text