#			WeeklyComicReleases.py
#
#           Author: Stonepaw
#
#			Fetches rss feeds of weekly comics releases
#
#			Versions:
#						0.6 Preferences, publisher, blacklist, and textlist exporting. Also moved to a more modular design
#						0.5 Cover functionality and checkboxes
#                       0.4 Complete rewrite with filtering, local data saving, and new gui
#						0.3 Fixed autoselection of newest week
#						0.2 Removed Links from rss feed
#						0.1 First Script
#
#
#                       Credits: bkagan of the ComicRack forums for the idea.
#
#                       Anyone is free to use all, part or modify this script
##################################################################

import clr
import System

import MainDisplay

#@Name	Weekly Comic Releases
#@Image	feedicon.png
#@Key		weekly-comic-releases-stonepaw
#@Hook	Library

def WeeklyComicReleases(books):
	try:
                MainDisplay.ComicRack = ComicRack
		m = MainDisplay.MainDisplay()
		m.ShowDialog()
		m.Dispose()
	except Exception, e:
		print str(e)
		print type(e)

