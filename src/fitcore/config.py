'''
    GD 20210214

    Configuration file handling
'''

import os
import logging
import configparser
from pathlib import Path


# pylint: disable=too-few-public-methods
class FitConfig():
    ''' Proxy for the configuration data '''
    AppRoot = "FITROOT"

    def __init__( self ):
        ''' Ctor '''
        try:
            self._rootdir = os.environ[ self.AppRoot ]
        except KeyError as ex:
            # Can't continue
            raise EnvironmentError( "'FITROOT' is not defined." ) from ex

        self.cfg = configparser.ConfigParser()
        self.cfg.read( Path( self._rootdir ) / "etc" / "fit.cfg" )
        if not self.cfg.sections():
            raise EnvironmentError( "Could not read from config file" )

    def get_value( self, section, name ):
        ''' Internal generic get '''
        try:
            val = self.cfg[ section ][ name ]
        except KeyError as ex:
            logging.error( "ERR: %s", ex )
            val = None

        return val


# Singleton instance
__CONFIG = FitConfig()


# Getters
def get_log_dir():
    return __CONFIG.get_value( "PATHS", "LOG_DIR" )

def get_import_dir():
    return __CONFIG.get_value( "PATHS", "IMPORT_DIR" )

def get_data_dir():
    return __CONFIG.get_value( "PATHS", "DATA_DIR" )

def get_static_dir():
    return __CONFIG.get_value( "PATHS", "STATIC_DIR" )
