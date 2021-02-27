'''
    GD 20210227

    Class to represent an 'athlete' !
'''

from datetime import date


class Assessment():
    ''' An assessment of capability.

        eg bike FTP, swim CSS, ...
    '''

    def __init__( self, date=date.today() ):
        ''' Ctor '''

        # All this says that the assessment was a 400m swim completed in a time of 7:37 minutes
        self.date = date
        self.name = ""
        self.activity = ""          # eg. swim
        self.span_value = -1        # eg. 400(m)
        self.span_type = None       # eg. distance
        self.span_units = None      # eg. metres
        self.metric_value = -1      # eg. 7:37
        self.metric_type = None     # eg. time
        self.metric_units = None    # eg. minutes-and-seconds
        self.comment = ""


class Athlete():
    ''' The Athlete class '''

    def __init__( self, name, age=30, weight=75, comment="" ):
        ''' Ctor '''
        self.name = ""
        self.age = -1
        self.weight = -1
        self.comment = ""

        self._assessments = None

