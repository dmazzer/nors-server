# import logging
# 
# logger = logging.getLogger(__name__)
# logging.basicConfig(level='INFO',
#                 format='[%(asctime)s %(threadName)s] %(message)s',
#                 datefmt='%d/%m/%Y %H:%M:%S')
#     
# logger.info("teste info")        
# logger.debug("teste debug")


from logger import Logger

lllog = Logger('info')

lllog.log('teste info', 'info')
lllog.log('teste debug', 'debug')
lllog.log('teste default')
        
