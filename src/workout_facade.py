'''
    GD 20210214

    Adapter to allow the server pages to communicate with the Workout objects
'''


import workout



class WorkoutFacade():
    ''' The facade '''

    def __init( self, wo=None ):
        ''' Ctor '''
        self.wo = wo


    def get_map( self ):
        ''' Returns the map html '''

    def get_plot( self, name="heart_rate" ):
        ''' Gets the named plot of data, or None if not available. '''
