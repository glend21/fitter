'''
    GD 202102104

    Merge in the notes details from an xlsx file into the dataframe for an activity
'''

import os
import sys

import pandas as pd


def main( argc, argv ):
    ''' It '''

    if argc != 3 :
        print( "%d <dataframe> <xlsx>" % argv[0] )
        sys.exit( -1 )

    xl = pd.read_excel( argv[2] )
    print( xl )


if __name__ == "__main__":
    main( len( sys.argv ), sys.argv )
