# !/usr/bin/env python3
# Pcrypt_CLI.py

# Standard library imports
import sys
# Third-party imports
import hashlib as hashlib
from getpass import getpass
from random import randint
from functools import partial
import argparse
# Local application/library specific imports
from Encryption_Manager import EncryptionManager
from Credential_Manager import CredentialManager
from File_Manager import FileManager

class PcryptCLI:

    def encryptFile(file, secret, nonce):
        FileManager.processBar(file, "Encryption")
        em = EncryptionManager(secret, nonce)
        em.encryptFile(file)

    def decryptFile(file, secret, nonce):
        FileManager.processBar(file, "Decryption")
        em = EncryptionManager(secret, nonce)
        fileHash = em.decryptFile(file)
        CredentialManager.verifyFileIntegrity(file, fileHash)

    def main(argv):

        parser = argparse.ArgumentParser(description='PCrypt256 - File Encryption Tool\n\n'
        'OooOOo.     .oOOOo. \n'                                                
        'O      O .O     o                           .oOOo. OooOOo .oOOo.\n'
        'o      O o                              O        O o      O\n '     
        'O     .o o                             oOo       o O      o \n'      
        'oOooOO   o          OoOo. O   o .oOo.   o       O  ooOOo. OoOOo.\n' 
        'o        O          o     o   O O   o   O      O        O O    O\n'
        'O         o     .o  O     O   o o   O   o    .O         o O    o\n' 
        'o          OoooO    o      OoOO oOoO     oO oOoOoO  OooO   OooO \n' 
        '                              O 0                               \n'
        '                              o 0                               \n',
        formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("-eF", "--encrypt_file", required=False, help="Encrypt a single file", nargs=1)
        parser.add_argument("-dF", "--decrypt_file", required=False, help="Decrypt a single file", nargs=1)
        parser.add_argument("-eD", "--encrypt_directory", required=False, help="Encrypt all files of a single directory (containing all subdirectories)", nargs=1)
        parser.add_argument("-dD", "--decrypt_directory", required=False, help="Decrypt all files of a single directory (containing all subdirectories)", nargs=1)
    
        args = parser.parse_args()
        
        if len(sys.argv) == 1:
            args.status = True

        if args.encrypt_file:
            file = args.encrypt_file[0]
            if not FileManager.checkFile(file):
                print(f"Error:{file} does not exist")
                sys.exit(0)
            secret, nonce = CredentialManager.createSecret()
            PcryptCLI.encryptFile(file, secret, nonce)
            print(f"\n")

        
        elif args.decrypt_file:
            file = args.decrypt_file[0]
            if not FileManager.checkFile(file):
                print(f"Error:{file} does not exist")
                sys.exit(0)
            secret, nonce = CredentialManager.verifySecret(file)
            PcryptCLI.decryptFile(file, secret, nonce)
            print(f"\n")
        
        elif args.encrypt_directory:
            dir = args.encrypt_directory[0]
            files=FileManager.getAllFiles(dir)
            secret, nonce = CredentialManager.createSecret()
            for file in files:
                PcryptCLI.encryptFile(str(file), secret, nonce)
                print(f"\n")
            print(f"\n")

        elif args.decrypt_directory:
            dir = args.decrypt_directory[0]
            files=FileManager.getAllFiles(dir)
            secret, nonce = CredentialManager.createSecret()
            for file in files:
                PcryptCLI.decryptFile(str(file), secret, nonce)
                print(f"\n")
            print(f"\n")

if __name__ == "__main__":
    pcryptCLI = PcryptCLI()
    pcryptCLI.main()

