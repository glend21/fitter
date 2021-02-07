'''
    GD 20210207

    Updates the local DB from the nominated dump dir
'''

import os
import sys

import workout


def ingest( frm, to ):
    ''' Ensure each src .FIT file has a corresponding .df file in the dest data dir '''

    for dir in [frm, to]:
        if not os.path.isdir( dir ):
            return "%s is not a directory." % frm

    for fitfile in [ os.path.join( frm, f) for f in os.listdir( frm ) ]:
        # We're only looking for the .FIT files, ignore anything else that may be there
        # Workout.ingest() will take care of any similarly-named .xlsx files
        if os.path.splitext( fitfile )[ 1 ] == ".fit":
            print( "Ingesting %s" % fitfile )
            wo = workout.Workout()
            err = wo.ingest( fitfile, to )
            if err != "":
                print( " ... Failed [%s]" % err )


def main( argc, argv ):
    ''' It '''
    if argc != 3:
        print( "%s <srcdir> <destdir>" % argv[ 0 ] )
        sys.exit( -1 )

    ingest( argv[ 1 ], argv[ 2 ] )


if __name__ == "__main__":
    main( len( sys.argv ), sys.argv )
