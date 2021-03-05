'''
    GD 20210207

    Updates the local DB from the nominated dump dir
'''

import sys
import argparse
import logging

from datetime import datetime
from pathlib import Path
from timeit import default_timer as timer

from fitcore import workout, config, utils


def ingest( frm, to, static=None, date_after=None ):
    ''' Ensure each src .FIT file has a corresponding .df file in the dest data dir
        frm, to are Paths
    '''

    for path in [ frm, to, static ]:
        if not path.is_dir():
            logging.warning( "%s is not a directory.", path )
            return

    logging.info( " ========= Start =========" )
    ast = timer()

    # All files with a .fit suffix and newer than 'after, iff 'after is specified
    # (all in one expression. cop that)
    n = 0
    for n, fitfile in enumerate( f for f in Path( frm ).iterdir() if \
                                      f.suffix == ".fit" and \
                                      (date_after is None or f.stat().st_ctime > date_after.timestamp()) ):
        logging.info( "Ingesting %s", str( fitfile ) )
        wo = workout.Workout()
        st = timer()
        err = wo.ingest( fitfile, to, static )
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


def init_fail( msg, skip_log=False ):
    ''' Handle initialisation failures (terminates process) '''
    if not skip_log:
        logging.error( msg )
    print( msg )
    sys.exit( -1 )


def main():
    ''' It '''

    # Init the log subsystem first
    retval = utils.init_log( sys.argv[0] )
    if retval != "":
        # Could not set up logging, can only print to console
        init_fail( retval )

    # Now handle the command line
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument( "-a", "--athlete",
                        help="Ingest files for the named athlete. Dirs are specified in config file." )
    group.add_argument( "-t", "--todor",
                        help="Explicit location to which to store the ingested data." )
    parser.add_argument( "-f", "--fromdir",
                         help="Location from which to ingest the raw data." )
    parser.add_argument( "-s", "--staticdir",
                         "Location in which to store static assets" )
    parser.add_argument( "-d", "--date",
                        help="Ingest only those files newer than date (yyyy-mm-dd)." )
    args = parser.parse_args()

    if args.athlete is not None:
        # We're using the standard output location from the config file, with the athlete name appended
        dest = Path( config.get_data_dir() ) / args.athlete
    elif args.todir is not None:
        # Explicit destination dir
        dest = Path( args.to ).resolve()
    else:
        init_fail( "Must specify one of -a <athlete> or -t <to>" )

    if args.fromdir is not None:
        src = Path( args.fromdir ).resolve()
    else:
        init_fail( "Must specify -s <source-dir>" )

    if args.staticdir is not None:
        static = Path( args.staticdir ).resolve()
    else:
        static = Path( config.get_static_dir() )

    if args.date is not None:
        try:
            dt = datetime.fromisoformat( args.date )
        except ValueError:
            init_fail( "-d <date> is not in ISO format yyyy-mm-dd" )
    else:
        dt = None

    ingest( src, dest, static, dt )


if __name__ == "__main__":
    main()
