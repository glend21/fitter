'''
    GD 20210207

    Updates the local DB from the nominated dump dir
'''

import sys
import logging
from pathlib import Path
from timeit import default_timer as timer

from fitcore import workout, utils


def ingest( frm, to ):
    ''' Ensure each src .FIT file has a corresponding .df file in the dest data dir '''

    for path in [frm, to]:
        if not Path( path ).is_dir():
            logging.warning( "%s is not a directory.", frm )
            return

    logging.info( " ========= Start =========" )
    ast = timer()
    for n, fitfile in enumerate( f for f in Path( frm ).iterdir() ):
        # We're only looking for the .FIT files, ignore anything else that may be there
        # Workout.ingest() will take care of any similarly-named .xlsx files
        if fitfile.suffix == ".fit":
            logging.info( "Ingesting %s", str( fitfile ) )
            wo = workout.Workout()
            st = timer()
            err = wo.ingest( fitfile, to )
            et = timer()
            if err == "":
                logging.info( " ... Success in %.3f seconds", (et - st) )
            else:
                logging.error( " ... Failed [%s]", err )

    aet = timer()

    dur = aet - ast
    logging.info( "Processed %d files in %d secs [%d:%d], mean=%.2f sec", \
            n,
            dur,
            int(dur / 60),
            int(dur % 60),
            dur / n
         )
    logging.info( " ========= Finish =========" )


def main( argc, argv ):
    ''' It '''

    retval = utils.init_log( sys.argv[0] )
    if retval != "":
        # Could not set up logging, can only print to console
        print( retval )
        sys.exit( -1 )

    if argc != 3:
        logging.error( "%s <srcdir> <destdir>", argv[ 0 ] )
        sys.exit( -1 )

    ingest( argv[ 1 ], argv[ 2 ] )


if __name__ == "__main__":
    main( len( sys.argv ), sys.argv )
