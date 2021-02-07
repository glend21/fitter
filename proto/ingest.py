'''
    GD 20210130

    Reads FIT data file(s) and turns it/them into Pandas dataframes
    Saves a points file to the same input dir, same name, extention '-P.df'
    Saves a laps file to the same input dir, same name, extension '-L.df'
'''

import os
import sys
from typing import Dict, Union, Optional,Tuple

import pandas as pd
import fitdecode


POINT_FEATURES = ( "timestamp", "position_lat", "position_long", "heart_rate", "altitude", "speed", "vertical_speed", "cadence", "power" )
LAP_FEATURES = ( "number", "start_time", "total_distance", "total_elapsed_time", "max_speed", "max_heart_rate", "avg_heart_rate" )


def main( argc, argv ):
    ''' It '''

    for ifname in argv[ 1 : ]:
        with fitdecode.FitReader( ifname ) as ifh:
            point_data = []
            lap_data = []

            for frame in ifh:
                if isinstance( frame, fitdecode.records.FitDataMessage ):
                    if frame.name == 'lap':
                        # This frame contains data about a lap.
                        lap: Dict[ str, Union[ float, datetime, timedelta, int ] ] = {}

                        for fld in LAP_FEATURES[ 1 : ]:
                            if frame.has_field( fld ):
                                lap[ fld ] = frame.get_value( fld )
                        lap_data.append( lap )
                    
                    elif frame.name == 'record':
                        for f in frame.fields:
                            print( f.name )

                        if frame.has_field( POINT_FEATURES[0] ) and \
                           frame.has_field( POINT_FEATURES[1] ):
                           # FIXME not all record frames will have lat/long data
                           # eg. swimming, indoor rowing, gym, etc
                           
                            print( 'a' )
                            # This frame contains data about a "track point".
                            # Build a vanilla Python list of the data
                            pt: Dict[ str, Union[ float, int, str, datetime ] ] = {}
                            for fld in POINT_FEATURES:
                                if frame.has_field( fld ):
                                    pt[ fld ] = frame.get_value( fld )
                                    # print( "%s: %s" % (fld, pt[fld]) ) 
                            point_data.append( pt )

            # Create dataframes from the lists (and convert the point lat and long values)
            points_df = pd.DataFrame( point_data, columns=POINT_FEATURES )
            points_df[ "position_lat" ] = points_df[ "position_lat" ] / ( (2 ** 32) / 360 )
            points_df[ "position_long" ] = points_df[ "position_long" ] / ( (2 ** 32) / 360 )
            points_df.fillna( method="bfill", inplace=True )        # NaNs == bad
            points_df.to_csv( "%s-P%s" % (os.path.splitext( ifname )[0], ".df"), na_rep="NaN" )

            laps_df = pd.DataFrame( lap_data, columns=LAP_FEATURES )
            laps_df.to_csv( "%s-L%s" % (os.path.splitext( ifname )[0], ".df"), na_rep="NaN" )


if __name__ == "__main__":
    main( len( sys.argv ), sys.argv )
