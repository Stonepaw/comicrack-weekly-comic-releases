"""
Settings.py
Created by SharpDevelop.
User: Stonepaw
Description: A class for settings, including loading and saving to xml file
"""

import clr
clr.AddReference('System.Xml')
import System.Xml
from System.Xml import XmlReader, XmlWriter, XmlWriterSettings
from System.IO import File

import common

class Settings:
	def __init__(self):
		self.DisplayCovers = True
		self.DownloadCovers = True
		self.DisplayPrice = True
		self.DisplayPublisher = True
		self.BlackList = []
		self.Export = True
	def Load(self, path="settings.dat"):
		#Get settings for the settings.xml file
                #Change the xml to dat. This will be removed in later versions.
		if File.Exists(common.SCRIPTDIRECTORY + "settings.xml"):
                        File.Move(common.SCRIPTDIRECTORY + "settings.xml", common.SCRIPTDIRECTORY + path)
                if File.Exists(common.SCRIPTDIRECTORY + path):
			xreader = XmlReader.Create(common.SCRIPTDIRECTORY + path)
			while xreader.Read():
				if xreader.Name == "DisplayCovers":
					self.DisplayCovers = xreader.ReadElementContentAsBoolean()
					#print self.DisplayCovers
				if xreader.Name == "DownloadCovers":
					self.DownloadCovers = xreader.ReadElementContentAsBoolean()
					#print self.DownloadCovers
				if xreader.Name == "BlackList":
					blacklist = xreader.ReadElementContentAsString()
					self.BlackList = blacklist.split(",")
					#print self.BlackList
				if xreader.Name == "DisplayPrice":
					self.DisplayPrice = xreader.ReadElementContentAsBoolean()
				if xreader.Name == "DisplayPublisher":
					self.DisplayPublisher = xreader.ReadElementContentAsBoolean()
				if xreader.Name == "Export":
                                        self.Export = xreader.ReadElementContentAsBoolean()
			xreader.Close()
			xreader.Dispose()
		else:
			print "settings.xml does not exist yet....\nUsing default values"
			return
	
	def Save(self, path="settings.dat"):
		xsettings = XmlWriterSettings()
		xsettings.Indent = True
		xwriter = XmlWriter.Create(common.SCRIPTDIRECTORY + path, xsettings)
		xwriter.WriteStartElement("Settings")
		xwriter.WriteStartElement("DisplayCovers")
		xwriter.WriteValue(self.DisplayCovers)
		xwriter.WriteEndElement()
		xwriter.WriteStartElement("DownloadCovers")
		xwriter.WriteValue(self.DownloadCovers)
		xwriter.WriteEndElement()
		xwriter.WriteStartElement("BlackList")
		xwriter.WriteString(",".join(self.BlackList))
		xwriter.WriteEndElement()
		xwriter.WriteStartElement("DisplayPrice")
		xwriter.WriteValue(self.DisplayPrice)
		xwriter.WriteEndElement()
		xwriter.WriteStartElement("DisplayPublisher")
		xwriter.WriteValue(self.DisplayPublisher)
		xwriter.WriteEndElement()
		xwriter.WriteStartElement("Export")
		xwriter.WriteValue(self.Export)
		xwriter.WriteEndElement()
		xwriter.Close()
		xwriter.Dispose()
		
	def AddToBlackList(self, pubname):
		"""
		pubname should be string of publisher that will nolonger be downloaded.
		"""
		if pubname:
			if not pubname in self.BlackList:
				self.BlackList.append(pubname)
			else:
				print pubname + " already in blacklist"
