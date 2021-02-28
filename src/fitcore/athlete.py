'''
    GD 20210227

    Class to represent an 'athlete' !
'''

import abc
import io
import gzip
import logging

from datetime import date
from pathlib import Path

import pandas as pd

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


#
# FIXME will get moved to it's own module
#

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
#
#

class Athlete():
    ''' The Athlete class '''

    def __init__( self, name="", age=30, weight=75, comment="" ):
        ''' Ctor '''
        self.prop_name = name
        self.prop_age = -age
        self.prop_weight = weight
        self.prop_comment = comment
        self.prop_start_date = None
        self.prop_end_date = None

        self._assessments = None

        self.myfname = None


    def load( self, fname ):
        ''' Load the date from disk '''
        try:
            logging.info( "Load athlete from '%s'", fname )
            with gzip.open( fname, "rb" ) as zifh:
                # FIXME this will have to chang ewhen we add more dataframes to the file
                rawstr = zifh.read()
                rawstr = rawstr.decode()
                if len( rawstr ) > 0:
                    df = pd.read_csv( io.StringIO( rawstr ) )

        except IOError as ex:
            logging.error( "Athlete load error: %s" % ex )
            return False

        if len( df.index ) == 1:
            self._properties_from_obs( df.iloc[ 0 ] )
        else:
            logging.error( "%d lines in athlete header; should be only 1" % len( df.index ) )
            return False

        return True
 

    def save( self ):
        ''' Save the athlete data to the named file, or the stored filename if None specified

            return: True on success, False otherwise
        '''

        # All data should be contained within this object by this stage
        ofile = Path( config.get_data_dir() ) / self.prop_name / "athlete.dfz"
        logging.debug( "Will save to %s", str( ofile ) )

        if not ofile.parent.exists():
            ofile.parent.mkdir()
            logging.info( "Created athlete dir %s", ofile.parent )

        # The aim is to Pandafy the core data of this object automatically, so that I can
        # add properties later and they will get picked up without having to edi different
        # parts of the code
        df = pd.DataFrame( data=[ self._obs_from_properties() ],
                           columns=self._features_from_properties() )
        print( df )

        # Serialise to strings first, as we will be dumping mutliple dataframes into the one file
        dfstr = df.to_csv( path_or_buf=None, na_rep="NaN ")

        # TODO file header record

        with gzip.open( ofile, "wb" ) as zofh:
            zofh.write( str.encode( dfstr ) )
        logging.info( "Wrote athlete data" )

        return True

    #
    # Factory class methods
    @classmethod
    def from_file( cls, fname ):
        ''' Creates a new Athlete object from the named file '''
        if Path( fname ).exists():
            retval = Athlete()
            try:
                retval.load( fname )
                return retval
            except IOError as ex:
                logging.error( ex )

        return None


    @classmethod
    def from_data( cls, name="", age=30, weight=75, comment="" ):
        ''' Creates a new Athlete object from the passed-in values '''
        return Athlete( name, age, weight, comment )


    #
    # protected:
    def _features_from_properties( self ):
        ''' Return a list of names of properties of this object '''
        return [ prop for prop in dir( self ) if str( prop )[ 0 : 5 ] == "prop_"]

    def _obs_from_properties( self ):
        ''' Return a list of values of properties of this object '''

        # Apparently can't do this with a list comprehension. Pout-emoji
        obs = []
        for prop in dir( self ):
            if str( prop )[ 0 : 5 ] == "prop_":
                obs.append( eval( "self.%s" % prop ) )

        return obs


    def _properties_from_obs( self, observation ):
        ''' Set this object's property members from the observation (Pandas Series) '''

        for feat in observation.index:
            if feat[ 0 : 5 ] == "prop_":
                print( "%s --> %s" % (feat, observation[ feat ] ) )
                # Everything is stored as a string in the dataframe
                exec( "self.%s = '%s'" % (feat, observation[ feat ] ) )


#
# Util functions
#

def all_athletes():
    ''' Return list of all athlete's data '''

    # For each subdir in the data dir, if that dir contains an athlete file,
    # include it in the returned list
    retval = []
    for directory in ( d for d in Path( config.get_data_dir() ).iterdir() if d.is_dir() ):
        print( str( directory ) )
        athfile = directory / "athlete.dfz"
        if athfile.exists():
            print( "   yep" )
            retval.append( Athlete.from_file( athfile ) )

    return retval

