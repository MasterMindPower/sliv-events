import os
import zlib
from cryptography.fernet import Fernet

FERNET_KEY = os.environ.get("FERNET_KEY")
PRIVATE_REPO_URL = os.environ.get("PRIVATE_REPO_URL")

if not FERNET_KEY:
    raise Exception("FERNET_KEY environment variable not set")
if not PRIVATE_REPO_URL:
    raise Exception("PRIVATE_REPO_URL environment variable not set")

fernet = Fernet(FERNET_KEY.encode())

with open("script/main-enc-new.py", "rb") as f:
    encrypted_script = f.read()

decompressed = zlib.decompress(fernet.decrypt(encrypted_script))

# Pass the PRIVATE_REPO_URL into the decrypted script's globals before exec
globals_dict = {"PRIVATE_REPO_URL": PRIVATE_REPO_URL}

exec(decompressed, globals_dict)
