"""
Progress.py
Created by SharpDevelop.
User: Stonepaw
Description: As simple progress bar form
"""

import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

class Progress(Form):
	def __init__(self):
		self.InitializeComponent()
	
	def InitializeComponent(self):
		self._progressBar1 = System.Windows.Forms.ProgressBar()
		self.SuspendLayout()
		# 
		# progressBar1
		# 
		self._progressBar1.Dock = System.Windows.Forms.DockStyle.Fill
		self._progressBar1.Location = System.Drawing.Point(0, 0)
		self._progressBar1.Name = "progressBar1"
		self._progressBar1.Size = System.Drawing.Size(318, 34)
		self._progressBar1.Style = System.Windows.Forms.ProgressBarStyle.Marquee
		self._progressBar1.TabIndex = 0
		# 
		# ProgressForm
		# 
		self.ClientSize = System.Drawing.Size(318, 34)
		self.ControlBox = False
		self.Controls.Add(self._progressBar1)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow
		self.Name = "ProgressForm"
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
		self.Text = "Text Here"
		self.TopMost = True
		self.ResumeLayout(False)
