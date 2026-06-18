from flask import Flask, request, jsonify
from cipher.playfair import PlayfairCipher

app = Flask(__name__)

# PLAYFAIR CIPHER ALGORITHM
playfair_cipher = PlayfairCipher()

@app.route('/api/playfair/set_key', methods=['POST'])
def playfair_set_key():
    data = request.json
    key = data['key']
    playfair_cipher.set_key(key)
    return jsonify({'message': 'Key set successfully', 'key': key})

@app.route('/api/playfair/matrix', methods=['GET'])
def playfair_get_matrix():
    key = playfair_cipher.load_key()
    matrix = playfair_cipher.get_matrix(key)
    return jsonify({'key': key, 'matrix': matrix})

@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    data = request.json
    message = data['message']
    key = playfair_cipher.load_key()
    encrypted_message = playfair_cipher.encrypt(message, key)
    return jsonify({'encrypted_message': encrypted_message})

@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    data = request.json
    ciphertext = data['ciphertext']
    key = playfair_cipher.load_key()
    decrypted_message = playfair_cipher.decrypt(ciphertext, key)
    return jsonify({'decrypted_message': decrypted_message})




# main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
