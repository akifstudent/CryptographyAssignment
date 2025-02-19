import time
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import number

# Function to manually calculate modular inverse using Extended Euclidean Algorithm
def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

# Function to generate RSA keys using the built-in library
#def generate_rsa_keys(bits=2048):
#    key = RSA.generate(bits)
#    private_key = key
#    public_key = key.publickey()
#    return public_key, private_key

# Function to generate RSA keys manually
def generate_rsa_keys(bits=2048):
    # Step 1: Generate two large prime numbers p and q
    p = number.getPrime(bits // 2)
    q = number.getPrime(bits // 2)
    n = p * q  # Compute modulus
    phi_n = (p - 1) * (q - 1)  # Compute Euler's totient function

    # Step 2: Choose public exponent e (commonly 65537)
    e = 65537
    while number.GCD(e, phi_n) != 1:  # Ensure e is coprime with phi_n
        e = number.getPrime(16)  # Generate a different prime if not coprime

    # Step 3: Compute private exponent d using mod_inverse
    d = mod_inverse(e, phi_n)

    # Step 4: Construct public and private key objects
    public_key = (n, e)  # Public key (n, e)
    private_key = (n, d)  # Private key (n, d)
    
    return public_key, private_key

# AES Encryption (with CBC mode)
def aes_encrypt(data, aes_key):
    cipher = AES.new(aes_key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
    return cipher.iv + ciphertext  # Return the IV with ciphertext

# AES Decryption (with CBC mode)
def aes_decrypt(ciphertext, aes_key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size)
    return decrypted_data.decode()

# RSA Encryption (manual process using pow)
def rsa_encrypt(message, public_key):
    n, e = public_key
    m = int.from_bytes(message.encode('utf-8'), byteorder='big')
    cipher = pow(m, e, n)  # C = M^e mod n
    return cipher

# RSA Decryption (manual process using pow)
def rsa_decrypt(ciphertext, private_key):
    n, d = private_key
    m = pow(ciphertext, d, n)  # M = C^d mod n
    message_bytes = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big')
    return message_bytes.decode('utf-8')

# Simulate bit errors (flip random bits)
import random
def simulate_bit_error(ciphertext, error_bits=1):
    byte_array = bytearray(ciphertext)
    for _ in range(error_bits):
        index = random.randint(0, len(byte_array) - 1)
        bit = 1 << random.randint(0, 7)
        byte_array[index] ^= bit
    return bytes(byte_array)

# Measure Time for RSA and AES Operations
def measure_time(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    return result, end - start

# Main Process
def aes_rsa():
    print("\n----- Key Exchange & Encryption/Decryption Process -----")

    # Step 1: Generate RSA keys for Person A and Person B
    print("\n[Step 1] Generating RSA key pairs for Person A and Person B:")
    public_key_a, private_key_a = generate_rsa_keys(bits=2048)
    public_key_b, private_key_b = generate_rsa_keys(bits=2048)
    print("\nPublic key A: " ,public_key_a)
    print("\nPrivate key A: " ,private_key_a)
    print("\nPublic key B: " ,public_key_b)
    print("\nPublic key B: " ,private_key_a)

    # Step 2: Person A generates an AES key
    print("\n[Step 2] Person A generates an AES key for secure communication:")
    aes_key = get_random_bytes(16)
    print(f"AES Key: {aes_key.hex()}")

    # Step 3: Encrypt AES key with RSA (Person A to Person B)
    print("\n[Step 3] Encrypting AES key with RSA (Person A uses Person B's Public Key):")
    encrypted_aes_key, rsa_enc_time = measure_time(rsa_encrypt, aes_key.hex(), public_key_b)
    print(f"Encrypted AES Key: {encrypted_aes_key}")
    print(f"RSA Encryption Time: {rsa_enc_time:.6f} seconds")

    # Step 4: Decrypt AES key with RSA (Person B)
    print("\n[Step 4] Decrypting AES key with RSA (Person B uses their Private Key):")
    decrypted_aes_key_hex, rsa_dec_time = measure_time(rsa_decrypt, encrypted_aes_key, private_key_b)
    decrypted_aes_key = bytes.fromhex(decrypted_aes_key_hex)
    print(f"Decrypted AES Key: {decrypted_aes_key.hex()}")
    print(f"RSA Decryption Time: {rsa_dec_time:.6f} seconds")

    # Step 5: AES Encryption (Person A to Person B)
    message = input("\nEnter a message to send from Person A to Person B: ")
    encrypted_message, aes_enc_time = measure_time(aes_encrypt, message, decrypted_aes_key)
    print(f"\nEncrypted Message (AES): {encrypted_message.hex()}")
    print(f"AES Encryption Time: {aes_enc_time:.6f} seconds")

    # Step 6: AES Decryption (Person B)
    decrypted_message, aes_dec_time = measure_time(aes_decrypt, encrypted_message, decrypted_aes_key)
    print(f"\nDecrypted Message (AES): {decrypted_message}")
    print(f"AES Decryption Time: {aes_dec_time:.6f} seconds")

    # Step 7: Simulating Bit Errors
    print("\n[Step 7] Simulating Bit Errors in the AES Ciphertext:")
    for error_count in [1, 2, 5, 10]:
        corrupted_ciphertext = simulate_bit_error(encrypted_message, error_bits=error_count)
        try:
            corrupted_message = aes_decrypt(corrupted_ciphertext, decrypted_aes_key)
            print(f"\n{error_count} Bit Error(s): Decrypted Message: {corrupted_message}")
        except Exception as e:
            print(f"\n{error_count} Bit Error(s): Decryption failed with error: {str(e)}")

    # Step 8: Summary of Times
    print("\n----- Time Analysis Summary -----")
    print(f"RSA Encryption Time: {rsa_enc_time:.6f} seconds")
    print(f"RSA Decryption Time: {rsa_dec_time:.6f} seconds")
    print(f"AES Encryption Time: {aes_enc_time:.6f} seconds")
    print(f"AES Decryption Time: {aes_dec_time:.6f} seconds")

if __name__ == "__main__":
    aes_rsa()
