'''
    GD 20210209

    Adapter to allow the calendar component to communicate with the server page
'''

from fitcalendar import Calendar


class CalendarAdapter():
    ''' Calendar adapter '''

    def __init__( self ):
        ''' Ctor '''
        self.cal = None


    def get_days( year, month ):
        ''' Gets all days for the given year and month
            Returns a list of
                {
                    daynum: day of the month
                    session: S, B, R, G, str (etch), M (ore than one)
                }
        '''

        if cal is None or cal.get_date() != (year, month):
            self.cal = Calendar( year, month )

        sessions = self.cal.get_monthly()
        data = []
        for day in range( self.cal.get_max_days() ):
            if day in sessions:
                # We may (will) have more than one session per date.
                # This means the FitCalendar will have to return a list for each date
                daily = sessions[ day ]
                if len( daily ) > 1:
                    mnemonic = 'M'
                else:
                    mnemonic = daily[ 0 ][ 'activity' ][ 0 ]    # first letter of the only sess 
            else:
                mnemonic = ''

            data.append( 
                {
                    'daynum' : day,
                    'session' : mnemonic
                } )


#TODO TestMe
    