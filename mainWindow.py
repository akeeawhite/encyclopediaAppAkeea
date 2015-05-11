__author__ = 'Jesse'
from tkinter import *
import webbrowser
import textwrap
import flickrapi
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tkinter import messagebox
import threading
import sqlite3

# create a new database and connect to it
cxn = sqlite3.connect('EncyclopediaDB')
# initialize a cursor object to run execute commands on the connected database.
cur = cxn.cursor()
try:
    # create the table and fill it with data
    cur.execute('CREATE TABLE flickr(search VARCHAR(50), result VARCHAR(200))')
    print("Successfully created the flickr table.")
    cur.execute('CREATE TABLE wiki(search VARCHAR(50), result VARCHAR(200))')
    print("Successfully created the wiki table.")
    cur.execute('CREATE TABLE twitter(search VARCHAR(50), result VARCHAR(200))')
    print("Successfully created the twitter table.")
except sqlite3.OperationalError:
    print("The table could not be created")
#
# class ThreadedClient(threading.Thread):
#     def __init__(self, queue1, fcn):
#         self.queue1 = queue1
#         self.fcn = fcn
#         threading.Thread.__init__(self)
#     def run(self):
#         Main.create(self.queue1, self.fcn)
        # time.sleep(1)
        # self.queue1.put(self.fcn())

# def spawnthread(fcn):
#     thread = ThreadedClient(queue, fcn)
#     thread.start()


############### Streaming Flickr #########################
flKey = '13c592d3851810c8f1a97ed2bd38af90'
flSecret = 'c3e96f35fe4ef875'

class flickrSearch:
    def __init__(self, userSearchFlickr):
        k = 0
        h = 0
        i = 0
        x = 0
        j = 0
        p = 0
        flickrArray = []

        try:
            #While loop that opens the flickDB files to overwrite them so you can continuously search
            while(k < 10):
                saveFileFlickr = open('flickDB' + str(h) + '.csv', 'w')
                saveFileFlickr.close()
                k += 1
                h += 1

            #Sets flickr key, secret, and format and then searches using the user input and sets how many images to display
            flickr = flickrapi.FlickrAPI(flKey, flSecret, format='parsed-json')
            photos = flickr.photos.search(tags=userSearchFlickr, title=userSearchFlickr, per_page='10')

            #While loop that gets specific data of the images for building the photo URL while i < 10
            while(i < 10):
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
            while(j < 10):
                saveFileFlickr = open('flickDB' + str(x) + '.csv', 'a')
                saveFileFlickr.write(flickrArray[p])
                saveFileFlickr.close()
                j += 1
                x += 1
                p += 1

        except:
            messagebox.showinfo("Error", "No Results returned")


############### Streaming Tweets ######################
cKey = 'xLwpqmwpQLNfkKI5Ux5eHSRAP'
cSecret = '56HR60btiSEjc03GO3Xm0i5VQSVOb9Xs5XQQZi2COQoxhjkqJE'
aToken = '1187764111-LK8d4jwuumvY5XVFx5GKeHSQVcUxJsiEJoE1pMS'
aSecret = 'o30rmM7frd8OONtU2QPZGTsw7s8KmGHEpdFYtEKsfJWjw'

class Listener(StreamListener):

    def __init__(self, api=None):
        super(Listener, self).__init__()

        self.numTweets = 0
        self.i = 1

        #Opens the tDB3 file and overwrites it so you can append it repeatedly
        saveFile2 = open('tDB3.csv', 'w')
        saveFile2.close()

    def on_data(self, raw_data):

        try:

            #Sets tweet array and splits the data at text to the source, and then while numTweets is less than 10 it adds tweets to array
            self.tweetArray = []
            tweet = raw_data.split(',"text":"')[1].split('","source')[0]

            self.numTweets += 1

            if(self.numTweets < 11):
                textwrapTweet = ('\n' .join(textwrap.wrap(tweet, 85)))
                self.tweetArray.append(textwrapTweet)
                #print(self.tweetArray)
                saveFile2 = open('tDB3.csv', 'a')
                saveFile2.write(str(self.i) + "." + ")" + " ")
                saveFile2.write(textwrapTweet + "\n")
                saveFile2.close()
                self.i += 1
                return True
            else:
                return False
        except:
            print("Failed")

    #Prints status of error if error occurs
    def on_error(self, status_code):
        print(status_code)

#Sets consumer keys and access tokens
authorize = OAuthHandler(cKey, cSecret)
authorize.set_access_token(aToken, aSecret)

#Streams the tweets using the Listener class and depending on the criteria of the userSearch
#twitterStream = Stream(authorize, Listener())
#twitterStream.filter(track=[userSearch])

#Boolean variable for the search thread that sets the variable to true while running and false when you quit the program
alive = True

class Main(Frame):

    def __init__(self, master):

        Frame.__init__(self, master)

        #Creates userSearch Variable for storing user input and creates int vars for checkboxes
        self.userSearch = StringVar()
        self.chkVar1 = IntVar()
        self.chkVar2 = IntVar()
        self.chkVar3 = IntVar()

        #sets window to master, sets title, and window size
        self.master = master
        self.master.title("Encyclopedia App")
        self.master.resizable(width=FALSE, height=FALSE)
        self.canvas = Canvas(self.master, borderwidth=0, highlightthickness=0)
        self.frame = Frame(self.canvas)
        self.vertScrollBar = Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vertScrollBar.set)

        #Puts scrollbar and canvas in grid and creates window
        self.vertScrollBar.grid(row=0, column=10, sticky="NS")
        self.canvas.grid(row=0, column=0)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", tags="self.frame")

        # #Scrollbar
        # scrlBar = Scrollbar(self.master, orient=VERTICAL)
        # scrlBar.grid(row=1, column=10)
        # self.canvas.config(width=1800, height=580)
        # self.canvas.config(yscrollcommand=scrlBar.set)
        # self.canvas.grid(column=0, row=0, sticky=N+S+E+W)

        #Creates Widgets
        lblTitle = Label(self.frame, text="Searchster", font=("Times 18 bold"), fg="green")
        lblSearch = Label(self.frame, text="Search: ", font=("Times 10"))
        txtBoxSearch = Entry(self.frame, width=17, textvariable=self.userSearch)
        btnSearch = Button(self.frame, text="Search", width=14, command=self.threadedSearch)
        btnClear = Button(self.frame, text="Clear", width=14, command=self.clear)
        btnQuit = Button(self.frame, text="Close", width=14, command=self.close)
        chkBtnWikipedia = Checkbutton(self.frame, text="Wikipedia", variable=self.chkVar1, justify=LEFT)
        chkBtnFlickr = Checkbutton(self.frame, text="Flickr", variable=self.chkVar2, justify=LEFT)
        chkBtnTwitter = Checkbutton(self.frame, text="Twitter", variable=self.chkVar3, justify=LEFT)
        lblBlankLabel = Label(self.frame, text="                  ")
        lblWikiLabel = Label(self.frame, text="Wikipedia:", font=("Times 10 bold"))
        lblFlickrLabel = Label(self.frame, text="Flickr:", font=("Times 10 bold"))
        lblTwitterLabel = Label(self.frame, text="Twitter:", font=("Times 10 bold"))


        #Places Widgets in grid format
        lblTitle.grid(row=1, column=2, sticky=W)
        lblSearch.grid(row=2, column=1, sticky=E)
        txtBoxSearch.grid(row=2, column=2, sticky=W)
        chkBtnWikipedia.grid(row=3, column=2, sticky=W)
        chkBtnFlickr.grid(row=4, column=2, sticky=W)
        chkBtnTwitter.grid(row=5, column=2, sticky=W)
        btnSearch.grid(row=7, column=2, sticky=W)
        btnClear.grid(row=8, column=2, sticky=W)
        btnQuit.grid(row=9, column=2, sticky=W)
        lblBlankLabel.grid(row=10, column=2)
        lblWikiLabel.grid(row=11, column=2, sticky=W)
        lblFlickrLabel.grid(row=13, column=2, sticky=W)
        lblTwitterLabel.grid(row=25, column=2, sticky=W)

        #Initialize the Labels and set there position in the grid so they can be reset repeatedly
        self.lblDisplayWikiURL = Label(self.frame, text="")
        self.lblDisplayFlickrURL = Label(self.frame, text="")
        self.lblDisplayTwitterURL = Label(self.frame, text="")
        self.lblDisplayFlickrData = Label(self.frame, text="")
        self.lblDisplayFlickrData2 = Label(self.frame, text="")
        self.lblDisplayFlickrData3 = Label(self.frame, text="")
        self.lblDisplayFlickrData4 = Label(self.frame, text="")
        self.lblDisplayFlickrData5 = Label(self.frame, text="")
        self.lblDisplayFlickrData6 = Label(self.frame, text="")
        self.lblDisplayFlickrData7 = Label(self.frame, text="")
        self.lblDisplayFlickrData8 = Label(self.frame, text="")
        self.lblDisplayFlickrData9 = Label(self.frame, text="")
        self.lblDisplayFlickrData10 = Label(self.frame, text="")
        self.lblDisplayTwitterData = Label(self.frame, text="")
        self.lblDisplayWikiURL.grid(row=12, column=2, sticky=W)
        self.lblDisplayFlickrURL.grid(row=14, column=2, sticky=W)
        self.lblDisplayTwitterURL.grid(row=26, column=2, sticky=W)

        self.frame.bind("<Configure>", self.OnFrameConfigure)

    def OnFrameConfigure(self, event):
        #Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), height=400, width=600)

    #Wikipedia Callback Event
    def wikicallback(self, event):
        userSearch = self.userSearch.get()
        #Opens the hyperlink when left-clicked on
        webbrowser.open("http://en.wikipedia.org/w/index.php?title=" + str(userSearch))

    #Flickr Callback Event
    def flickrcallback(self, event):
        userSearch = self.userSearch.get()
        #Opens the hyperlink when left-clicked on
        webbrowser.open("http://www.flickr.com/search/?q=" + str(userSearch))

    #Opens the flickr image
    def flickrDisplayPhotocallback(self, event):
        saveFileFlickr = open('flickDB0.csv')
        readFileFlickr = saveFileFlickr.read()
        saveFileFlickr.close()
        webbrowser.open(readFileFlickr)

    #Opens the flickr image
    def flickrDisplayPhotocallback2(self, event):
        saveFileFlickr = open('flickDB1.csv')
        readFileFlickr = saveFileFlickr.read()
        saveFileFlickr.close()
        webbrowser.open(readFileFlickr)

    #Opens the flickr image
    def flickrDisplayPhotocallback3(self, event):
        saveFileFlickr = open('flickDB2.csv')
        readFileFlickr = saveFileFlickr.read()
        saveFileFlickr.close()
        webbrowser.open(readFileFlickr)

    #Opens the flickr image
    def flickrDisplayPhotocallback4(self, event):
        saveFileFlickr = open('flickDB3.csv')
        readFileFlickr = saveFileFlickr.read()
        saveFileFlickr.close()
        webbrowser.open(readFileFlickr)

    #Opens the flickr image
    def flickrDisplayPhotocallback5(self, event):
        saveFileFlickr = open('flickDB4.csv')
        readFileFlickr = saveFileFlickr.read()
        saveFileFlickr.close()
        webbrowser.open(readFileFlickr)

    #Opens the flickr image
    def flickrDisplayPhotocallback6(self, event):
        saveFileFlickr = open('flickDB5.csv')
        readFileFlickr = saveFileFlickr.read()
        saveFileFlickr.close()
        webbrowser.open(readFileFlickr)

    #Opens the flickr image
    def flickrDisplayPhotocallback7(self, event):
        saveFileFlickr = open('flickDB6.csv')
        readFileFlickr = saveFileFlickr.read()
        saveFileFlickr.close()
        webbrowser.open(readFileFlickr)

    #Opens the flickr image
    def flickrDisplayPhotocallback8(self, event):
        saveFileFlickr = open('flickDB7.csv')
        readFileFlickr = saveFileFlickr.read()
        saveFileFlickr.close()
        webbrowser.open(readFileFlickr)

    #Opens the flickr image
    def flickrDisplayPhotocallback9(self, event):
        saveFileFlickr = open('flickDB8.csv')
        readFileFlickr = saveFileFlickr.read()
        saveFileFlickr.close()
        webbrowser.open(readFileFlickr)

    #Opens the flickr image
    def flickrDisplayPhotocallback10(self, event):
        saveFileFlickr = open('flickDB9.csv')
        readFileFlickr = saveFileFlickr.read()
        saveFileFlickr.close()
        webbrowser.open(readFileFlickr)

    #Twitter Callback Event
    def twittercallback(self, event):
        userSearch = self.userSearch.get()
        #Opens the hyperlink when left-clicked on
        webbrowser.open("http://twitter.com/search?q=" + str(userSearch) + "&src=typd")

    #Threading for search function
    def threadedSearch(self):

        #Search Function
        def search():

            #Gets text from search textbox
            userSearch = self.userSearch.get()

            #Wikipedia Checkbox
            if(self.chkVar1.get()):
                #webbrowser.open("http://en.wikipedia.org/w/index.php?title=" + str(userSearch))

                #Displays Wikipedia hyperlink in label and binds it to left-click event and places in grid
                self.lblDisplayWikiURL.config(text="http://en.wikipedia.org/w/index.php?title=" + str(userSearch), font=("Times 10"), fg="Blue", cursor="hand2")
                self.lblDisplayWikiURL.bind('<Button-1>', self.wikicallback)

            #Flickr Checkbox
            if(self.chkVar2.get()):
                #sets the userSearchFlickr to the userSearch get method
                flickrPull = flickrSearch(userSearchFlickr=str(userSearch))
                flickrPull.userSearch = userSearch
                #webbrowser.open("http://www.flickr.com/search/?q=" + str(userSearch))

                #Opens the flickDB files and reads them for displaying in the lblDisplayFlickrData labels below, and then closes it
                saveFileFlickr = open('flickDB0.csv')
                readFileFlickr = saveFileFlickr.read()
                saveFileFlickr.close()

                saveFileFlickr = open('flickDB1.csv')
                readFileFlickr2 = saveFileFlickr.read()
                saveFileFlickr.close()

                saveFileFlickr = open('flickDB2.csv')
                readFileFlickr3 = saveFileFlickr.read()
                saveFileFlickr.close()

                saveFileFlickr = open('flickDB3.csv')
                readFileFlickr4 = saveFileFlickr.read()
                saveFileFlickr.close()

                saveFileFlickr = open('flickDB4.csv')
                readFileFlickr5 = saveFileFlickr.read()
                saveFileFlickr.close()

                saveFileFlickr = open('flickDB5.csv')
                readFileFlickr6 = saveFileFlickr.read()
                saveFileFlickr.close()

                saveFileFlickr = open('flickDB6.csv')
                readFileFlickr7 = saveFileFlickr.read()
                saveFileFlickr.close()

                saveFileFlickr = open('flickDB7.csv')
                readFileFlickr8 = saveFileFlickr.read()
                saveFileFlickr.close()

                saveFileFlickr = open('flickDB8.csv')
                readFileFlickr9 = saveFileFlickr.read()
                saveFileFlickr.close()

                saveFileFlickr = open('flickDB9.csv')
                readFileFlickr10 = saveFileFlickr.read()
                saveFileFlickr.close()

                #Displays Flickr hyperlink in label and binds it to left-click event and places in grid
                self.lblDisplayFlickrURL.config(text="http://www.flickr.com/search/?q=" + str(userSearch), fg="Blue", cursor="hand2")
                self.lblDisplayFlickrURL.bind('<Button-1>', self.flickrcallback)

                self.lblDisplayFlickrData.config(text=readFileFlickr, font=("Times 10"), fg="Blue", cursor="hand2", justify=LEFT)
                self.lblDisplayFlickrData.bind('<Button-1>', self.flickrDisplayPhotocallback)
                self.lblDisplayFlickrData.grid(row=15, column=2, sticky=W)

                self.lblDisplayFlickrData2.config(text=readFileFlickr2, font=("Times 10"), fg="Blue", cursor="hand2", justify=LEFT)
                self.lblDisplayFlickrData2.bind('<Button-1>', self.flickrDisplayPhotocallback2)
                self.lblDisplayFlickrData2.grid(row=16, column=2, sticky=W)

                self.lblDisplayFlickrData3.config(text=readFileFlickr3, font=("Times 10"), fg="Blue", cursor="hand2", justify=LEFT)
                self.lblDisplayFlickrData3.bind('<Button-1>', self.flickrDisplayPhotocallback3)
                self.lblDisplayFlickrData3.grid(row=17, column=2, sticky=W)

                self.lblDisplayFlickrData4.config(text=readFileFlickr4, font=("Times 10"), fg="Blue", cursor="hand2", justify=LEFT)
                self.lblDisplayFlickrData4.bind('<Button-1>', self.flickrDisplayPhotocallback4)
                self.lblDisplayFlickrData4.grid(row=18, column=2, sticky=W)

                self.lblDisplayFlickrData5.config(text=readFileFlickr5, font=("Times 10"), fg="Blue", cursor="hand2", justify=LEFT)
                self.lblDisplayFlickrData5.bind('<Button-1>', self.flickrDisplayPhotocallback5)
                self.lblDisplayFlickrData5.grid(row=19, column=2, sticky=W)

                self.lblDisplayFlickrData6.config(text=readFileFlickr6, font=("Times 10"), fg="Blue", cursor="hand2", justify=LEFT)
                self.lblDisplayFlickrData6.bind('<Button-1>', self.flickrDisplayPhotocallback6)
                self.lblDisplayFlickrData6.grid(row=20, column=2, sticky=W)

                self.lblDisplayFlickrData7.config(text=readFileFlickr7, font=("Times 10"), fg="Blue", cursor="hand2", justify=LEFT)
                self.lblDisplayFlickrData7.bind('<Button-1>', self.flickrDisplayPhotocallback7)
                self.lblDisplayFlickrData7.grid(row=21, column=2, sticky=W)

                self.lblDisplayFlickrData8.config(text=readFileFlickr8, font=("Times 10"), fg="Blue", cursor="hand2", justify=LEFT)
                self.lblDisplayFlickrData8.bind('<Button-1>', self.flickrDisplayPhotocallback8)
                self.lblDisplayFlickrData8.grid(row=22, column=2, sticky=W)

                self.lblDisplayFlickrData9.config(text=readFileFlickr9, font=("Times 10"), fg="Blue", cursor="hand2", justify=LEFT)
                self.lblDisplayFlickrData9.bind('<Button-1>', self.flickrDisplayPhotocallback9)
                self.lblDisplayFlickrData9.grid(row=23, column=2, sticky=W)

                self.lblDisplayFlickrData10.config(text=readFileFlickr10, font=("Times 10"), fg="Blue", cursor="hand2", justify=LEFT)
                self.lblDisplayFlickrData10.bind('<Button-1>', self.flickrDisplayPhotocallback10)
                self.lblDisplayFlickrData10.grid(row=24, column=2, sticky=W)

            #Twitter Checkbox
            if(self.chkVar3.get()):
                #webbrowser.open("http://twitter.com/search?q=" + str(userSearch) + "&src=typd")1q

                #Streams the tweets using the Listener class and searches with the criteria of the userSearch
                twitterStream = Stream(authorize, Listener())

                #Filters the twitter results with the user search input
                twitterStream.filter(track=[userSearch])

                #Opens the tDB3 file and reads for displaying in the lblDisplayTwitterData below, and then closes it
                saveFile2 = open('tDB3.csv')
                readFile = saveFile2.read()
                saveFile2.close()

                #Displays Twitter hyperlink in label and binds it to left-click event and places in grid
                self.lblDisplayTwitterURL.config(text="http://twitter.com/search?q=" + str(userSearch) + "&src=typd", fg="Blue", cursor="hand2")
                self.lblDisplayTwitterURL.bind('<Button-1>', self.twittercallback)
                self.lblDisplayTwitterData.config(text=readFile, font=("Times 10"), justify=LEFT)
                self.lblDisplayTwitterData.grid(row=27, column=2, sticky=W)

            #Function that starts the thread
            def run():
                while alive:
                    multi = threading.Thread(target=search)
                    multi.start()

        multi = threading.Thread(target=search)
        multi.start()
        # fill and show the database has to be outside of the thread otherwise it is not working
        self.fillDB()
        self.showDB()

    def fillDB(self):
        userSearch = self.userSearch.get()
        flickrAddress = "http://www.flickr.com/search/?q=" + str(userSearch)
        wikiAddress = "http://en.wikipedia.org/w/index.php?title=" + str(userSearch)
        twitterAddress = "http://twitter.com/search?q=" + str(userSearch) + "&src=typd"
        cur.execute('INSERT INTO flickr VALUES(?, ?);', (userSearch, flickrAddress))
        cur.execute('INSERT INTO wiki VALUES(?, ?);', (userSearch, wikiAddress))
        cur.execute('INSERT INTO twitter VALUES(?, ?);', (userSearch, twitterAddress))
        cxn.commit()
        print('Successfully committed')

    def showDB(self):

        cur.execute('SELECT * FROM flickr')
        for eachUser in cur.fetchall():
            print("Flickr table.")
            print(eachUser)

        cur.execute('SELECT * FROM wiki')
        for eachUser in cur.fetchall():
            print("Wiki table.")
            print(eachUser)

        cur.execute('SELECT * FROM twitter')
        print("Twitter table.")
        for eachUser in cur.fetchall():

            print(eachUser)



    #Function for clearing the labels
    def clear(self):
        self.lblDisplayWikiURL.config(text="")
        self.lblDisplayFlickrURL.config(text="")
        self.lblDisplayTwitterURL.config(text="")
        self.lblDisplayFlickrData.grid_forget()
        self.lblDisplayFlickrData2.grid_forget()
        self.lblDisplayFlickrData3.grid_forget()
        self.lblDisplayFlickrData4.grid_forget()
        self.lblDisplayFlickrData5.grid_forget()
        self.lblDisplayFlickrData6.grid_forget()
        self.lblDisplayFlickrData7.grid_forget()
        self.lblDisplayFlickrData8.grid_forget()
        self.lblDisplayFlickrData9.grid_forget()
        self.lblDisplayFlickrData10.grid_forget()
        self.lblDisplayTwitterData.grid_forget()

    #Function for closing the window
    def close(self):
        alive = False
        cur.execute('DROP TABLE flickr')
        cur.execute('DROP TABLE wiki')
        cur.execute('DROP TABLE twitter')
        cur.close()
        cxn.close()
        self.master.destroy()



# class MyMainApp(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     #Function for clearing the labels
#
#     def run(self):
#         self.root = Tk()
#         Main(self.root)

def main():
    root = Tk()
    Main(root)
    root.mainloop()


#Loops the code so the windows stay open
if __name__ == "__main__":
    main()

#         self.root.mainloop()
# app = MyMainApp()
# app.start()

#Creates the root window and loops it
