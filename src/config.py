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
            self._rootdir = =os.environ( self.AppRoot )
        except KeyError:
            # Can't continue
            raise EnvironmentError( "'FITROOT' is not defined." )

        self.cfg = configparser.ConfigParser()
        self.cfg.read( os.path.join( self._rootdir, "etc", "fit.cfg" ) )
        if not self.cfg.sections():
            raise EnvironmentError( "Could not read from config file" )


# Singleton instance
config = Config()
