#!/usr/bin/env python2

""" 
gen_id.py: UUID Generator

"""

__author__ = "Daniel Mazzer"
__copyright__ = "Copyright 2016, NORS project"
__credits__ = ""
__license__ = "GPL"
__maintainer__ = "Daniel Mazzer"
__email__ = "dmazzer@gmail.com"


from uuid import uuid1

print("NORS - Noticia Remote Management and Supervisor")
print("Sensor ID - UUID Generator")
print("UUID: " +  str(uuid1()))
