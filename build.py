"""把 letters.json 加密成 letters.enc.json。
用法： python3 build.py 你的密码
letters.json 是明文原稿，不要上传；只上传 letters.enc.json。
"""
import json, os, sys, base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ITER = 200_000

def main():
    if len(sys.argv) < 2:
        sys.exit("用法: python3 build.py 密码")
    pw = sys.argv[1].encode()
    here = os.path.dirname(os.path.abspath(__file__))
    letters = json.load(open(os.path.join(here, "letters.json"), encoding="utf-8"))
    salt, iv = os.urandom(16), os.urandom(12)
    key = PBKDF2HMAC(hashes.SHA256(), 32, salt, ITER).derive(pw)
    ct = AESGCM(key).encrypt(iv, json.dumps(letters, ensure_ascii=False).encode(), None)
    b = lambda x: base64.b64encode(x).decode()
    out = {"v": 1, "iter": ITER, "salt": b(salt), "iv": b(iv), "data": b(ct)}
    json.dump(out, open(os.path.join(here, "letters.enc.json"), "w"))
    # 每次打包都给缓存换个新版本号，手机上才会拿到新的信
    import re, time
    swp = os.path.join(here, "sw.js")
    sw = open(swp, encoding="utf-8").read()
    ver = "mailbox-" + time.strftime("%Y%m%d-%H%M%S")
    sw = re.sub(r'const VERSION = "[^"]*";', f'const VERSION = "{ver}";', sw)
    open(swp, "w", encoding="utf-8").write(sw)
    print(f"加密好了：{len(letters)} 封信 -> letters.enc.json（缓存版本 {ver}）")

main()
