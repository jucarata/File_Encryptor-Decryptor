import os
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


class Encryptor:

    def __init__(self):
        pass

    
    def __generate_key(password: str, salt=None):
        if salt is None:
            salt = os.urandom(16) # Se acostumbra usar una salt de 16 bytes

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32, # Longitud de la clave, en este caso nos pide que sea de 256 bits( 32 bytes )
            salt=salt, # La salt que asignamos previamente
            iterations=100000,
            backend=default_backend()
        )

        key = kdf.derive(password.encode())

        return key, salt

    def encrypt(self, file, password: str):

        # El hash SHA-256 del archivo original (Lo pide como req)
        sha256_hash = hashlib.sha256(file).digest()

        key, salt = self.__generate_key(password) # Se genera la clave
        iv = os.urandom(16)  # Vector de inicialización de 16 bytes para AES

        # Configura el cifrador AES en modo CBC y crea la instancia del encryptor
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Rellena los datos para que se ajusten al tamaño de bloque de AES (128 bits)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(file) + padder.finalize()

        # Cifra los datos
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Organiza la salida (Primero el salt, luego el iv, luego el encrypted file y por ultimo el hash del archivo origial)
        encrypted_output = salt + iv + encrypted_data + sha256_hash

        return encrypted_output
    

    def encryptByPath(self, input_file: str, password: str, output_file: str):
        with open(input_file, 'rb') as f:
            data = f.read()

        sha256_hash = hashlib.sha256(data).digest()

        key, salt = self.__generate_key(password)
        iv = os.urandom(16)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        with open(output_file, 'wb') as f:
            f.write(salt + iv + encrypted_data + sha256_hash)

