"""
inputbox.py
Created by SharpDevelop.
User: Stonepaw
"""
import clr
import System
clr.AddReference("System.Drawing")
import System.Drawing
clr.AddReference("System.Windows.Forms")
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

class InputBox(Form):
	def __init__(self):
		self.InitializeComponent()
		self._typeselect.SelectedIndex = 0
	def InitializeComponent(self):
		self._textBox = System.Windows.Forms.TextBox()
		self._accept = System.Windows.Forms.Button()
		self._typeselect = System.Windows.Forms.ComboBox()
		self._label1 = System.Windows.Forms.Label()
		self.SuspendLayout()
		# 
		# textBox
		# 
		self._textBox.Location = System.Drawing.Point(12, 34)
		self._textBox.Name = "textBox"
		self._textBox.Size = System.Drawing.Size(233, 20)
		self._textBox.TabIndex = 0
		# 
		# accept
		# 
		self._accept.DialogResult = System.Windows.Forms.DialogResult.OK
		self._accept.Location = System.Drawing.Point(251, 31)
		self._accept.Name = "accept"
		self._accept.Size = System.Drawing.Size(75, 23)
		self._accept.TabIndex = 1
		self._accept.Text = "Accept"
		self._accept.UseVisualStyleBackColor = True
		self._accept.Click += self.AcceptClick
		# 
		# typeselect
		# 
		self._typeselect.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._typeselect.FormattingEnabled = True
		self._typeselect.Items.AddRange(System.Array[System.Object](
			["Is",
			"Starts with",
			"Ends with",
			"Contains"]))
		self._typeselect.Location = System.Drawing.Point(78, 4)
		self._typeselect.Name = "typeselect"
		self._typeselect.Size = System.Drawing.Size(121, 21)
		self._typeselect.TabIndex = 2
		# 
		# label1
		# 
		self._label1.Location = System.Drawing.Point(12, 7)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(60, 21)
		self._label1.TabIndex = 3
		self._label1.Text = "Publisher:"
		# 
		# InputBox
		# 
		self.AcceptButton = self._accept
		self.ClientSize = System.Drawing.Size(336, 66)
		self.Controls.Add(self._label1)
		self.Controls.Add(self._typeselect)
		self.Controls.Add(self._accept)
		self.Controls.Add(self._textBox)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow
		self.KeyPreview = True
		self.Name = "InputBox"
		self.ShowIcon = False
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
		self.Text = "Please Enter the Publisher to add to the exclude list"
		self.KeyDown += self.InputBoxKeyDown
		self.ResumeLayout(False)
		self.PerformLayout()

	def InputBoxKeyDown(self, sender, e):
		if e.KeyCode == Keys.Escape:
			self.DialogResult = DialogResult.Cancel
			self.Close()

	def AcceptClick(self, sender, e):
		if self._typeselect.SelectedIndex == 1:
			self._textBox.Text = self._textBox.Text + "*"
		elif self._typeselect.SelectedIndex == 2:
			self._textBox.Text = "*" + self._textBox.Text
		elif self._typeselect.SelectedIndex == 3:
			self._textBox.Text = "*" + self._textBox.Text + "*"