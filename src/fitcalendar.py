'''
    GD 20210208

    Calendar functionality
'''

import os
import sys
import datetime
import glob


# Hard-coded for the moment .. see the github issue re. proper config
_DATADIR = "../data"


class Calendar():
    ''' Calendar class '''

    def __init__( self, year=2021, month=1 ):
        ''' Ctor '''

        if not (year > 0 and month > 0):
            raise ValueError( "Invalid date (y=%d, m=%d)" % (year, month) )

        self.year = year
        self.month = month
        self.sessions = []

        self._doInit()


    # public:
    def get_monthly( self ):
        ''' Returns the summary data for the month '''
        return self.sessions


    # protected:
    def _doInit( self ):
        ''' Build a list of sessions for the given year-month '''
        fspec = os.path.join( _DATADIR, "Move_%04d_%02d*.df" % (self.year, self.month) )
        files = glob.glob( fspec )

        for f in files:
            base = os.path.splitext( f )[ 0 ]
            parts = base.split( '_' )
            day = parts[ 3 ]
            activity = parts[ -1 ]  # part after last underscore
            self.sessions.append(
                    { 'day' : day,
                      'month' : self.month,
                      'year' : self.year,
                      'fname' : f,
                      'activity' : activity
                    }
                )



def test( argc, argv ):
    ''' unit testing '''

    cal = Calendar( 2019 )
    print( cal.get_monthly() )



if __name__ == "__main__":
    test( len( sys.argv ), sys.argv )
