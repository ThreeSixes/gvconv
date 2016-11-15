#!/usr/bin/python

"""

"""

import datetime
import time
import argparse
import re
import sys

class gvConv():
    def __init__(self, inFile = None):
        
        """
        GammaView file printout conversion handler. Can create monogDB data or files.
        
        inFile = Input file. If not specified this will crash.
        """
        
        # Set class-wide variables.
        self.__inFile = inFile
        self.__extractedData = []
        
        if inFile == None:
            return RuntimeError("An input file name must be specified.")
    
    def __parseLine(self, line):
        """
        Parse a given line into data fields. Returns a dict with the follwing structure:
        [
            <id>: {'bin': <n>, 'counts': <ct>},
            ....
            <id'>: {'bin': <n'>, 'counts': <ct>},
        ]
        """
        # Return value.
        retVal = []
        
        try:
            # Split the starting energy bin number off.
            lineParts = line.strip().split(':')
            
            # Type-correct and push.
            startBin = int(lineParts[0])
            
            counts = re.sub(' +', ' ', lineParts[1].strip()).split(' ')
            
            # Zero out bin ocunt.
            binCt = 0
            
            # For each energy level we have...
            for count in counts:
                # Tack each bin number and count for that bin.
                retVal.append(
                    {'bin': startBin + binCt,
                    'count': int(count)}
                )
                
                # Increment bin count.
                binCt += 1
            
        except:
            raise
        
        return retVal
    
    def __processFile(self):
        """
        Actually process the input file.
        """
        try:
            # Load the input file.
            with open(self.__inFile) as inF:
                # Keep track of the current line!
                lineCursor = 0
                
                # For each line in the opened file.
                for line in inF:
                    # See if we're past the first 4 lines.
                    if lineCursor > 3:
                        # For each entry in each line...
                        lineData = self.__parseLine(line)
                        
                        # Handle each data point.
                        for dataPoint in lineData:
                            # Build an array of our extracted data.
                            
                            self.__extractedData.append(
                                {
                                    'bin': dataPoint['bin'],
                                    'count': dataPoint['count'],
                                }
                            )
                    
                    # Set the next line's #.
                    lineCursor += 1
        
        except:
            raise
        
        return
        
    def __dumpData(self):
        """
        Dump our data.
        """
        try:
            # Dump CSV lines.
            for data in self.__extractedData:
                print("%s, %s" %(data['bin'], data['count']))
        
        except:
            raise
        
        return
        
    def run(self):
        """
        Execute the procedure.
        """
        
        try:
            self.__processFile()
            self.__dumpData()
        
        except:
            raise
        
        return

# Are we being called from CLI?
if __name__ == "__main__":
    import traceback
    
    # Longer strings here:
    epilogStr = "All energy levels are returned in keV, and the script skips the first 3 lines of the input file."
    
    # Set up command line interface.
    parser = argparse.ArgumentParser(description = "Convert GammaVision text \"printout\" to a CSV file with the 'bin' number as the first column, and the event count as the second column.", epilog = "")
    parser.add_argument('infile', help = 'Input file name.')
    
    args = parser.parse_args()
    
    try:
        gvc = gvConv(inFile = args.infile)
        gvc.run()
    
    except:
        tb = traceback.format_exc()
        print("Unhandled exception:\n%s" %tb)