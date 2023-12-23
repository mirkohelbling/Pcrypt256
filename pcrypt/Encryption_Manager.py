#Encryption_Manager.py

# Standard library imports
import os
# Third-party imports
from tqdm import tqdm
from termcolor import colored,cprint
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from datetime import datetime
import xml.etree.ElementTree as et
import hashlib as hashlib
import base64
# Local application/library specific imports
from Config_Parser import ConfigParser

class EncryptionManager:
    """_summary_
    """


    file = et.Element("file")
           
    def __init__(self, secret, nonce):
        """_summary_

        Args:
            key (_type_): _description_
            nonce (_type_): _description_
        """
        self.secret = secret
        self.nonce = nonce
        #self.context = Cipher(algorithms.AES(secret), modes.GCM(nonce), backend=default_backend())
        self.context = Cipher(algorithms.AES(secret),modes.CTR(nonce),backend=default_backend())
        self.encryptor = self.context.encryptor()
        self.decryptor = self.context.decryptor()

    def updateEncryptor(self, plaintext):
        """_summary_

        Args:
            plaintext (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.encryptor.update(plaintext)

    def finalizeEncryptor(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.encryptor.finalize()

    def updateDecryptor(self, ciphertext):
        """_summary_

        Args:
            ciphertext (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.decryptor.update(ciphertext)

    def finalizeDecryptor(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.decryptor.finalize()

    def encryptFile(self, file):
        """_summary_

        Args:
            file_name (_type_): _description_
        """
        with open(file, 'rb') as fo:
            plaintext = fo.read()
        
        secretXml = et.SubElement(self.file, "secret")
        secretXml.text = (base64.b64encode(self.secret).decode("ascii"))
  
        fileHashXml = et.SubElement(self.file, "fileHash", algorithm="SHA512")
        fileHashXml.text = base64.b64encode(hashlib.sha512(plaintext).digest()).decode("ascii")

        dateXml = et.SubElement(self.file, "timestamp")
        dateXml.text = datetime.now().strftime("%H:%M:%S"+" "+ "%d:%m:%y")

        algorithmXml = et.SubElement(self.file, "algorithm", mode="CTR")
        algorithmXml.text = ConfigParser.getAlgorithm()

        ciphertext = self.updateEncryptor(plaintext) + self.finalizeEncryptor()
        dataXml = et.SubElement(self.file, "data")
     
        dataXml.text = base64.b64encode(ciphertext).decode("ascii")

        tree = et.ElementTree(self.file)
        tree.write(file + ConfigParser.getFileType())
        #os.remove(file_name)

    def decryptFile(self, file_name):
        """_summary_

        Args:
            file_name (_type_): _description_
        """
        
        file = et.parse(file_name + ConfigParser.getFileType())
        
        ciphertext = base64.b64decode(file.findtext("data"))
        data = self.updateDecryptor(ciphertext) + self.finalizeDecryptor()
        with open(file_name, 'wb') as fo:
            fo.write(data)
        return hashlib.sha512(data).digest()
        #os.remove(file_name)

    def encryptFiles(self, __dir__):
        """_summary_
        """
        assert os.path.isdir(__dir__)

        files= self.getAllFiles(__dir__)
        for file_name in files:
            self.encryptFile(file_name)
            #print("\n"+file_name)

    def decryptFiles(self, __dir__):
        """_summary_
        """
        files = self.getAllFiles(__dir__)
        for file_name in files:
            self.decryptFile(file_name)


