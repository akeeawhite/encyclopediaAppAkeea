__author__ = 'Owner'
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import textwrap

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

            if(self.numTweets < 6):
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