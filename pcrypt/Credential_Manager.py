# Credential_Manager.py 

# Standard library imports
from os import sys
# Third-party imports
import hashlib as hashlib
from getpass import getpass
import xml.etree.ElementTree as et
import base64
# Local application/library specific imports
from Config_Parser import ConfigParser

class CredentialManager:
    
    @staticmethod
    def createSecret():
        clearSecret = getpass(f"Enter Secret: ")
        hashedSecret = hashlib.sha256(clearSecret.encode(encoding="utf8")).digest()
        nonce = hashlib.sha256(hashedSecret).digest()[0:16]
        return hashedSecret, nonce
    
    @staticmethod
    def verifySecret(file_name):
        clearSecret = getpass(f"Enter Secret: ")
        hashedSecret = hashlib.sha256(clearSecret.encode(encoding="utf8")).digest()
        nonce = hashlib.sha256(hashedSecret).digest()[0:16]
        file = et.parse(file_name)
        if not CredentialManager.compareValues((base64.b64decode(file.findtext("secret"))), hashedSecret):
            print(f"Error: Secret do not match")
        return hashedSecret, nonce
    
    @staticmethod
    def verifyFileIntegrity(file_name, fileHash):
        file = et.parse(file_name)
        if not CredentialManager.compareValues(base64.b64decode(file.findtext("fileHash")), fileHash):
            print("Error: File integrity mismatch")

    @staticmethod
    def compareValues(val1, val2):
        return val1 == val2
