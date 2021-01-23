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
from System.Windows.Forms import Application, MessageBox

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
            nodes = x.DocumentNode.SelectNodes("pre")
            #Find the largest paragraph in the source.
            #The largest paragraph contains the comiclist
            index = {"index": 0, "length": 0}
            comiclistNode = None
            for node in nodes:
                if comiclistNode is None or len(node.InnerText) > len(comiclistNode.InnerText):
                    comiclistNode = node
                Application.DoEvents()


            if comiclistNode is None:
                print "No comic list found"
                return None, None
            #Now that we know which node the comiclist is, parse it into a csv list
            try:
                comiclist = HtmlEntity.DeEntitize(nodes[0].InnerHtml).replace('<br>', '\n').splitlines()
            except Exception, ex:
                print ex
                print "Something failed"
                return None, None
            
            #Don't need these
            del(x)
            del(nodes)

            # print comiclist
            
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

                    date, code, publisher, title, price = l
    
                    row["ID"] = count
                    count += 1
                    row["Publisher"] = publisher
                    
                    if not publisher in publisherlist and not publisher in self.BlackList:
                        publisherlist.append(publisher)
                    row["Title"] = title
                    if price:
                        row["Price"] = price
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
            print "Done parsing"
            return row2, data
        else:
            print "Rss already downloaded"
            return None, None
