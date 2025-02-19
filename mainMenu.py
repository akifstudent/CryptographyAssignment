import sys
import time
import random
import Aes_rsa
import playfair3
import RailFenceCipher
import ProductClassicalCipher


def main():
    while True:
        print("\nCryptography Menu")
        print("1. Playfair Cipher")
        print("2. Rail Fence Cipher")
        print("3. Product Classical Symmetric Cipher")
        print("4. AES & RSA Encryption")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            # playfair cipher
            playfair3.playfair()
        elif choice == '2':
            # rail fence cipher
            RailFenceCipher.main()
        elif choice == '3':
            ProductClassicalCipher.main()
        elif choice == '4':
            Aes_rsa.aes_rsa ()
        elif choice == '5':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()