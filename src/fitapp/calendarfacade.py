'''
    GD 20210209

    Adapter to allow the calendar component to communicate with the server page
'''

import sys

from fitcore import fitcalendar, utils


# pylint: disable=too-few-public-methods
class CalendarFacade():
    ''' Calendar facade '''

    def __init__( self ):
        ''' Ctor '''
        self.cal = None


    def get_days( self, year, month ):
        ''' Gets all days for the given year and month
            Returns a list of
                {
                    daynum: day of the month
                    session: S, B, R, G, str (etch), M (ore than one)
                }
        '''

        if self.cal is None or self.cal.get_date() != (year, month):
            self.cal = fitcalendar.Calendar( year, month )

        sessions = self.cal.get_monthly()
        alldata = []
        for day in range( 1, self.cal.get_max_days() + 1 ):     # days in month are 1-indexed
            data = []
            if day in sessions:
                # We may (will) have more than one session per date.
                # This means the FitCalendar will have to return a list for each date
                # mnemonics = []
                # urls = []
                daily = sessions[ day ]
                for idx, sess in enumerate( daily ):
                    data.append( { 'mnemonic' : sess[ 'type' ][ 0 ],
                                   'wid' : utils.session_to_wid( idx, sess )
                                 }
                               )

            else:
                data.append( { 'mnemonic' : '-',
                               'id' : ''
                             }
                           )

            alldata.append(
                {
                    'daynum' : day,
                    'sessions' : data
                } )

        # print( alldata )
        return alldata



# pylint: disable=unused-argument
def _test( argc, argv ):
    ''' unit testing '''

    facade = CalendarFacade()

    print( facade.get_days( 2021, 1 ) )


if __name__ == "__main__":
    _test( len( sys.argv ), sys.argv )
