## Fitter

Some Python tools for reading .fit files and analysing data.

### Overview

This repo contains some tools for displaying and analysing workout results recorded in .fit files.
As a result of Suunto discontinuing support for the very useful Movescount site, I thought I'd
write my own.

__/fitcore/__ : core package reading .fit binary files, creating a local datastore, generating plots

__/fitapp/__ : components for a very basic Flask app. Very much in progress

__/utils/__ : command-line utils. Currently only the driver for creating a custom datastore from downloaded data.

The .fit file format doesn't allow for storing notes or comments about a workout, although this facility was
available on Movescount. Any Movescount workout that contained notes (eg. gym sessions detailing sets and
reps) was downloaded twice: once as a .fit file containing HR data + an other properties, such as geo
locations, power, cadence, etc; and a second time as an .xlsx which contains the 'notes'. The _ingest_
process merges these two files - if both are available for a given workout - taking only the notes from
the .xlsx and all other data from the .fit. The results are stored in a custom file type, whcih is a
concatenation of several Pandas dataframes into one file, which is then gzipped (ie. a .dfz file). The original .fit and
.xlsx files are then no longer needed.

The Flask app build a monthly calendar of workouts from all available .dfz files and allows the user to
drill down into each one. It uses (currently) Folium to produce a static map of the workout, if geo data is
available. eg. run, bike workouts.

It will eventually allow adding of comments to workouts (as per Movescount), tracking KPIs over time, ...


### Dependencies

- Flask
- Flask-WTF (forms)
- Pandas
- Folium
- Bokeh (plots, TBD)
- geojson
- openpyxl
- fitdecode


### Status

Currently importing and merging .fit and .xlsx files.

Very very basic web app, likely with links broken, and bereft of almost any styling whatsoever. Embryonic.

Storing and editing data about an 'athlete' (tee hee!) in progress. Including this set of features as I
can envision creating different athlete profiles over time, depending on training focus.
