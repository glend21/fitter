'''
    GD 20210204

    Creates a GeoJson object out of the raw activity dataframe
'''


import os
import sys

import pandas as pd

import geojson


def main( argc, argv ):
    ''' It '''
    if argc != 3:
        print( "%s <dataframe> <geojson>" )
        sys.exit( -1 )

    df = pd.read_csv( argv[1] )
    if df is None:
        print( "Could not read dataframe from %s" % argv[1] )
        sys.exit( -1 )

    # (long, lat) pairs ... the order is important
    coords = list( zip( df.position_long, df.position_lat ) )

    # Build a list of features
    features = []
    for i in range( len( coords ) - 1 ):
        endpoint = (coords[ i ], coords[ i + 1 ])
        #print( endpoint, df.heart_rate[i] )
        features.append( geojson.Feature( geometry=geojson.LineString( endpoint ), properties=df.heart_rate[ i ] ) )

    # print( features )

    # Create a feature collection from the features and get it's strign representation
    geo_string = geojson.dumps( geojson.FeatureCollection( features ) )
    # print( geo_string )

    with open( argv[2], "wt" ) as ofh:
        ofh.write( geo_string )



if __name__ == "__main__":
    main( len( sys.argv ), sys.argv )
