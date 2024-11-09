import io
from flask import Flask, render_template, request, send_file

from model.Encryptor import Encryptor
from model.Decryptor import Decryptor


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/process', methods=['POST'])
def process():
    file = request.files['file']
    password = request.form['password']
    action = request.form['action']
    
    file_data = file.read()
    file_name = getFileName(file.filename)
    
    encryptor = Encryptor()
    decryptor = Decryptor()

    if action == "encrypt":
        encrypted_data = encryptor.encrypt(file_data, password)
        output = process_data(encrypted_data)
        return send_file(output, as_attachment=True, download_name=f"{file_name}.cif")
    
    elif action == "decrypt":
        decrypted_data = decryptor.decrypt(file_data, password)
        output = process_data(decrypted_data)

        if decrypted_data == file_data:
            return send_file(output, as_attachment=True, download_name=f"{file_name}.cif")
        else:
            return send_file(output, as_attachment=True, download_name=f"{file_name}")


    else:
        return "Acción no válida", 400

def process_data(data):
    output_file = io.BytesIO(data)
    output_file.seek(0)

    return output_file


def getFileName(file):
    return file.rsplit(".", 1)[0]

if __name__ == '__main__':
    app.run(debug=True)
