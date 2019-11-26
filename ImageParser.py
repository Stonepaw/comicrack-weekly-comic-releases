"""
ImageParser.py
Created by SharpDevelop.
User: Stonepaw
"""
import re
import clr
import common
import System

clr.AddReference('System.Net')
import System.Net

clr.AddReference("System.Xml")
from System.Xml import XmlDocument

clr.AddReference("HtmlAgilityPack")
import HtmlAgilityPack

clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Application

from System.IO import Directory, File

localdir = common.SCRIPTDIRECTORY

class imageParser:
	def __init__(self):
		self.imageRssList = ["http://feeds2.feedburner.com/Comiclist-Marvel","http://feeds2.feedburner.com/Comiclist-DC","http://feeds2.feedburner.com/ComiclistDarkHorseThisWeek","http://feeds2.feedburner.com/Comiclist-Image"]
		self.rssCache = {}
		
	def LoadRss(self):
		"""
		Caches the rss feeds so they don't have to be redownloaded over and over again
		"""
		for rss in self.imageRssList:
			if rss not in self.rssCache:
				#TODO replace download with comicracks download functions
				Application.DoEvents()
				#print "rss does not exist, fetching"
				try:
					imgXml = XmlDocument()			
					imgXml.Load(rss)
					
					#Load the wanted items
					imgItems = imgXml.SelectNodes("rss/channel/item")
					self.rssCache[rss] = imgItems
					
				except Exception, ex:
					MessageBox.Show("Something went wrong accessing the rss feed. Are you connected to the internet?")
					print str(ex)
					return False
		#print self.rssCache.keys()
		return True
		
	def ParseImages(self, weekname, data):
		"""
		This is where the images are downloaded from the rss feed
		
		Variables:
			weekname is the name of the week to scrape
			data should be the data table to add to
		"""
		print "Starting to find images"
		
		#Fetched rss feed entrys are stored in the imageRssDownloaded with a key of the url 
		for rss in self.imageRssList:
			imgItems = self.rssCache[rss]
			for imgItem in imgItems:
				Application.DoEvents()

				try:
					if re.search("\d*/\d*/\d*", imgItem['title'].InnerText).group(0) == weekname:
						
						#Load rss into htmldocument for ease of navigation
						
						htdoc = HtmlAgilityPack.HtmlDocument()
						htdoc.LoadHtml(imgItem['description'].InnerText)
						imgTags = htdoc.DocumentNode.SelectNodes("table/tr/td/a/img")
						
						for tag in imgTags:
							Application.DoEvents()
							
							imgTitle = tag.GetAttributeValue("title", None)
							
							imgSrc = tag.GetAttributeValue("src", None)
							
							#If we have both and title and src. No point in doing all this if there is no src or title
							if imgTitle and imgSrc:
								
								#find rows that have a simular title.
								#NOTE: replace occurences of ' with '' to avoid errors
								imgRows = data.Select("Title LIKE '%" + imgTitle.replace("'", "''") + "%'")
								
								for imgRow in imgRows:
									Application.DoEvents()
									try:
										#Create the imagedownloaded
										imgDownloader = System.Net.WebClient()
										
										#Replace illegal charachers in the file name
										imgFileName = re.sub('[\\\\<>\|:"\*/\?]', "", imgTitle)
										imgdirname = re.sub('[\\\\<>\|:"\*/\?]', "", weekname)
										
										#Make sure the directory is not already there
										if not Directory.Exists(localdir + imgdirname):
											Directory.CreateDirectory(localdir + imgdirname)
											
										#In the case of varients and other duplicates. This fixes an bug in 0.5
										if not File.Exists(localdir + imgdirname + "\\" + imgFileName  + ".jpg"):
											imgDownloader.DownloadFile(imgSrc, localdir + imgdirname + "\\" + imgFileName + ".jpg")
										
										#Now set the image column to the path of the image. Note that this is already set to a blank string when the list was first downloaded.
										imgRow["Image"] = localdir + imgdirname + "\\" + imgFileName + ".jpg"
									except Exception, ex:
										print "Error 1"
										print str(ex)
				except Exception, ex:
					print "Error 2"
					print ex