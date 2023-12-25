#Config_Parser.py
from tabulate import tabulate
import yaml

class ConfigParser:

    config_data=""

    @staticmethod
    def readConfig():
        with open("config.yaml", "r") as config_file:
            ConfigParser.config_data = yaml.safe_load(config_file)

    @staticmethod
    def getFileType():
        ConfigParser.readConfig()
        return ConfigParser.config_data.get("File_Ending", "")
    
    @staticmethod
    def getAlgorithm():
        ConfigParser.readConfig()
        return ConfigParser.config_data.get("Encryption_Algorithm", "")
    
    @staticmethod
    def getSupportedFiles():
        ConfigParser.readConfig()
        return ConfigParser.config_data.get("Supported_Files", "")
    
    @staticmethod
    def listConfig():
        ConfigParser.readConfig()

        # Check if "Supported_Files" key exists in the config_data
        supported_files = ConfigParser.config_data.get("Supported_Files", [])

        # Join the supported_files into a single string with line breaks
        supported_files_str = "\n".join(supported_files)

        print("Supported Files:")

        config_table = [
            ["Property", "Configuration"],
            ["File_Ending", ConfigParser.config_data.get("File_Ending", "")],
            ["Encryption_Algorithm", ConfigParser.config_data.get("Encryption_Algorithm", "")],
            ["Supported_Files", supported_files_str],
            # Add more properties as needed
        ]

        print(tabulate(config_table, headers="firstrow", tablefmt="fancy_grid"))
