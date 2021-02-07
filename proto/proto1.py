

import os
import sys

import fitdecode


fdir = "/mnt/h_drive/SuuntoDiaspora"
fname = "Move_2021_01_25_17_36_09_Running.fit"


with fitdecode.FitReader(os.path.join( fdir, fname ) ) as fit_file:
    for frame in fit_file:
        if isinstance(frame, fitdecode.records.FitDataMessage):
            if frame.name == 'lap':
                # This frame contains data about a lap.
                print("lap")
            
            elif frame.name == 'record':
                # This frame contains data about a "track point".
                print( frame.name )
                for fld in frame.fields:
                    print( "   ", fld.name )
                break;
