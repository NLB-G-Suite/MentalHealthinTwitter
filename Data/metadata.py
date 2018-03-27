import json
import Utility
import datetime
import calendar
import pytz
import datetime
from twarc import Twarc
import config

def dataCollection():
    t = Twarc(config.consumer_key, config.consumer_secret, config.access_token, config.access_secret)
    localtz = pytz.timezone('America/New_York')
    lastDate = Utility.dateStrToDate("Tue Mar 06 00:00:00 +0000 2018") + datetime.timedelta(1)
    firstDate = Utility.dateStrToDate("Sun Oct 01 00:00:00 +0000 2017")
    firstDate = firstDate.replace(tzinfo=localtz)
    lastDate = lastDate.replace(tzinfo=localtz)
    for tweet in t.timeline(screen_name='realDonaldTrump'):
        currentDate = Utility.getNewYorkTime(tweet["created_at"])
        if (currentDate - firstDate) <= datetime.timedelta(0):
            try:
                outfile.close()
            except:
                pass
            break
        if str(lastDate)[:10] != str(currentDate)[:10]:
            try:
                outfile.close()
                outfile = open("Data/Trump/Trumpjson/"+str(currentDate)[:10]+".json","a")
            except:
                outfile = open("Data/Trump/Trumpjson/"+str(currentDate)[:10]+".json","a")
        lastDate = currentDate
        outfile.write(json.dumps(tweet) + '\n')

def txt():
    localtz = pytz.timezone('America/New_York')
    beginDate = Utility.dateStrToDate("Tue Mar 06 00:00:00 +0000 2018") + datetime.timedelta(1)
    beginDate = beginDate.replace(tzinfo=localtz)
    firstDate = Utility.dateStrToDate("Sun Oct 01 00:00:00 +0000 2017")
    firstDate = firstDate.replace(tzinfo=localtz)
    while beginDate - firstDate >= datetime.timedelta(0):
        print(beginDate)
        try:
            #print('0')
            data = Utility.readJsonFile("Data/Trump/Trumpjson/"+str(beginDate)[:10])
            #print('1')
            textfile = open("Data/Trump/Trumptxt/"+str(beginDate)[:10]+".txt","a")
            #print('2')
            for line in data:
                txt = line["text"]
                if "https:" in txt:
                    txt = txt[:txt.index("https:")]
                textfile.write(txt + "\n")
            textfile.close()
        except:
            pass
        beginDate -= datetime.timedelta(1)


def metadata():
    metadata = open("Data/Trump/metadata.csv","a")
    metadata.write("Date,Day of week,Number of tweets,Number of tweets in the morning(8-12),Number of tweets in the afternoon(12-18),Number of tweets in the night(18-8),Main tweeting time,Number of words,Number of urls contained,Number of tweets with ?,Number of tweets with !,Number of user mentioned,Number of reply\n")
    localtz = pytz.timezone('America/New_York')
    currentDate = Utility.dateStrToDate("Sun Oct 01 00:00:00 +0000 2017")
    lastDate = Utility.dateStrToDate("Mon Feb 26 00:00:00 +0000 2018") + datetime.timedelta(1)
    currentDate = currentDate.replace(tzinfo=localtz)
    lastDate = lastDate.replace(tzinfo=localtz)
    while currentDate - lastDate <= datetime.timedelta(0):
        try:
            jsondata = Utility.readJsonFile("Data/Trump/Trumpjson/" + str(currentDate)[:10])
            textfile = open("Data/Trump/Trumptxt/" + str(currentDate)[:10] + ".txt","r")
        except:
            currentDate += datetime.timedelta(1)
            continue
        textdata = textfile.read()
        textfile.close()
        date = str(currentDate)[:10]
        dayofweek = calendar.day_name[currentDate.weekday()]
        numTweets = len(textdata.split("\n"))
        if textdata.split("\n")[-1] == '':
            numTweets -= 1
        numMorning = 0
        numAfternoon = 0
        numNight = 0
        mainTweetTime = ""
        numWords = len(textdata.split(" "))
        numUrl = 0
        numQuestion = 0
        numSurprise = 0
        numUserMentioned = 0
        numReply = 0
        for tweet in jsondata:
            if int(str(Utility.dateStrToDate(tweet['created_at']))[11:13]) in range(8,12):
                numMorning += 1
            elif int(str(Utility.dateStrToDate(tweet['created_at']))[11:13]) in range(12,18):
                numAfternoon += 1
            else:
                numNight += 1
            if "https" in tweet["text"]:
                numUrl += 1
            if "?" in tweet["text"]:
                numQuestion += 1
            if "https" in tweet["text"]:
                numSurprise += 1
            if tweet["in_reply_to_status_id"] != None:
                numReply += 1
            numUserMentioned += len(tweet["entities"]["user_mentions"])
        maxTime = max(numMorning,numAfternoon,numNight)
        if maxTime == numMorning:
            mainTweetTime += 'Morning '
        if maxTime == numAfternoon:
            mainTweetTime += 'Afternoon '
        if maxTime == numNight:
            mainTweetTime += 'Night'
        metadata.write(date + "," + dayofweek + ',' + str(numTweets) + "," + str(numMorning) + "," + str(numAfternoon) + "," + str(numNight) + "," + mainTweetTime + "," + str(numWords) + "," + str(numUrl) + "," + str(numQuestion) + "," + str(numSurprise) + "," + str(numUserMentioned) + "," + str(numReply) + "\n")
        currentDate += datetime.timedelta(1)
    metadata.close()

#dataCollection()
txt()
metadata()