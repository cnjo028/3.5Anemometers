"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app -p wx
"""

from setuptools import setup
import pytz
pytz.zoneinfo=pytz.tzinfo
pytz.zoneinfo.UTC=pytz.UTC

APP = ['anemometer.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': False,
	  'packages':['wx','matplotlib'],
          'site_packages':True,
	  'plist': {
		'CFBundleName':'Anemometer',
		'CFBundleShortVersionString':'0.1',
		},
	   }

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
