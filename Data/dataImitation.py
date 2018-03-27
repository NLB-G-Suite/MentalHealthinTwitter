import Utility
import config
from twarc import Twarc
import json
def dataImitation():
    depressed = open("Data/Depressed.txt","r")
    undepressed = open("Data/UnDepressed.txt","r")
    depressedList = depressed.read().split('\n')
    undepressedList = undepressed.read().split('\n')
    if undepressedList[-1] == '':
        undepressedList = undepressedList[:-1]
    if depressedList[-1] == '':
        depressedList = depressedList[:-1]
    t = Twarc(config.consumer_key, config.consumer_secret, config.access_token, config.access_secret)
    for user in depressedList:
        tweetFile = open("Data/Imitation/Depressed/Tweets/" + user[1:] + ".txt", "a")
        dataFile = open("Data/Imitation/Depressed/Data/" + user[1:] + ".json", "a")
        try:
            for tweet in t.timeline(screen_name=user):
                txt = tweet["text"]
                dataFile.write(json.dumps(tweet) + '\n')
                tweetFile.write(txt + '\n')
        except:
            print(user[1:] + "error\n")
        tweetFile.close()
        dataFile.close()

    for user in undepressedList:
        tweetFile = open("Data/Imitation/Undepressed/Tweets/" + user[1:] + ".txt", "a")
        dataFile = open("Data/Imitation/Undepressed/Data/" + user[1:] + ".json", "a")
        try:
            for tweet in t.timeline(screen_name=user):
                txt = tweet["text"]
                dataFile.write(json.dumps(tweet) + '\n')
                tweetFile.write(txt + '\n')
        except:
            print(user[1:] + "error\n")
        tweetFile.close()
        dataFile.close()

dataImitation()