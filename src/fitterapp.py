'''
    GD 20210207

    Mainline of the Flask server app
'''

import os
import sys
from datetime import date

from flask import Flask, render_template

from calendaradapter import CalendarAdapter


app = Flask( __name__ )

caladp = CalendarAdapter()


@app.route( "/" )
def home():
    today = date.today()
    return render_template( "month.html", 
                            year=today.year, 
                            month=today.strftime( "%B" ),
                            days=caladp.get_days( today.year, today.month ) )


@app.route( "/about" )
def about():
    return render_template( "About.html" )


@app.route( "/month" )
def month():
    return render_template( "month.html", days=dummy_data )



if __name__ == "__main__":
    app.run( debug=True )
