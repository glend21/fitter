'''
    GD 20210130
    Basics stats analysis of an activity dataframe
'''


import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema


def calc_extrema( df, feature ):
    ''' Returns [local_maxima], [local_minima] of the feature of df as arrays '''
    lmax = argrelextrema( df[ feature ].to_numpy(), np.greater, order=30 )
    max_values = np.array( [ df[ feature ][ i ] for i in lmax[0] ] )
    max_times = np.array( [ df.timestamp[ i ] for i in lmax[0] ] )

    lmin = argrelextrema( df[ feature ].to_numpy(), np.less, order=30 )
    min_values = np.array( [ df[ feature ][ i ] for i in lmin[0] ] )
    min_times = np.array( [ df.timestamp[ i ] for i in lmin[0] ] )

    df1 = pd.DataFrame( min_values, index=min_times )
    df2 = pd.DataFrame( max_values, index=max_times )
    return df1, df2

    # return pd.DataFrame( [ min_times, max_values ] ).T, pd.DataFrame( max_times, max_values ).T


def calc_variability( minima, maxima, mean ):
    ''' Calculates the variability of effort over the activity '''
    # Merges the minima and maxima arrays into 1, in timeseries order
    # Average the absolute values of the differences of each extrema from the mean

    minseries = pd.Series( minima[1])
    minseries.index = minima[0]
    print( minseries )

    return None, None



def main( argc, argv ):
    ''' It '''

    # Only looks at one file, at this stage
    if argc != 2:
        print( "specifiy an input file" )
        sys.exit( -1 )

    df = pd.read_csv( argv[ 1 ] )

    avg = df[ "heart_rate" ].mean()
    print( "Mean HR: %.2f" %  avg )
    std = df[ "heart_rate" ].std() 
    print( "Std. Dev HR: %.2f" % std )
    quant = df[ "heart_rate" ].quantile( (0.25, 0.5, 0.75) )
    print( "Quantile HR: ", quant )

    # Let's smooth HR and see what happens
    plt.figure()
    for i, window in enumerate( (3, 5, 10, 15, 20 ) ):
        name = "smooth%02d" % window
        df[ name ] = df[ "heart_rate" ].rolling( window ).mean()
        plt.subplot( 510 + i + 1 )
        plt.title( "%d" % window, loc='left' )
        plt.plot( df[ name] )
    plt.show()      # savefig( "%s.png" % name )
    return

    # Sets of local maxima and minima of the raw HR values
    minima, maxima = calc_extrema( df, "hr_smooth5" )
    print( "MINIMA:" )
    print( minima )
    print( "MAXIMA:" )
    print( maxima )

    #plt.plot( df.heart_rate, "c" )
    plt.plot( df.timestamp, df.hr_smooth5, "m" )
    # plt.plot( df.timestamp, df.heart_rate )
    plt.plot( maxima, "go" )
    plt.plot( minima, "ro")
    plt.show() 


if __name__ == "__main__":
    main( len( sys.argv ), sys.argv )
