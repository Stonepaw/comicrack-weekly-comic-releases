"""
textexporter.py
Created by SharpDevelop.
User: Stonepaw
Description: A class for exporting a text list from given data rows
"""

from System.IO import StreamWriter, File


class textExporter:
	def __init__(self):
		pass
	
	def SaveList(self, exportlist, week, path, price, publisher):
		if path:
			print "Creating file"
			w = StreamWriter(path, False)
			w.WriteLine("Checklist for week of " + week)
			w.WriteLine()
			w.WriteLine()
			for item in exportlist:
				w.Write("[] ")
				if publisher:
					w.Write(item["Publisher"] + " ")
				w.Write(item["Title"])
				if price:
					w.Write(" " + item["Price"])
				w.WriteLine()
			w.Close()
			w.Dispose()
