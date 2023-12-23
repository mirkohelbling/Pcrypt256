#Config_Parser.py

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
        return ConfigParser.config_data.get("fileType", "")
    
    @staticmethod
    def getAlgorithm():
        ConfigParser.readConfig()
        return ConfigParser.config_data.get("algorithm", "")

