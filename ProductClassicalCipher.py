import numpy as np
import time

def generate_playfair_matrix(key):
    key = key.replace("J", "I").upper()
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = []
    used_chars = set()

    for char in key + alphabet:
        if char not in used_chars:
            matrix.append(char)
            used_chars.add(char)

    return np.array(matrix).reshape(5, 5)

def find_position(matrix, char):
    row, col = np.where(matrix == char)
    return row[0], col[0]

def prepare_text(text):
    text = text.replace("J", "I").upper()
    text = "".join(filter(str.isalpha, text))
    prepared_text = ""
    i = 0

    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else "X"

        if a == b:
            prepared_text += a + "X"
            i += 1
        else:
            prepared_text += a + b
            i += 2

    if len(prepared_text) % 2 != 0:
        prepared_text += "X"

    return prepared_text

def playfair_encrypt(text, key):
    matrix = generate_playfair_matrix(key)
    text = prepare_text(text)
    cipher_text = ""

    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:
            cipher_text += matrix[row_a, (col_a + 1) % 5] + matrix[row_b, (col_b + 1) % 5]
        elif col_a == col_b:
            cipher_text += matrix[(row_a + 1) % 5, col_a] + matrix[(row_b + 1) % 5, col_b]
        else:
            cipher_text += matrix[row_a, col_b] + matrix[row_b, col_a]

    return cipher_text

def playfair_decrypt(text, key):
    matrix = generate_playfair_matrix(key)
    plain_text = ""

    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:
            plain_text += matrix[row_a, (col_a - 1) % 5] + matrix[row_b, (col_b - 1) % 5]
        elif col_a == col_b:
            plain_text += matrix[(row_a - 1) % 5, col_a] + matrix[(row_b - 1) % 5, col_b]
        else:
            plain_text += matrix[row_a, col_b] + matrix[row_b, col_a]

    return plain_text

def rail_fence_encrypt(message, depth):
    if depth <= 1:
        return message
    rails = ["" for _ in range(depth)]
    row, direction = 0, 1
    for char in message:
        rails[row] += char
        row += direction
        if row == 0 or row == depth - 1:
            direction *= -1
    return "".join(rails)

def rail_fence_decrypt(cipher_text, depth):
    if depth <= 1:
        return cipher_text
    pattern = [[] for _ in range(depth)]
    row, direction = 0, 1
    for _ in cipher_text:
        pattern[row].append(None)
        row += direction
        if row == 0 or row == depth - 1:
            direction *= -1
    index = 0
    for r in range(depth):
        for c in range(len(pattern[r])):
            pattern[r][c] = cipher_text[index]
            index += 1
    row, direction = 0, 1
    result = []
    for _ in cipher_text:
        result.append(pattern[row].pop(0))
        row += direction
        if row == 0 or row == depth - 1:
            direction *= -1
    return "".join(result)

def encrypt_combined(message, playfair_key, rail_fence_depth):
    playfair_cipher = playfair_encrypt(message, playfair_key)
    return rail_fence_encrypt(playfair_cipher, rail_fence_depth)


def decrypt_combined(cipher_text, playfair_key, rail_fence_depth):
    rail_fence_plain = rail_fence_decrypt(cipher_text, rail_fence_depth)
    return playfair_decrypt(rail_fence_plain, playfair_key)


def main():
# if __name__ == "__main__":
    playfair_key = input("Enter the Playfair cipher key: ")
    rail_fence_depth = int(input("Enter the Rail Fence depth: "))
    message = input("Enter the message: ")

    #time set and encryption
    start_encrypt = time.time()
    encrypted_text = encrypt_combined(message, playfair_key, rail_fence_depth)
    end_encrypt = time.time()
    encryption_time = end_encrypt - start_encrypt

    #time set and decryption
    start_decrypt = time.time()
    decrypted_text = decrypt_combined(encrypted_text, playfair_key, rail_fence_depth)
    end_decrypt = time.time()
    decryption_time = end_decrypt - start_decrypt

    print(f"\nEncrypted Text: {encrypted_text}")
    print(f"Decrypted Text: {decrypted_text}")
    print(f"\nEncryption Time: {encryption_time:.6f} seconds")
    print(f"Decryption Time: {decryption_time:.6f} seconds")
