'''
filelessexporter.py
Author: Stonepaw
Last modified: September 8, 2010
Description: a module that creats fileless comics  using an inputted set of datarows

Anyone is free to modify or use this code for ComicRack scripts.
'''


import clr
import System
import re
import System.Drawing
from System.Drawing import Bitmap
class filelessexporter:
    def __init__(self):
        pass
    
    def createFilelessComics(self, exportlist, tagstext):
        #Get a correctly formated string of the tags
        #print "Starting to create"
        tags = ""
        if tagstext:
            tags = self.createtaglist(tagstext)
            #print "finished getting tags"
        
        for item in exportlist:
            #The series and number and come together in the title, seperate them out.
            series, number, count = self.seperateSeriesAndNumber(item["Title"])
            
            comic = ComicRack.App.AddNewBook(False)
            comic.Series = series

            #Remember number is a string and count is an integer
            comic.Number = number
            if count:
                comic.Count = int(count)
            comic.Publisher = item["Publisher"].title()
            
            comic.Tags = tags

            #Try to add a cover by loading a bitmap from the cover's file path
            try:
                if item["Image"]:
                    b = Bitmap(item["Image"])
                    ComicRack.App.SetCustomBookThumbnail(comic, b)
                    del(b)
            except Exception, ex:
                print ex

    def createtaglist(self, tagstext):
        #create a formated comma sperated string
        tags = tagstext.split(",")
        for i in tags:
            tags[tags.index(i)] = i.strip()
        tags.sort()
        return ", ".join(tags)
        
    def seperateSeriesAndNumber(self, title):
                #seperate the series, series number and count(if available)
        if title.Contains("#"):
                series, number = title.split("#")
                #print series + " " + number
                series = series.strip()
                #using regex to find any sequences of one or more numbers
                matches = re.findall("\d+", number)
                number = matches[0]

                #Count
                if len(matches) > 1:
                    count = matches[1]
                else:
                    count = ""
                return series, number, count
        return title, "", ""
