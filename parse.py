#note: currently must be run in a directory that contains this code, a subdirectory that contains
#the data called data, an empty directory called withHeaders, and an empty directory called processed.

#this needs to be pushed to the repository 3:30pm 11/26
#commit "works! now to get the logger1 and logger2 runs to concatenate"

import numpy as np
import pandas as pd
import csv
import sys
import os
import time
from datetime import datetime
import scipy

class parse(object):

    def __init__(self, home, islog2, files1):
        self.home = home #where this script is
        self.datapath = self.home + '/data' #where the data is
        self.files = np.array(os.listdir(self.datapath)) #list of files of data
        self.prog = 0; #keeps track of progress
        self.filestat = np.array(os.listdir(self.datapath))
        self.reheader = False;
        self.islog2 = islog2;
        self.files1 = files1;
        self.nodatetime = False;

    #Takes no parameters
    #Iterates through all files in a directory of data, and adds headers
    #to the columns so that they can be grabbed later and reorganized
    #using pandas.
    def addHeaders(self,headers):
        j = 0;
        for f in self.files: 
            os.chdir(self.home)
            if(self.reheader):
                os.chdir(self.home + '/processed')
            else:
                os.chdir(self.datapath)
            if f[0] != '.':
                self.prog = self.prog + 1;
                #progress();
                a = open(f, 'rt')
                p = pd.read_csv(a);
                if self.nodatetime: #removes date/time column so it can be concatenated to logger1 data
                    p = scipy.delete(p,0,1);
                #headers = np.array(["Date/Time","AN0Speed","AN0Gust","AN0Pulse","AN1Speed","AN1Gust","AN1Pulse","AN2Speed","AN2Gust","AN2Pulse","CNT0","CNT1","CNT2","Wdir(Not Used)","Analog0","WV0","WV1","TempC","WV2","Analog5","Analog6","Analog7","?(Not Used)"])[np.newaxis];
                a = np.concatenate((headers,p), axis=0);
                if(self.reheader == False):
                    os.chdir(self.home + '/withHeaders')
                np.savetxt(f,a, delimiter=',',fmt="%s")
                print f;
            j = j + 1;
        os.chdir(self.home)



    #Takes no parameters
    #Iterates through directory of data and reorders the data. Outputs final files
    #with selected data columns in a new directory '/processed'
    def reorder(self):
        print "headers"
        self.path = self.home + '/withHeaders';
        os.chdir(self.path)
        print os.getcwd()
        self.files = np.array(os.listdir(self.path))
        print self.files
        midrt0st = datetime.strptime("2011-11-07","%Y-%m-%d")
        midrt0ed = datetime.strptime("2012-05-01","%Y-%m-%d")
        roof2st = datetime.strptime("2011-11-07","%Y-%m-%d")
        roof2ed = datetime.strptime("2012-01-05","%Y-%m-%d")
        stair2st = datetime.strptime("2012-01-06","%Y-%m-%d")
        stair2ed = datetime.strptime("2012-02-03","%Y-%m-%d")
        catrt2st = datetime.strptime("2012-03-31","%Y-%m-%d")
        catrt2ed = datetime.strptime("2012-05-01","%Y-%m-%d")
        catlt2st = datetime.strptime("2011-08-24","%Y-%m-%d")
        log1 = datetime.strptime("2012-05-01","%Y-%m-%d")
        log2mv = datetime.strptime("2012-05-01","%Y-%m-%d")
        log2mv = datetime.strptime("2012-05-01","%Y-%m-%d")
        log2mv = datetime.strptime("2012-05-01","%Y-%m-%d")
        j =0;

        for f in self.files: 
            loc0 = np.array((''), dtype=str);
            loc1 = np.array((''), dtype=str);
            loc2 = np.array((''), dtype=str);
            print self.files
            print f[0]
            if f[0] != '.':
                print f[0]
                sys.stdout.flush()
                time.sleep(2)
                a = pd.read_csv(f)
                times = np.array([a['Date/Time']])
                times = np.transpose(times)
                s = datetime.strptime(times[j][0], "%Y-%m-%d %H:%M:%S")
                for k in range(0,times.shape[0]):
                    tread = datetime.strptime(times[k][0],"%Y-%m-%d %H:%M:%S")
                    if tread < log1:
                        loc0 = np.append(loc0,"front dome");
                        loc1 = np.append(loc1,"lower right");
                        loc2 = np.append(loc2,"lower left");
                    else:
                        loc0 = np.append(loc0,"middle right");
                        loc1 = np.append(loc1,"top right");
                        if roof2st < tread and tread < roof2ed:
                            loc2 = np.append(loc2,"roof");
                        elif stair2st < tread and tread < stair2ed:
                            loc2 = np.append(loc2,"stairwell");
                        elif catrt2st < tread and tread < catrt2ed:
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
                os.chdir(self.home + '/processed')
                np.savetxt(f,times, delimiter=',',fmt="%s")
                filetemp = pd.read_csv(f)
                np.savetxt(f,times, delimiter=',',fmt="%s")
                os.chdir(self.home + '/withHeaders')
                #print self.files[j]
        j += 1;
    #os.chdir(self.home)
        if !(islog2):
            self.reheader = True
            self.addHeaders(np.array(["Date/Time","AN0Loc","AN0Speed","WV0","AN1Loc","AN1Speed","WV1","AN2Loc","AN2Speed","WV2"])[np.newaxis]);
        elif !(checkday(f)):
            self.reheader = True
            self.addHeaders(np.array(["Date/Time","AN3Loc","AN3Speed","WV3","AN4Loc","AN4Speed","WV4","AN5Loc","AN5Speed","WV5"])[np.newaxis]);
        else:
            self.reheader = True
            self.nodatetime = True
            self.addHeaders(np.array(["AN0Loc","AN0Speed","WV0","AN1Loc","AN1Speed","WV1","AN2Loc","AN2Speed","WV2"])[np.newaxis]);
        self.prog = self.prog + 1;
        self.progress();
        
    def progress(self):
        print('\r>> progress : %i/%i' % (self.prog, self.filestat.shape[0]))
        sys.stdout.flush()
        time.sleep(2)
        
    def checkday(self, file):
        return file in self.files1;


if __name__ == "__main__":
    h = parse();
    #headers = np.array()
    h.addHeaders(headers = np.array(["Date/Time","AN0Speed","AN0Gust","AN0Pulse","AN1Speed","AN1Gust","AN1Pulse","AN2Speed","AN2Gust","AN2Pulse","CNT0","CNT1","CNT2","Wdir(Not Used)","Analog0","WV0","WV1","TempC","WV2","Analog5","Analog6","Analog7","?(Not Used)"])[np.newaxis]);
    h.reorder();