#Name: Bryan Huebner
#Date: 14 November 2014
#Description:
    #Script for mining Instagram API data to collect
    #the geolocation of specified 'photo hashtags' to be used
    #in further analyses (point density analysis) in ArcMap.

#Instagram account info:
    #Email: bryanhuebner@gmail.com
    #Username: bryanhuebner
    #Semperfi01$
    #ClientID: 019c0320b6444066a9ad321f40f6c09f
    #Client Secret: 81301b4e69a247c4bd6a585a6b0ba5c8
    #Website URL: http://students.washington.edu/bhuebner/
    #RedirectURL: http://students.washington.edu/bhuebner/

import unicodedata
from instagram.client import InstagramAPI
import arcpy
from arcpy import env
import time

print "All modules have been imported"  

env.workspace = "G:\GIS_501\Project\Data"
fc = "fish_pics.shp"
chart1 = arcpy.SpatialReference(4326)  # EPSG: Projection WGS84(Factory Code: 4326)
spat_ref = (chart1)  # spatial reference = WGS 84
filepath = "G:/GIS_501/Project/Data/"  # Set file path

def latlong():  # Define the search for specific "photo hashtags" (keywords to look for)
    search = ["fishing","fishon","salmonfishing","kingfishing","cohofishing",
              "steelheadfishing","steelie","salmon","riverfishing","kings","silvers"]
    api = InstagramAPI(client_id='019c0320b6444066a9ad321f40f6c09f',  # Access Instagram API
                          client_secret='81301b4e69a247c4bd6a585a6b0ba5c8')   
    date = time.strftime("%H_%M_%S")  # Timestamp each datatable created to bypass overwrite function
    for term in search:
        igram, a = api.tag_recent_media(tag_name=term)
        
        filename = date + "_" + term + ".dbf"  # Add the timestamp and search term to each datatable
        featurename = term + ".shp"  # Add search term as the name for each shapefile
        outfile = open(filepath+date + "_" + term + ".txt", "w")  # Create text file for possible future analysis
                   
        arcpy.CreateTable_management(filepath,filename)  # Create datatable for each search term
        fields = ["TAG_ID","LAT","LONG","USERNAME","TEXT","URL","DATE_TIME"]  # Fields to be created in datatable
        
        arcpy.AddField_management(filepath+filename,fields[0],"TEXT","","",50,"","NULLABLE")  # photo tag id
        arcpy.AddField_management(filepath+filename,fields[1],"FLOAT","","",25,"","NULLABLE")  # latitude
        arcpy.AddField_management(filepath+filename,fields[2],"FLOAT","","",25,"","NULLABLE")  # longitude
        arcpy.AddField_management(filepath+filename,fields[3],"TEXT","","",20,"","NULLABLE")  # username
        arcpy.AddField_management(filepath+filename,fields[4],"TEXT","","",250,"","NULLABLE")  # text
        arcpy.AddField_management(filepath+filename,fields[5],"TEXT","",250,"","NULLABLE")  # photo url
        arcpy.AddField_management(filepath+filename,fields[6],"TEXT","","",20,"","NULLABLE")  # date/time


        arcpy.CreateFeatureclass_management(filepath, featurename, "POINT", "", "", "", spat_ref)  # Create feature class for each search term
        fields2 = ["TAG_ID","LAT","LONG","USERNAME","TEXT","URL","DATE_TIME","SHAPE@XY"]  # Fielda to be created in the attribute table of each featureclass

        arcpy.AddField_management(filepath+featurename, "TAG_ID", "TEXT", "", "", 30, "", "NULLABLE")  # photo tag id
        arcpy.AddField_management(filepath+featurename, "LAT", "FLOAT", "", "", 16, "", "NULLABLE")  # latitude
        arcpy.AddField_management(filepath+featurename, "LONG", "FLOAT", "", "", 16, "", "NULLABLE")  # longitude
        arcpy.AddField_management(filepath+featurename, "USERNAME", "TEXT", "", "", 25, "", "NULLABLE")  # username
        arcpy.AddField_management(filepath+featurename, "TEXT", "TEXT", "", "", 250, "", "NULLABLE")  # text
        arcpy.AddField_management(filepath+featurename, "URL", "TEXT", "", "", 250, "", "NULLABLE")  # photo url
        arcpy.AddField_management(filepath+featurename, "DATE_TIME", "TEXT", "", "", 12, "", "NULLABLE")  # date/time


        insert = arcpy.da.InsertCursor(filepath+filename, fields) # insert cursor for datatables
        in_curs = arcpy.da.InsertCursor(filepath+featurename, fields2) # insert cursor for featureclasses

        for media in igram:  # Create loop to itereate through search terms and find coordinate points           
          try:
              tagid = unicode(media.id)
              Y = float(media.location.point.latitude)  # Swapped X and Y coordinates to locate points in correst geographic areas
              X = float(media.location.point.longitude)
              name = unicode(media.user)
              text = unicode(media.caption.text)
              url = unicode((media.images['standard_resolution'].url))
              dt = media.created_time                
              insert.insertRow([tagid,X,Y,name,text,url,dt])
              in_curs.insertRow([tagid,X,Y,name,text,url,dt, (X,Y)])  
          except AttributeError:
              tagid = unicode(media.id)
              X = 0
              Y = 0
              name = unicode(media.user)
              text = unicode("NULL")
              url = unicode((media.images['standard_resolution'].url))
              dt = media.created_time
              try:
                  tagid = unicode(media.id)
                  X = 0
                  Y = 0
                  name = unicode(media.user)
                  text = unicode(media.caption.text)
                  url = unicode((media.images['standard_resolution'].url))
                  dt = media.created_time
                  insert.insertRow([tagid,X,Y,name,text,url,dt])
                  in_curs.insertRow([tagid,X,Y,name,text,url,dt, (X,Y)])
              except AttributeError:
                  insert.insertRow([tagid,X,Y,name,text,url,dt])
                  in_curs.insertRow([tagid,X,Y,name,text,url,dt, (X,Y)])

latlong()  # Call latlong       

print "Successful operation"
                


