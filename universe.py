from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.Hash import SHA
import base64
import util
from alien_translator import AlienTranslator


class UniverseGod:

    def __init__(self):

        with open('master-private.pem') as f:
            self.rsa_private_key = RSA.importKey(f.read())

        with open('master-public.pem') as f:
            self.rsa_public_key = RSA.importKey(f.read())

        self.date = None
        self.time_signature = None

    def gen_current_time_signature(self):
        now = util.gen_date()
        if self.date and self.time_signature and now == self.date:
            return self.time_signature

        self.time_signature = self._gen_signature(now)
        self.date = util.gen_date()

        return self.time_signature

    def gen_passed_time_signature(self, time):
        if time > util.gen_date():
            return "INVALID DATE"

        self.time_signature = self._gen_signature(time)
        self.date = util.gen_date()

        return self.time_signature

    def _gen_signature(self, message):
        signer = Signature_pkcs1_v1_5.new(self.rsa_private_key)
        digest = SHA.new()
        digest.update(message.encode())
        sign = signer.sign(digest)
        signature = base64.b64encode(sign)

        return signature

    def gen_future_code(self, date, message):
        time_signature = self._gen_signature(date)
        translator = AlienTranslator(time_signature)

        return translator.encrypt_to_code(message)



