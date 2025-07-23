import os
import base64
import hashlib
from Crypto.Cipher import AES, DES3
from Crypto.Util.Padding import pad, unpad
from random import randint

class CipherImplementations:
    def encrypt(self, cipher, plaintext, key):
        if cipher == "AES":
            return self.aes_encrypt(plaintext, key)
        elif cipher == "Caesar":
            return self.caesar_encrypt(plaintext, key)
        elif cipher == "Vigenère":
            return self.vigenere_encrypt(plaintext, key)
        elif cipher == "OTP":
            return self.otp_encrypt(plaintext, key)
        elif cipher == "Atbash":
            return self.atbash_encrypt(plaintext)
        elif cipher == "Rail Fence":
            return self.rail_fence_encrypt(plaintext, key)
        elif cipher == "DES3":
            return self.des3_encrypt(plaintext, key)
        else:
            raise ValueError("Unsupported cipher selected.")
    
    def decrypt(self, cipher, ciphertext, key):
        if cipher == "AES":
            return self.aes_decrypt(ciphertext, key)
        elif cipher == "Caesar":
            return self.caesar_decrypt(ciphertext, key)
        elif cipher == "Vigenère":
            return self.vigenere_decrypt(ciphertext, key)
        elif cipher == "OTP":
            return self.otp_decrypt(ciphertext, key)
        elif cipher == "Atbash":
            return self.atbash_decrypt(ciphertext)
        elif cipher == "Rail Fence":
            return self.rail_fence_decrypt(ciphertext, key)
        elif cipher == "DES3":
            return self.des3_decrypt(ciphertext, key)
        else:
            raise ValueError("Unsupported cipher selected.")
    
    def aes_encrypt(self, plaintext, key):
        if not key:
            raise ValueError("Key is required for AES encryption")
        key_hash = hashlib.sha256(key.encode()).digest()[:16]
        cipher = AES.new(key_hash, AES.MODE_CBC)
        padded_text = pad(plaintext.encode(), AES.block_size)
        ciphertext = cipher.encrypt(padded_text)
        return base64.b64encode(cipher.iv + ciphertext).decode()
    
    def aes_decrypt(self, ciphertext, key):
        if not key:
            raise ValueError("Key is required for AES decryption")
        key_hash = hashlib.sha256(key.encode()).digest()[:16]
        data = base64.b64decode(ciphertext.encode())
        iv = data[:AES.block_size]
        ciphertext = data[AES.block_size:]
        cipher = AES.new(key_hash, AES.MODE_CBC, iv=iv)
        decrypted = cipher.decrypt(ciphertext)
        return unpad(decrypted, AES.block_size).decode()
    
    def caesar_encrypt(self, text, key):
        if not key:
            raise ValueError("Key is required for Caesar cipher")
        key = int(key)
        return ''.join(
            chr((ord(char) - 97 + key) % 26 + 97) if char.islower() else
            chr((ord(char) - 65 + key) % 26 + 65) if char.isupper() else char
            for char in text
        )
    
    def caesar_decrypt(self, text, key):
        return self.caesar_encrypt(text, -int(key))
    
    def vigenere_encrypt(self, text, key):
        if not key:
            raise ValueError("Key is required for Vigenère cipher")
        def shift(char, k):
            if not char.isalpha():
                return char
            offset = 65 if char.isupper() else 97
            return chr((ord(char) - offset + k) % 26 + offset)

        expanded_key = (key * ((len(text) // len(key)) + 1))[:len(text)]
        return ''.join(shift(char, ord(k) - 97) if char.isalpha() else char
                   for char, k in zip(text, expanded_key))
    
    def vigenere_decrypt(self, text, key):
        if not key:
            raise ValueError("Key is required for Vigenère cipher")
        def shift(char, k):
            if not char.isalpha():
                return char
            offset = 65 if char.isupper() else 97
            return chr((ord(char) - offset - k) % 26 + offset)

        expanded_key = (key * ((len(text) // len(key)) + 1))[:len(text)]
        return ''.join(shift(char, ord(k) - 97) if char.isalpha() else char
                   for char, k in zip(text, expanded_key))
    
    def otp_encrypt(self, text, key):
        if not key:
            raise ValueError("Key is required for OTP encryption")
        if len(key) < len(text):
            raise ValueError("OTP key must be at least as long as the plaintext")
        return ''.join(chr(ord(t) ^ ord(k)) for t, k in zip(text, key))
    
    def otp_decrypt(self, text, key):
        return self.otp_encrypt(text, key)
    
    def atbash_encrypt(self, text):
        return ''.join(
            chr(155 - ord(char)) if char.isupper() else
            chr(219 - ord(char)) if char.islower() else char
            for char in text
        )
    
    def atbash_decrypt(self, text):
        return self.atbash_encrypt(text)
    
    def rail_fence_encrypt(self, text, key):
        if not key:
            raise ValueError("Key is required for Rail Fence cipher")
        key = int(key)
        rail = [''] * key
        direction_down = False
        row = 0
        for char in text:
            rail[row] += char
            if row == 0 or row == key - 1:
                direction_down = not direction_down
            row += 1 if direction_down else -1
        return ''.join(rail)
    
    def rail_fence_decrypt(self, text, key):
        if not key:
            raise ValueError("Key is required for Rail Fence cipher")
        key = int(key)
        rail = [''] * key
        direction_down = False
        row = 0
        mark = [''] * len(text)
        for i in range(len(text)):
            mark[i] = row
            if row == 0 or row == key - 1:
                direction_down = not direction_down
            row += 1 if direction_down else -1

        index = 0
        for i in range(key):
            for j in range(len(text)):
                if mark[j] == i:
                    rail[i] += text[index]
                    index += 1

        result = ''
        row = 0
        direction_down = False
        for i in range(len(text)):
            result += rail[row][0] 
            rail[row] = rail[row][1:]
            if row == 0 or row == key - 1:
                direction_down = not direction_down
            row += 1 if direction_down else -1

        return result
    
    def des3_encrypt(self, plaintext, key):
        if not key:
            raise ValueError("Key is required for DES3 encryption")
        key_hash = hashlib.sha256(key.encode()).digest()[:24]
        cipher = DES3.new(key_hash, DES3.MODE_CBC)
        padded_text = pad(plaintext.encode(), DES3.block_size)
        ciphertext = cipher.encrypt(padded_text)
        return base64.b64encode(cipher.iv + ciphertext).decode()
    
    def des3_decrypt(self, ciphertext, key):
        if not key:
            raise ValueError("Key is required for DES3 decryption")
        key_hash = hashlib.sha256(key.encode()).digest()[:24]
        data = base64.b64decode(ciphertext.encode())
        iv = data[:DES3.block_size]
        ciphertext = data[DES3.block_size:]
        cipher = DES3.new(key_hash, DES3.MODE_CBC, iv=iv)
        decrypted = cipher.decrypt(ciphertext)
        return unpad(decrypted, DES3.block_size).decode()