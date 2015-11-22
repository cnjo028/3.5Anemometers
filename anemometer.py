#! /usr/bin/local python
"""
Graph Anemometer Data

Usage: python anemometer.py 

"""

__author__ = "Joseph Huehnerhoff"
__date__="Date: 2011/09/10"

import os, time, sys, getopt, string, re,pprint,thread,threading,subprocess,math
import wx,dateutil
import matplotlib
matplotlib.use('WXAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as dt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
from pytz import timezone


class BarsFrame(wx.Frame):
    title = 'Anamometer Grapher'
    def __init__(self):
        wx.Frame.__init__(self, None,-1, self.title,wx.DefaultPosition,wx.Size(1450,800))
        
        self.anemometer_arr=[]
        self.anemometer2_arr=[]
        self.tel_arr=[]
        self.tel_wind=[]
        self.shut_arr=[]
        self.loc=0
        self.loc2=0
        self.windLoc=0
        self.azLoc=0
        self.ll=None

        self.current=None
        self.create_menu()
        self.create_status_bar()
        self.create_main_panel()
        self.create_sub_panel()

        self.FrameSizer=wx.BoxSizer(wx.HORIZONTAL)
        self.FrameSizer.Add(self.panel)
        self.FrameSizer.Add(self.panel2)
        self.SetSizer(self.FrameSizer)
        
        #self.textcsv.SetValue('/Volumes/Data-Raid/imdirs/jwhueh/anemometer/csv/')
        #self.textlog.SetValue('/Volumes/Data-Raid/imdirs/jwhueh/anemometer/tcc/')
        #self.textmech.SetValue('/Volumes/Data-Raid/imdirs/jwhueh/anemometer/telmech/')
        #self.textimage.SetValue('/Volumes/Data-Raid/imdirs/jwhueh/anemometer/images/')

        self.textcsv.SetValue('/Users/jwhueh/anemometer/logger1/test/')
        self.textlog.SetValue('/Users/jwhueh/anemometer/tcc/test/')
        self.textmech.SetValue('/Users/jwhueh/anemometer/telmech/test/')
        self.textimage.SetValue('/Users/jwhueh/anemometer/images/')

        self.opt1.SetValue(True)
        self.opt2.SetValue(True)
        self.opt3.SetValue(True)
        self.opt9.SetValue(True)
        self.opt10.SetValue(True)
        self.opt11.SetValue(True)
        self.opt12.SetValue(True)

        self.opt4.SetValue(True)
        self.opt5.SetValue(True)
        self.opt6.SetValue(True)
        self.opt7.SetValue(True)

        self.draw_figure()

    def create_menu(self):
        self.menubar = wx.MenuBar()
        
        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
        
        menu_help = wx.Menu()
        m_about = menu_help.Append(-1, "&About\tF1", "About")
        self.Bind(wx.EVT_MENU, self.on_about, m_about)
        
        self.menubar.Append(menu_file, "&File")
        self.menubar.Append(menu_help, "&Help")
        self.SetMenuBar(self.menubar)

    def create_main_panel(self):
        self.panel = wx.Panel(self)
        
        self.dpi = 100
        self.fig = Figure((6.5, 8.0), dpi=self.dpi)
        self.canvas = FigCanvas(self.panel, -1, self.fig)

        self.axes = self.fig.add_subplot(111)

        self.canvas.mpl_connect('key_press_event', self.on_pick)
        
        self.labelcsv=wx.StaticText(self.panel,label='CSV Dir: ')
        self.textcsv = wx.TextCtrl(self.panel,size=(400,-1))
        self.labellog=wx.StaticText(self.panel,label='Log Dir: ')
        self.textlog = wx.TextCtrl(self.panel,size=(400,-1))
        self.labelmech=wx.StaticText(self.panel,label='Telmech Dir: ')
        self.textmech = wx.TextCtrl(self.panel,size=(400,-1))
        self.labelimage=wx.StaticText(self.panel,label='Image Dir: ')
        self.textimage = wx.TextCtrl(self.panel,size=(400,-1))
        
        self.textmulti=wx.TextCtrl(self.panel,size=(325,150),style=wx.TE_MULTILINE)

        self.getButton=wx.Button(self.panel,-1,'Parse Data')
        self.Bind(wx.EVT_BUTTON,self.on_get_button,self.getButton)

        self.folderbutton = wx.Button(self.panel, -1, "Graph")
        self.Bind(wx.EVT_BUTTON, self.on_graph_button, self.folderbutton)

        self.clImage=wx.Button(self.panel, -1, "Clear Images")
        self.Bind(wx.EVT_BUTTON, self.clearImage, self.clImage)

        self.convertButton=wx.Button(self.panel, -1, "Make GIF")
        self.Bind(wx.EVT_BUTTON, self.on_convert_button, self.convertButton)

        self.opt1=wx.CheckBox(self.panel,-1,"Front (Blue)",style=wx.ALIGN_RIGHT)
        self.opt2=wx.CheckBox(self.panel,-1,"Left (Green)",style=wx.ALIGN_RIGHT)
        self.opt3=wx.CheckBox(self.panel,-1,"Right (Red)",style=wx.ALIGN_RIGHT)
        self.opt9=wx.CheckBox(self.panel,-1,"Middle (Cyan)",style=wx.ALIGN_RIGHT)
        self.opt10=wx.CheckBox(self.panel,-1,"Top (Magenta)",style=wx.ALIGN_RIGHT)
        self.opt11=wx.CheckBox(self.panel,-1,"Roof (Yellow)",style=wx.ALIGN_RIGHT)
        self.opt12=wx.CheckBox(self.panel,-1,"Tower (black)",style=wx.ALIGN_RIGHT)
    
        self.opt4=wx.CheckBox(self.panel,-1,"Speed",style=wx.ALIGN_RIGHT)
        self.opt5=wx.CheckBox(self.panel,-1,"Gust",style=wx.ALIGN_RIGHT)
        self.opt6=wx.CheckBox(self.panel,-1,"Direction",style=wx.ALIGN_RIGHT)
        self.opt7=wx.CheckBox(self.panel,-1,"TelData",style=wx.ALIGN_RIGHT)
        self.opt8=wx.CheckBox(self.panel,-1,"MakeImage",style=wx.ALIGN_RIGHT)

        self.advanceText=wx.StaticText(self.panel,label='Advance Length (m): ')
        self.advanceAmount=wx.TextCtrl(self.panel,size=(40,-1),style=wx.ALIGN_RIGHT)
        self.advanceAmount.AppendText('100')

        self.intervalText=wx.StaticText(self.panel,label='Step Pause: ')
        self.intervalAmount=wx.TextCtrl(self.panel,size=(40,-1),style=wx.ALIGN_RIGHT)
        self.intervalAmount.AppendText('0.1')

        self.skipText=wx.StaticText(self.panel,label='Show Every: ')
        self.skipAmount=wx.TextCtrl(self.panel,size=(40,-1),style=wx.ALIGN_RIGHT)
        self.skipAmount.AppendText('1')
       
        self.toolbar = NavigationToolbar(self.canvas)
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.vbox.AddSpacer(10)
        
        self.hbox=wx.BoxSizer(wx.HORIZONTAL)
        self.vboxSmall=wx.BoxSizer(wx.VERTICAL)

        self.hzero=wx.BoxSizer(wx.HORIZONTAL)
        self.hzero.Add(self.toolbar, 0)
        self.hzero.AddSpacer(30)

        self.hboxOptions=wx.BoxSizer(wx.HORIZONTAL)
        self.hboxOptions.Add(self.opt1,0, border=3)
        self.hboxOptions.Add(self.opt2,0, border=3)
        self.hboxOptions.Add(self.opt3,0, border=3)
        self.hboxOptions.Add(self.opt9,0, border=3)
        self.hboxOptions.Add(self.opt10,0, border=3)
        self.hboxOptions.Add(self.opt11,0, border=3)
        self.hboxOptions.Add(self.opt12,0, border=3)
        self.hboxOptions.AddSpacer(30)

        self.hboxOptions2=wx.BoxSizer(wx.HORIZONTAL)
        self.hboxOptions2.Add(self.opt4,0, border=3)
        self.hboxOptions2.Add(self.opt5,0, border=3)
        self.hboxOptions2.Add(self.opt6,0, border=3)
        self.hboxOptions2.Add(self.opt7,0, border=3)
        self.hboxOptions2.Add(self.opt8,0, border=3)
        self.hboxOptions.AddSpacer(30)

        self.hboxStep=wx.BoxSizer(wx.HORIZONTAL)
        self.hboxStep.Add(self.advanceText,0,border=3)
        self.hboxStep.Add(self.advanceAmount,0,border=3)
        self.hboxStep.Add(self.intervalText,0,border=3)
        self.hboxStep.Add(self.intervalAmount,0,border=3)
        self.hboxStep.Add(self.skipText,0,border=3)
        self.hboxStep.Add(self.skipAmount,0,border=3)

        self.hboxcsv = wx.BoxSizer(wx.HORIZONTAL)
        flags = wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL
        self.hboxcsv.Add(self.labelcsv,0,border=3,flag=flags)
        self.hboxcsv.Add(self.textcsv, 0, border=3, flag=flags)
        self.hboxcsv.AddSpacer(30)

        self.hboxlog = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxlog.Add(self.labellog,0,border=3,flag=flags)
        self.hboxlog.Add(self.textlog, 0, border=3, flag=flags)
        self.hboxlog.AddSpacer(30)

        self.hboxmech = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxmech.Add(self.labelmech,0,border=3,flag=flags)
        self.hboxmech.Add(self.textmech, 0, border=3, flag=flags)
        self.hboxmech.AddSpacer(30)

        self.hboximage = wx.BoxSizer(wx.HORIZONTAL)
        self.hboximage.Add(self.labelimage,0,border=3,flag=flags)
        self.hboximage.Add(self.textimage, 0, border=3, flag=flags)
        self.hboximage.AddSpacer(30)

        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox2.Add(self.getButton, 0, border=3, flag=flags)
        self.hbox2.Add(self.folderbutton, 0, border=3, flag=flags)
        self.hbox2.Add(self.clImage, 0, border=3, flag=flags)
        self.hbox2.Add(self.convertButton, 0, border=3, flag=flags)
        self.hbox2.AddSpacer(30)

        self.vboxSmall.Add(self.hzero,0, flag = wx.ALIGN_CENTER | wx.TOP)
        self.vboxSmall.Add(self.hboxOptions,0, flag = wx.ALIGN_CENTER | wx.TOP)
        self.vboxSmall.Add(self.hboxOptions2,0, flag = wx.ALIGN_CENTER | wx.TOP)
        self.vboxSmall.Add(self.hboxStep,0, flag = wx.ALIGN_CENTER | wx.TOP)
        self.vboxSmall.Add(self.hboxcsv, 0, flag = wx.ALIGN_CENTER | wx.TOP)
        self.vboxSmall.Add(self.hboxlog, 0, flag = wx.ALIGN_CENTER | wx.TOP)
        self.vboxSmall.Add(self.hboxmech, 0, flag = wx.ALIGN_CENTER | wx.TOP)
        self.vboxSmall.Add(self.hboximage, 0, flag = wx.ALIGN_CENTER | wx.TOP)
        self.vboxSmall.Add(self.hbox2, 0, flag = wx.ALIGN_CENTER | wx.TOP)    

        self.hbox.Add(self.vboxSmall,0, flag = wx.ALIGN_CENTER | wx.TOP)
        self.hbox.Add(self.textmulti, 0, flag = wx.ALIGN_CENTER | wx.TOP)

        self.vbox.Add(self.hbox, 0, flag = wx.ALIGN_CENTER | wx.TOP)
        
        self.panel.SetSizer(self.vbox)

    def create_sub_panel(self):
        self.panel2 = wx.Panel(self,size=(400,500))
        self.panel2.Bind(wx.EVT_PAINT,self.draw_init)
        self.statbmp = wx.StaticBitmap(self.panel2)
        self.draw_bmp = wx.EmptyBitmap(400, 500)        
        
    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()

    def draw_figure(self):
      if self.current ==None:
        self.axes.clear()        
        self.canvas.draw()
        
    def clearImage(self,event):
        os.system('rm %s*.jpg' % self.textimage.GetValue())
        self.textmulti.AppendText('Images Deleted\n')

    def on_convert_button(self,event):
        thread.start_new_thread(self.convert,())

    def convert(self):
        os.system('convert -delay 25 %s*.jpg %s%s.gif' % (self.textimage.GetValue(),self.textimage.GetValue(), time.strftime('%Y%m%d_%H%M%S')))
        wx.CallAfter(self.textmulti.AppendText,('GIF created\n'))
        return

    def on_graph_button(self,event):
        thread.start_new_thread(self.graph,())

    def on_get_button(self,event):
        thread.start_new_thread(self.parse,())

    def on_pick(self, event):
        #print event.key,event.xdata,event.ydata
        #if g is pressed it gets the information for that time stamp and displays the telescope diagram
        if event.key=='g':
            for index,date in enumerate(self.anemometer_arr[0]):
                if event.xdata <=date:
                    #print date,index
                    self.loc=index
                    break
            for index,date in enumerate(self.anemometer2_arr[0]):
                if event.xdata <=date:
                    #print date,index
                    self.loc2=index
                    break
            self.currentPos(self.loc,self.loc2)      
        #if n is pressed it will take the time from the last time g was pressed and increment one array value (10s)
        if event.key=='n':
            self.advance()
        #pressing p will decrement the diagram one array value (10s)
        if event.key=='p':
            self.retreat()
        #pressing r will run the diagram through the array for the given time in specified in the Advance length box
        if event.key=='r':
            thread.start_new_thread(self.run,())

    def on_text_enter(self, event):
        self.draw_figure()

    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"
        
        dlg = wx.FileDialog(
            self, 
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            self.flash_status_message("Saved to %s" % path)
        
    def on_exit(self, event):
        self.Destroy()
        
    def on_about(self, event):
        msg = """An interactive grapher for In Dome Anemometer Data
         Instructions
         1) data needs to be in separate csv and log directories
         2) select Parse button, depending on log file size this could take 5 minutes
         3) make sure all graphing options are selected, then hit Graph.  
         4) after initial graph individual graphs can be selected and reGraphed
         5) use zoom tool to look at target times
        """
        dlg = wx.MessageDialog(self, msg, "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    
    def flash_status_message(self, msg, flash_len_ms=1500):
        self.statusbar.SetStatusText(msg)
        self.timeroff = wx.Timer(self)
        self.Bind(
            wx.EVT_TIMER, 
            self.on_flash_status_off, 
            self.timeroff)
        self.timeroff.Start(flash_len_ms, oneShot=True)
    
    def on_flash_status_off(self, event):
        self.statusbar.SetStatusText('')

    def numGraph(self):
        #this is s a setup routine for subplots.  it will look at what subplots need to be made and set that to the proper integer value
        x=0
        if self.opt4.GetValue()==True:
            x=x+1
        if self.opt5.GetValue()==True:
            x=x+1
        if self.opt6.GetValue()==True:
            x=x+1
        if self.opt7.GetValue()==True:
            x=x+1
        return x

    def graph(self):
        a_normal=.5
        wx.CallAfter(self.textmulti.AppendText,'-----Graphing-----\n')
        self.fig.clf()
        self.fig.subplots_adjust(hspace=.4)
        self.axes.clear()
        num=str(self.numGraph())+'1'+'1'     #set it to automatically account for number of subplots.
        #plot wind speed
        if self.opt4.GetValue()==True:
            self.axes=self.fig.add_subplot(int(num))
            num=int(num)+1
            self.axes.set_ylabel('mph',size='x-small')
            self.axes.set_title('Wind Speed',size='small')
            if self.opt1.GetValue()==True:
                self.axes.plot_date(self.anemometer_arr[0],self.anemometer_arr[1],alpha=a_normal,fmt='b',tz=timezone('US/Mountain'),xdate=True)
            if self.opt2.GetValue()==True:
                self.axes.plot_date(self.anemometer_arr[0],self.anemometer_arr[7],alpha=a_normal,fmt='g',tz=timezone('US/Mountain'),xdate=True)
            if self.opt3.GetValue()==True:
                self.axes.plot_date(self.anemometer_arr[0],self.anemometer_arr[4],alpha=a_normal,fmt='r',tz=timezone('US/Mountain'),xdate=True)
            if self.opt9.GetValue()==True:
                self.axes.plot_date(self.anemometer2_arr[0],self.anemometer2_arr[1],alpha=a_normal,fmt='c',tz=timezone('US/Mountain'),xdate=True)
            if self.opt10.GetValue()==True:
                self.axes.plot_date(self.anemometer2_arr[0],self.anemometer2_arr[4],alpha=a_normal,fmt='m',tz=timezone('US/Mountain'),xdate=True)
            if self.opt11.GetValue()==True:
                self.axes.plot_date(self.anemometer2_arr[0],self.anemometer2_arr[7],alpha=a_normal,fmt='y',tz=timezone('US/Mountain'),xdate=True)
            if self.opt12.GetValue()==True:
                self.axes.plot_date(self.tel_wind[0],self.tel_wind[2],fmt='k',alpha=.3,tz=timezone('US/Mountain'),xdate=True)
            
            for xlabel_i in self.axes.get_xticklabels():
                xlabel_i.set_fontsize(8)
            for ylabel_i in self.axes.get_yticklabels():
                ylabel_i.set_fontsize(8)
            
        if self.opt5.GetValue()==True:
            self.ax2=self.fig.add_subplot(int(num), sharex=self.axes)
            num=int(num)+1
        
            self.ax2.set_ylabel('mph',size='x-small')
            self.ax2.set_title('Gust',size='small')
            if self.opt1.GetValue()==True:
                self.ax2.plot_date(self.anemometer_arr[0],self.anemometer_arr[2],alpha=a_normal,fmt='b',tz=timezone('US/Mountain'),xdate=True)
            if self.opt2.GetValue()==True:
                self.ax2.plot_date(self.anemometer_arr[0],self.anemometer_arr[8],alpha=a_normal,fmt='g',tz=timezone('US/Mountain'),xdate=True)
            if self.opt3.GetValue()==True:
                self.ax2.plot_date(self.anemometer_arr[0],self.anemometer_arr[5],alpha=a_normal,fmt='r',tz=timezone('US/Mountain'),xdate=True)
            if self.opt9.GetValue()==True:
                self.ax2.plot_date(self.anemometer2_arr[0],self.anemometer2_arr[2],alpha=a_normal,fmt='c',tz=timezone('US/Mountain'),xdate=True)
            if self.opt10.GetValue()==True:
                self.ax2.plot_date(self.anemometer2_arr[0],self.anemometer2_arr[5],alpha=a_normal,fmt='m',tz=timezone('US/Mountain'),xdate=True)
            if self.opt11.GetValue()==True:
                self.ax2.plot_date(self.anemometer2_arr[0],self.anemometer2_arr[8],alpha=a_normal,fmt='y',tz=timezone('US/Mountain'),xdate=True)
        
            for xlabel_i in self.ax2.get_xticklabels():
                xlabel_i.set_fontsize(8)
            for ylabel_i in self.ax2.get_yticklabels():
                ylabel_i.set_fontsize(8)

        #plot direction
        if self.opt6.GetValue()==True:
            self.ax3=self.fig.add_subplot(int(num), sharex=self.axes)
            num=int(num)+1
            self.ax3.set_ylabel('direction (deg)',size='x-small')
            self.ax3.set_title('Direction',size='small')
            if self.opt1.GetValue()==True:
                self.ax3.plot_date(self.anemometer_arr[0],self.anemometer_arr[3],alpha=a_normal,fmt='b.',tz=timezone('US/Mountain'),xdate=True)
            if self.opt2.GetValue()==True:
                self.ax3.plot_date(self.anemometer_arr[0],self.anemometer_arr[9],alpha=a_normal,fmt='g.',tz=timezone('US/Mountain'),xdate=True)
            if self.opt3.GetValue()==True:
                self.ax3.plot_date(self.anemometer_arr[0],self.anemometer_arr[6],alpha=a_normal,fmt='r.',tz=timezone('US/Mountain'),xdate=True)
            if self.opt9.GetValue()==True:
                self.ax3.plot_date(self.anemometer2_arr[0],self.anemometer2_arr[3],alpha=a_normal,fmt='c.',tz=timezone('US/Mountain'),xdate=True)
            if self.opt10.GetValue()==True:
                self.ax3.plot_date(self.anemometer2_arr[0],self.anemometer2_arr[6],alpha=a_normal,fmt='m.',tz=timezone('US/Mountain'),xdate=True)
            if self.opt11.GetValue()==True:
                self.ax3.plot_date(self.anemometer2_arr[0],self.anemometer2_arr[9],alpha=a_normal,fmt='y.',tz=timezone('US/Mountain'),xdate=True)

        
            for xlabel_i in self.ax3.get_xticklabels():
                xlabel_i.set_fontsize(8)
            for ylabel_i in self.ax3.get_yticklabels():
                ylabel_i.set_fontsize(8)
                
        #plot telescope axes position
        if self.opt7.GetValue()==True:
            self.ax4=self.fig.add_subplot(int(num), sharex=self.axes)
            num=int(num)+1
            self.ax4.set_ylabel('deg az=blue',size='x-small')
            self.ax4.set_title('Telescope Data',size='small')
            self.ax4.plot_date(self.tel_arr[0],self.tel_arr[1],fmt='b',tz=timezone('US/Mountain'),xdate=True)
            self.ax4.plot_date(self.tel_arr[0],self.tel_arr[2],fmt='g',tz=timezone('US/Mountain'),xdate=True)
            self.ax4.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d/%m %H'))
            self.ax4.set_xlim(self.anemometer_arr[0][0],self.anemometer_arr[0][len(self.anemometer_arr[0])-1])
            for xlabel_i in self.ax4.get_xticklabels():
                xlabel_i.set_fontsize(8)
            for ylabel_i in self.ax4.get_yticklabels():
                ylabel_i.set_fontsize(8)
        self.shutters()
        self.canvas.draw()
        
    def parse(self):
        file_arr=[]
        time=[]
        time2=[]
        front_speed=[]
        front_gust=[]
        right_speed=[]
        right_gust=[]
        left_speed=[]
        left_gust=[]
        front_dir=[]
        right_dir=[]
        left_dir=[]
        middle_speed=[]
        middle_gust=[]
        middle_dir=[]
        top_speed=[]
        top_gust=[]
        top_dir=[]
        roof_speed=[]
        roof_gust=[]
        roof_dir=[]
        temp=[]
        time_tcc=[]
        alt=[]
        az=[]
        time_mech=[]
        shutter=[]
        
        time_wind_out=[]
        wind_out_speed=[]
        wind_out_dir=[]
        csvdir=self.textcsv.GetValue()
        files=subprocess.Popen(['ls',csvdir],shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p=files.stdout.readlines()
        wx.CallAfter(self.textmulti.AppendText,'---Anemometer Data---\n')
        wx.CallAfter(self.textmulti.AppendText,'---Logger 1---\n')
        for f in p:
            try:
                wx.CallAfter(self.textmulti.AppendText,f)
                file_arr.append(csvdir+f.rstrip('\n'))
                c=open(csvdir+f.rstrip('\n'))
                for index,line in enumerate(c):
                    try:
                        l= line.split(',')
                        if len(l)==23:
                            t=l[0].replace(' ','T')+' MST'
                            dates1=matplotlib.dates.date2num(dateutil.parser.parse(t))
                            time.append(dates1)
                            
                            front_speed.append(l[1])
                            front_gust.append(l[2])
                            right_speed.append(l[4])
                            right_gust.append(l[5])
                            left_speed.append(l[7])
                            left_gust.append(l[8])
                            if float(l[15])<340:
                                front_dir.append(l[15])
                            else:
                                front_dir.append(str(float(l[15])-360))
                            if float(l[16])<340:
                                right_dir.append(l[16])
                            else:
                                right_dir.append(str(float(l[16])-360))
                            left=360-float(l[18])
                            if float(left)<340:
                                left_dir.append(left)
                            else:
                                left_dir.append(str(float(left)-360))

                            temp.append(l[17])
                    except:
                        print 'error with line '+index
                c.close()
            except:
                None
        wx.CallAfter(self.textmulti.AppendText, 'Data Points: '+str(len(time))+'\n')
        print str(len(front_speed)), str(len(front_gust)), str(len(right_speed)), str(len(right_gust)), str(len(left_speed)), str(len(left_gust)), str(len(front_dir)), str(len(right_dir)), str(len(left_dir))
        self.anemometer_arr=[time,front_speed,front_gust,front_dir,right_speed,right_gust,right_dir,left_speed,left_gust,left_dir,temp]

        # Get data for logger 2
        log2dir=csvdir.replace('1','2')
        files=subprocess.Popen(['ls',log2dir],shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p=files.stdout.readlines()
        wx.CallAfter(self.textmulti.AppendText,'---Logger 2---\n')
        for f in p:
            try:
                wx.CallAfter(self.textmulti.AppendText,f)
                file_arr.append(log2dir+f.rstrip('\n'))
                c=open(log2dir+f.rstrip('\n'))
                for index,line in enumerate(c):
                    try:
                        l= line.split(',')
                        if len(l)==23:
                            t2=l[0].replace(' ','T')+' MST'
                            dates2=matplotlib.dates.date2num(dateutil.parser.parse(t2))
                            time2.append(dates2)
                            
                            middle_speed.append(l[1])
                            middle_gust.append(l[2])
                            top_speed.append(l[4])
                            top_gust.append(l[5])
                            roof_speed.append(l[7])
                            roof_gust.append(l[8])
                            if float(l[15])<340:
                                middle_dir.append(l[15])
                            else:
                                middle_dir.append(str(float(l[15])-360))
                            if float(l[16])<340:
                                top_dir.append(l[16])
                            else:
                                top_dir.append(str(float(l[16])-360))
                            roof=360-float(l[18])
                            if float(roof)<340:
                                roof_dir.append(roof)
                            else:
                                roof_dir.append(str(float(roof)-360))
                    except:
                        print 'error with line '+index
                c.close()
            except:
                None
        wx.CallAfter(self.textmulti.AppendText, 'Data Points: '+str(len(time2))+'\n')
        print str(len(time2)),str(len(middle_speed)), str(len(middle_gust)), str(len(top_speed)), str(len(top_gust)),str(len(middle_dir)), str(len(top_dir))
        self.anemometer2_arr=[time2,middle_speed,middle_gust,middle_dir,top_speed,top_gust,top_dir,roof_speed,roof_gust,roof_dir]

        #look at the tcc logs for axes position
        wx.CallAfter(self.textmulti.AppendText,'---TCC Log Data---\n')
        logdir=self.textlog.GetValue()
        logs=subprocess.Popen(['ls',logdir],shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        q=logs.stdout.readlines()
        for f in q:
            try:
                file=open(logdir+f.rstrip('\n'),'r')
                wx.CallAfter(self.textmulti.AppendText,f)
                for line in file:
                    if re.search('AxePos',line):
                        s=line.split(';')
                        time=s[0].split(' <')
                        time=matplotlib.dates.date2num(dateutil.parser.parse(time[0].replace(' ','T'))) 
                        time_tcc.append(time)
                        pos=s[2].replace('AxePos=','')
                        pos=pos.split(',')
                        az.append(float(pos[0]))
                        alt.append(float(pos[1]))
                    if re.search('WindSpeed=',line):
                        q=line.split(';')
                        qt=q[0].split('<')
                        time_out=matplotlib.dates.date2num(dateutil.parser.parse(qt[0].replace(' ','T'))) 
                        time_wind_out.append(time_out)
                        ws=qt[1].split('=')
                        ws=ws[1].replace(' ','')
                        wd=q[1].replace('WindDir=','')
                        wd=wd.replace(' ','')
                        wd=wd.rstrip("'\n")
                        wind_out_speed.append(ws)
                        wind_out_dir.append(wd)
                file.close()
            except:
                None
        
        #look at the telmech log for when the telescope was open or closed
        wx.CallAfter(self.textmulti.AppendText,'Data Points: '+str(len(time_tcc))+'\n') 
        wx.CallAfter(self.textmulti.AppendText,'---Telmech Log Data---\n')
        mechdir=self.textmech.GetValue()
        #print mechdir
        mechlogs=subprocess.Popen(['ls',mechdir],shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        q=mechlogs.stdout.readlines()
        for f in q:
            try:
                file=open(mechdir+f.rstrip('\n'),'r')
                wx.CallAfter(self.textmulti.AppendText,f)
                for line in file:
                    if re.search('device=shutters',line):
                        s=line.split(';')
                        time=s[0].split(' <')
                        time=matplotlib.dates.date2num(dateutil.parser.parse(time[0].replace(' ','T'))) 
                        time_mech.append(time)
                        pos=s[1].split('=')
                        shutter.append(pos[1])
                file.close()
            except:
                None
        wx.CallAfter(self.textmulti.AppendText,'Data Points: '+str(len(time_mech))+'\n') 
        wx.CallAfter(self.textmulti.AppendText,'-------Finished-------\n')
        self.tel_arr=[time_tcc,az,alt]
        self.tel_wind=[time_wind_out,wind_out_dir,wind_out_speed]
        self.shut_arr=[time_mech,shutter]
 
    def draw_init(self,event):
        self.dc=wx.MemoryDC(self.draw_bmp)
        self.gc=wx.GraphicsContext.Create(self.dc)
 
    def windData(self,t):
        for index,time in enumerate(self.tel_wind[0]):
            if t<=time:
                self.windLoc=index
                break
        return

    def azData(self,t):
        for index,time in enumerate(self.tel_arr[0]):
            if t<=time:
                self.azLoc=index
                break
        return

    def currentPos(self,index, index2):
        w=self.getData(index,index2)
        t=str(matplotlib.dates.num2date(w[0][0])).split('+')
        self.step(w[0],w[1],w[2],w[3],t[0])
        self.saveImage(t[0])

    def advance(self):
        w=self.getData(self.loc,self.loc2)
        t=str(matplotlib.dates.num2date(self.anemometer_arr[0][self.loc])).split('+')
        self.step(w[0],w[1],w[2],w[3],t[0])
        self.loc=self.loc+1
        self.loc2=self.loc2+1
        self.saveImage(t[0])

    def retreat(self):
        w=self.getData(self.loc,self.loc2)
        t=str(matplotlib.dates.num2date(self.anemometer_arr[0][self.loc])).split('+')
        self.step(w[0],w[1],w[2],w[3],t[0])
        self.loc=self.loc-1
        self.loc2=self.loc2-1
        self.saveImage(t[0])

    def run(self):
        for x in range(int(float(self.advanceAmount.GetValue())*6)):
            w=self.getData(self.loc,self.loc2)
            t=str(matplotlib.dates.num2date(self.anemometer_arr[0][self.loc])).split('+')
            self.step(w[0],w[1],w[2],w[3],t[0])
            self.loc=self.loc+1  
            self.loc2=self.loc2+1
            self.saveImage(t[0])
            time.sleep(float(self.intervalAmount.GetValue()))
            
    def saveImage(self,t):
        self.statbmp.SetBitmap(self.draw_bmp)
        finished_image = self.statbmp.GetBitmap()
        if self.opt8.GetValue()==True:
            finished_image.SaveFile('%s%s.jpg' % (self.textimage.GetValue(),t), wx.BITMAP_TYPE_JPEG)

    def getData(self,i,i2):
        self.windData(float(self.anemometer_arr[0][i]))
        self.azData(float(self.anemometer_arr[0][i]))
        #time,front,right,left
        dir=[float(self.anemometer_arr[0][i]),float(self.anemometer_arr[3][i]),float(self.anemometer_arr[6][i]),float(self.anemometer_arr[9][i]),float(self.tel_wind[1][self.windLoc]),float(self.tel_arr[1][self.azLoc])]
        #front,right,left
        mag=[float(self.anemometer_arr[1][i]),float(self.anemometer_arr[4][i]),float(self.anemometer_arr[7][i]),float(self.tel_wind[2][self.windLoc]), float(self.tel_arr[2][self.azLoc])]
        #right middle, right top, roof
        dir2=[float(self.anemometer2_arr[0][i2]),float(self.anemometer2_arr[3][i2]),float(self.anemometer2_arr[6][i2]),float(self.anemometer2_arr[9][i2])]
        mag2=[float(self.anemometer2_arr[1][i2]),float(self.anemometer2_arr[4][i2]),float(self.anemometer2_arr[7][i2])]
        return [dir,mag,dir2,mag2]
                   
    def step(self,dir,mag,dir2,mag2,tel_time):
        self.dc.Clear()
        wind=float(dir[4])
        az=float(dir[5])
        alt=float(mag[4])
        #print az,alt
        self.gc.SetPen(wx.Pen('black',1))
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD) 
        text='az: %.1f   alt: %.1f' %(float(az),float(alt))
        text2='Velocity -> outside: %2.1f  front: %2.1f  left: %2.1f  right: %2.1f  middle: %2.1f  top: %2.1f' %(float(mag[3]),float(mag[0]), float(mag[1]),float(mag[2]),float(mag2[0]),float(mag2[1]))
        t2=str(tel_time)
        self.gc.SetFont(font) 
        bigw=400/2
        w1,h1=self.gc.GetTextExtent(text)
        w2,h2=self.gc.GetTextExtent(t2)
        w3,h3=self.gc.GetTextExtent(text2)
        self.gc.DrawText(text, bigw-(w1/2),445) 
        self.gc.DrawText(t2,bigw-(w2/2),425)
        self.gc.DrawText(text2, bigw-(w3/2),465) 

        font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD) 
        self.gc.SetFont(font) 
        self.gc.DrawText('N', 190, 5)
        self.gc.DrawText('E',10,200)
        self.gc.PushState()
        self.gc.PopState()


        arr=self.startPoint(az)    
        self.gc.SetPen(wx.Pen('blue',2))
        #font
        self.arrow([arr[0],arr[1]-5],dir[1]-az,mag[0])   
        #left
        self.gc.SetPen(wx.Pen('green',2))
        self.arrow([arr[10],arr[11]],dir[2]-az,mag[1])  
        #right lower
        self.gc.SetPen(wx.Pen('red',2))
        self.arrow([arr[8],arr[9]],dir[3]-az,mag[2]) 
        #right middle
        self.gc.SetPen(wx.Pen('cyan',2))
        self.arrow([arr[8]+10,arr[9]],dir2[1]-az,mag2[0]) 
        #right top
        self.gc.SetPen(wx.Pen('magenta',2))
        self.arrow([arr[8]+20,arr[9]],dir2[2]-az,mag2[1]) 
        #roof
        self.gc.SetPen(wx.Pen('red',2))
        self.arrow([200,200],dir2[3]-az,mag2[2]) 


        #outside wind
        self.gc.SetPen(wx.Pen('coral',2))
        self.windArrow([300,50],wind+180,mag[3])
        #building, alt vector
        self.gc.SetPen(wx.Pen('black',3))
        self.arrow([200,200],-dir[5]+180,(90-mag[4])/10.)
        
    def startPoint(self,angle):
        x1=0
        y1=0
        x2=0
        y2=0
        x3,y3,x4,y4=0,0,0,0
        if angle <0:
            angle=angle+360
	angle=float(angle)
	a=0
	x=200-(100)*math.sin(float(angle)*(math.pi/180.0))
	y=200+(100)*math.cos(float(angle)*(math.pi/180.0))
	xe=200+(100)*math.sin(float(angle)*(math.pi/180.0))
	ye=200-(100)*math.cos(float(angle)*(math.pi/180.0))

	if angle>=0 and angle<90:
		a=angle
		a=a*(math.pi/180.0)
		x1=x+(100.0*math.cos(a))
		y1=y+(100.0*math.sin(a))
		x2=x-(100.0*math.cos(a))
		y2=y-(100.0*math.sin(a))
                x3=xe-(100.0*math.cos(a))
		y3=ye-(100.0*math.sin(a))
                x4=xe+(100.0*math.cos(a))
                y4=ye+(100*math.sin(a))
	if angle>=90 and angle<180:
		a=180-angle
		a=a*(math.pi/180.0)
		x1=x-(100.0*math.cos(a))
		y1=y+(100.0*math.sin(a))
		x2=x+(100.0*math.cos(a))
		y2=y-(100.0*math.sin(a))
                x3=xe+(100.0*math.cos(a))
		y3=ye-(100.0*math.sin(a))
                x4=xe-(100.0*math.cos(a))
                y4=ye+(100.0*math.sin(a))
	if angle>=180 and angle<270:
		a=270-angle
		a=90-a
		a=a*(math.pi/180.0)
		x1=x-(100.0*math.cos(a))
		y1=y-(100.0*math.sin(a))
		x2=x+(100.0*math.cos(a))
		y2=y+(100.0*math.sin(a))
                x3=xe+(100.0*math.cos(a))
		y3=ye+(100.0*math.sin(a))
                x4=xe-(100.0*math.cos(a))
                y4=ye-(100.0*math.sin(a))
	if angle>=270 and angle<360:
		a=360-angle
		a=a*(math.pi/180.0)
		x1=x+(100.0*math.cos(a))
		y1=y-(100.0*math.sin(a))
		x2=x-(100.0*math.cos(a))
		y2=y+(100.0*math.sin(a))
                x3=xe-(100.0*math.cos(a))
		y3=ye+(100.0*math.sin(a))
                x4=xe+(100.0*math.cos(a))
                y4=ye-(100.0*math.sin(a))
        #print angle,x1,y1
        path=self.gc.CreatePath()
        path.MoveToPoint(x1,y1)
        path.AddLineToPoint(x2,y2)
        path.MoveToPoint(x2,y2)
        path.AddLineToPoint(x3,y3)
        path.MoveToPoint(x3,y3)
        path.AddLineToPoint(x4,y4)
        path.MoveToPoint(x4,y4)
        path.AddLineToPoint(x1,y1)
        self.gc.DrawPath(path)
        
        self.gc.PushState
	return [x,y,xe,ye,x1,y1,x2,y2,x3,y3,x4,y4]
 

    def arrow(self,start, angle, length):
        phi=(90-float(angle))*(math.pi/180.0)
        al=10
        ag=.4
        length=float(length)*12
        path=self.gc.CreatePath()
        path.MoveToPoint(start[0],start[1])
        path.AddLineToPoint(length*math.cos(phi)+start[0],length*math.sin(phi)+start[1])
        path.MoveToPoint(start[0],start[1])
        path.AddLineToPoint(al*math.cos(phi+ag)+start[0], al*math.sin(phi+ag)+start[1])
        path.MoveToPoint(start[0],start[1])
        path.AddLineToPoint(al*math.cos(phi-ag)+start[0], al*math.sin(phi-ag)+start[1])
        self.gc.DrawPath(path)
        self.gc.PushState()


    def windArrow(self,start, angle, length):
        space=150
        yspace=150
        for x in range(3):
            self.arrow([space,35],angle,length)
            self.arrow([space,375],angle,length)
            space+=50
        for y in range(3):
            self.arrow([50,yspace],angle,length)
            self.arrow([350,yspace],angle,length)
            yspace+=50

    def shutters(self):
        current='close'
        previous='close'
        tmp=[]
        for t,s in enumerate(self.shut_arr[1]):
            current=s
            if current != previous:
                tmp.append(t)
            previous=current
        x=0
        for l in range(len(tmp)/2):
            self.axes.axvspan(self.shut_arr[0][tmp[x]],self.shut_arr[0][tmp[x+1]],facecolor='.5',alpha=.5)
            self.ax2.axvspan(self.shut_arr[0][tmp[x]],self.shut_arr[0][tmp[x+1]],facecolor='.5',alpha=.5)
            self.ax3.axvspan(self.shut_arr[0][tmp[x]],self.shut_arr[0][tmp[x+1]],facecolor='.5',alpha=.5)
            self.ax4.axvspan(self.shut_arr[0][tmp[x]],self.shut_arr[0][tmp[x+1]],facecolor='.5',alpha=.5)
                           
            self.canvas.draw() 
            x=x+2

class MyApp(wx.App):
    def OnInit(self):
        frame = BarsFrame()
        frame.Show()  
        return 1


app=MyApp(0)
app.MainLoop()
  
