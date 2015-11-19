#note: currently must be run in a directory that contains this code, a subdirectory that contains
#the data called data, an empty directory called withHeaders, and an empty directory called processed.

import numpy as np
import pandas as pd
import csv
import sys
import os
import time
from datetime import datetime

class parse(object):

    def __init__(self):
        self.homedir = os.getcwd() #where this script is
        self.path = self.homedir + '/data' #where the data is
        self.files = np.array(os.listdir(self.path)) #list of files of data

    #Takes no parameters
    #Iterates through all files in a directory of data, and adds headers
    #to the columns so that they can be grabbed later and reorganized
    #using pandas.
    def addHeaders(self,headers):
        j=0;
        print 'Adding Headers...'
        for f in self.files: 
            print('\r>> progress : %i/%i' % (j + 1, self.files.shape[0])),
            sys.stdout.flush()
            time.sleep(2)
            os.chdir(self.homedir)
            os.chdir(self.path)
            if self.files[j][0] != '.':
                a = open(self.files[j], 'rt')
                p = pd.read_csv(a);
                np.transpose(headers);
                a = np.concatenate((headers,p), axis=0);
                os.chdir(self.homedir + '/withHeaders')
                np.savetxt(self.files[j],a, delimiter=',',fmt="%s")
                j += 1;
        time.sleep(2)
        os.chdir(self.homedir)
        print '\ndone'

    #Takes no parameters
    #Iterates through directory of data and reorders the data. Outputs final files
    #with selected data columns in a new directory '/processed'
    def reorder(self):
        self.path = self.homedir + '/withHeaders';
        os.chdir(self.path)
        self.files = np.array(os.listdir(self.path))
        
        files = os.listdir(os.getcwd() + '/withHeaders')
        os.chdir(os.getcwd() + '/withHeaders')

        midrt0st = datetime.strptime("2011-11-07","%Y-%m-%d")
        midrt0ed = datetime.strptime("2012-05-01","%Y-%m-%d")
        roof2st = datetime.strptime("2011-11-07","%Y-%m-%d")
        roof2ed = datetime.strptime("2012-01-05","%Y-%m-%d")
        stair2st = datetime.strptime("2012-01-06","%Y-%m-%d")
        stair2ed = datetime.strptime("2012-02-03","%Y-%m-%d")
        catrt2st = datetime.strptime("2012-03-31","%Y-%m-%d")
        catrt2ed = datetime.strptime("2012-05-01","%Y-%m-%d")
        catlt2st = datetime.strptime("2012-05-01","%Y-%m-%d")

        log1 = datetime.strptime("2011-11-07","%Y-%m-%d")
        log2mv = datetime.strptime("2012-05-01","%Y-%m-%d")
        j =0;
        for f in files:
            if files[j][0] != '.':
                a = pd.read_csv(f)
                times = np.array([a['Date/Time']])
                times = np.transpose(times)
                s = datetime.strptime(times[j][0], "%Y-%m-%d %H:%M:%S")
                loc0 = np.array((''), dtype=str);
                loc1 = np.array((''), dtype=str);
                loc2 = np.array((''), dtype=str);
                for j in range(0,times.shape[0]):
                    time = datetime.strptime(times[j][0],"%Y-%m-%d %H:%M:%S")
                    if time < log1:
                        loc0 = np.append(loc0,"front dome");
                        loc1 = np.append(loc1,"lower right");
                        loc2 = np.append(loc2,"lower left");
                    elif time < log2mv:
                        loc0 = np.append(loc0,"middle right");
                        loc1 = np.append(loc1,"top right");
                        if roof2st < time and time < roof2ed:
                            loc2 = np.append(loc2,"roof");
                        elif stair2st < time and time < stair2ed:
                            loc2 = np.append(loc2,"stairwell");
                        elif catrt2st < time < catrt2ed:
                            loc2 = np.append(loc2,"catwalk right");
                        else:
                            loc2 = np.append(loc2,"catwalk left");
                loc0 = np.delete(loc0,0)[np.newaxis];
                loc1 = np.delete(loc1,0)[np.newaxis];
                loc2 = np.delete(loc2,0)[np.newaxis];
                loc0 = np.transpose(loc0);
                loc1 = np.transpose(loc1);
                loc2 = np.transpose(loc2);
                times = np.c_[times,loc0]
                times = np.c_[times,a['AN0Speed']]
                times = np.c_[times,a['WV0']]
                times = np.c_[times,loc1]
                times = np.c_[times,a['AN1Speed']]
                times = np.c_[times,a['WV1']]
                times = np.c_[times,loc2]
                times = np.c_[times,a['AN2Speed']]
                times = np.c_[times,a['WV2']]
                np.savetxt(f,times, delimiter=',',fmt="%s")
                a = pd.read_csv('um.csv')

                #add the headers back
        os.chdir(self.homedir + '/processed')
        np.savetxt(self.files[j],a, delimiter=',',fmt="%s")
        j += 1;
        #time.sleep(2)
        #print '\ndone'
        
    #just a test method ._.
    #def test(self):
        
        
if __name__ == "__main__":
    h = parse();
    h.addHeaders(headers = np.array(["Date/Time","AN0Speed","AN0Gust","AN0Pulse","AN1Speed","AN1Gust","AN1Pulse","AN2Speed","AN2Gust","AN2Pulse","CNT0","CNT1","CNT2","Wdir(Not Used)","Analog0","WV0","WV1","TempC","WV2","Analog5","Analog6","Analog7","?(Not Used)"])[np.newaxis]);