# Reporte Final de Ciberseguridad

**Integrantes:**
- Juan Felipe Castillo Gómez
- Juan Camilo Ramírez Tabares

## Cómo realizamos el proyecto

### Elección de tecnologías y arquitectura
El primer paso fue definir las tecnologías que usaríamos para desarrollar el proyecto. Decidimos utilizar una arquitectura web clásica de cliente-servidor, eligiendo Python como lenguaje principal para el modelo, empleando el framework Flask.

Tambien, optamos por implementar toda la lógica de cifrado y descifrado usando programación orientada a objetos.

### Implementación de la lógica de negocio
Como parte de la implementación del cifrado y descifrado, estudiamos la estructura de cada algoritmo para identificar los requisitos y entender su funcionamiento. Nos apoyamos en ChatGPT y en apuntes de clase (Semana 3) para guiar la implementación.

Definimos que necesitábamos un algoritmo para generar la clave a partir de una contraseña en formato de texto (string). El ejercicio especificaba que la contraseña debía emplear el algoritmo PBKDF2 y generar una clave de 256 bits.

[Imagen del Código]

A continuación, se solicitó que cifráramos el archivo utilizando el algoritmo AES. Implementamos AES en modo CBC, ya que ofrece mayor seguridad al asegurar que dos archivos cifrados con la misma clave no generen la misma salida.

También se solicitaba adjuntar el hash SHA-256 del archivo original para comparar la integridad al descifrarlo en el futuro.

[Imagen del Código]

Por último, el proceso de descifrado sigue el mismo procedimiento, pero a la inversa. Implementamos el cálculo de la clave, el algoritmo de descifrado AES en modo CBC, y la comparación del hash del archivo original con el del archivo descifrado para asegurar la integridad de la salida.

[Imagen del Código]

## Dificultades que enfrentamos

## Conclusiones
