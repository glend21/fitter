'''
    GD 20210204

    Creates an html map from the supplied geojson file
'''


import os
import sys
import json

import pandas as pd

import folium


def dummy_data():
    ''' '''
    return '''
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [
            115.85752487182617,
            -31.94269430495502
          ],
          [
            115.85022926330566,
            -31.95463830571558
          ],
          [
            115.85898399353026,
            -31.956968661395003
          ],
          [
            115.85838317871092,
            -31.958206638801293
          ],
          [
            115.8734893798828,
            -31.963886556494902
          ],
          [
            115.8823299407959,
            -31.963012745870323
          ],
          [
            115.88353157043458,
            -31.957624063276988
          ],
          [
            115.88172912597656,
            -31.952599195996637
          ],
          [
            115.8800983428955,
            -31.952963326052004
          ],
          [
            115.87984085083008,
            -31.950997006605842
          ],
          [
            115.88069915771483,
            -31.948302352341685
          ],
          [
            115.87735176086426,
            -31.94684574956223
          ],
          [
            115.86919784545898,
            -31.948957816058574
          ],
          [
            115.8584690093994,
            -31.94327697516178
          ]
        ]
      }
    }
  ]
}
'''

def style( feature ):
    ''' Style function for the line string '''
    #print( feature[ "properties" ] )

    # Hard-coding these here for the moment. They are just statistical quartiles. copied
    # from an analysis of 1 run. I will replace them with proper HR zones.
    lower_quartile = 158.0
    upper_quartile = 162.0
    if feature[ "properties" ] < lower_quartile:
        color = "#00ab00"
    elif feature[ "properties" ] > upper_quartile:
        color = "#ab0000"
    else:
        color = "#abab00"

    return { 'color': color,
             'weight': '5' ,
             'fill_opacity': '1.0' 
            }


def main( argc, argv ):
    ''' It '''
    
    if argc != 2:
        print( "%s <geojson>" % argv[0] )
        sys.exit( -1 )

    # '''
    with open( argv[1], "rt" ) as gfh:
        geo = json.load( gfh )

    mymap = folium.Map( location=[ -31.947, 115.859 ], zoom_start=15 )
    folium.GeoJson( geo, 
                    name="Run",
                    style_function=style
                  ).add_to( mymap )
    mymap.save( "foo.html" )


if __name__ == "__main__":
    main( len( sys.argv ), sys.argv )
