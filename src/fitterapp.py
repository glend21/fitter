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
    return render_template( "month.html", days=caladp.get_days( today.year, today.month ) )


@app.route( "/about" )
def about():
    return render_template( "About.html" )


dummy_data = [
                {
                    'num': 1,
                    'title': 'sdfsff',
                    'desc': 'a'
                },
                {
                    'num': 2,
                    'title': 'dfsfsfdf',
                    'desc': 'b'
                },
                {
                    'num': 3,
                    'title': 'ggthrnrnry',
                    'desc': 'c'
                },
                {
                    'num': 4,
                    'title': 'aaa',
                    'desc': 'd'
                },
                {
                    'num': 5,
                    'title': '2345678',
                    'desc': 'e'
                },
                {
                    'num': 6,
                    'title': 'bsbetrter',
                    'desc': 'f'
                },
                {
                    'num': 7,
                    'title': 'asdfghj',
                    'desc': 'g'
                },
                {
                    'num': 8,
                    'title': 'wrwrewrewerwerw',
                    'desc': 'h'
                },
             ]


@app.route( "/month" )
def month():
    return render_template( "month.html", days=dummy_data )



if __name__ == "__main__":
    app.run( debug=True )
