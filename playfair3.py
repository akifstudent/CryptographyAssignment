import numpy as np
import time
import os
os.system('cls')


#5x5 matrix setup 
def generate_playfair_matrix(key):
    key = key.replace("J", "I").upper()             #Replacing J with I
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = []
    used_chars = set()
    
    for char in key + alphabet:                     #Filling the matrix row-wise, first with the keyword, then with the remaining alphabet letters (excluding "J").
        if char not in used_chars:
            matrix.append(char)
            used_chars.add(char)
    
    return np.array(matrix).reshape(5, 5)

def find_position(matrix, char):
    row, col = np.where(matrix == char)
    return row[0], col[0]

#Setup the plaintext for the playfair cipher
def prepare_text(text):
    text = text.replace("J", "I").upper()                #letter i and j are assume as the same letter at the same place/index
    text = "".join(filter(str.isalpha, text))
    prepared_text = ""
    i = 0
    
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else "X"
        
        if a == b:
            prepared_text += a + "X"
            i += 1
        else:
            prepared_text += a + b
            i += 2
    
    if len(prepared_text) % 2 != 0:
        prepared_text += "X"
    
    return prepared_text


#To encrypt the plaintext
def playfair_encrypt(text, key):
    matrix = generate_playfair_matrix(key)
    text = prepare_text(text)
    cipher_text = ""
    
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)
        
        if row_a == row_b:
            cipher_text += matrix[row_a, (col_a + 1) % 5] + matrix[row_b, (col_b + 1) % 5]
        elif col_a == col_b:
            cipher_text += matrix[(row_a + 1) % 5, col_a] + matrix[(row_b + 1) % 5, col_b]
        else:
            cipher_text += matrix[row_a, col_b] + matrix[row_b, col_a]
    
    return cipher_text


#To decrypt the ciphertext
def playfair_decrypt(text, key):
    matrix = generate_playfair_matrix(key)
    plain_text = ""
    
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)
        
        if row_a == row_b:
            plain_text += matrix[row_a, (col_a - 1) % 5] + matrix[row_b, (col_b - 1) % 5]
        elif col_a == col_b:
            plain_text += matrix[(row_a - 1) % 5, col_a] + matrix[(row_b - 1) % 5, col_b]
        else:
            plain_text += matrix[row_a, col_b] + matrix[row_b, col_a]
    
    return plain_text


#Main Function
def playfair():
    # User input
    key = input("Enter the key: ")
    message = input("Enter the message: ")

    matrix = generate_playfair_matrix(key)
    print("\nGenerated Playfair Cipher Matrix:")
    print(matrix)
    print("\033[3mPlease note that letter 'i' and 'j' is at the same index. i=j. \033[0m")


    start_encrypt = time.time()
    cipher_text = playfair_encrypt(message, key)
    end_encrypt = time.time()
    encryption_time = end_encrypt - start_encrypt

    start_decrypt = time.time()
    plain_text = playfair_decrypt(cipher_text, key)
    end_decrypt = time.time()
    decryption_time = end_decrypt - start_decrypt

    print(f"\nEncrypted: {cipher_text}")
    print(f"Decrypted: {plain_text}")
    print(f"\nEncryption Time: {encryption_time:.6f} seconds")
    print(f"Decryption Time: {decryption_time:.6f} seconds")