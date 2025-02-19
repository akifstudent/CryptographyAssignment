import time

def rail_fence_encrypt(message, depth):
    """Encrypts a message using the Rail Fence Cipher with the given depth."""
    if depth <= 1:
        return message  # No encryption needed if depth is 1

    # Create an empty list of strings to hold each row
    rails = [""] * depth
    row, direction = 0, 1

    # Place characters in a zigzag pattern
    for char in message:
        rails[row] += char
        row += direction

        # Change direction at the top and bottom
        if row == 0 or row == depth - 1:
            direction *= -1

    return "".join(rails)  # Combine all rows to get the cipher text

def rail_fence_decrypt(cipher_text, depth):
    """Decrypts a Rail Fence Cipher text given the depth."""
    if depth <= 1:
        return cipher_text  # No decryption needed if depth is 1

    # Determine the zigzag pattern positions
    pattern = [[] for _ in range(depth)]
    row, direction = 0, 1

    for _ in cipher_text:
        pattern[row].append(None)  # Mark positions
        row += direction

        if row == 0 or row == depth - 1:
            direction *= -1

    # Fill the pattern with cipher text characters
    index = 0
    for r in range(depth):
        for c in range(len(pattern[r])):
            pattern[r][c] = cipher_text[index]
            index += 1

    # Read characters in zigzag order
    row, direction = 0, 1
    result = []

    for _ in cipher_text:
        result.append(pattern[row].pop(0))
        row += direction

        if row == 0 or row == depth - 1:
            direction *= -1

    return "".join(result)  # Construct the original message


def main():
    # Input prompt
    # if __name__ == "__main__":
    key_depth = int(input("Enter the depth: "))
    plain_text = input("Enter the message: ")

    #time set and encryption
    start_encrypt = time.time()
    encrypted_text = rail_fence_encrypt(plain_text, key_depth)
    end_encrypt = time.time()
    encryption_time = end_encrypt - start_encrypt

    #time set and decryption
    start_decrypt = time.time()
    decrypted_text = rail_fence_decrypt(encrypted_text, key_depth)
    end_decrypt = time.time()
    decryption_time = end_decrypt - start_decrypt

    print(f"\nEncrypted Text: {encrypted_text}")
    print(f"Decrypted Text: {decrypted_text}")
    print(f"\nEncryption Time: {encryption_time:.6f} seconds")
    print(f"Decryption Time: {decryption_time:.6f} seconds")