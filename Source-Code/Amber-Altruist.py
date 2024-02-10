# Amber Altruist:
#
# Welcome to Amber Altruist, the app that makes identifying missing
# children much easier. Instead of waiting for an amber alert, writing
# down a name, looking it up for a name, and repeating, you can simply
# start the app and get informed.
import feedparser
from datetime import *


def main():

    # Gathers the state appropriate URI and parses it.
    stateCode = takeState()
    URI = (f"https://www.missingkids.org/missingkids/servlet/XmlServlet?act=rss&LanguageCountry=en_US&orgPrefix=NCMC&state={stateCode}")
    feed = feedparser.parse(URI)
    print()

    # Prints names, dates/locations of disappearance, and image url of every
    # queried missing child in the state who went missing in the last 30 days.
    iterator = 0
    while iterator < len(feed.entries):
        spot = feed.entries[iterator]['description'].find("Missing:") + 9
        spot2 = feed.entries[iterator]['description'].find("ANYONE")
        spot3 = feed.entries[iterator]['description'].find("CONTACT")
        date = datetime.strptime(feed.entries[iterator]['description'][spot :spot + 10:1],
                                 '%m/%d/%Y')
        if (spot != -1) and (date > datetime.now() - timedelta(days=30)):
            
            print(feed.entries[iterator]['title'])
            print(feed.entries[iterator]['description'][spot :spot2 - 1:1])
            print(feed.entries[iterator].enclosures[0]['url'])
            print(feed.entries[iterator]['description'][spot3: : 1])
            
            print()
        iterator += 1


# Saves state data, unless this step is skipped.
def takeState():
    stateFile = open("state.txt", "r+")
    stateData = input("Insert 2-letter State Code: ")
    if (stateData != ''):
        stateFile.truncate(0)
        stateFile.write(stateData)
    stateFile = open("state.txt", "r")    
    stateCode = stateFile.read()
    stateFile.close()
    return stateCode


main()
