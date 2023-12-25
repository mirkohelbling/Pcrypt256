# Standard library imports
import os
from datetime import datetime
import xml.etree.ElementTree as et
import hashlib
import base64

# Third-party imports
from tqdm import tqdm
from termcolor import colored, cprint
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Local application/library specific imports
from Config_Parser import ConfigParser

class EncryptionManager:

    template_file = et.Element("file")

    def __init__(self, secret, nonce, mode=modes.CTR):
        self.secret = secret
        self.nonce = nonce
        self.authTag = None
        self.context = Cipher(algorithms.AES(secret), mode(nonce), backend=default_backend())
        self.encryptor = self.context.encryptor()
        self.decryptor = self.context.decryptor()

    def updateEncryptor(self, plaintext):
        return self.encryptor.update(plaintext)

    def finalizeEncryptor(self):
        return self.encryptor.finalize()

    def updateDecryptor(self, ciphertext):
        return self.decryptor.update(ciphertext)

    def finalizeDecryptor(self):
        return self.decryptor.finalize()

    def encryptFile(self, origin_file_name):

        with open(origin_file_name, 'rb') as fo:
            plaintext = fo.read()

        secretXml = et.SubElement(self.template_file, "secret")
        secretXml.text = base64.b64encode(self.secret).decode("ascii")

        fileHashXml = et.SubElement(self.template_file, "fileHash", algorithm="SHA512")
        fileHashXml.text = base64.b64encode(hashlib.sha512(plaintext).digest()).decode("ascii")

        dateXml = et.SubElement(self.template_file, "timestamp")
        dateXml.text = datetime.now().strftime("%H:%M:%S" + " " + "%d:%m:%y")

        algorithmXml = et.SubElement(self.template_file, "algorithm", mode="CTR")
        algorithmXml.text = ConfigParser.getAlgorithm()

        self.authTag = os.urandom(16)
        authTagXml = et.SubElement(self.template_file, "authTag")
        authTagXml.text = base64.b64encode(self.authTag).decode("ascii")

        ciphertext = self.updateEncryptor(plaintext) + self.finalizeEncryptor()
        dataXml = et.SubElement(self.template_file, "data")
        dataXml.text = base64.b64encode(ciphertext).decode("ascii")

        tree = et.ElementTree(self.template_file)
        tree.write(origin_file_name + ConfigParser.getFileType())

        fo.close()

    def decryptFile(self, file_name):
        file = et.parse(file_name)

        ciphertext = base64.b64decode(file.findtext("data"))
        authTag = base64.b64decode(file.findtext("authTag"))

        # Update with ciphertext and finalize with an empty byte string
        data = self.updateDecryptor(ciphertext) + self.finalizeDecryptor()

        file_name_new = file_name[:-len(".secret.xml")]

        with open(file_name_new, 'wb') as fo:
            fo.write(data)
        fo.close()

        return hashlib.sha512(data).digest()


    def encryptFiles(self, directory):
        assert os.path.isdir(directory)

        files = self.getAllFiles(directory)
        for file_name in files:
            self.encryptFile(file_name)

    def decryptFiles(self, directory):
        files = self.getAllFiles(directory)
        for file_name in files:
            self.decryptFile(file_name)
