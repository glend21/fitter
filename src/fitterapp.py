'''
    GD 20210207

    Mainline of the Flask server app
'''

import sys
import logging
from datetime import date

from flask import Flask, render_template

from fitcore import utils
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
    except ValueError as ex:
        logging.error( "Date components are incorrect - %s", ex )
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
    womap = wo_facade.get_map( wid=wid )
    with open( "./static/map.html", "wt" ) as ofh:
        ofh.write( womap )

    return render_template( "workout.html" )



if __name__ == "__main__":

    retval = utils.init_log( sys.argv[0] )
    if retval != "":
        # Could not set up logging, can only print to console
        print( retval )
        sys.exit( -1 )

    app.run( debug=True )
