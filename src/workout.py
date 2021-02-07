'''
    GD 20210205

    The core Workout class for the activity processing system
'''

import os
import sys
import io
from typing import Dict, Union, Optional,Tuple

import pandas as pd
import fitdecode as fit
import geojson


_HEADER_FEATURES = ( "Activity", "StartTime", "Feeling", "Notes")
_POINT_FEATURES = ( "timestamp", "position_lat", "position_long", "heart_rate", "altitude", "speed", "vertical_speed", "cadence", "power" )
_LAP_FEATURES = ( "number", "start_time", "total_distance", "total_elapsed_time", "max_speed", "max_heart_rate", "avg_heart_rate" )


class Workout:
    ''' The workkout class '''

    def __init__( self, fname=None ):
        ''' ctor '''
        self.df_header = None
        self.df_points = None
        self.df_laps = None
        self.js_geo = None

        if not fname is None:
            self.load( fname )


    # public:
    def ingest( self, fname, destdir ):
        ''' Build the data store for the workout from the input file(s) '''

        srcdir, srcfname = os.path.split( fname )
        srcstub, srcext = os.path.splitext( srcfname )
        src = { 'dir' : srcdir,
                'fname' : srcfname,
                'stub' : srcstub,
                'ext' : srcext,
                'fullpath' : fname
              }

        if src[ 'ext' ] != ".fit" :
            return "No .FIT file specified"

        if self._isIngested( destdir, src[ 'stub' ] ):
            # Nothing to do, but should log something here
            print( " ... already ingested." )
            return ""

        return self._doIngest( src, destdir )


    def load( self, fdir, fname ):
        ''' Loads the df file from disk '''
        try:
            print( "Load '%s'" % os.path.join( fdir, fname ) )
            with open( os.path.join( fdir, fname ), "rt" ) as ifh:
                header = ifh.readline()
                [shdr, spts, slaps, sgeo] = [ int(v) for v in header.split() ]

                self.df_header = self._load_dataframe( ifh, shdr, "header" )
                self.df_points = self._load_dataframe( ifh, spts, "points" )
                self.df_laps = self._load_dataframe( ifh, slaps, "laps" )
                self.df_geo = self._load_json( ifh, sgeo, "geo" )

        except IOError as ex:
            err = "ERR: %s" % ex
            return err

        return ""


    def save( self, destdir, name ):
        ''' Save the object state to disk in destdir '''

        hdrstr = self.df_header.to_csv( path_or_buf=None, na_rep="NaN" )
        ptstr = self.df_points.to_csv( path_or_buf=None, na_rep="NaN" )  # shouldn't have NaNs
        lapstr = self.df_laps.to_csv( path_or_buf=None, na_rep="NaN" )
        print( type( self.js_geo ) )
        geostr = geojson.dumps( self.js_geo )

        # Format: The first line contains the lengths of the following blocks, with a newline
        #   Then each block
        #   Each block is a dataframe with a header line
        outstr = "%d %d %d %d\n" % (len(hdrstr), len(ptstr), len(lapstr), len(geostr)) 
        outstr += hdrstr
        outstr += ptstr
        outstr += lapstr
        outstr += geostr

        with open( os.path.join( destdir, name ), "wt" ) as ofh:
            ofh.write( outstr )
        print( " ... saved to %s" % os.path.join( destdir, name ) )


    # protected: 
    def _isIngested( self, destdir, srcstub ):
        ''' Returns True if this file has already been processed '''

        # Todo relative modification time check
        return os.path.exists( "%s.df" % os.path.join( destdir, srcstub ) )


    def _doIngest( self, src, destdir ):
        ''' Build the data store '''

        retval = self._ingest_fit( src )
        if retval == "":
            retval = self._ingest_xlsx( src )

        if retval == "":
            self.save( destdir, "%s.df" % src[ 'stub' ] )

        return retval


    def _ingest_fit( self, src ):
        ''' Processes a .FIT file
            Updates the object's internal state, returns an empty sting on
             success, or an error string on failure
        '''

        point_data = []
        lap_data = []
        with fit.FitReader( src[ 'fullpath' ] ) as ifh:
            for frame in ifh:
                if isinstance( frame, fit.records.FitDataMessage ):
                    if frame.name == "lap":
                        self._process_lap( frame, lap_data )

                    elif frame.name == "record":
                        self._process_record( frame, point_data )

        # Create dataframes from the lists (and perform some cleanups)
        self.df_points = pd.DataFrame( point_data, columns=_POINT_FEATURES )
        self.df_points[ "position_lat" ] = self.df_points[ "position_lat" ] / ( (2 ** 32) / 360 )
        self.df_points[ "position_long" ] = self.df_points[ "position_long" ] / ( (2 ** 32) / 360 )
        self.df_points.fillna( method="bfill", inplace=True )        # NaNs == bad

        self.df_laps = pd.DataFrame( lap_data, columns=_LAP_FEATURES )

        # Now some geojson
        self._make_geo()

        return ""


    def _process_lap( self, frame, laps ):
        ''' Process a frame representing a single lap '''
        lap: Dict[ str, Union[ float, datetime, timedelta, int ] ] = {}

        for fld in _LAP_FEATURES[ 1 : ]:
            if frame.has_field( fld ):
                lap[ fld ] = frame.get_value( fld )
        laps.append( lap )


    def _process_record( self, frame, points ):
        ''' Process a frame representing a track point '''
        if frame.has_field( _POINT_FEATURES[0] ):
            # This frame contains data about a "track point".
            # Build a vanilla Python list of the data
            pt: Dict[ str, Union[ float, int, str, datetime ] ] = {}
            for fld in _POINT_FEATURES:
                if frame.has_field( fld ):
                    pt[ fld ] = frame.get_value( fld )
            points.append( pt )


    def _ingest_xlsx( self, src ):
        ''' Process a single .xlsx file
            Updates the object's internal state
        '''
        fname = "%s.xlsx" % os.path.join( src[ 'dir' ], src[ 'stub' ] )
        vals = [ "" ] * len( _HEADER_FEATURES )

        try:
            df = pd.read_excel( fname )

            # Stoopid export format of the .xlsx file doesn't put feature names in the first row
            for idx, feat in enumerate( _HEADER_FEATURES ):
                for col in df:
                    # And we only want the first word of the column header
                    # ... and only the first occurance of that column name. Jeebus ...
                    if df[ col ][ 0 ].split()[ 0 ] == feat and vals[ idx ] == "":
                        vals[ idx ] = df[ col ][ 1 ]

        except FileNotFoundError as ex:
            # OK for this file to not be present
            # If it's not there, we'll just save an empty header record to the .df
            print( " ... no .xlsx to process" )
            vals = [ "", "", "", "" ]

        # Turn the vals list into an object dataframe
        self.df_header = pd.DataFrame( [ vals ], columns=_HEADER_FEATURES )
        print( " ... processed an xlsx file" )

        return ""


    def _load_dataframe( self, ifile, offset, name="" ):
        ''' Reads the next 'offset' chars and (tries to) forms a DataFrame from them.
            Throws IOError on file read error
            Throws something or other if can't create the DF
            Return the created DataFrame
        '''
        rawstr = ifile.read( offset )
        if len( rawstr ) != offset:
            raise IOError( "Reached EOF reading %s data" % name )

        if len( rawstr ) > 0:
            df = pd.read_csv( io.StringIO( rawstr ) )
            return df

        return None


    def _make_geo( self ):
        ''' Creates the geojson object from the points dataframe '''

        # Create a list of coordinates, turn those into linestring endpoints, contstruct
        # the actuall linestrings from those, and add them to the feature list
        # (long, lat) -- this is important
        coords = list( zip( self.df_points.position_long, self.df_points.position_lat ) )
        features = []
        for i in range( len( coords ) - 1 ):
            endpt = ( coords[ i ], coords[ i + 1 ] )
            props = { "hr" : self.df_points[ "heart_rate" ] }
            if "power" in self.df_points.columns:
                props[ "pwr" ] : self.df_points[ "power" ][ i ]

            features.append( geojson.Feature( geometry=geojson.LineString( endpt ), 
                                              properties={}
                                            )
                           )
        self.js_geo = geojson.FeatureCollection( features )
           

    def _load_json( self, ifile, offset, name="" ):
        ''' Reads the geo json component of the input stream '''
        rawstr = ifile.read( offset )
        if len( rawstr ) != offset:
            raise IOError( "Reached EOF reading %s data" % name )

        if len( rawstr ) > 0:
            geo = geojson.loads( io.StringIO( rawstr ) )
            return geo

        return None



if __name__ == "__main__":
    # testing only
    s = "/mnt/h_drive/SuuntoDiaspora/Move_2021_01_25_17_36_09_Running.fit"
    d = "../data"
    wo = Workout()
    wo.ingest( s, d )
    wo.save( d, "wibble" )

    new_wo = Workout()
    new_wo.load( os.path.join( d, "wibble" ) )
