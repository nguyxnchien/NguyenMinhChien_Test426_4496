"""
playfair_cipher.py
Class PlayfairCipher: dong goi thuat toan Playfair Cipher theo phong cach
giong RSACipher (set_key/load_key thay cho generate_keys/load_keys,
vi Playfair la ma hoa doi xung, khoa do nguoi dung tu chon).
"""
import os
import json

KEY_FILE = os.path.join(os.path.dirname(__file__), "keys", "playfairKey.json")


class PlayfairCipher:
    def __init__(self):
        self.key = None

    # ----- Quan ly khoa (tuong tu generate_keys/load_keys cua RSACipher) -----

    def set_key(self, key: str):
        """Luu khoa Playfair (chuoi ky tu) vao file, tuong tu generate_keys()
        cua RSA nhung o day nguoi dung tu cung cap khoa thay vi sinh ngau nhien."""
        if not key:
            raise ValueError("Khoa khong duoc de trong.")

        os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
        with open(KEY_FILE, "w", encoding="utf-8") as f:
            json.dump({"key": key}, f)

        self.key = key
        return self.key

    def load_key(self) -> str:
        """Doc khoa da luu tu file, tuong tu load_keys() cua RSA."""
        if self.key:
            return self.key

        if not os.path.exists(KEY_FILE):
            raise FileNotFoundError("Chua co khoa nao duoc thiet lap. Hay goi set_key truoc.")

        with open(KEY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.key = data["key"]
        return self.key

    # ----- Sinh ma tran khoa 5x5 -----

    def get_matrix(self, key: str = None):
        key = key or self.load_key()
        key = key.upper().replace("J", "I")
        key = "".join(filter(str.isalpha, key))

        seen = set()
        matrix_chars = []

        for ch in key:
            if ch not in seen:
                seen.add(ch)
                matrix_chars.append(ch)

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # khong co J
        for ch in alphabet:
            if ch not in seen:
                seen.add(ch)
                matrix_chars.append(ch)

        return [matrix_chars[i:i + 5] for i in range(0, 25, 5)]

    @staticmethod
    def matrix_to_string(matrix) -> str:
        return "\n".join("  ".join(row) for row in matrix)

    @staticmethod
    def _find_position(matrix, ch):
        for r, row in enumerate(matrix):
            for c, val in enumerate(row):
                if val == ch:
                    return r, c
        return None

    @staticmethod
    def _prepare_text(text: str):
        text = text.upper().replace("J", "I")
        text = "".join(filter(str.isalpha, text))

        prepared = []
        i = 0
        while i < len(text):
            a = text[i]
            if i + 1 < len(text):
                b = text[i + 1]
                if a == b:
                    prepared.append(a + "X")
                    i += 1
                else:
                    prepared.append(a + b)
                    i += 2
            else:
                prepared.append(a + "X")
                i += 1
        return prepared

    # ----- Ma hoa / giai ma -----

    def encrypt(self, message: str, key: str = None) -> str:
        key = key or self.load_key()
        matrix = self.get_matrix(key)
        digraphs = self._prepare_text(message)
        result = []

        for pair in digraphs:
            a, b = pair[0], pair[1]
            ra, ca = self._find_position(matrix, a)
            rb, cb = self._find_position(matrix, b)

            if ra == rb:  # cung hang -> dich phai
                result.append(matrix[ra][(ca + 1) % 5])
                result.append(matrix[rb][(cb + 1) % 5])
            elif ca == cb:  # cung cot -> dich xuong
                result.append(matrix[(ra + 1) % 5][ca])
                result.append(matrix[(rb + 1) % 5][cb])
            else:  # hinh chu nhat -> doi cot
                result.append(matrix[ra][cb])
                result.append(matrix[rb][ca])

        return "".join(result)

    def decrypt(self, ciphertext: str, key: str = None) -> str:
        key = key or self.load_key()
        matrix = self.get_matrix(key)

        ciphertext = ciphertext.upper().replace("J", "I")
        ciphertext = "".join(filter(str.isalpha, ciphertext))
        digraphs = [ciphertext[i:i + 2] for i in range(0, len(ciphertext), 2)]
        result = []

        for pair in digraphs:
            if len(pair) < 2:
                continue
            a, b = pair[0], pair[1]
            ra, ca = self._find_position(matrix, a)
            rb, cb = self._find_position(matrix, b)

            if ra == rb:  # cung hang -> dich trai
                result.append(matrix[ra][(ca - 1) % 5])
                result.append(matrix[rb][(cb - 1) % 5])
            elif ca == cb:  # cung cot -> dich len
                result.append(matrix[(ra - 1) % 5][ca])
                result.append(matrix[(rb - 1) % 5][cb])
            else:  # doi cot nguoc lai
                result.append(matrix[ra][cb])
                result.append(matrix[rb][ca])

        return "".join(result)
