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

class parse(object):

    def __init__(self, direc):
        self.homedir = os.getcwd() #where this script is
        self.dir = direc;
        self.logdir = self.homedir + self.dir;
        self.datapath = self.logdir + '/data' #where the data is
        self.files = np.array(os.listdir(self.datapath)) #list of files of data
        self.prog = 0; #keeps track of progress
        self.filestat = np.array(os.listdir(self.datapath))
        self.reheader = False;

    #Takes no parameters
    #Iterates through all files in a directory of data, and adds headers
    #to the columns so that they can be grabbed later and reorganized
    #using pandas.
    def addHeaders(self,headers):
        j = 0;
        for f in self.files: 
	    print f
            os.chdir(self.logdir)
            if(self.reheader):
                os.chdir(self.logdir+ '/processed')

            else:
                os.chdir(self.datapath)
            if f[0] != '.':
                self.prog = self.prog + 1;
                #progress();
                if not (os.stat(f).st_size == 0):
                    a = open(f, 'rt')
                    p = pd.read_csv(a);
                    #headers = np.array(["Date/Time","AN0Speed","AN0Gust","AN0Pulse","AN1Speed","AN1Gust","AN1Pulse","AN2Speed","AN2Gust","AN2Pulse","CNT0","CNT1","CNT2","Wdir(Not Used)","Analog0","WV0","WV1","TempC","WV2","Analog5","Analog6","Analog7","?(Not Used)"])[np.newaxis];
                    a = np.concatenate((headers,p), axis=0);
                    if(self.reheader == False):
                        os.chdir(self.logdir + '/withHeaders')
                    np.savetxt(f,a, delimiter=',',fmt="%s")
                    print f;
            j = j + 1;
        os.chdir(self.logdir)



    #Takes no parameters
    #Iterates through directory of data and reorders the data. Outputs final files
    #with selected data columns in a new directory '/processed'
    def reorder(self):
        print "headers"
        self.path = self.logdir + '/withHeaders';
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
                    if self.dir == '/log1':
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
                if self.dir == '/log1':
                    times = np.c_[times,a['AN0Speed']]
                    times = np.c_[times,a['WV0']]
                    times = np.c_[times,loc1]
                    times = np.c_[times,a['AN1Speed']]
                    times = np.c_[times,a['WV1']]
                    times = np.c_[times,loc2]
                    times = np.c_[times,a['AN2Speed']]
                    times = np.c_[times,a['WV2']]
                else:
                    times = np.c_[times,a['AN3Speed']]
                    times = np.c_[times,a['WV3']]
                    times = np.c_[times,loc1]
                    times = np.c_[times,a['AN4Speed']]
                    times = np.c_[times,a['WV4']]
                    times = np.c_[times,loc2]
                    times = np.c_[times,a['AN5Speed']]
                    times = np.c_[times,a['WV5']]
                os.chdir(self.logdir + '/processed')
                np.savetxt(f,times, delimiter=',',fmt="%s")
                filetemp = pd.read_csv(f)
                np.savetxt(f,times, delimiter=',',fmt="%s")
                os.chdir(self.logdir + '/withHeaders')
                #print self.files[j]
        j += 1;
    #os.chdir(self.homedir)
        self.reheader = True
        if self.dir == '/log1':
            self.addHeaders(np.array(["Date/Time","AN0Loc","AN0Speed","WV0","AN1Loc","AN1Speed","WV1","AN2Loc","AN2Speed","WV2"])[np.newaxis]);
        else:
            self.addHeaders(np.array(["Date/Time","AN3Loc","AN3Speed","WV3","AN4Loc","AN4Speed","WV4","AN5Loc","AN5Speed","WV5"])[np.newaxis]);

        self.prog = self.prog + 1;
        self.progress();
        
    def progress(self):
        print('\r>> progress : %i/%i' % (self.prog, self.filestat.shape[0]))
        sys.stdout.flush()
        time.sleep(2)
        
        
if __name__ == "__main__":
    h = parse('/log1');
    l1files = h.files;
    h.addHeaders(headers = np.array(["Date/Time","AN0Speed","AN0Gust","AN0Pulse","AN1Speed","AN1Gust","AN1Pulse","AN2Speed","AN2Gust","AN2Pulse","CNT0","CNT1","CNT2","Wdir(Not Used)","Analog0","WV0","WV1","TempC","WV2","Analog5","Analog6","Analog7","?(Not Used)"])[np.newaxis]);
    h.reorder();
    os.chdir(h.homedir);
    g = parse('/log2');
    l2files = g.files;
    g.addHeaders(headers = np.array(["Date/Time","AN3Speed","AN3Gust","AN3Pulse","AN4Speed","AN4Gust","AN4Pulse","AN5Speed","AN5Gust","AN5Pulse","CNT3","CNT4","CNT5","Wdir(Not Used)","Analog0","WV3","WV4","TempC","WV5","Analog5","Analog6","Analog7","?(Not Used)"])[np.newaxis]);
    g.reorder();
    os.chdir(h.homedir);
    os.mkdir('processedData')

    
    for f in l1files:
        if f in l2files:
            if f[0] != '.':
                a1 = open(h.logdir + '/processed/' + f, 'rt')
                p1 = pd.read_csv(a1);
                a2 = open(g.logdir + '/processed/' + f, 'rt')
                p2 = pd.read_csv(a2)
                print p2;
                p2 = p2[["AN3Loc","AN3Speed","WV3","AN4Loc","AN4Speed","WV4","AN5Loc","AN5Speed","WV5"]]
                #latest error is right here, says can't concatenate because dimensions aren't the same
                combined = pd.concat([p1["Date/Time"],p1["AN0Loc"],p1["AN0Speed"],p1["WV0"],p1['AN1Loc'],p1['AN1Speed'],p1['WV1'],p1['AN2Loc'],p1['AN2Speed'],p1['WV2'],p2["AN3Loc"],p2["AN3Speed"],p2["WV3"],p2["AN4Loc"],p2["AN4Speed"],p2["WV4"],p2["AN5Loc"],p2["AN5Speed"],p2["WV5"]], axis=1)
                #p1 = [p1, p2["AN3Loc"],p2["AN3Speed"],p2["WV3"],p2["AN4Loc"],p2["AN4Speed"],p2["WV4"],p2["AN5Loc"],p2["AN5Speed"],p2["WV5"]]
                headers = np.array(["Date/Time","AN0Loc","AN0Speed","WV0","AN1Loc","AN1Speed","WV1","AN2Loc","AN2Speed","WV2","AN3Loc","AN3Speed","WV3","AN4Loc","AN4Speed","WV4","AN5Loc","AN5Speed","WV5"])[np.newaxis]
                combined = np.concatenate((headers,combined), axis=0);
                np.savetxt(h.homedir + '/processedData/' + f + '_processed',combined, delimiter=',',fmt="%s")
        else:
            os.rename(h.logdir + '/processed/' + f, os.getcwd() + '/processedData/' + f + '_processed')


