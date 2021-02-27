'''
    GD 20210214

    Utility functions
'''

import logging
from pathlib import Path

from fitcore import config


__DUMMYWID = "yyyymmdd-nn"


def init_log( exename ):
    ''' Set up logging '''
    logdir = config.get_log_dir()
    if logdir is None:
        # System init impossible
        return "ERR: Could not start system: no log dir in config file"

    logpath = Path( logdir )
    newlogdir = False
    if not logpath.is_dir():
        logpath.mkdir()
        newlogdir = True

    logname = Path( exename ).stem + ".log"
    logging.basicConfig( filename=Path( logdir ) / Path( logname ),
                         level=logging.DEBUG,
                         format="%(asctime)s %(levelname)-8s %(message)s",
                         datefmt='%m-%d %H:%M',
                         filemode="a" )

    if newlogdir:
        logging.info( "created log directory: %s", logdir )

    return ""


def session_to_wid( idx, sess ):
    ''' Converts a session dictionary to an id string '''
    try:
        return "/%04d%02d%02d-%02d" % (sess[ 'year' ], sess[ 'month'], sess[ 'day' ], idx)
    except KeyError as ex:
        logging.error( "ERR: %s", ex )
        return None


def wid_to_session( wid ):
    ''' Constructs a session dictionary from an id string '''
    pass


def components_to_session( day=None, month=None, year=None, fname=None, stype=None ):
    ''' Builds a session dict from its comonent parts '''
    return {
                'day' : int( day ),
                'month' : int( month ),
                'year' : int( year ),
                'fname' : fname,
                'type' : stype
            }


def wid_to_glob( wid ):
    ''' Creates (globbable string from the workout id, i'th session of day) from the wid string '''
    if len( wid ) == len( __DUMMYWID ):
        return ( int( wid[ -2 : ] ),
                 "Move_%s_%s_%s*.dfz" % (wid[ : 4 ], wid[ 4 : 6 ], wid[ 6 : 8 ])
               )

    return (-1, None)
