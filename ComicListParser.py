"""
ComicListParser.py
Created by SharpDevelop.
User: Stonepaw
"""
import re
import clr
clr.AddReference('System.Data')
from System.Data import DataTable, DataColumn

clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Application

clr.AddReference('HtmlAgilityPack')
import HtmlAgilityPack
from HtmlAgilityPack import HtmlEntity

import System

class ComicListParser:
    def __init__(self):
        pass
    
    def Parse(self, entry):
        #print "Starting to parse entry"
        #print entry
        titlename = re.search("\d*/\d*/\d*", entry.title).group(0)
        #print "Name of entry title is: "
        #print titlename
        if not self.ComicList.Tables.Contains(titlename):
            #print "Table is not yet in dataset"
            Application.DoEvents()
            
            #print "Creating row for WeekList but do not add it yet as it still needs the publisherlist"
            row2 = self.ComicList.Tables["WeekList"].NewRow()
            #print "Created new row in weeklist"
            
            row2["Date"] = titlename
            
            
            publisherlist = []
            
            #print "Create the datatable for the list of comics"
            data = DataTable(titlename)
            id = DataColumn("ID")
            pub = DataColumn("Publisher")
            title = DataColumn("Title")
            price = DataColumn("Price")
            image = DataColumn("Image")
            image.DataType = System.Type.GetType('System.String')
            id.DataType = System.Type.GetType('System.Int32')
            pub.DataType = System.Type.GetType('System.String')
            title.DataType = System.Type.GetType('System.String')
            price.DataType = System.Type.GetType('System.String')
            data.Columns.Add(id)
            data.Columns.Add(pub)
            data.Columns.Add(title)
            data.Columns.Add(price)
            data.Columns.Add(image)
            #print "Finished Creating data columns"
            
            #print "Now finding the list of comics"
            x = HtmlAgilityPack.HtmlDocument()
            x.LoadHtml(entry.content)
            nodes = x.DocumentNode.SelectNodes("p")
            #Find the largest paragraph in the source.
            #The largest paragraph contains the comiclist
            index = {"index": 0, "length": 0}
            count = 0
            for node in nodes:
                Application.DoEvents()
                if len(node.InnerText) > index["length"]:
                    index["index"] = count
                    index["length"] = len(node.InnerText)
                count += 1

            #Now that we know which node the comiclist is, put those lines in an list
            #print "Splitting lines"
            try:
                comiclist = HtmlEntity.DeEntitize(nodes[index["index"]].InnerText).splitlines()
            except Exception, ex:
                print ex
                print "Something failed"
                return none, none
            #print len(comiclist)
            
            #Don't need these
            del(x)
            del(nodes)
            
            count = 1
            #Go through all the lines in the list execpt the first one which is the definitions.
            for line in comiclist[1:]:
                try:
                    #print count
                    print line
                    Application.DoEvents()
                    #Using python list doesn't work, so use System.Array
                    l = System.Array[str](line.strip().replace('"', '').split(','))
                    row = data.NewRow()
    
                    row["ID"] = count
                    count += 1
                    row["Publisher"] = l[1]
                    
                    if not l[1] in publisherlist and not l[1] in self.BlackList:
                        publisherlist.append(l[1])
                    row["Title"] = l[2]
                    if len(l) > 3:
                        row["Price"] = l[3]
                    else:
                        row["Price"] = ""
                    row["Image"] = ""
                    data.Rows.Add(row)
                except Exception, ex:
                    #Line was not formated in the normal pattern
                    #print ex
                    #print type(ex)
                    #print line
                    continue

            #print "Done adding items into the dataset"
            
            #Remove unwanted items. We have to seperate the items with wildcard characters from the ones that don't. This is somewhat inefficent.
            #Something to think about would be to create a seprate place to store them in the settings class.
            
            #No sense in doing anything if there is nothing in the blacklist.
            if self.BlackList:
                
                blacklistwildchar = []
                blacklistnormal = []
                
                for listitem in self.BlackList:
                    
                    if listitem.endswith("*") or listitem.startswith("*"):
                        blacklistwildchar.append(listitem)
                        
                    if listitem.endswith("*") and listitem.startswith("*"):
                        blacklistwildchar.append(listitem)
                        
                    else:
                        blacklistnormal.append(listitem)
                
                print "Publisher IN ('" + "','".join(blacklistnormal) + "')"
                
                rowstodelete = data.Select("Publisher IN ('" + "','".join(blacklistnormal) + "')")
                for rowtodelete in rowstodelete:
                    rowtodelete.Delete()
                    
                for listitem in blacklistwildchar:
                    print "Publisher LIKE '" + listitem + "'"
                    rowstodelete = data.Select("Publisher LIKE '" + listitem + "'")
                    for rowtodelete in rowstodelete:
                        rowtodelete.Delete()
                    
                    #Also remove from publisher list
                    if listitem.endswith("*"):
                        #Important to make a copy of the publisherlist to iterat through since we may be deleting things from it.
                        for pubitem in publisherlist[:]:
                            if pubitem.startswith(listitem[:-1]):
                                publisherlist.remove(pubitem)
                    elif listitem.startswith("*"):
                        #Important to make a copy of the publisherlist it iterat through since we may be deleting things from it.
                        for pubitem in publisherlist[:]:
                            if pubitem.endswith(listitem[1:]):
                                publisherlist.remove(pubitem)
                data.AcceptChanges()

            row2["Publishers"] = u",".join(publisherlist)
            return row2, data
        else:
            print "Rss already downloaded"
            return None, None
