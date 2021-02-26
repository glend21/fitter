'''
    GD 20210205

    The core Workout class for the activity processing system
'''

import os
import io
import re
import pathlib
import logging
import gzip
from typing import Dict, Union
from datetime import datetime, timedelta

import pandas as pd

import fitdecode as fit
import geojson



_HEADER_FEATURES = ( "Activity", "StartTime", "Feeling", "Notes")
_POINT_FEATURES = ( "timestamp", "position_lat", "position_long", "heart_rate", "altitude",
                    "speed", "vertical_speed", "cadence", "power" )
_POINT_DATA_FEATURES =_POINT_FEATURES[ 3 : ]
_LAP_FEATURES = ( "number", "start_time", "total_distance", "total_elapsed_time", "max_speed",
                  "max_heart_rate", "avg_heart_rate" )


class Workout:
    ''' The workkout class '''

    def __init__( self, fname=None ):
        ''' Ctor
            If the filename is specified, it is automatically loaded '''
        self.df_header = None
        self.df_points = None
        self.df_laps = None
        self.js_geo = None

        if not fname is None:
            self.load( fname )


    # public:
    def ingest( self, fname, destdir ):
        ''' Build the data store for the workout from the input file(s) '''

        fileset = self._can_ingest( fname, destdir )
        if fileset is not None:
            return self._do_ingest( fileset )

        return ""


    def load( self, src ):
        ''' Loads the df file from disk '''
        try:
            logging.info( "Load '%s'", src )
            with gzip.open( src, "rb" ) as zifh:
                header = zifh.readline()
                [shdr, spts, slaps, sgeo] = [ int(v) for v in header.split() ]

                self.df_header = self._load_dataframe( zifh, shdr, "header" )
                self.df_points = self._load_dataframe( zifh, spts, "points" )
                self.df_laps = self._load_dataframe( zifh, slaps, "laps" )
                self.js_geo = self._load_json( zifh, sgeo, "geo" )

        except IOError as ex:
            err = "ERR: %s" % ex
            return err

        return ""


    def save( self, dest ):
        ''' Save the object state to disk in destdir '''

        hdrstr = self.df_header.to_csv( path_or_buf=None, na_rep="NaN" )
        ptstr = self.df_points.to_csv( path_or_buf=None, na_rep="NaN" )  # shouldn't have NaNs
        lapstr = self.df_laps.to_csv( path_or_buf=None, na_rep="NaN" )

        # May not have geo data. eg. gym, swim
        if self.js_geo is not None:
            geostr = geojson.dumps( self.js_geo, indent=2 )
        else:
            geostr = ""

        # Format: The first line contains the lengths of the following blocks, with a newline
        #   Then each block
        #   Each block is a dataframe with a header line
        outstr = "%d %d %d %d\n" % (len(hdrstr), len(ptstr), len(lapstr), len(geostr))
        outstr += hdrstr
        outstr += ptstr
        outstr += lapstr
        outstr += geostr

        with gzip.open( dest, "wb" ) as zofh:
            zofh.write( str.encode( outstr ) )
        logging.info( " ... saved to %s", dest )


    def feature_list( self ):
        ''' Returns the available features for the data '''
        if not self.df_points is None:
            dataset = set( self.df_points.columns.tolist() )
            return dataset.intersection( _POINT_DATA_FEATURES )

        return None


    # protected:
    def _normalise_name_stub( self, iname ):
        ''' Ensures the filename is standard format:
            Move_<yyyy>_<mm>_<dd>_<hh>_<MM>_<ss>_<type>

            Note the extension is omited, this is left as an exercise for the caller
        '''

        if iname[ 0 : 4 ] == "Move":
            return iname

        # Yes, yes I am ...
        match = re.match( r"(^\w+)_(\d{4})-(\d{2})-(\d{2})T(\d{2})_(\d{2})_(\d{2}).fit", iname )
        if not match:
            raise ValueError( "'%s' has unknown name format" )

        ofname = "Move_%s_%s_%s_%s_%s_%s_%s" % ( \
                        match[ 2 ],         # year
                        match[ 3 ],         # month
                        match[ 4 ],         # day
                        match[ 5 ],         # hour
                        match[ 6 ],         # minute
                        match[ 7 ],         # second
                        match[ 1 ] )        # activity type
        return ofname


    def _can_ingest( self, inpath, outdir ):
        ''' Determines what, if any, work needs to be done for this file path
            Returns:
                {
                    datafile : full path to .fir file
                    auxfile : full path to .xlsx, if one is present
                    outfile : full path to output .df file
                }
            None if .fit file does not exist, or if .df file exists and is older than
                    both .fit and .xlsx files

            It is OK for the .xlsx to be missing
            It is mandatory for the .fit to be present
        '''

        srcdir, srcfname = os.path.split( inpath )

        datafile = pathlib.Path( inpath )
        auxfile = pathlib.Path( srcdir ) / "%s.xlsx" % srcfname
        outfile = pathlib.Path( outdir ) / "%s.dfz" % self._normalise_name_stub( srcfname )

        # If no .fit file, nothing to do
        if not datafile.exists():
            return None

        retval = { 'datafile' : datafile,
                   'outfile' : outfile
                 }
        if auxfile.exists():
            retval[ 'auxfile' ] = auxfile
        else:
            retval[ 'auxfile' ] = None

        # If no .dfz file, must perform the ingest
        if not outfile.exists():
            return retval

        # If any file in the input set is newer than the output file, ingest
        for file in ( datafile, auxfile ):
            if file.stat().st_ctime > outfile.stat().st_ctime:
                return retval

        # Output file exists, is newer than all input file(s), do nothing
        return None


    # --
    def _do_ingest( self, files ):
        ''' Build the data store '''

        retval = self._ingest_fit( files[ 'datafile' ] )
        if retval == "":
            if files[ 'auxfile' ] is not None:
                retval = self._ingest_xlsx( files[ 'auxfile' ] )

        if retval == "":
            self.save( files[ 'outfile' ] )

        return retval


    def _ingest_fit( self, src ):
        ''' Processes a .FIT file
            Updates the object's internal state, returns an empty sting on
             success, or an error string on failure
        '''

        point_data = []
        lap_data = []
        with fit.FitReader( src ) as ifh:
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
        self.df_points.fillna( method="ffill", inplace=True )

        self.df_laps = pd.DataFrame( lap_data, columns=_LAP_FEATURES )

        # Now some geojson
        if not self.df_points[ "position_lat" ].isna().all() and \
           not self.df_points[ "position_long" ].isna().all():
            logging.debug( "Making geo" )
            self._make_geo()
        else:
            logging.info( " ... no geo data" )

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
        vals = [ "" ] * len( _HEADER_FEATURES )

        try:
            df = pd.read_excel( src )

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
            logging.info( " ... no .xlsx to process" )
            vals = [ "", "", "", "" ]

        else:
            logging.info( " ... processed an xlsx file" )

        finally:
            # Turn the vals list into an object dataframe
            self.df_header = pd.DataFrame( [ vals ], columns=_HEADER_FEATURES )

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

        rawstr = rawstr.decode()
        if len( rawstr ) > 0:
            df = pd.read_csv( io.StringIO( rawstr ) )
            return df

        return None


    def _load_json( self, ifile, offset, name="" ):
        ''' Reads the geo json component of the input stream '''
        rawstr = ifile.read( offset )
        if len( rawstr ) != offset:
            raise IOError( "Reached EOF reading %s data" % name )

        if len( rawstr ) > 0:
            geo = geojson.loads( rawstr )
            return geo

        return None


    def _make_geo( self ):
        ''' Creates the geojson object from the points dataframe '''

        # Create a list of coordinates, turn those into linestring endpoints, contstruct
        # the actual linestrings from those, and add them to the feature list
        # (long, lat) -- this is important
        coords = list( zip( self.df_points.position_long, self.df_points.position_lat ) )
        features = []
        for i in range( len( coords ) - 1 ):
            endpt = ( coords[ i ], coords[ i + 1 ] )
            props = { "hr" : self.df_points[ "heart_rate" ][ i ] }
            if pd.notna( self.df_points[ "power" ][ i ] ):
                props[ "pwr" ] = self.df_points[ "power" ][ i ]

            features.append( geojson.Feature( geometry=geojson.LineString( endpt ),
                                              properties=props
                                            )
                           )
        self.js_geo = geojson.FeatureCollection( features )



import folium

if __name__ == "__main__":
    # testing only
    s = "/mnt/h_drive/SuuntoDiaspora/Running_2021-02-10T18_08_20.fit"
    d = "./"
    wo = Workout()
    wo.ingest( s, d )
    #wo.save( d, "wibble" )

    new_wo = Workout()
    new_wo.load( "./Move_2021_02_10_18_08_20_Running.dfz" )
    print( new_wo.js_geo )

'''
    mymap = folium.Map( location=[ -31.947, 115.859 ], zoom_start=15 )
    folium.GeoJson( new_wo.js_geo,
                    name="Run"
                    #style_function=style
                  ).add_to( mymap )
    mymap.save( "foo.html" )
'''
