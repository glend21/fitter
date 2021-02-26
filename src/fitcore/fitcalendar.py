'''
    GD 20210208

    Calendar functionality
'''

import os
import sys
import calendar
import pathlib

from fitcore import utils, config


class Calendar():
    ''' Calendar class '''

    def __init__( self, year=2021, month=1 ):
        ''' Ctor '''

        if not (year > 0 and month > 0):
            raise ValueError( "Invalid date (y=%d, m=%d)" % (year, month) )

        self.year = year
        self.month = month
        self.sessions = {}

        self._do_init()


    # public:
    def get_monthly( self ):
        ''' Returns the summary data for the month '''
        return self.sessions

    def get_date( self ):
        ''' Returns the year and month that this calenddar is for '''
        return (self.year, self.month)

    def get_max_days( self ):
        ''' Returns the number of days in this calendar's month '''
        return calendar.monthrange( self.year, self.month )[ 1 ]


    # protected:
    def _do_init( self ):
        ''' Build a list of sessions for the given year-month '''
        # fspec = os.path.join( config.get_data_dir(),
        #                      "Move_%04d_%02d*.dfz", self.year, self.month )
        #files = glob.glob( fspec )

        for file in pathlib.Path( config.get_data_dir() ).glob( \
                                     "Move_%04d_%02d*.dfz" % (self.year, self.month) ):
        #for f in files:
            base = os.path.splitext( file )[ 0 ]
            parts = base.split( '_' )
            day = parts[ 3 ]
            activity = parts[ -1 ]  # part after last underscore

            # Need to build a list of data items for each day, even if that list contains
            # only 1 workout
            if day not in self.sessions:
                self.sessions[ int( day ) ] = []

            self.sessions[ int( day ) ].append(
                    utils.components_to_session( day, self.month, self.year, file, activity ) )



# pylint: disable=unused-argument
def _test( argc, argv ):
    ''' unit testing '''

    cal = Calendar( 2019 )
    print( cal.get_monthly() )



if __name__ == "__main__":
    _test( len( sys.argv ), sys.argv )
