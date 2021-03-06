import json
import Utility
import datetime
import calendar

def metadata():
    metadata = open("Data/Trump/metadata.csv","a")
    metadata.write("Date,Day of week,Number of tweets,Number of tweets in the morning(8-12),Number of tweets in the afternoon(12-18),Number of tweets in the night(18-8),Main tweeting time,Number of words,Number of urls contained,Number of tweets with ?,Number of tweets with !,Number of user mentioned,Number of reply\n")
    currentDate = Utility.dateStrToDate("Sun Oct 01 00:00:00 +0000 2017")
    lastDate = Utility.dateStrToDate("Mon Feb 26 00:00:00 +0000 2018") + datetime.timedelta(1)
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

metadata()
