""" 
kenn.py: Integration with Kenn.io 

"""

__author__ = "Daniel Mazzer"
__copyright__ = "Copyright 2016, NORS project"
__credits__ = ""
__license__ = "GPL"
__maintainer__ = "Daniel Mazzer"
__email__ = "dmazzer@gmail.com"

import keen

class Nors_KennUpload(object):
    def __init__(self):
        
    keen.project_id = "5821c49e8db53dfda8a779ee"
    keen.write_key = "B1DE8FB2F41A7CB49F214151F2D6F13A7AA7F88D53AD08428935F6B806F9955BA670414308F42611FF34B37E5FAE384E9EA0974C88180A2FF07F91EDC54286982D89B7D7BB5D5A610AD9DAD60F0EAA1760DD2DC1AED7A4D2F4099F4FC43B6FDF"

    def publish_event(self, data_event):
        keen.add_event(data_event)
    
#     keen.add_event("signups", {
#       "username": "lloyd",
#       "referred_by": "harry"
#     })