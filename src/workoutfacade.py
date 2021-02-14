'''
    GD 20210214

    Adapter to allow the server pages to communicate with the Workout objects
'''

# NB, currently using Folium, might be switching to Bokeh

import os
import json
import glob

import folium

import workout
import config
import utils


class WorkoutFacade():
    ''' The facade '''

    def __init__( self, wo=None, wid=None ):
        ''' Ctor '''

        self.wo = wo
        self.wid = wid

        if self.wo is None and self.wid is not None:
            self._load( self.wid )


    def get_map( self, wid=None ):
        ''' Returns the map html '''

        if wid is not None and wid != self.wid:
            if not self._load( wid ):
                return None

        # Massive leap of faith that the geojson is correct
        origin = self.wo.js_geo[ "features" ][ 0 ][ "geometry" ][ "coordinates" ][ 0 ]
        mymap = folium.Map( location=tuple( reversed( origin ) ), zoom_start=14 )
        folium.GeoJson( self.wo.js_geo, 
                        name="Workout"
                        #style_function=style
                      ).add_to( mymap )
        
        mymap.save( "foo.html" )        # DEBUG
        return mymap._repr_html_()


    def get_plot( self, name="heart_rate" ):
        ''' Gets the named plot of data, or None if not available. '''


    # protected:
    def _load( self, wid ):
        ''' Loads the data for the given workout ID 
            Returns success bool
        '''

        fname = self._get_dfname( wid )
        if not fname is None:
            wo = workout.Workout( fname )
            if wo.js_geo is not None and wo.df_points is not None:
                self.wo = wo
                return True

        return False


    def _get_dfname( self, wid ):
        ''' Discovers and returns the data file name '''

        # We're assuming here that we have a wid
        idx, pattern = utils.wid_to_glob( wid )
        if idx >= 0:
            files = glob.glob( os.path.join( config.config.get_data_dir(), pattern ) )
            if len( files ) >= idx:
                return files[ idx ]

        return None