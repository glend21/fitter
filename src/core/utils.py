'''
    GD 20210214

    Utility functions
'''

__dummywid = "yyyymmdd-nn"


def session_to_wid( idx, sess ):
    ''' Converts a session dictionary to an id string '''
    try:
        return "/%04d%02d%02d-%02d" % (sess[ 'year' ], sess[ 'month'], sess[ 'day' ], idx)
    except KeyError as ex:
        # FIXME LOGGING
        print( "ERR: %s" % s )
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
    ''' Creates (globbable string from the workout id, i'th session of day) from the wo id string '''
    if len( wid ) == len( __dummywid ):
        return ( int( wid[ -2 : ] ),
                 "Move_%s_%s_%s*.dfz" % (wid[ : 4 ], wid[ 4 : 6 ], wid[ 6 : 8 ])
               )
               
    return (-1, None)