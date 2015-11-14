#note: currently must be run in a directory that contains this code, a subdirectory that contains
#the data called data, an empty directory called withHeaders, and an empty directory called processed.

import numpy as np
import pandas as pd
import csv
import sys
import os
import time

class parse(object):

    def __init__(self):
        self.homedir = os.getcwd() #where this script is
        self.path = self.homedir + '/data' #where the data is
        self.files = np.array(os.listdir(self.path)) #list of files of data

    #Takes no parameters
    #Iterates through all files in a directory of data, and adds headers
    #to the columns so that they can be grabbed later and reorganized
    #using pandas.
    def addHeaders(self):
        j=0;
        print 'Adding Headers...'
        for f in self.files: 
            print('\r>> progress : %i/%i' % (j + 1, self.files.shape[0])),
            sys.stdout.flush()
            time.sleep(2)
            os.chdir(self.homedir)
            os.chdir(self.path)
            a = open(self.files[1], 'rt')
            p = pd.read_csv(a);
            headers = np.array(["Date/Time","AN0Speed","AN0Gust","AN0Pulse","AN1Speed","AN1Gust","AN1Pulse","AN2Speed","AN2Gust","AN2Pulse","CNT0","CNT1","CNT2","Wdir(Not Used)","Analog0","WV0","WV1","TempC","WV2","Analog5","Analog6","Analog7","?(Not Used)"])[np.newaxis]
            np.transpose(headers);
            a = np.concatenate((headers,p), axis=0);
            os.chdir(self.homedir + '/withHeaders')
            np.savetxt(self.files[j],a, delimiter=',',fmt="%s")
            j += 1;
        time.sleep(2)
        print '\ndone'

    #Takes no parameters
    #Iterates through directory of data and reorders the data. Outputs final files
    #with selected data columns in a new directory '/processed'
    def reorder(self):
        self.path = self.homedir + '/withHeaders';
        os.chdir(self.path)
        self.files = np.array(os.listdir(self.path))
        #print 'Reorganizing the data...'
        #for f in self.files: 
            #print('\r>> progress : %i/%i' % (j + 1, self.files.shape[0])),
            #sys.stdout.flush()
            #time.sleep(2)
            #loc0 = np.array(um?)
            #loc1 = np.array(uh)
            #loc2 = np.array(er)
            #date = f['DATE\TIME']
             #   for j in range(0,date.shape[1]):
              #      if blah < date < blah
               #         loc0[j] = ""
                #        loc1[j] = ""
                 #       loc2[j] = ""
                  #  else if ......
                   #     loc0[j] = ""
                    #    loc1[j] = ""
                     #   loc2[j] = ""
                    #else ....
                     #   loc0[j] = ""
                      #  loc1[j] = ""
                       # loc2[j] = ""
                #end 
            
            #something like that

            #dates of location changes are in README

            os.chdir(self.homedir + '/processed')
            np.savetxt(self.files[j],a, delimiter=',',fmt="%s")
            j += 1;
        #time.sleep(2)
        #print '\ndone'
        
    #just a test method ._.
    def test(self):
        
        
if __name__ == "__main__":
    h = parse();
    h.addHeaders();