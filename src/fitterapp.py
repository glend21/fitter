'''
    GD 20210207

    Mainline of the Flask server app
'''

import os
import sys
from datetime import date

from flask import Flask, render_template

from calendarfacade import CalendarFacade
from workoutfacade import WorkoutFacade


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
        print( "--> %d %d" % (int( yy ), int( mm )) )
    except Exception as ex:
        print( "Date components are incorrect - ", ex )
        return "Date components are incorrect"

    return render_template( "month.html", 
                            year=yy, 
                            month=dt.strftime( "%B" ),
                            days=cal_facade.get_days( yy, mm ) )


@app.route( "/workout/<string:wid>" )
def workout( wid ):
    ''' Render a specific workout '''
    return wo_facade.get_map( wid=wid )
    #return "Workout - %s" % wid


if __name__ == "__main__":
    app.run( debug=True )
