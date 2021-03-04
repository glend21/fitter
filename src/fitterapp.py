'''
    GD 20210207

    Mainline of the Flask server app
'''

import sys
import logging
from datetime import date

from flask import Flask, render_template, flash, redirect

from fitcore import utils
from fitapp.calendarfacade import CalendarFacade
from fitapp.workoutfacade import WorkoutFacade
from fitapp.athletefacade import AthleteFacade
from fitapp.athleteform import AthleteForm


app = Flask( __name__ )
app.config['SECRET_KEY'] = "wibblewobble"


cal_facade = CalendarFacade()
wo_facade = WorkoutFacade()
ath_facade = AthleteFacade()


@app.route( "/" )
def home():
    # today = date.today()
    # return month( today.year, today.month )

    athletes = ath_facade.get_all()
    return render_template( "home.html", athletes=athletes )


@app.route( "/about" )
def about():
    return render_template( "About.html" )


@app.route( "/athlete/<string:name>", methods=['GET', 'POST'] )
def athlete( name ):
    form = AthleteForm()
    if form.validate_on_submit():
        print( "Pickle me" )
        flash('Form did something {}, age=={}'.format( form.name.data, form.age.data))
        ath_facade.save_header( form )
        return redirect('/')
    else:
        print( "Validation failed" )

    today = date.today()
    return render_template( "athlete.html", 
                            title="Athlete %s" % name, 
                            name=name, 
                            form=form,
                            date={ 'year' : today.year,
                                   'month' : today.month,
                                   'days' : cal_facade.get_days( today.year, today.month )
                                 } )


# FIXME Will probably go ...
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


@app.route( "/sandbox", methods=['GET', 'POST'] )
def sandbox():
    logging.debug( "sandbox" )

    form = AthleteForm()

    if form.validate_on_submit():
        print( "Pickle me" )
        flash('Form did something {}, age=={}'.format( form.name.data, form.age.data))
        #ath_facade.save_header( form )
        return redirect('/')
    else:
        print( "Validation failed" )

    today = date.today()
    return render_template( "sandbox01.html", title="Athlete Foo", 
                            name="Sandbox", 
                            form=form,
                            date={ 'year' : today.year,
                                   'month' : today.month,
                                   'days' : cal_facade.get_days( today.year, today.month )
                                 } )


if __name__ == "__main__":

    retval = utils.init_log( sys.argv[0] )
    if retval != "":
        # Could not set up logging, can only print to console
        print( retval )
        sys.exit( -1 )

    app.run( debug=True )
