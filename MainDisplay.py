'''MainDiplay.py
Author:Stonepaw
Last Modified: September 8, 2010

Description: This is the main form for the rss feed.
'''
#Credits: Method for check boxes adapted from http://www.windowsclient.net/Samples/Go%20To%20Market/DataGridView/DataGridView%20FAQ.doc

import clr
import re
import System

import Progress
from Progress import Progress

import ComicListParser
import ImageParser

clr.AddReference("System.Drawing")
import System.Drawing
from System.Drawing import Image, Bitmap, Graphics, Point
#from System.Drawing import Image, Bitmap, Graphics

clr.AddReference("System.Windows.Forms")
import System.Windows.Forms
from System.Windows.Forms import *

#For parsing html
#HtmlAgility Pack is licened under the Microsoft Public Licence and as such can be used in this script
#http://htmlagilitypack.codeplex.com/
clr.AddReference('HtmlAgilityPack')
import HtmlAgilityPack
from HtmlAgilityPack import HtmlDocument

import System.IO
from System.IO import FileNotFoundException, File, Directory


clr.AddReference('System.Net')
import System.Net

clr.AddReference('System.Xml')
import System.Xml
from System.Xml import XmlDocument

import Preferences
from Preferences import Preferences

clr.AddReference("System.Data")
import System.Data
from System.Data import DataTable, DataSet, DataColumn, DataRow

from Settings import Settings

import ComicList

import common

import ExportSettings

#for parsing xml
#Xml2py is licenced under the Microsoft Public Licence and as such can be used in this script
#http://devhawk.net/2008/05/07/Deserializing+XML+With+IronPython.aspx
#  Copyright (c) Harry Pierson
import xml2py

localdir = common.SCRIPTDIRECTORY

imageRssDownloaded = {}

class MainDisplay(Form):
	def __init__(self):
		self.InitializeComponent()
		
		self.ComicList = ComicList.ComicListData()
		
		#For storing the check box checked state as a dict with ID value of row and true or false for checkbox value
		#This is to allow for sorting the bound data columns
		self.checkstate = {}
		self.checkstatelist = {}
		
		#Stores images for the grid display
		self.imagelist = {}
		
		#Transparent image for the image display otherwise there is a missing image icon
		self.transparent = Bitmap(10, 10)
		
	def InitializeComponent(self):
		self._components = System.ComponentModel.Container()
		self._weeklist = System.Windows.Forms.ListBox()
		self._label1 = System.Windows.Forms.Label()
		self._filtering = System.Windows.Forms.GroupBox()
		self._publisherFilter = System.Windows.Forms.CheckedListBox()
		self._label2 = System.Windows.Forms.Label()
		self._label3 = System.Windows.Forms.Label()
		self._titleFilter = System.Windows.Forms.TextBox()
		self._comicDisplay = System.Windows.Forms.DataGridView()
		self._refreshFeed = System.Windows.Forms.Button()
		self._dataStore = System.Data.DataSet()
		self._bindingSourceDataGrid = System.Windows.Forms.BindingSource(self._components)
		self._bindingSourceWeek = System.Windows.Forms.BindingSource(self._components)
		self._deselectAll = System.Windows.Forms.Button()
		self._titleType = System.Windows.Forms.ComboBox()
		self._selectAll = System.Windows.Forms.Button()
		self._checkAll = System.Windows.Forms.CheckBox()
		self._comiclistlink = System.Windows.Forms.LinkLabel()
		self._label4 = System.Windows.Forms.Label()
		self._label5 = System.Windows.Forms.Label()
		self._cclink = System.Windows.Forms.LinkLabel()
		self._flowLayoutPanel1 = System.Windows.Forms.FlowLayoutPanel()
		self._preferences = System.Windows.Forms.Button()
		self._displayRightMenu = System.Windows.Forms.ContextMenuStrip(self._components)
		self._addPubBlackList = System.Windows.Forms.ToolStripMenuItem()
		self._exportSelected = System.Windows.Forms.ToolStripMenuItem()
		self._Column1 = System.Windows.Forms.DataGridViewCheckBoxColumn()
		self._Publisher = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Title = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Price = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._ImageDisplay = System.Windows.Forms.DataGridViewImageColumn()
		self._addSelPubBlackList = System.Windows.Forms.ToolStripMenuItem()
		self._filtering.SuspendLayout()
		self._comicDisplay.BeginInit()
		self._dataStore.BeginInit()
		self._bindingSourceDataGrid.BeginInit()
		self._bindingSourceWeek.BeginInit()
		self._flowLayoutPanel1.SuspendLayout()
		self._displayRightMenu.SuspendLayout()
		self.SuspendLayout()
		# 
		# weeklist
		# 
		self._weeklist.DataSource = self._bindingSourceWeek
		self._weeklist.DisplayMember = "Date"
		self._weeklist.FormattingEnabled = True
		self._weeklist.Location = System.Drawing.Point(4, 31)
		self._weeklist.Name = "weeklist"
		self._weeklist.Size = System.Drawing.Size(237, 69)
		self._weeklist.TabIndex = 0
		# 
		# label1
		# 
		self._label1.Location = System.Drawing.Point(4, 9)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(100, 19)
		self._label1.TabIndex = 2
		self._label1.Text = "Select Week:"
		# 
		# filtering
		# 
		self._filtering.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left
		self._filtering.AutoSize = True
		self._filtering.Controls.Add(self._selectAll)
		self._filtering.Controls.Add(self._titleType)
		self._filtering.Controls.Add(self._deselectAll)
		self._filtering.Controls.Add(self._titleFilter)
		self._filtering.Controls.Add(self._label3)
		self._filtering.Controls.Add(self._publisherFilter)
		self._filtering.Controls.Add(self._label2)
		self._filtering.Location = System.Drawing.Point(4, 141)
		self._filtering.MinimumSize = System.Drawing.Size(212, 310)
		self._filtering.Name = "filtering"
		self._filtering.Size = System.Drawing.Size(237, 340)
		self._filtering.TabIndex = 3
		self._filtering.TabStop = False
		self._filtering.Text = "Filtering"
		# 
		# publisherFilter
		# 
		self._publisherFilter.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
		self._publisherFilter.CheckOnClick = True
		self._publisherFilter.FormattingEnabled = True
		self._publisherFilter.Location = System.Drawing.Point(7, 105)
		self._publisherFilter.Name = "publisherFilter"
		self._publisherFilter.Size = System.Drawing.Size(224, 229)
		self._publisherFilter.Sorted = True
		self._publisherFilter.TabIndex = 0
		self._publisherFilter.SelectedIndexChanged += self.UpdateFilter
		# 
		# label2
		# 
		self._label2.Location = System.Drawing.Point(7, 81)
		self._label2.Name = "label2"
		self._label2.Size = System.Drawing.Size(100, 23)
		self._label2.TabIndex = 1
		self._label2.Text = "Publishers:"
		# 
		# label3
		# 
		self._label3.Location = System.Drawing.Point(7, 16)
		self._label3.Name = "label3"
		self._label3.Size = System.Drawing.Size(34, 18)
		self._label3.TabIndex = 2
		self._label3.Text = "Title:"
		# 
		# titleFilter
		# 
		self._titleFilter.Location = System.Drawing.Point(7, 40)
		self._titleFilter.Name = "titleFilter"
		self._titleFilter.Size = System.Drawing.Size(224, 20)
		self._titleFilter.TabIndex = 3
		self._titleFilter.TextChanged += self.UpdateFilter
		# 
		# comicDisplay
		# 
		self._comicDisplay.AllowUserToAddRows = False
		self._comicDisplay.AllowUserToDeleteRows = False
		self._comicDisplay.AllowUserToResizeRows = False
		self._comicDisplay.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
		self._comicDisplay.AutoGenerateColumns = False
		self._comicDisplay.AutoSizeRowsMode = System.Windows.Forms.DataGridViewAutoSizeRowsMode.AllCells
		self._comicDisplay.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize
		self._comicDisplay.Columns.AddRange(System.Array[System.Windows.Forms.DataGridViewColumn](
			[self._Column1,
			self._Publisher,
			self._Title,
			self._Price,
			self._ImageDisplay]))
		self._comicDisplay.DataSource = self._bindingSourceDataGrid
		self._comicDisplay.Location = System.Drawing.Point(247, 0)
		self._comicDisplay.Name = "comicDisplay"
		self._comicDisplay.RowHeadersVisible = False
		self._comicDisplay.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect
		self._comicDisplay.Size = System.Drawing.Size(472, 462)
		self._comicDisplay.TabIndex = 0
		self._comicDisplay.VirtualMode = True
		self._comicDisplay.MouseClick += self.ComicDisplayCellMouseClick
		self._comicDisplay.CellValueNeeded += self.ComicDisplayCellValueNeeded
		self._comicDisplay.CellValuePushed += self.ComicDisplayCellValuePushed
		# 
		# refreshFeed
		# 
		self._refreshFeed.AutoSize = True
		self._refreshFeed.Location = System.Drawing.Point(23, 106)
		self._refreshFeed.Name = "refreshFeed"
		self._refreshFeed.Size = System.Drawing.Size(81, 23)
		self._refreshFeed.TabIndex = 4
		self._refreshFeed.Text = "Refresh Feed"
		self._refreshFeed.UseVisualStyleBackColor = True
		self._refreshFeed.Click += self.RefreshFeedClick
		# 
		# dataStore
		# 
		self._dataStore.DataSetName = "NewDataSet"
		# 
		# deselectAll
		# 
		self._deselectAll.AutoSize = True
		self._deselectAll.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
		self._deselectAll.Location = System.Drawing.Point(158, 76)
		self._deselectAll.Name = "deselectAll"
		self._deselectAll.Size = System.Drawing.Size(73, 23)
		self._deselectAll.TabIndex = 5
		self._deselectAll.Text = "Deselect All"
		self._deselectAll.UseVisualStyleBackColor = True
		self._deselectAll.Click += self.DeselectAllClick
		# 
		# titleType
		# 
		self._titleType.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._titleType.FormattingEnabled = True
		self._titleType.Items.AddRange(System.Array[System.Object](
			["Starts With",
			"Ends With",
			"Contains",
			"Is"]))
		self._titleType.Location = System.Drawing.Point(47, 13)
		self._titleType.Name = "titleType"
		self._titleType.Size = System.Drawing.Size(91, 21)
		self._titleType.TabIndex = 6
		self._titleType.SelectedIndexChanged += self.UpdateFilter
		# 
		# selectAll
		# 
		self._selectAll.AutoSize = True
		self._selectAll.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
		self._selectAll.Location = System.Drawing.Point(91, 76)
		self._selectAll.Name = "selectAll"
		self._selectAll.Size = System.Drawing.Size(61, 23)
		self._selectAll.TabIndex = 7
		self._selectAll.Text = "Select All"
		self._selectAll.UseVisualStyleBackColor = True
		self._selectAll.Click += self.SelectAllClick
		# 
		# checkAll
		# 
		self._checkAll.AutoSize = True
		self._checkAll.Location = System.Drawing.Point(254, 4)
		self._checkAll.Name = "checkAll"
		self._checkAll.Size = System.Drawing.Size(15, 14)
		self._checkAll.TabIndex = 1
		self._checkAll.UseVisualStyleBackColor = True
		self._checkAll.CheckedChanged += self.CheckAllCheckedChanged
		# 
		# comiclistlink
		# 
		self._comiclistlink.AutoSize = True
		self._comiclistlink.Location = System.Drawing.Point(126, 0)
		self._comiclistlink.Name = "comiclistlink"
		self._comiclistlink.Size = System.Drawing.Size(170, 13)
		self._comiclistlink.TabIndex = 5
		self._comiclistlink.TabStop = True
		self._comiclistlink.Text = " Charles LePage @ ComicList.com"
		self._comiclistlink.LinkClicked += self.ComiclistlinkLinkClicked
		# 
		# label4
		# 
		self._label4.Anchor = System.Windows.Forms.AnchorStyles.Top
		self._label4.AutoSize = True
		self._label4.Location = System.Drawing.Point(3, 0)
		self._label4.Name = "label4"
		self._label4.Size = System.Drawing.Size(117, 13)
		self._label4.TabIndex = 6
		self._label4.Text = "Rss feed is copyright(c)"
		# 
		# label5
		# 
		self._label5.AutoSize = True
		self._label5.Location = System.Drawing.Point(302, 0)
		self._label5.Name = "label5"
		self._label5.Size = System.Drawing.Size(37, 13)
		self._label5.TabIndex = 7
		self._label5.Text = "under:"
		# 
		# cclink
		# 
		self._cclink.AutoSize = True
		self._cclink.Location = System.Drawing.Point(345, 0)
		self._cclink.Name = "cclink"
		self._cclink.Size = System.Drawing.Size(406, 13)
		self._cclink.TabIndex = 8
		self._cclink.TabStop = True
		self._cclink.Text = " Creative Commons Attribution-Noncommercial-Share Alike 3.0 United States License"
		self._cclink.LinkClicked += self.CclinkLinkClicked
		# 
		# flowLayoutPanel1
		# 
		self._flowLayoutPanel1.Anchor = System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left
		self._flowLayoutPanel1.AutoSize = True
		self._flowLayoutPanel1.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
		self._flowLayoutPanel1.Controls.Add(self._label4)
		self._flowLayoutPanel1.Controls.Add(self._comiclistlink)
		self._flowLayoutPanel1.Controls.Add(self._label5)
		self._flowLayoutPanel1.Controls.Add(self._cclink)
		self._flowLayoutPanel1.Location = System.Drawing.Point(247, 468)
		self._flowLayoutPanel1.Name = "flowLayoutPanel1"
		self._flowLayoutPanel1.Size = System.Drawing.Size(754, 13)
		self._flowLayoutPanel1.TabIndex = 9
		# 
		# preferences
		# 
		self._preferences.Location = System.Drawing.Point(140, 106)
		self._preferences.Name = "preferences"
		self._preferences.Size = System.Drawing.Size(75, 23)
		self._preferences.TabIndex = 10
		self._preferences.Text = "Preferences"
		self._preferences.UseVisualStyleBackColor = True
		self._preferences.Click += self.PreferencesClick
		# 
		# displayRightMenu
		# 
		self._displayRightMenu.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._addPubBlackList,
			self._addSelPubBlackList,
			self._exportSelected]))
		self._displayRightMenu.Name = "displayRightMenu"
		self._displayRightMenu.RenderMode = System.Windows.Forms.ToolStripRenderMode.System
		self._displayRightMenu.ShowImageMargin = False
		self._displayRightMenu.Size = System.Drawing.Size(242, 92)
		self._displayRightMenu.ItemClicked += self.DisplayRightMenuItemClicked
		# 
		# addPubBlackList
		# 
		self._addPubBlackList.Name = "addPubBlackList"
		self._addPubBlackList.Size = System.Drawing.Size(241, 22)
		self._addPubBlackList.Text = "Add publisher to blacklist"
		# 
		# exportSelected
		# 
		self._exportSelected.Name = "exportSelected"
		self._exportSelected.Size = System.Drawing.Size(241, 22)
		self._exportSelected.Text = "Export Selected"
		# 
		# Column1
		# 
		self._Column1.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.None
		self._Column1.FalseValue = "False"
		self._Column1.HeaderText = ""
		self._Column1.Name = "Column1"
		self._Column1.Resizable = System.Windows.Forms.DataGridViewTriState.False
		self._Column1.TrueValue = "True"
		self._Column1.Width = 25
		# 
		# Publisher
		# 
		self._Publisher.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.AllCells
		self._Publisher.DataPropertyName = "Publisher"
		self._Publisher.HeaderText = "Publisher"
		self._Publisher.Name = "Publisher"
		self._Publisher.ReadOnly = True
		self._Publisher.Width = 75
		# 
		# Title
		# 
		self._Title.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.AllCells
		self._Title.DataPropertyName = "Title"
		self._Title.HeaderText = "Title"
		self._Title.Name = "Title"
		self._Title.ReadOnly = True
		self._Title.Width = 52
		# 
		# Price
		# 
		self._Price.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.AllCells
		self._Price.DataPropertyName = "Price"
		self._Price.HeaderText = "Price"
		self._Price.Name = "Price"
		self._Price.ReadOnly = True
		self._Price.Width = 56
		# 
		# ImageDisplay
		# 
		self._ImageDisplay.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.AllCells
		self._ImageDisplay.HeaderText = "Cover"
		self._ImageDisplay.Name = "ImageDisplay"
		self._ImageDisplay.ReadOnly = True
		self._ImageDisplay.Width = 41
		# 
		# addSelPubBlackList
		# 
		self._addSelPubBlackList.Name = "addSelPubBlackList"
		self._addSelPubBlackList.Size = System.Drawing.Size(241, 22)
		self._addSelPubBlackList.Text = "Add Selected Publishers to Black List"
		# 
		# MainDisplay
		# 
		self.ClientSize = System.Drawing.Size(719, 486)
		self.Controls.Add(self._flowLayoutPanel1)
		self.Controls.Add(self._checkAll)
		self.Controls.Add(self._preferences)
		self.Controls.Add(self._filtering)
		self.Controls.Add(self._comicDisplay)
		self.Controls.Add(self._label1)
		self.Controls.Add(self._refreshFeed)
		self.Controls.Add(self._weeklist)
		self.Name = "MainDisplay"
		self.ShowIcon = False
		self.Text = "Weekly Comic Releases"
		self.Load += self.MainDisplayLoad
		self.FormClosing += self.MainDisplayFormClosing
		self._filtering.ResumeLayout(False)
		self._filtering.PerformLayout()
		self._comicDisplay.EndInit()
		self._dataStore.EndInit()
		self._bindingSourceDataGrid.EndInit()
		self._bindingSourceWeek.EndInit()
		self._flowLayoutPanel1.ResumeLayout(False)
		self._flowLayoutPanel1.PerformLayout()
		self._displayRightMenu.ResumeLayout(False)
		self.ResumeLayout(False)
		self.PerformLayout()

	def RefreshFeedClick(self, sender, e):
		"""
		Get and refresh the database infromation from the feed
		Note that most of this is best put into another thead operation, however, I don't know enough about threading to do it safely.
		"""
		#First try to get the feed xml.
		p = Progress()
		p.Text = "Fetching new rss Items. Please wait..."
		p.Show(self)
		try:
			rssItems = xml2py.parse("http://feeds2.feedburner.com/ncrl")
		except System.Net.WebException, ex:
			print("Something went wrong accessing the rss feed. Are you connected to the internet?")
			MessageBox.Show("Something went wrong accessing the rss feed. Are you connected to the internet?")
			p.Close()
			p.Dispose()
			return
		except Exception, ex:
			print("An unknown error occured accessing the rss feed.")
			MessageBox.Show("An unknown error occured accessing the rss feed.")
			p.Close()
			p.Dispose()
			return
		Application.DoEvents()
		print "got feed"
		clp = ComicListParser.ComicListParser()
		clp.ComicList = self.ComicList.Data
		clp.BlackList = self.Settings.BlackList
		print "moving on"
		if self.Settings.DownloadCovers:
			print "Setting up image downloader"
			imgParser = ImageParser.imageParser()
		#have to do this distinction since rssItems complains if there is only one item
		try:
			#Important to reverse here so that the most recent item gets added to the top of the data table
						
			#For some reason I couldn't get list.reverse to work so...
			entries = []

			for item in rssItems.entry:
				entries.insert(0, item)
				Application.DoEvents()
			
			for entry in entries:
				#Find the data in the title and add it to the WeekList datatable
				print "parsing entry"
				p.Text = "Parsing data for " + entry.title
				weeklistrow, newdatatable = clp.Parse(entry)
				
				#If there was new data found:
				if weeklistrow:
					print "Returned data successfully"
					if self.Settings.DownloadCovers:
						success = imgParser.LoadRss()
						if success:
							p.Text = "Downloading Covers for week of " +  newdatatable.TableName
							imgParser.ParseImages(newdatatable.TableName, newdatatable)
					try:
						#Important to insert the new row at the top position so that they are in order of most recent.
						self.ComicList.Data.Tables["WeekList"].Rows.InsertAt(weeklistrow, 0)
					except Exception, ex:
						print "failed to add datarow"
						print ex				
					try:
						self.ComicList.Data.Tables.Add(newdatatable)
					except Exception, ex:
						print "failed to add data table"
						print ex
				print "finished parsing entry"				
				Application.DoEvents()
				
		except TypeError, e:
			print e
			#Only one entry in the feed
			p.Text = "Parsing data for " + rssItems.entry.title
			weeklistrow, newdatatable = clp.Parse(rssItems.entry)
			
			#If there was new data found:
			if weeklistrow:
				print "Returned data successfully"
				if self.Settings.DownloadCovers:
					success = imgParser.LoadRss()
					if not success:
						p.Close()
						p.Dispose()
						return
					p.Text = "Downloading Covers for week of " +  newdatatable.TableName
					imgParser.ParseImages(newdatatable.TableName, newdatatable)
				try:
					#Important to insert the new row at the top position so that they are in order of most recent.
					self.ComicList.Data.Tables["WeekList"].Rows.InsertAt(weeklistrow, 0)
				except Exception, ex:
					print "failed to add datarow"
					print ex				
				try:
					self.ComicList.Data.Tables.Add(newdatatable)
				except Exception, ex:
					print "failed to add data table"
					print ex
			print "finished parsing entry"				
			Application.DoEvents()
		
		#Check if the datastore has more then 5 week entries
		#If so delete the table in weeklist at the highest index, the oldest
		#And delete the related Table
		tableName = ""
		WeekList = self.ComicList.Data.Tables["WeekList"]
		if WeekList.Rows.Count > 5:
			#Rows starts at 0 but Rows.Count starts at 1
			p.Text = "Deleting old entries"
			Application.DoEvents()
			tableName = WeekList.Rows[WeekList.Rows.Count-1]["Date"]
			WeekList.Rows.RemoveAt(WeekList.Rows.Count-1)
			self.ComicList.Data.Tables.Remove(tableName)
			#Also delete the directory of image if it exists
			dirName = re.sub('[\\\\<>\|:"\*/\?]', "", tableName)
			if Directory.Exists(localdir + dirName):
				Directory.Delete(localdir + dirName, True)
		p.Close()
		p.Dispose()

	def BindingSourceWeekPositionChanged(self, sender, e):
		"""
		Raised when the self._bindingSourceWeek Position changes
		
		Here is where the DataGridView is changed to the selected week from self._bindingSourceWeek.Current
		Also the list of checked rows is changed to a stored list if it exists
				
		"""
		print "Changing Week Position"
		#When the form starts up there is not yet a datatable name
		try:
			self.checkstatelist[self._bindingSourceDataGrid.DataSource.TableName] = self.checkstate
		except AttributeError, err:
			#This is the case when there is not yet something bound to the datagridview.
			#No action needs to be taken.
			print "No datatable bound to the grid view yet"
		
		#Reset the DataGridView to the chosen DataTable
		try:
			self._bindingSourceDataGrid.DataSource = self.ComicList.Data.Tables[self._bindingSourceWeek.Current["Date"]]
		except Exception, e:
			#self._bindingSourceDataGrid.DataSource = None
			print e
			print "Something went wrong"
		try:
		#Clear the filter incase it does not change itself
			self._bindingSourceDataGrid.Filter = ""
			
			#Repopulate the Publisher list
			self.RePopulatePublisherList()
			
			#Set the checkstate list to any a stored list if it exists for the selected tablename
			if self._bindingSourceDataGrid.DataSource.TableName in self.checkstatelist:
				print "checked state is in list"
				self.checkstate = self.checkstatelist[self._bindingSourceDataGrid.DataSource.TableName]
			else:
				print "checked state is not in list"
				self.checkstate = {}
			self.imagelist = {}
		except Exception, ex:
			print "error #1:"
			print ex

	
	def MainDisplayLoad(self, sender, e):
		#Create transparent image
		#TODO: Make a seperate 10X10 white image. See if loading is faster.
		print "Main display loading"
		graphics  = Graphics.FromImage(self.transparent)
		graphics.FillRectangle(System.Drawing.Brushes.Transparent, 0,0,10,10)
		graphics.Dispose()
		
		

		
		self.ComicList.Load()		
		self.Settings = Settings()
		self.Settings.Load()
		self.SetDisplayColumns()
		
		self._bindingSourceWeek.PositionChanged += self.BindingSourceWeekPositionChanged

		self._titleType.SelectedIndex = 0
		
		

		self._bindingSourceWeek.DataSource = self.ComicList.Data.Tables["WeekList"]
		self._bindingSourceWeek.Position = 0
		try:
			self._bindingSourceDataGrid.DataSource = self.ComicList.Data.Tables[self._bindingSourceWeek.Current["Date"]]
		except Exception, ex:
			print ex
			print "Error #2"

	def UpdateFilter(self, sender, e):
		
		publisherfilter = ""
		titlefilter = ""
		if self._publisherFilter.CheckedItems:
			list = self._publisherFilter.CheckedItems
			publisherfilter = "Publisher IN ("
			
			for item in list:
				publisherfilter += "'" + item.replace("'", "\'") + "', "
			#Remove the last ", "
			publisherfilter = publisherfilter.strip(", ") + ")"			
		
		if self._titleFilter.Text:
			titlefilter = "Title LIKE '"
			if self._titleType.SelectedItem == "Ends With" or self._titleType.SelectedItem == "Contains":
				titlefilter += "%"
			titlefilter += self._titleFilter.Text
			if self._titleType.SelectedItem == "Starts With" or self._titleType.SelectedItem == "Contains":
				titlefilter += "%"
			titlefilter += "'"
		
		#Three difference cases here: title and publisher filters, just publisher and just title
		if publisherfilter:
			if titlefilter:
				self._bindingSourceDataGrid.Filter = publisherfilter + " AND " + titlefilter
			else:
				self._bindingSourceDataGrid.Filter = publisherfilter
		else:
			self._bindingSourceDataGrid.Filter = titlefilter

	def DeselectAllClick(self, sender, e):
		#Iterate through a range of index numbers and set theItem  Checked state to false
		for n in range(0, self._publisherFilter.Items.Count):
			self._publisherFilter.SetItemChecked(n, False)
		self.UpdateFilter(None,None)

	def MainDisplayFormClosing(self, sender, e):
		#Update the data.xml file when the windows closes
		try:
			print "Saving data"
			self.ComicList.Save()
			print "Saving Settings"
			self.Settings.Save()
		except Exception, ex:
			print ex
		
		
	def SelectAllClick(self, sender, e):
		for n in range(0, self._publisherFilter.Items.Count):
			self._publisherFilter.SetItemChecked(n, True)
		self.UpdateFilter(None, None)

	def ComicDisplayCellValueNeeded(self, sender, e):
		#Set the value of the cell from the dict
		
		try:
			if e.ColumnIndex == 0:
				ID = sender.Rows[e.RowIndex].DataBoundItem["ID"]
				if ID in self.checkstate:
					e.Value = self.checkstate[ID]
				else:
					e.Value = False
		#Just in case
		except Exception, err:
			print err
			print type(err)
		try:
			if e.ColumnIndex == 4:
				imgPath = sender.Rows[e.RowIndex].DataBoundItem["Image"]
				if imgPath:
					if imgPath in self.imagelist:
						e.Value = self.imagelist[imgPath]
					else:
						self.imagelist[imgPath] = Image.FromFile(imgPath)
						e.Value = self.imagelist[imgPath]
				else:
					e.Value = self.transparent
		except Exception, err:
			print err
			


	def ComicDisplayCellValuePushed(self, sender, e):
		#Set the dict value as the cell value
		#print "Cell value pushed"
		try:
			if e.ColumnIndex == 0:
				ID = sender.Rows[e.RowIndex].DataBoundItem["ID"]
				
				self.checkstate[ID] = e.Value
			#print self.checkstate
		#Just in case
		except Exception, err:
			print err
			print type(err)
	def CheckAllCheckedChanged(self, sender, e):
		#Set every row as the value of the checkbox
		for row in self._comicDisplay.Rows:
			row.Cells[0].Value = sender.Checked
			
	def ComiclistlinkLinkClicked(self, sender, e):
		#Credit where credit is due:
		#print sender.Name
		System.Diagnostics.Process.Start("http://www.comiclist.com/")

	def CclinkLinkClicked(self, sender, e):
		#Licence link
		#print sender.Name
		System.Diagnostics.Process.Start("http://creativecommons.org/licenses/by-nc-sa/3.0/us/")

	def PreferencesClick(self, sender, e):
		pref = Preferences(self.Settings, self.ComicList)
		pref.ShowDialog()
		#print self.Settings.DisplayCovers
		#print self.Settings.DownloadCovers
		self.SetDisplayColumns()
		#print self.imagelist
		#Reload the publisherlist:
		
		#if all data was erased: Have to do this explicitly since they don't seem to be updating automatically
		if not self.ComicList.Data.Tables["WeekList"].Rows:
			self._bindingSourceWeek.ResetBindings(True)
			self._bindingSourceDataGrid.DataSource = None
			self._publisherFilter.Items.Clear()
		else:
			self.RePopulatePublisherList()
		pref.Dispose()

	def ComicDisplayCellMouseClick(self, sender, e):
		if e.Button == MouseButtons.Right:
			hit = sender.HitTest(e.X, e.Y)
			if hit.Type == DataGridViewHitTestType.Cell:
				#Clear other selection and select the row that was right-click on. Have to do this explictly since it's not done automatically
				sender.ClearSelection()
				selectedrow = sender.Rows[hit.RowIndex]
				selectedrow.Selected = True
				
				#Select the publisher from the databound item and add it to the right-click menu item and the tag as well.
				pub = selectedrow.DataBoundItem["Publisher"]
				self._displayRightMenu.Items[0].Text = "Add \"" + pub + "\" to blacklist"
				self._displayRightMenu.Items[0].Tag = pub
				
				#Show the menu at the location where the user click the mouse realtive to the current control.
				self._displayRightMenu.Show(sender, Point(e.X, e.Y))

	def DisplayRightMenuItemClicked(self, sender, e):
		#Close the contextmenu since it will otherwise display above the messageboxs. I don't know why.
		sender.Close()
		if e.ClickedItem.Name == "addPubBlackList":
			print "Add pub clicked"
			
			#We put the publisher name into the item's tag value
			#Should be type str
			pubSelected = e.ClickedItem.Tag
			if type(pubSelected) == str:
				print pubSelected + " is type str"
				print pubSelected
				if MessageBox.Show(pubSelected + " will be added to the blacklist and will no longer be downloaded with new issues.\nAre you sure you want to do this?", "Add Publisher to BlackList", MessageBoxButtons.YesNo, MessageBoxIcon.Warning) == DialogResult.Yes:				
					result = MessageBox.Show("Would you also like to remove all occurences of the publisher " + pubSelected + " from any existing weeklists?", "Delete Existing?", MessageBoxButtons.YesNoCancel, MessageBoxIcon.Question)
					if result == DialogResult.Yes:
						self.ComicList.RemovePublisher(pubSelected)
					elif result == DialogResult.Cancel:
						print "User canceled operation"
						return
					self.Settings.AddToBlackList(pubSelected)
					self.RePopulatePublisherList()
			else:
				MessageBox.Show("Something went wrong passing a publisher to the blacklist.\nPlease try again.")
		elif e.ClickedItem.Name == "addSelPubBlackList":
			print "Add selected pub clicked"
			self._comicDisplay.EndEdit()
			tabledata = self._bindingSourceDataGrid.DataSource
			pubsSelected = []
			for ID in self.checkstate:
				if self.checkstate[ID]:
					selectedrow = tabledata.Select("ID = '" + ID + "'")
					if selectedrow:
						pubSelected = selectedrow[0]["Publisher"]
						if not pubSelected in pubsSelected:
							pubsSelected.append(pubSelected)
			print pubsSelected
			if MessageBox.Show(", ".join(pubsSelected) + " will be added to the blacklist and will no longer be downloaded with new issues.\nAre you sure you want to do this?", "Add Publisher to BlackList", MessageBoxButtons.YesNo, MessageBoxIcon.Warning) == DialogResult.Yes:
                                result = MessageBox.Show("Would you also like to remove all occurences of the publishers " + ", ".join(pubsSelected) + " from any existing weeklists?", "Delete Existing?", MessageBoxButtons.YesNoCancel, MessageBoxIcon.Question)
                                if result == DialogResult.Yes:
                                        for pubSelected in pubsSelected:
                                                self.ComicList.RemovePublisher(pubSelected)
				elif result == DialogResult.Cancel:
                                        print "User canceled operation"
					return
                                for pubSelected in pubsSelected:
                                        self.Settings.AddToBlackList(pubSelected)
##			for pubSelected in pubsSelected:
##				print pubSelected + " is type str"
##				print pubSelected
##				if MessageBox.Show(pubSelected + " will be added to the blacklist and will no longer be downloaded with new issues.\nAre you sure you want to do this?", "Add Publisher to BlackList", MessageBoxButtons.YesNo, MessageBoxIcon.Warning) == DialogResult.Yes:				
##					result = MessageBox.Show("Would you also like to remove and occurences of the publisher " + pubSelected + " from any existing weeklists?", "Delete Existing?", MessageBoxButtons.YesNoCancel, MessageBoxIcon.Question)
##					if result == DialogResult.Yes:
##						self.ComicList.RemovePublisher(pubSelected)
##					elif result == DialogResult.Cancel:
##						print "User canceled operation"
##						return
##					self.Settings.AddToBlackList(pubSelected)
			self.RePopulatePublisherList()

		
		elif e.ClickedItem.Name == "exportSelected":
			self._comicDisplay.EndEdit()
			tabledata = self._bindingSourceDataGrid.DataSource
			if tabledata:
				exportlist = []
				for item in self.checkstate:
					print item
					if self.checkstate[item]:
						try:
							rows = tabledata.Select("ID = '" + str(item) + "'")[0]
							exportlist.append(rows)
						except Exception, ex:
							print ex
							continue
				print exportlist
				if len(exportlist) == 0:
					MessageBox.Show("You must select some comics in order for this function to work.")
					return
				ExportSettings.ComicRack = ComicRack					
				exporter = ExportSettings.ExportSettings(exportlist, tabledata.TableName, self.Settings.Export)
				
				exporter.ShowDialog()
                                self.Settings.Export = exporter._textlist.Checked
				exporter.Dispose()
				
		print self.Settings.BlackList

	def RePopulatePublisherList(self):
		list  = self._bindingSourceWeek.Current["Publishers"].split(',')
		self._publisherFilter.Items.Clear()
		for item in list:
				self._publisherFilter.Items.Add(item, False)
		del(list)
	
	def SetDisplayColumns(self):
		#Column 0 is checkboxes - never hides
		#Column 1 is publisher
		#Column 2 is title -Never hides
		#column 3 is price
		#column 4 is image display
		self._comicDisplay.Columns[1].Visible = self.Settings.DisplayPublisher
		self._comicDisplay.Columns[3].Visible = self.Settings.DisplayPrice
		self._comicDisplay.Columns[4].Visible = self.Settings.DisplayCovers
		
