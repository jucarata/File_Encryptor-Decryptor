import os
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


class Decryptor:

    def __init__(self):
        pass

    def __generate_key(self, password: str, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        return key

    def decrypt(self, encrypted_file, password: str):
        # Se extrae el salt, iv, encrypted_data y original_hash
        salt = encrypted_file[:16]
        iv = encrypted_file[16:32]
        encrypted_data = encrypted_file[32:-32]
        original_hash = encrypted_file[-32:]

        # Genera la clave que es la que se usa para cifrar y descifrar
        key = self.__generate_key(password, salt)

        # Configura el descifrador AES en modo CBC
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        # En este caso el cipher se configura en modo decryptor
        decryptor = cipher.decryptor()


        try:
            # Descifra y elimina el relleno de los datos
            padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            data = unpadder.update(padded_data) + unpadder.finalize()

            # Verifica la integridad del archivo descifrado
            computed_hash = hashlib.sha256(data).digest()
            if computed_hash != original_hash:
                raise ValueError("Error de integridad: el archivo descifrado no coincide con el original.")

            return data
        
        except Exception:
            return encrypted_file

    def decryptByPath(self, input_file: str, password: str, output_file: str):
        with open(input_file, 'rb') as f:
            encrypted_data = f.read()

        salt = encrypted_data[:16]
        iv = encrypted_data[16:32]
        encrypted_data_content = encrypted_data[32:-32]
        original_hash = encrypted_data[-32:]

        key = self.__generate_key(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        padded_data = decryptor.update(encrypted_data_content) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()

        computed_hash = hashlib.sha256(data).digest()
        if computed_hash != original_hash:
            raise ValueError("Error de integridad: el archivo descifrado no coincide con el original.")

        with open(output_file, 'wb') as f:
            f.write(data)
