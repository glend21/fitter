'''
    GD 20210207

    Mainline of the Flask server app
'''

import os
import sys


from flask import Flask, render_template


app = Flask( __name__ )


@app.route( "/" )
def month_cur():
    return render_template( "home.html" )


@app.route( "/month/" )
def month( mth ):
    return render_template( "month" )



if __name__ == "__main__":
    app.run( debug=True )
