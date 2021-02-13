'''
    GD 20210207

    Updates the local DB from the nominated dump dir
'''

import os
import sys

from timeit import default_timer as timer

import workout


def ingest( frm, to ):
    ''' Ensure each src .FIT file has a corresponding .df file in the dest data dir '''

    for dir in [frm, to]:
        if not os.path.isdir( dir ):
            return "%s is not a directory." % frm

    ast = timer()
    for n, fitfile in enumerate( [ os.path.join( frm, f) for f in os.listdir( frm ) ] ):
        # We're only looking for the .FIT files, ignore anything else that may be there
        # Workout.ingest() will take care of any similarly-named .xlsx files
        if os.path.splitext( fitfile )[ 1 ] == ".fit":
            print( "Ingesting %s" % fitfile )
            wo = workout.Workout()
            st = timer()
            err = wo.ingest( fitfile, to )
            et = timer()
            if err == "":
                print( " ... Success in %.3f seconds" % (et - st) )
            else:
                print( " ... Failed [%s]" % err )

    aet = timer()

    dur = aet - ast
    print( "Processed %d files in %d secs [%d:%d], mean=%.2f sec" % \
            (n, 
            dur,
            int(dur / 60),
            int(dur % 60),
            dur / n)
         )


def main( argc, argv ):
    ''' It '''
    if argc != 3:
        print( "%s <srcdir> <destdir>" % argv[ 0 ] )
        sys.exit( -1 )

    ingest( argv[ 1 ], argv[ 2 ] )


if __name__ == "__main__":
    main( len( sys.argv ), sys.argv )
