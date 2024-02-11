# Amber Altruist:
#
# Welcome to Amber Altruist, the app that makes identifying missing
# children much easier. Instead of waiting for an amber alert, writing
# down a name, looking it up for a name, and repeating, you can simply
# start the app and get informed.
import feedparser
from datetime import *
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO


stateDict = {
    "" : "",
    "Alabama" : "AL",
    "Alaska" : "AK",
    "Arizona" : "AZ",
    "Arkansas" : "AR",
    "California" : "CA",
    "Colorado" : "CO",
    "Connecticut" : "CT",
    "Delaware" : "DE",
    "Washington DC" : "DC",
    "Florida" : "FL",
    "Georgia" : "GA",
    "Hawaii" : "HI",
    "Idaho" : "ID",
    "Illinois" : "IL",
    "Indiana" : "IN",
    "Iowa" : "IA",
    "Kansas" : "KS",
    "Kentucky" : "KY",
    "Louisiana" : "LA",
    "Maine" : "ME",
    "Maryland" : "MD",
    "Massachusetts" : "MA",
    "Michigan" : "MI",
    "Minnesota" : "MN",
    "Mississippi" : "MS",
    "Missouri" : "MO",
    "Montana" : "MT",
    "Nebraska" : "NE",
    "Nevada" : "NV",
    "New Hampshire" : "NH",
    "New Jersey" : "NJ",
    "New Mexico" : "NM",
    "New York" : "NY",
    "North Carolina" : "NC",
    "North Dakota" : "ND",
    "Ohio" : "OH",
    "Oklahoma" : "OK",
    "Oregon" : "OR",
    "Pennsylvania" : "PA",
    "Rhode Island" : "RI",
    "South Carolina" : "SC",
    "South Dakota" : "SD",
    "Tennessee" : "TN",
    "Texas" : "TX",
    "Utah" : "UT",
    "Vermont" : "VT",
    "Virginia" : "VA",
    "Washington" : "WA",
    "West Virginia" : "WV",
    "Wisconsin" : "WI",
    "Wyoming" : "Wy"
}


def main():
    stateFile = open('state.txt', 'r')
    if (stateFile.read() == ''):
        newStart()
        stateFile.close()
        return
    else:
        URL = takeState(stateFile.read())
        returning(URL)
        stateFile.close()
        return
    
    
# Saves state data, unless this step is skipped.
def takeState(str):
    stateFile = open("state.txt", "r+")
    stateData = str
    if (stateData != ''):
        stateFile.truncate(0)
        stateFile.write(stateData)
    stateFile = open("state.txt", "r")    
    stateCode = stateFile.read()
    stateFile.close()
    URI = (f"https://www.missingkids.org/missingkids/servlet/XmlServlet?act=rss&LanguageCountry=en_US&orgPrefix=NCMC&state={stateCode}")
    return URI

def clearState():
    stateFile = open("state.txt", "r+")
    stateFile.truncate(0)
    stateFile.close()

# Initiates new startup sequence to initialize the user's US state.
# Choice is saved.
def newStart():

    stateList = [None] * 52
    i = 0
    for x in stateDict.keys():
        stateList[i] = x
        i += 1
    
    root = Tk()
    root.resizable(False, False)
    root.title("Amber Altruist")
    root.geometry('350x600')
    root.config(bg='orange')
    n = StringVar()
    combobox = Combobox(root, width = 25, textvariable = n, state="readonly")
    combobox['values'] = stateList
    combobox.grid(column=1, row=1)
    combobox.current()
    combobox.place(relx=0.5, rely=0.1, anchor=CENTER)
    button = Button(root, width = 15, text="Set State", command= lambda: takeState(stateDict[combobox.get()]))
    clearbutton = Button(root, width = 15, text="Clear State", command = clearState)
    button.place(relx=0.5, rely=0.15, anchor=CENTER)
    clearbutton.place(relx=0.5, rely=0.2, anchor=CENTER)


    root.mainloop()

# Initiates a return startup sequence with a known state.
# Choice can be removed for reprocessing later.
def returning(URL):
    feed = feedparser.parse(URL)

    root = Tk()
    root.resizable(False, False)
    root.title("Amber Altruist")
    root.geometry('350x600') 
    root.config(bg='orange')

    imageurl = feed.entries[0].enclosures[0]['url']
    spot = feed.entries[0]['description'].find("Missing:") + 9
    spot2 = feed.entries[0]['description'].find("ANYONE") - 1
    spot3 = feed.entries[0]['description'].find("CONTACT")
    spot4 = feed.entries[0]['title'].find(':') + 2
    spot5 = feed.entries[0]['title'].find('(') - 1
    spot6 = feed.entries[0]['description'].find("(")
    missingname = feed.entries[0]['title'][spot4: spot5:1]
    missingline = feed.entries[0]['description'][spot: spot2: 1]
    missingcall = feed.entries[0]['description'][spot3: spot6 - 1: 1]
    missingphone = feed.entries[0]['description'][spot6: : 1]

    openurl = urlopen(imageurl)
    rawData = openurl.read()
    openurl.close()

    imagefile = Image.open(BytesIO(rawData))
    imagefile = imagefile.resize((345, 500))
    missingimage = ImageTk.PhotoImage(imagefile)
    label = Label(image=missingimage)
    label.image = missingimage
    label.pack()
    
    
    labelText = Label(text=f"{missingname}\n{missingline}\n{missingcall}\n{missingphone}", justify=CENTER, background='orange')
    labelText.pack()

    clearbutton = Button(root, width = 15, text="Clear State", command = clearState)
    clearbutton.place(relx=0.5, rely=0.97, anchor=CENTER)



    root.mainloop()

# Starts the program    
main() #end of file.
