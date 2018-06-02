import hashlib
import base64
import sys

with open(sys.argv[1], "rb") as f:
    print base64.b64encode(hashlib.sha512(f.read()).digest())
