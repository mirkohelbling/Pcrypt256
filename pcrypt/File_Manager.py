#File_Manager.py
# Standard library imports
from os import sys
import time
# Third-party imports
from pathlib import Path
from math import ceil
# Local application/library specific imports
from Config_Parser import ConfigParser

class FileManager:

    
    @staticmethod
    def checkFile(file_name, expected_ending="*.*")-> bool:
        file_path = Path(file_name)
        try:
                assert FileManager.checkFileType(file_path)
                assert file_path.exists()       
        except AssertionError as e:
                return False
        return True
    
    @staticmethod
    def checkFileType(file_path):
        # Check if the file type (extension) is in the list of allowed extensions
        return any(file_path.suffix.lower() == ext.lower() for ext in ConfigParser.getSupportedFiles())
    
    @staticmethod
    def getFileSize(file)->int:
        path=Path(file)
        if path.is_file():
            # Use the stat method to get file information
            file_stat = path.stat()
            # Access the st_size attribute to get the file size in bytes
            file_size = file_stat.st_size
        return file_size
    
    @staticmethod
    def processBar(file,task="",length=30):
        size = FileManager.getFileSize(file)
        path=Path(file)
        iterations= max(1, ceil(size / 1e6)) # Using 1e6 MB for an iteration
        for i in range(iterations + 1):
            percent = (i / iterations) * 100
            filled_length = int(length * i // iterations)
            bar = '█' * filled_length + '-' * (length - filled_length)
            sys.stdout.write(f'\r{path.name} |{bar}| {percent:.1f}% {ConfigParser.getAlgorithm()} {task} Complete')
            sys.stdout.flush()
            time.sleep(0.1)

    @staticmethod
    def getAllUncryptedFiles(dir) -> list:
        dir_path = Path(dir)
        uFiles = [file for file in dir_path.rglob('*') if file.is_file() and not file.name.endswith(ConfigParser.getFileType())]
        return uFiles

    @staticmethod
    def getAllEncryptedFiles(dir) -> list:
        files = Path(dir)
        eFiles = [file for file in files.rglob('*'+ConfigParser.getFileType()) if file.is_file()]
        return eFiles
