import caesarCypher
import rsa
import binary
import os

# Open file, retrieve data, then close file
file = open("data.txt", "rt")
content = file.read()
file.close()

# Ask user what decryption method they want to use
print("1: Binary")
print("2: Caesar Cypher")
print("3: RSA")
method = input("Please Enter The Corresponding Number Of The Decryption Method You Wish To Use: ")
if method == "1":
    print("You Have Selected The Binary Decryption Method.\n")
elif method == "2":
    print("You Have Selected The Caesar Cypher Decryption Method.\n")
elif method == "3":
    print("You Have Selected The RSA Decryption Method.\n")
else:
    print("Uh Oh, Please Try Again And Enter A Number Corresponding To The Method You Wish To Use.")

encryptedText = ""

# Binary Encryption
if method == "1": 
    decryptedText = binary.decrypt(content)
    

# Caesar Cypher Encryption
if method == "2": 
    decryptedText = caesarCypher.decrypt(content)
    
    
# RSA Encryption
if method == "3": 
    d = int(input("\nPlease Enter Your RSA Private Key Here {d}: "))
    n = int(input("\nPlease Enter Your RSA Public Key Portion Here {n}: "))

    encrypted_blocks = eval(content)
    decryptedText = rsa.decrypt_text(encrypted_blocks, d, n)
    print("\n[Decryption successful!]\n[Please check the data.txt file to view your message.]\n")
    

# Open file, write data, then close file
file = open("data.txt", "w")
file.write(decryptedText)
file.close()