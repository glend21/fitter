'''
    GD 20210214

    Configuration file handling
'''

import os
import configparser


class FitConfig():
    ''' Proxy for the configuration data '''
    AppRoot = "FITROOT"

    def __init__( self ):
        ''' Ctor '''
        try:
            self._rootdir = os.environ[ self.AppRoot ]
        except KeyError:
            # Can't continue
            raise EnvironmentError( "'FITROOT' is not defined." )

        self.cfg = configparser.ConfigParser()
        self.cfg.read( os.path.join( self._rootdir, "etc", "fit.cfg" ) )
        if not self.cfg.sections():
            raise EnvironmentError( "Could not read from config file" )


    # Getters
    def get_log_dir( self ):
        return self._get_value( "PATHS", "LOG_DIR" )

    def get_import_dir( self ):
        return self._get_value( "PATHS", "IMPORT_DIR" )

    def get_data_dir( self ):
        return self._get_value( "PATHS", "DATA_DIR" )



    # protected:
    def _get_value( self, section, name ):
        ''' Internal generic get '''
        try:
            val = self.cfg[ section ][ name ]
        except KeyError as ex:
            # Logging is next on the TODO list
            print( "ERR: %s" % ex )
            val = None

        return val


# Singleton instance
config = FitConfig()
