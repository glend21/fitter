'''
    GD 20210214

    Utility functions
'''


def session_to_wid( idx, sess ):
    ''' Converts a session dictionary to an id string '''
    return "/%04d%02d%02d-%02d" % (sess[ 'year' ], sess[ 'month'], sess[ 'day' ], idx)
 


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
 