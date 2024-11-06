import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


class Encryptor:
    def __init__(self, password):
        self.password = password
        self.key = self.generate_key(password)

    def generate_key(self, password, salt=b'salt', iterations=100000):
        return PBKDF2(password, salt, dkLen=32, count=iterations)

    def encrypt_file(self, input_file, output_file):
        # Leer datos del archivo de entrada
        with open(input_file, 'rb') as f:
            data = f.read()

        # Calcular hash SHA-256 del archivo original
        original_hash = hashlib.sha256(data).digest()

        # Inicializar cifrador AES en modo CBC
        cipher = AES.new(self.key, AES.MODE_CBC)
        iv = cipher.iv

        # Relleno para que los datos sean múltiplos del bloque
        padding_length = 16 - (len(data) % 16)
        data += bytes([padding_length]) * padding_length

        # Cifrar datos
        encrypted_data = cipher.encrypt(data)

        # Escribir datos cifrados, IV y hash en el archivo de salida
        with open(output_file, 'wb') as f:
            f.write(iv)
            f.write(encrypted_data)
            f.write(original_hash)
