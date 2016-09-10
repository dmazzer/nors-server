""" 
config.py: Program Configuration Manager 

"""

__author__ = "Daniel Mazzer"
__copyright__ = "Copyright 2016, NORS project"
__credits__ = ""
__license__ = "MIT"
__maintainer__ = "Daniel Mazzer"
__email__ = "dmazzer@gmail.com"

from configparser import ConfigParser
from configparser import RawConfigParser
from optparse import OptionParser
from norsutils.logmsgs.logger import Logger

logger = Logger('info')

parser = OptionParser(usage="%prog: [options]")
parser.add_option("-c", "--config-filename", action="store", type="string", dest="config_filename", help="load configuration file")
(options, args) = parser.parse_args()
if(str(options.config_filename) == "None"):
    logger.log("ERROR: config-filename cannot be empty", 'error')
    quit()

class Nors_Configuration:
    def __init__(self, filename=None):
        
        logger.log("Configuration - Started", 'debug')

        if filename is None:
            self.config_filename = options.config_filename
        else:
            self.config_filename = filename
        self.config = self.__LoadConfigFile(self.config_filename)

    def __LoadConfigFile(self, config_filename):
        try:
            
            # ConfigParser initialization and configuration file read
            config = RawConfigParser()
            config.read(config_filename)
            return config
            
        except Exception as inst:
            logger.log("Problem reading configuration file", 'error')
            logger.log(inst)
            raise
        
    def __SaveConfigFile(self, config, config_filename, section, option, value):
        try:
            config.set(section, option, value)
            with open(config_filename, 'wb') as filetowrite:
                logger.log('Saving configuration file', 'debug')
                config.write(filetowrite)

        except Exception as inst:
            logger.log("Problem writing configuration file", 'error')
            logger.log(inst)
            raise
    
    def ReadConfig(self, section, option):
        try:
            value = self.config.get(section,option)
            return value
        except Exception as inst:
            logger.log("Problem reading configuration file", 'error')
            logger.log(inst)
            return None

    def SaveConfig(self, section, option, value):
        self.__SaveConfigFile(self.config, self.config_filename, section, option, value)
        
        
        