'''
    GD 20210228

    Facade to marshall data to/from the Athlete and it's form
'''

import logging


from fitcore import athlete
from fitapp.athleteform import AthleteForm


class AthleteFacade():
    ''' The facade '''

    def __init__( self ):
        ''' Ctor '''
        pass
        

    def save_header( self, theform ):
        ''' Save the Athlete's header details '''
        ath = self._find_existing( theform.name )
        if ath is None:
            # The form should have taken care of making sure everything that is mandatory is present
            logging.debug( "%s %s %s", theform.name.data, theform.age.data, theform.weight.data )
            ath = athlete.Athlete.from_data( \
                        theform.name.data,
                        theform.age.data,
                        theform.weight.data,
                        theform.comment.data )

        return ath.save()


    def _find_existing( self, name ):
        ''' Return an Athlete object if it already exists, None otherwise '''
        for ath in athlete.all_athletes():
            if ath.name == name:
                return ath

        return None


    def get_all( self ):
        ''' Return objects for all existing Athletes '''
        aths = athlete.all_athletes()
        logging.debug( aths )
        return aths
        