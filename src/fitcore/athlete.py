'''
    GD 20210227

    Class to represent an 'athlete' !
'''

import abc
import gzip
import logging

from datetime import date
from pathlib import Path

from fitcore import config


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


class Calculator( metaclass=abc.ABCMeta ):
    ''' Abstract base functor for Calculating a metric (eg. CSS) from one or more assessments '''
    def __call__( self, assess ):
        raise NotImplementedError


class CalcCSS( Calculator ):
    ''' Calculate Critical Swim Speed '''
    def __call__( self, assess ):
        ''' functor
            assess is list of 2 swim times: [400m, 200m]
        '''
        return None


class CalcBikeFTP( Calculator ):
    ''' Calculates bike functional threshold power '''
    pass


class CalcRunFTP( Calculator ):
    ''' Calculates run functional threshold pace '''
    pass


class Athlete():
    ''' The Athlete class '''

    def __init__( self, name="", age=30, weight=75, comment="" ):
        ''' Ctor '''
        self.name = ""
        self.age = -1
        self.weight = -1
        self.comment = ""

        self._assessments = None

    def load( self, fname ):
        #  with gzip.open( athfile, "rb" ) as zifh:
        pass

    def save( self, fname ):
        pass

    #
    # Factory class methods
    @classmethod
    def from_file( cls, fname ):
        ''' Creates a new Athlete object from the named file '''
        if Path( fname ).exists():
            retval = Athlete()
            try:
                athlete.load( fname )
                return athlete
            except IOError as ex:
                logging.error( ex )

        return None


    @classmethod
    def from_data( cls, name="", age=30, weight=75, comment="" ):
        ''' Creates a new Athlete object from the passed-in values '''
        return Athlete( name, age, weight, comments )



def all_athletes():
    ''' Return list of all athlete's data '''

    # For each subdir in the data dir, if that dir contains an athlete file,
    # include it in the returned list
    retval = []
    for directory in ( Path( d ) for d in config.get_data_dir().iterdir() if \
                            d.is_dir() ):
        athfile = directory / "athlete.dfz"
        if athfile.exists():
            retval.append( Athlete.from_file( athfile ) )

    return retval

