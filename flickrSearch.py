__author__ = 'Owner'
import flickrapi
from tkinter import messagebox


############### Streaming Flickr #########################
flKey = '13c592d3851810c8f1a97ed2bd38af90'
flSecret = 'c3e96f35fe4ef875'

class flickrSearch:
    def __init__(self, userSearchFlickr):
        k = 0
        #h = 0
        i = 0
        x = 0
        j = 0
        p = 0
        flickrArray = []

        try:
            #While loop that opens the flickDB files to overwrite them so you can continuously search
            while(k < 5):
                saveFileFlickr = open('flickDB' + str(k) + '.csv', 'w')
                saveFileFlickr.close()
                k += 1

            #Sets flickr key, secret, and format and then searches using the user input and sets how many images to display
            flickr = flickrapi.FlickrAPI(flKey, flSecret, format='parsed-json')
            photos = flickr.photos.search(tags=userSearchFlickr, title=userSearchFlickr, per_page='5')

            #While loop that gets specific data of the images for building the photo URL while i < 10
            while(i < 5):
                photoFarm = str(photos['photos']['photo'][i]['farm'])
                photoServer = str(photos['photos']['photo'][i]['server'])
                photoID = str(photos['photos']['photo'][i]['id'])
                photoSecret = str(photos['photos']['photo'][i]['secret'])

                #Builds the photo URL
                buildPhotoURL = ("http://farm" + photoFarm + ".static.flickr.com/" + photoServer + "/" + photoID + "_" + photoSecret + "_m.jpg")

                #Adds the built image URLs to the flickrArray
                flickrArray.append(buildPhotoURL)

                i += 1

            #While loop that writes the photo URLS to the flickDB file
            while(j < 5):
                saveFileFlickr = open('flickDB' + str(x) + '.csv', 'a')
                saveFileFlickr.write(flickrArray[p])
                saveFileFlickr.close()
                j += 1
                x += 1
                p += 1

        except:
            messagebox.showinfo("Error", "No Results returned")