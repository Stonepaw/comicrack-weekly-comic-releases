"""
ExportSettings.py
Created by SharpDevelop.
User: Stonepaw
"""
import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

import textexporter
import filelessexporter

class ExportSettings(Form):
	def __init__(self, exportlist, week, exportsetting):
		self.InitializeComponent()
		self.exportlist = exportlist
		self.weekname = week
                self._textlist.Checked = exportsetting
                self._cbzfiles.Checked = not exportsetting
	
	def InitializeComponent(self):
		self._textlist = System.Windows.Forms.RadioButton()
		self._cbzfiles = System.Windows.Forms.RadioButton()
		self._folderpath = System.Windows.Forms.TextBox()
		self._browse = System.Windows.Forms.Button()
		self._groupBox1 = System.Windows.Forms.GroupBox()
		self._publisher = System.Windows.Forms.CheckBox()
		self._price = System.Windows.Forms.CheckBox()
		self._groupBox2 = System.Windows.Forms.GroupBox()
		self._groupBox3 = System.Windows.Forms.GroupBox()
		self._export = System.Windows.Forms.Button()
		self._cancel = System.Windows.Forms.Button()
		self._selectfile = System.Windows.Forms.SaveFileDialog()
		self._flowLayoutPanel1 = System.Windows.Forms.FlowLayoutPanel()
		self._flowLayoutPanel2 = System.Windows.Forms.FlowLayoutPanel()
		self._groupBox1.SuspendLayout()
		self._groupBox2.SuspendLayout()
		self._groupBox3.SuspendLayout()
		self._flowLayoutPanel1.SuspendLayout()
		self._flowLayoutPanel2.SuspendLayout()
		self.SuspendLayout()
		# 
		# textlist
		# 
		self._textlist.Checked = True
		self._textlist.Location = System.Drawing.Point(44, 19)
		self._textlist.Name = "textlist"
		self._textlist.Size = System.Drawing.Size(104, 24)
		self._textlist.TabIndex = 0
		self._textlist.TabStop = True
		self._textlist.Text = "Text List"
		self._textlist.UseVisualStyleBackColor = True
		self._textlist.CheckedChanged += self.CheckedChanged
		# 
		# cbzfiles
		# 
		self._cbzfiles.AutoSize = True
		self._cbzfiles.Location = System.Drawing.Point(44, 49)
		self._cbzfiles.Name = "cbzfiles"
		self._cbzfiles.Size = System.Drawing.Size(102, 17)
		self._cbzfiles.TabIndex = 1
		self._cbzfiles.TabStop = True
		self._cbzfiles.Text = "Fileless eComics"
		self._cbzfiles.UseVisualStyleBackColor = True
		self._cbzfiles.CheckedChanged += self.CheckedChanged
		# 
		# folderpath
		# 
		self._folderpath.Location = System.Drawing.Point(6, 19)
		self._folderpath.Name = "folderpath"
		self._folderpath.Size = System.Drawing.Size(188, 20)
		self._folderpath.TabIndex = 2
		# 
		# browse
		# 
		self._browse.Location = System.Drawing.Point(61, 45)
		self._browse.Name = "browse"
		self._browse.Size = System.Drawing.Size(75, 23)
		self._browse.TabIndex = 3
		self._browse.Text = "Browse"
		self._browse.UseVisualStyleBackColor = True
		self._browse.Click += self.BrowseClick
		# 
		# groupBox1
		# 
		self._groupBox1.Controls.Add(self._price)
		self._groupBox1.Controls.Add(self._publisher)
		self._groupBox1.Location = System.Drawing.Point(3, 180)
		self._groupBox1.Name = "groupBox1"
		self._groupBox1.Size = System.Drawing.Size(200, 80)
		self._groupBox1.TabIndex = 4
		self._groupBox1.TabStop = False
		self._groupBox1.Text = "3. Set Options"
		# 
		# publisher
		# 
		self._publisher.AutoSize = True
		self._publisher.Checked = True
		self._publisher.CheckState = System.Windows.Forms.CheckState.Checked
		self._publisher.Location = System.Drawing.Point(6, 19)
		self._publisher.Name = "publisher"
		self._publisher.Size = System.Drawing.Size(107, 17)
		self._publisher.TabIndex = 0
		self._publisher.Text = "Include Publisher"
		self._publisher.UseVisualStyleBackColor = True
		# 
		# price
		# 
		self._price.AutoSize = True
		self._price.Checked = True
		self._price.CheckState = System.Windows.Forms.CheckState.Checked
		self._price.Location = System.Drawing.Point(6, 52)
		self._price.Name = "price"
		self._price.Size = System.Drawing.Size(88, 17)
		self._price.TabIndex = 1
		self._price.Text = "Include Price"
		self._price.UseVisualStyleBackColor = True
		# 
		# groupBox2
		# 
		self._groupBox2.Controls.Add(self._textlist)
		self._groupBox2.Controls.Add(self._cbzfiles)
		self._groupBox2.Location = System.Drawing.Point(3, 3)
		self._groupBox2.Name = "groupBox2"
		self._groupBox2.Size = System.Drawing.Size(200, 78)
		self._groupBox2.TabIndex = 5
		self._groupBox2.TabStop = False
		self._groupBox2.Text = "1. Choose Export Type"
		# 
		# groupBox3
		# 
		self._groupBox3.AutoSize = True
		self._groupBox3.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
		self._groupBox3.Controls.Add(self._folderpath)
		self._groupBox3.Controls.Add(self._browse)
		self._groupBox3.Location = System.Drawing.Point(3, 87)
		self._groupBox3.Name = "groupBox3"
		self._groupBox3.Size = System.Drawing.Size(200, 87)
		self._groupBox3.TabIndex = 6
		self._groupBox3.TabStop = False
		self._groupBox3.Text = "2. Choose Location"
		# 
		# export
		# 
		self._export.Location = System.Drawing.Point(15, 3)
		self._export.Margin = System.Windows.Forms.Padding(15, 3, 3, 3)
		self._export.Name = "export"
		self._export.Size = System.Drawing.Size(75, 23)
		self._export.TabIndex = 7
		self._export.Text = "Export"
		self._export.UseVisualStyleBackColor = True
		self._export.Click += self.ExportClick
		# 
		# cancel
		# 
		self._cancel.DialogResult = System.Windows.Forms.DialogResult.Cancel
		self._cancel.Location = System.Drawing.Point(108, 3)
		self._cancel.Margin = System.Windows.Forms.Padding(15, 3, 3, 3)
		self._cancel.Name = "cancel"
		self._cancel.Size = System.Drawing.Size(75, 23)
		self._cancel.TabIndex = 8
		self._cancel.Text = "Cancel"
		self._cancel.UseVisualStyleBackColor = True
		# 
		# selectfile
		# 
		self._selectfile.Filter = "Text File|*.txt"
		# 
		# flowLayoutPanel1
		# 
		self._flowLayoutPanel1.AutoSize = True
		self._flowLayoutPanel1.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
		self._flowLayoutPanel1.Controls.Add(self._groupBox2)
		self._flowLayoutPanel1.Controls.Add(self._groupBox3)
		self._flowLayoutPanel1.Controls.Add(self._groupBox1)
		self._flowLayoutPanel1.Controls.Add(self._flowLayoutPanel2)
		self._flowLayoutPanel1.FlowDirection = System.Windows.Forms.FlowDirection.TopDown
		self._flowLayoutPanel1.Location = System.Drawing.Point(3, 1)
		self._flowLayoutPanel1.Name = "flowLayoutPanel1"
		self._flowLayoutPanel1.Size = System.Drawing.Size(206, 298)
		self._flowLayoutPanel1.TabIndex = 9
		# 
		# flowLayoutPanel2
		# 
		self._flowLayoutPanel2.AutoSize = True
		self._flowLayoutPanel2.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
		self._flowLayoutPanel2.Controls.Add(self._export)
		self._flowLayoutPanel2.Controls.Add(self._cancel)
		self._flowLayoutPanel2.Dock = System.Windows.Forms.DockStyle.Fill
		self._flowLayoutPanel2.Location = System.Drawing.Point(3, 266)
		self._flowLayoutPanel2.Name = "flowLayoutPanel2"
		self._flowLayoutPanel2.Size = System.Drawing.Size(200, 29)
		self._flowLayoutPanel2.TabIndex = 10
		# 
		# ExportSettings
		# 
		self.AcceptButton = self._export
		self.AutoSize = True
		self.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
		self.CancelButton = self._cancel
		self.ClientSize = System.Drawing.Size(224, 331)
		self.Controls.Add(self._flowLayoutPanel1)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog
		self.Name = "ExportSettings"
		self.ShowIcon = False
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
		self._groupBox1.ResumeLayout(False)
		self._groupBox1.PerformLayout()
		self._groupBox2.ResumeLayout(False)
		self._groupBox2.PerformLayout()
		self._groupBox3.ResumeLayout(False)
		self._groupBox3.PerformLayout()
		self._flowLayoutPanel1.ResumeLayout(False)
		self._flowLayoutPanel1.PerformLayout()
		self._flowLayoutPanel2.ResumeLayout(False)
		self.ResumeLayout(False)
		self.PerformLayout()

	def BrowseClick(self, sender, e):
		if self._selectfile.ShowDialog() == DialogResult.OK:
			self._folderpath.Text = self._selectfile.FileName
			
	def ExportClick(self, sender, e):
		#we are creating a text file
		if self._textlist.Checked == True:
			if self._folderpath.Text:
				#print "Creating export file"
				tep = textexporter.textExporter()
				try:
					tep.SaveList(self.exportlist, self.weekname, self._folderpath.Text, self._price.Checked, self._publisher.Checked)
				except Exception, ex:
					print ex
				self.Close()
			else:
				MessageBox.Show("You must specify a location to save the list")
		#We are creating fileless ecomics
		else:
                        filelessexporter.ComicRack = ComicRack
			filelesscreator = filelessexporter.filelessexporter()
			
			try:
				filelesscreator.createFilelessComics(self.exportlist, self._folderpath.Text)
				MessageBox.Show("Successfully created the fileless comics")
			except Exception, ex:
				print ex
				MessageBox.Show("There was an error creating the fileless comics. The error was: \n" + str(ex))			
			self.Close()
		
	def CheckedChanged(self, sender, e):
		if self._cbzfiles.Checked:
			self._groupBox3.Text = "2. Add tags seperated by commas"
			self._browse.Visible = False
			self._groupBox1.Visible = False
		
		else:
			self._groupBox3.Text = "2. Choose Location"
			self._browse.Visible = True
			self._groupBox1.Visible = True
