 #note: currently must be run in a directory that contains this code, a subdirectory that contains
 #the data called data, an empty directory called withHeaders, and an empty directory called processed.
 
+#this needs to be pushed to the repository 3:30pm 11/26
+#commit "works! now to get the logger1 and logger2 runs to concatenate"
+
 import numpy as np
 import pandas as pd
 import csv
 @@ -17,35 +20,46 @@ def __init__(self):
         self.files = np.array(os.listdir(self.datapath)) #list of files of data
         self.prog = 0; #keeps track of progress
         self.filestat = np.array(os.listdir(self.datapath))
+        self.reheader = False;
 
     #Takes no parameters
     #Iterates through all files in a directory of data, and adds headers
     #to the columns so that they can be grabbed later and reorganized
     #using pandas.
     def addHeaders(self,headers):
-        j=0;
+        j = 0;
         for f in self.files: 
             os.chdir(self.homedir)
-            os.chdir(self.datapath)
-            if self.files[j][0] != '.':
+            if(self.reheader):
+                os.chdir(self.homedir + '/processed')
+            else:
+                os.chdir(self.datapath)
+            if f[0] != '.':
                 self.prog = self.prog + 1;
-                self.progress();
-                a = open(self.files[j], 'rt')
+                #progress();
+                a = open(f, 'rt')
                 p = pd.read_csv(a);
-                np.transpose(headers);
+                #headers = np.array(["Date/Time","AN0Speed","AN0Gust","AN0Pulse","AN1Speed","AN1Gust","AN1Pulse","AN2Speed","AN2Gust","AN2Pulse","CNT0","CNT1","CNT2","Wdir(Not Used)","Analog0","WV0","WV1","TempC","WV2","Analog5","Analog6","Analog7","?(Not Used)"])[np.newaxis];
                 a = np.concatenate((headers,p), axis=0);
-                os.chdir(self.homedir + '/withHeaders')
-                np.savetxt(self.files[j],a, delimiter=',',fmt="%s")
-                j += 1;
+                if(self.reheader == False):
+                    os.chdir(self.homedir + '/withHeaders')
+                np.savetxt(f,a, delimiter=',',fmt="%s")
+                print f;
+            j = j + 1;
         os.chdir(self.homedir)
 
+
+
     #Takes no parameters
     #Iterates through directory of data and reorders the data. Outputs final files
     #with selected data columns in a new directory '/processed'
     def reorder(self):
+        print "headers"
         self.path = self.homedir + '/withHeaders';
         os.chdir(self.path)
+        print os.getcwd()
         self.files = np.array(os.listdir(self.path))
+        print self.files
         midrt0st = datetime.strptime("2011-11-07","%Y-%m-%d")
         midrt0ed = datetime.strptime("2012-05-01","%Y-%m-%d")
         roof2st = datetime.strptime("2011-11-07","%Y-%m-%d")
 @@ -54,8 +68,10 @@ def reorder(self):
         stair2ed = datetime.strptime("2012-02-03","%Y-%m-%d")
         catrt2st = datetime.strptime("2012-03-31","%Y-%m-%d")
         catrt2ed = datetime.strptime("2012-05-01","%Y-%m-%d")
-        catlt2st = datetime.strptime("2012-05-01","%Y-%m-%d")
-        log1 = datetime.strptime("2011-11-07","%Y-%m-%d")
+        catlt2st = datetime.strptime("2011-08-24","%Y-%m-%d")
+        log1 = datetime.strptime("2012-05-01","%Y-%m-%d")
+        log2mv = datetime.strptime("2012-05-01","%Y-%m-%d")
+        log2mv = datetime.strptime("2012-05-01","%Y-%m-%d")
         log2mv = datetime.strptime("2012-05-01","%Y-%m-%d")
         j =0;
 
 @@ -63,15 +79,18 @@ def reorder(self):
             loc0 = np.array((''), dtype=str);
             loc1 = np.array((''), dtype=str);
             loc2 = np.array((''), dtype=str);
-            if self.files[j][0] != '.':
+            print self.files
+            print f[0]
+            if f[0] != '.':
+                print f[0]
                 sys.stdout.flush()
                 time.sleep(2)
                 a = pd.read_csv(f)
                 times = np.array([a['Date/Time']])
                 times = np.transpose(times)
                 s = datetime.strptime(times[j][0], "%Y-%m-%d %H:%M:%S")
-                for j in range(0,times.shape[0]):
-                    tread = datetime.strptime(times[j][0],"%Y-%m-%d %H:%M:%S")
+                for k in range(0,times.shape[0]):
+                    tread = datetime.strptime(times[k][0],"%Y-%m-%d %H:%M:%S")
                     if tread < log1:
                         loc0 = np.append(loc0,"front dome");
                         loc1 = np.append(loc1,"lower right");
 @@ -106,9 +125,12 @@ def reorder(self):
                 np.savetxt(f,times, delimiter=',',fmt="%s")
                 filetemp = pd.read_csv(f)
                 np.savetxt(f,times, delimiter=',',fmt="%s")
-            j += 1;
+                os.chdir(self.homedir + '/withHeaders')
+                #print self.files[j]
+        j += 1;
     #os.chdir(self.homedir)
-        self.addHeaders(["Date/Time","AN0Loc","AN0Speed","WV0","AN1Loc","AN1Speed","WV1","AN2Loc","AN2Speed","WV2"])
+        self.reheader = True
+        self.addHeaders(np.array(["Date/Time","AN0Loc","AN0Speed","WV0","AN1Loc","AN1Speed","WV1","AN2Loc","AN2Speed","WV2"])[np.newaxis]);
         self.prog = self.prog + 1;
         self.progress();
         
 @@ -116,11 +138,10 @@ def progress(self):
         print('\r>> progress : %i/%i' % (self.prog, self.filestat.shape[0]))
         sys.stdout.flush()
         time.sleep(2)
-
         
         
 if __name__ == "__main__":
     h = parse();
     #headers = np.array()
     h.addHeaders(headers = np.array(["Date/Time","AN0Speed","AN0Gust","AN0Pulse","AN1Speed","AN1Gust","AN1Pulse","AN2Speed","AN2Gust","AN2Pulse","CNT0","CNT1","CNT2","Wdir(Not Used)","Analog0","WV0","WV1","TempC","WV2","Analog5","Analog6","Analog7","?(Not Used)"])[np.newaxis]);
-    #h.reorder(); 
+    h.reorder(); 
