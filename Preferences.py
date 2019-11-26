"""
Preferences.py
Created by SharpDevelop.
User: Stonepaw
"""
import clr
clr.AddReference("System.Drawing")
import System.Drawing
clr.AddReference("System.Windows.Forms")
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import MessageBox, MessageBoxButtons, MessageBoxIcon, Form, DialogResult

import Progress

from inputbox import InputBox

class Preferences(Form):
	def __init__(self, settings, clist):
		self.settings = settings
		self.ComicList = clist
		self.InitializeComponent()
		
		self._backWorker = System.ComponentModel.BackgroundWorker()
		# 
		# backWorker
		# 
		self._backWorker.DoWork += self.BackWorkerDoWork
		self._backWorker.RunWorkerCompleted += self.BackWorkerCompleted
		# 
		
		#Putting this stuff here since otherwise Sharpdevelop's form designer doesn't work
		self._displayCovers.Checked = self.settings.DisplayCovers
		self._downloadCovers.Checked = self.settings.DownloadCovers
		self._displayPublisher.Checked = self.settings.DisplayPublisher
		self._displayPrice.Checked = self.settings.DisplayPrice
		
		for listitem in self.settings.BlackList:
			self._blacklistdisplay.Items.Add(listitem)
	
	def InitializeComponent(self):
		self._groupBox1 = System.Windows.Forms.GroupBox()
		self._downloadCovers = System.Windows.Forms.CheckBox()
		self._displayCovers = System.Windows.Forms.CheckBox()
		self._blacklistdisplay = System.Windows.Forms.ListBox()
		self._blacklist = System.Windows.Forms.GroupBox()
		self._Add = System.Windows.Forms.Button()
		self._remove = System.Windows.Forms.Button()
		self._Data = System.Windows.Forms.GroupBox()
		self._deletealldata = System.Windows.Forms.Button()
		self._apply = System.Windows.Forms.Button()
		self._displayPrice = System.Windows.Forms.CheckBox()
		self._displayPublisher = System.Windows.Forms.CheckBox()
		self._groupBox1.SuspendLayout()
		self._blacklist.SuspendLayout()
		self._Data.SuspendLayout()
		self.SuspendLayout()
		# 
		# groupBox1
		# 
		self._groupBox1.Controls.Add(self._displayPublisher)
		self._groupBox1.Controls.Add(self._displayPrice)
		self._groupBox1.Controls.Add(self._displayCovers)
		self._groupBox1.Controls.Add(self._downloadCovers)
		self._groupBox1.Location = System.Drawing.Point(12, 12)
		self._groupBox1.Name = "groupBox1"
		self._groupBox1.Size = System.Drawing.Size(374, 88)
		self._groupBox1.TabIndex = 0
		self._groupBox1.TabStop = False
		self._groupBox1.Text = "Cover Images"
		# 
		# downloadCovers
		# 
		self._downloadCovers.AutoSize = True
		self._downloadCovers.Location = System.Drawing.Point(6, 36)
		self._downloadCovers.Name = "downloadCovers"
		self._downloadCovers.Size = System.Drawing.Size(110, 17)
		self._downloadCovers.TabIndex = 0
		self._downloadCovers.Text = "Download Covers"
		self._downloadCovers.UseVisualStyleBackColor = True
		# 
		# displayCovers
		# 
		self._displayCovers.Location = System.Drawing.Point(138, 19)
		self._displayCovers.Name = "displayCovers"
		self._displayCovers.Size = System.Drawing.Size(104, 24)
		self._displayCovers.TabIndex = 1
		self._displayCovers.Text = "Display Covers"
		self._displayCovers.UseVisualStyleBackColor = True
		# 
		# blacklistdisplay
		# 
		self._blacklistdisplay.FormattingEnabled = True
		self._blacklistdisplay.Location = System.Drawing.Point(6, 19)
		self._blacklistdisplay.Name = "blacklistdisplay"
		self._blacklistdisplay.Size = System.Drawing.Size(260, 186)
		self._blacklistdisplay.Sorted = True
		self._blacklistdisplay.TabIndex = 1
		self._blacklistdisplay.MouseDoubleClick += self.RemoveItem
		# 
		# blacklist
		# 
		self._blacklist.Controls.Add(self._remove)
		self._blacklist.Controls.Add(self._Add)
		self._blacklist.Controls.Add(self._blacklistdisplay)
		self._blacklist.ForeColor = System.Drawing.SystemColors.ControlText
		self._blacklist.Location = System.Drawing.Point(12, 107)
		self._blacklist.Name = "blacklist"
		self._blacklist.Size = System.Drawing.Size(374, 216)
		self._blacklist.TabIndex = 2
		self._blacklist.TabStop = False
		self._blacklist.Text = "Blacklist"
		# 
		# Add
		# 
		self._Add.Location = System.Drawing.Point(283, 49)
		self._Add.Name = "Add"
		self._Add.Size = System.Drawing.Size(75, 23)
		self._Add.TabIndex = 2
		self._Add.Text = "Add"
		self._Add.UseVisualStyleBackColor = True
		self._Add.Click += self.AddItem
		# 
		# remove
		# 
		self._remove.Location = System.Drawing.Point(283, 149)
		self._remove.Name = "remove"
		self._remove.Size = System.Drawing.Size(75, 23)
		self._remove.TabIndex = 3
		self._remove.Text = "Remove"
		self._remove.UseVisualStyleBackColor = True
		self._remove.MouseClick += self.RemoveItem
		# 
		# Data
		# 
		self._Data.Controls.Add(self._deletealldata)
		self._Data.Location = System.Drawing.Point(13, 330)
		self._Data.Name = "Data"
		self._Data.Size = System.Drawing.Size(373, 57)
		self._Data.TabIndex = 3
		self._Data.TabStop = False
		self._Data.Text = "Data"
		# 
		# deletealldata
		# 
		self._deletealldata.AutoSize = True
		self._deletealldata.ForeColor = System.Drawing.Color.Red
		self._deletealldata.Location = System.Drawing.Point(111, 17)
		self._deletealldata.Name = "deletealldata"
		self._deletealldata.Size = System.Drawing.Size(151, 23)
		self._deletealldata.TabIndex = 0
		self._deletealldata.Text = "Delete All Downloaded Data"
		self._deletealldata.UseVisualStyleBackColor = True
		self._deletealldata.Click += self.DeletealldataClick
		# 
		# apply
		# 
		self._apply.DialogResult = System.Windows.Forms.DialogResult.OK
		self._apply.Location = System.Drawing.Point(311, 402)
		self._apply.Name = "apply"
		self._apply.Size = System.Drawing.Size(75, 23)
		self._apply.TabIndex = 4
		self._apply.Text = "Done"
		self._apply.UseVisualStyleBackColor = True
		self._apply.Click += self.ApplyClick
		# 
		# displayPrice
		# 
		self._displayPrice.Location = System.Drawing.Point(264, 19)
		self._displayPrice.Name = "displayPrice"
		self._displayPrice.Size = System.Drawing.Size(104, 24)
		self._displayPrice.TabIndex = 2
		self._displayPrice.Text = "Display Price"
		self._displayPrice.UseVisualStyleBackColor = True
		# 
		# displayPublisher
		# 
		self._displayPublisher.AutoSize = True
		self._displayPublisher.Location = System.Drawing.Point(138, 57)
		self._displayPublisher.Name = "displayPublisher"
		self._displayPublisher.Size = System.Drawing.Size(106, 17)
		self._displayPublisher.TabIndex = 3
		self._displayPublisher.Text = "Display Publisher"
		self._displayPublisher.UseVisualStyleBackColor = True
		# 
		# Preferences
		# 
		self.AcceptButton = self._apply
		self.ClientSize = System.Drawing.Size(397, 437)
		self.Controls.Add(self._apply)
		self.Controls.Add(self._Data)
		self.Controls.Add(self._blacklist)
		self.Controls.Add(self._groupBox1)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog
		self.Name = "Preferences"
		self.ShowIcon = False
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
		self.Text = "Preferences"
		self._groupBox1.ResumeLayout(False)
		self._groupBox1.PerformLayout()
		self._blacklist.ResumeLayout(False)
		self._Data.ResumeLayout(False)
		self._Data.PerformLayout()
		self.ResumeLayout(False)

	def DeletealldataClick(self, sender, e):
		result = MessageBox.Show("Are you absolutely sure you want to delete all the downloaded data?", "Delete all data", MessageBoxButtons.YesNo, MessageBoxIcon.Warning)
		if result == DialogResult.Yes:
			#MessageBox.Show("Not yet implemented")
			#print self.Owner
			self.p = Progress.Progress()
			self.p.Text = "Deleting all downloaded data. Please wait...."
			self.p.Show()
			self._backWorker.RunWorkerAsync()
			

	def ApplyClick(self, sender, e):
		self.settings.DisplayCovers = self._displayCovers.Checked
		self.settings.DownloadCovers = self._downloadCovers.Checked
		self.settings.BlackList = list(self._blacklistdisplay.Items)
		self.settings.DisplayPrice = self._displayPrice.Checked
		self.settings.DisplayPublisher = self._displayPublisher.Checked
		print self.settings.BlackList
		
	def RemoveItem(self, sender, e):
		if not self._blacklistdisplay.SelectedIndex == -1:
			self._blacklistdisplay.Items.RemoveAt(self._blacklistdisplay.SelectedIndex)
	
	def AddItem(self, sender, e):
		input =  InputBox()
		result = input.ShowDialog()
		if result == DialogResult.OK:
			text = input._textBox.Text
			if text:
				mesgresult = MessageBox.Show(text + " will be added to the BlackList.\n\nWould you also like to remove any occurences of this publisher from the already downloaded data?\n\n(Clicking Cancel will not add this publisher to the BlackList)", "Delete existing?", MessageBoxButtons.YesNoCancel, MessageBoxIcon.Question)
				if mesgresult == DialogResult.Yes:
					self._blacklistdisplay.Items.Add(text)
					self.ComicList.RemovePublisher(text)
				elif mesgresult == DialogResult.No:
					self._blacklistdisplay.Items.Add(text)
		input.Dispose()
		#print input
		#MessageBox.Show("Not yet implemented")

	def BackWorkerDoWork(self, sender, e):
		self.ComicList.DeleteAll()
		
	def BackWorkerCompleted(self, sender, e):
		self.p.Close()
		self.p.Dispose()