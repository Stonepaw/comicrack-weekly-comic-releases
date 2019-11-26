"""
ComicList.py
Created by SharpDevelop.
User: Stonepaw
Date: 04/04/2010

"""

import clr
import System
import re

clr.AddReference('System.Data')
from System.Data import DataSet, DataColumn

clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import MessageBox

from System.IO import File, Directory

import common

class ComicListData:
	def __init__(self):
		self.Data = DataSet()
		self.Data.DataSetName = "WeekList"
	
	def Load(self):
		try:
			#Replace the old xml file with a dat file as suggested by cYo. This function can be removed in later versions
			if File.Exists(common.SCRIPTDIRECTORY + "Data.xml"):
				File.Move(common.SCRIPTDIRECTORY + "Data.xml", common.SCRIPTDIRECTORY + "data.dat")
			if File.Exists(common.SCRIPTDIRECTORY + "data.dat"):
				self.Data.ReadXml(common.SCRIPTDIRECTORY + "data.dat")
		except Exception, e:
			MessageBox.Show("Something went wrong loading the comic data.\nThe error was: " + str(e))
			return
		
		if not self.Data.Tables.Contains("WeekList"):
			#print "No weeklist yet"
			WeekList = self.Data.Tables.Add("WeekList")
			date = DataColumn("Date")
			date.DataType = System.Type.GetType("System.String")
			WeekList.Columns.Add(date)
			publishers = DataColumn("Publishers")
			publishers.DataType = System.Type.GetType("System.String")
			WeekList.Columns.Add(publishers)
	
	def Save(self):
		try:
			self.Data.WriteXml(common.SCRIPTDIRECTORY + "data.dat")
		except Exception, e:
			MessageBox.Show("Something went wrong saving the comic data.\nThe error was: " + str(e))
	
	def DeleteAll(self):
		#Delete all data in the dataset but keep the Weeklist table for later additions
		total = self.Data.Tables.Count
		#print "Index 0 is:"
		#print self.Data.Tables[0].TableName
		#print "Index 1 is:"
		#print self.Data.Tables[1].TableName
		for table in self.Data.Tables:
			print table.TableName
		indextoremove = []
		for index in range(0, total):
			print index
			
			table = self.Data.Tables[index]
			print table.TableName
			if table.TableName == "WeekList":
				table.Clear()
			else:
				#print "Table is not weeklist"				
				try:
					directoryname = re.sub('[\\\\<>\|:"\*/\?]', "", table.TableName)
					if Directory.Exists(common.SCRIPTDIRECTORY + directoryname):
						Directory.Delete(common.SCRIPTDIRECTORY + directoryname, True)
				except Exception, e:
					MessageBox.Show("Failed to delete directory: " + common.SCRIPTDIRECTORY + table.TableName + ". You will have to delete this directory manually\nThe error was: " + str(e))
				#print "print adding table to remove list: " + table.TableName + str(index)
				indextoremove.append(index)
		#print indextoremove
		indextoremove.sort()
		indextoremove.reverse()
		#print indextoremove
		for i in indextoremove:
			self.Data.Tables.RemoveAt(i)
				
		self.Data.AcceptChanges()
		#for table in self.Data.Tables:
			#print table.TableName

	def RemovePublisher(self, pub):
		if pub:
			#If publisher does not contains a wild character
			if pub.find("*") == -1:
				for table in self.Data.Tables:
					if not table.TableName == "WeekList":
						rowsToRemove = table.Select("Publisher = '" + pub + "'")
						for rowToRemove in rowsToRemove:
							rowToRemove.Delete()
						table.AcceptChanges()
					else:
						for weeklistrow in table.Rows:
							list = weeklistrow["Publishers"].split(",")
							if pub in list:
								list.remove(pub)
								weeklistrow["Publishers"] = ",".join(list)
			#Publisher contains wild character.
			else:
				for table in self.Data.Tables:
					if not table.TableName == "WeekList":
						rowsToRemove = table.Select("Publisher LIKE '" + pub + "'")
						for rowToRemove in rowsToRemove:
							rowToRemove.Delete()
						table.AcceptChanges()
					else:
						for weeklistrow in table.Rows:
							list = weeklistrow["Publishers"].split(",")							
							#If publisher contains...
							if pub.endswith("*") and pub.startswith("*"):
								for l in list[:]:
									if not l.find(pub[1:-1]) == -1:
										list.remove(l)							
							#If publisher ends with....
							elif pub.startswith("*"):
								for l in list[:]:
									if l.endswith(pub[1:]):
										list.remove(l)
							#If publisher starts with...
							elif pub.endswith("*"):
								for l in list[:]:
									if l.startswith(pub[:-1]):
										list.remove(l)
							weeklistrow["Publishers"] = ",".join(list)
