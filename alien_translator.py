from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import util


class AlienTranslator:

    def __init__(self, keyword):
        key, IV = util.gen_key(keyword)
        self.cipher = Cipher(algorithms.AES(key), modes.CTR(IV), backend=default_backend())

    def encrypt_to_code(self, msg):
        encryptor = self.cipher.encryptor()
        if type(msg) == str:
            msg = msg.encode()

        nonce = util.gen_padding()

        msg = util.mask_data(msg, nonce) + nonce

        ct = encryptor.update(msg)

        return util.bytes_to_code(ct)

    def decrypt_to_msg(self, code):
        decryptor = self.cipher.decryptor()
        msg = decryptor.update(util.code_to_bytes(code))

        try:
            msg = util.mask_data(msg[:-8], msg[-8:])
            msg = msg.decode()
        except UnicodeDecodeError:
            msg = "ERROR KEY OR CODE"

        return msg

