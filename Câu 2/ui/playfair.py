"""
ui/playfair.py
Cua so giao dien Playfair Cipher, load tu file ui/playfair.ui (Qt Designer).
Goi toi API Flask (api.py) de dat khoa, lay ma tran, ma hoa va giai ma.
"""
import os
import sys

import requests
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

API_BASE_URL = "http://localhost:5000/api/playfair"


class PlayfairWindow(QWidget):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "playfair.ui")
        uic.loadUi(ui_path, self)

        self.setKeyButton.clicked.connect(self.handle_set_key)
        self.encryptButton.clicked.connect(self.handle_encrypt)
        self.decryptButton.clicked.connect(self.handle_decrypt)
        self.clearButton.clicked.connect(self.handle_clear)

    def handle_set_key(self):
        key = self.keyLineEdit.text().strip()
        if not key:
            QMessageBox.warning(self, "Thiếu dữ liệu", "Vui lòng nhập khoá.")
            return
        try:
            requests.post(f"{API_BASE_URL}/set_key", json={"key": key}, timeout=5)
            resp = requests.get(f"{API_BASE_URL}/matrix", timeout=5)
            matrix = resp.json()["matrix"]
            self.matrixDisplay.setPlainText("\n".join("  ".join(row) for row in matrix))
            self.statusLabel.setText(f"Đã đặt khoá: {key}")
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Lỗi", "Không kết nối được API. Hãy chạy api.py trước (python api.py).")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def handle_encrypt(self):
        message = self.inputTextEdit.toPlainText().strip()
        if not message:
            QMessageBox.warning(self, "Thiếu dữ liệu", "Vui lòng nhập văn bản cần mã hoá.")
            return
        try:
            resp = requests.post(f"{API_BASE_URL}/encrypt", json={"message": message}, timeout=5)
            data = resp.json()
            if "error" in data:
                QMessageBox.critical(self, "Lỗi", data["error"])
                return
            self.outputTextEdit.setPlainText(data["encrypted_message"])
            self.statusLabel.setText("Đã mã hoá thành công.")
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Lỗi", "Không kết nối được API. Hãy chạy api.py trước (python api.py).")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def handle_decrypt(self):
        ciphertext = self.inputTextEdit.toPlainText().strip()
        if not ciphertext:
            QMessageBox.warning(self, "Thiếu dữ liệu", "Vui lòng nhập văn bản cần giải mã.")
            return
        try:
            resp = requests.post(f"{API_BASE_URL}/decrypt", json={"ciphertext": ciphertext}, timeout=5)
            data = resp.json()
            if "error" in data:
                QMessageBox.critical(self, "Lỗi", data["error"])
                return
            self.outputTextEdit.setPlainText(data["decrypted_message"])
            self.statusLabel.setText("Đã giải mã thành công.")
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Lỗi", "Không kết nối được API. Hãy chạy api.py trước (python api.py).")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def handle_clear(self):
        self.inputTextEdit.clear()
        self.outputTextEdit.clear()
        self.statusLabel.setText("")


def main():
    app = QApplication(sys.argv)
    window = PlayfairWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
