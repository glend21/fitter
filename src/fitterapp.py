'''
    GD 20210207

    Mainline of the Flask server app
'''

import os
import sys
import logging
from pathlib import Path
from datetime import date

from flask import Flask, render_template

from fitcore import config
from fitapp.calendarfacade import CalendarFacade
from fitapp.workoutfacade import WorkoutFacade


app = Flask( __name__ )

cal_facade = CalendarFacade()
wo_facade = WorkoutFacade()


@app.route( "/" )
def home():
    today = date.today()
    return month( today.year, today.month )
    # return render_template( "home.html" )


@app.route( "/about" )
def about():
    return render_template( "About.html" )


@app.route( "/month/<int:yy>/<int:mm>" )
def month( yy, mm ):
    try:
        dt = date( year=int( yy ), month=int( mm ), day=1 )
    except Exception as ex:
        logging.error( "Date components are incorrect - ", ex )
        return "Date components are incorrect"

    return render_template( "month.html", 
                            year=yy, 
                            month=dt.strftime( "%B" ),
                            days=cal_facade.get_days( yy, mm ) )


@app.route( "/workout/<string:wid>" )
def workout( wid ):
    ''' Render a specific workout '''

    logging.debug( "Boo" )
    # FIXME this is proto code
    map = wo_facade.get_map( wid=wid )
    with open( "./static/map.html", "wt" ) as ofh:
        ofh.write( map )

    return render_template( "workout.html" )


def init_log():
    ''' Set up logging '''
    logdir = config.config.get_log_dir()
    if logdir is None:
        # System init impossible
        print( "ERR: Could not start system: no log dir in config file" )
        sys.exit( -1 )

    logpath = Path( logdir )
    newlogdir = False
    if not logpath.is_dir():
        logpath.mkdir()
        newlogdir = True

    logging.basicConfig( filename=Path( logdir ) / Path( "%s.log" % sys.argv[0] ).stem,
                         level=logging.DEBUG,
                         format="%(asctime)s %(levelname)-8s %(message)s",
                         datefmt='%m-%d %H:%M',
                         filemode="a" )

    if newlogdir:
        logging.info( "created log directory: %s" % logdir )


if __name__ == "__main__":

    init_log()

    app.run( debug=True )

