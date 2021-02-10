'''
    GD 20210209

    Adapter to allow the calendar component to communicate with the server page
'''

import sys

from fitcalendar import Calendar


class CalendarAdapter():
    ''' Calendar adapter '''

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
            self.cal = Calendar( year, month )

        sessions = self.cal.get_monthly()
        alldata = []
        for day in range( self.cal.get_max_days() ):
            data = {}
            if day in sessions:
                # We may (will) have more than one session per date.
                # This means the FitCalendar will have to return a list for each date
                # mnemonics = []
                # urls = []
                daily = sessions[ day ]
                for ids, sess in enumerate( daily ):
                    data[ 'mnemonic' ] = sess[ 'activity' ][ 0 ]
                    data[ 'url' ] = "/workout/%04d%02d%02d-%02d" % \
                                    (sess[ 'year' ], sess[ 'month'], sess[ 'day' ], idx)  

                    #mnemonics.append( sess[ 'activity' ][ 0 ] )
                    #urls.append( "/workout/%04d%02d%02d-%02d" % \
                                 #(sess[ 'year' ], sess[ 'month'], sess[ 'day' ], idx) )
            else:
                data[ 'mnemonic' ] = '-'
                data[ 'url' ] = ''

            alldata.append( 
                {
                    'daynum' : day + 1,     # days in month are 1-based
                    'sessions' : data
                    #'sessions' : mnemonics,
                    #'links' : urls
                } )

        return alldata



def _test( argc, argv ):
    ''' unit testing '''

    cad = CalendarAdapter()

    print( cad.get_days( 2021, 1 ) )
    

if __name__ == "__main__":
    _test( len( sys.argv ), sys.argv )
