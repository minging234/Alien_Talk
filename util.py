import hashlib
import datetime
from Crypto import Random
from Crypto.PublicKey import RSA


m2e_dic = {0: "🤑", 1: "😂", 2: "😐", 3: "👍", 4: "😘", 5: "😔", 6: "😳", 7: "💁", 8: "🙀",
           9: "🙊", 10: "👀", 11: "😎", 12: "😇", 13: "🤣", 14: "😏", 15: "🤩", 16: "🤨", 17: "🤪",
           18: "🧐", 19: "🤓", 20: "🤯", 21: "😨", 22: "🤔", 23: "😶", 24: "🤥", 25: "🙄", 26: "🤤", 27: "🤗",
           28: "😮", 29: "🤢", 30: "🤠", 31: "👌"}

e2m_dic = {}

for m in m2e_dic.keys():
    e2m_dic[m2e_dic[m]] = m


def gen_rsa():
    random_generator = Random.new().read

    rsa = RSA.generate(1024, random_generator)

    private_pem = rsa.exportKey()
    with open('master-private.pem', 'wb') as f:
        f.write(private_pem)

    public_pem = rsa.publickey().exportKey()
    with open('master-public.pem', 'wb') as f:
        f.write(public_pem)


def bytes_to_code(ct):
    raw_code_num = int.from_bytes(ct, byteorder='big')
    code_text = ""

    while raw_code_num > 0:
        code_text += m2e_dic[raw_code_num & 15]
        raw_code_num = raw_code_num >> 4

    return code_text


def code_to_bytes(code):
    raw_code_num = 0
    end = len(code)
    blen = 0

    for i in range(len(code) - 1, -1, -1):
        if code[i:end] in e2m_dic:
            raw_code_num = raw_code_num << 4
            raw_code_num = raw_code_num | e2m_dic[code[i:end]]
            end = i
            blen += 1

    return raw_code_num.to_bytes(blen // 2, byteorder='big')


def gen_key(keywords):
    if type(keywords) == str:
        keywords = keywords.encode()
    block = hashlib.sha1(keywords).digest()
    for i in range(4):
        n_block = hashlib.sha1(block).digest()
        block = block + n_block

    return block[:32], block[-16:]


def gen_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")


def gen_padding():
    return Random.new().read(8)


def get_public_key():
    with open('master-public.pem') as f:
        public_key = f.read()
    return public_key


def mask_data(data, mask):
    l = 0
    stream = bytearray(data)
    while l < len(data):
        i = 0
        while l < len(data) and i < len(mask):
            stream[l] = stream[l] ^ mask[i]
            i += 1
            l += 1

    return bytes(stream)



