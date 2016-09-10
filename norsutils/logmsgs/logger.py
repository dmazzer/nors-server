import logging

class Logger():
    def __init__(self, level='info'):
        
        levels =  {
                    'debug':logging.DEBUG,
                    'info':logging.INFO,
                    'critical':logging.CRITICAL,
                    'error':logging.ERROR,
                    'fatal':logging.FATAL,
                    'warning':logging.WARNING,
                   }
  
        setlevel = levels.get(level, logging.NOTSET)
        
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=setlevel,
                        format='[%(asctime)s %(threadName)s] %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S')
    
    def log(self, msg, level='info'):
        levelsfun =  {
                    'debug':self.logger.debug,
                    'info':self.logger.info,
                    'critical':self.logger.critical,
                    'error':self.logger.error,
                    'fatal':self.logger.fatal,
                    'warning':self.logger.warning,
                   }
        self.setlevelfun = levelsfun.get(level, self.logger.info)
        self.setlevelfun(msg)
        
