from mediawiki import MediaWiki
from bs4 import BeautifulSoup

# VARIABLE DEFINITIONS
emptyList = []

# FUNCTION DEFINITIONS

def splitIntoPoints(text):
    temp = text.split('\n');
    for i in range(len(temp)):
        temp[i] = "- " + temp[i].strip()
    temp[:] = [x for x in temp if len(x) > 2] # empty strings resolve as false -> you can easily filter them out by checking "if {string}"
    return temp

# CLASS DEFINITIONS

class clocktowerCharacter:
    def __init__(self, name: str, wikiText: BeautifulSoup):
        self.name = name            # Page title (e.g., "Imp")
        self.wikiText = wikiText    # Original wiki text
        self.cType, self.ability, self.flavour, self.artist, self.summary, self.url, self.cleanedWikiText = "", "", "", "", "", "", "" 
        self.summaryPoints, self.howToRunPoints, self.examplePoints = [], [], []
        
    def infodump(self):
        print("====================")
        print(self.name + " {" + self.cType + "} - " + self.ability)
        print("")
        print('"' + self.flavour + '"')
        print("")
        print(self.summary)
        for point in self.summaryPoints:   
            print(point)
        print("")
        print("[How to Run]")
        for point in self.howToRunPoints:   
            print(point)
        print("")
        print("[Examples]")
        for point in self.examplePoints:   
            print(point)
        print("")
        print("Designed by The Pandemonium Institute. Icon by " + self.artist + ".")
        print("====================")
        
    def parseWikiText(self):
        self.cleanedWikiText = self.wikiText.getText()
        try: self.cType = str(self.wikiText.find_all("td")[1]).split('title="Character Types">')[1].split('<')[0]
        except: self.cType = "Unknown type"
        try: self.ability = str(self.wikiText.h2.find_all_next("p")[0]).split('"')[1].split('"')[0]
        except: self.ability = "Ability not found."
        try: self.flavour = str(self.wikiText.find_all("p", class_="flavour")).split('">"')[1].split('"')[0]
        except: self.flavour = "Nobody knows which way the wind goes. Or this flavour text."
        try: self.artist = str(self.wikiText.find_all("td")[3])[4:-5]
        except: self.artist = "Unknown artist"
        try: self.summary = str(self.wikiText.h2.find_all_next("p")[1])[3:-4].strip()
        except: self.summary = "This character does something. Not sure what."
        try: self.summaryPoints = splitIntoPoints(str(self.wikiText.h2.find_all_next("ul")[0])[4:-5].replace("<li>","").replace("</li>",""))
        except: self.summaryPoints = []
        try: self.howToRunPoints = splitIntoPoints(self.cleanedWikiText.split('How to Run[edit]')[1].split('Examples[edit]')[0].strip())
        except: self.howToRunPoints = []
        try: self.examplePoints = splitIntoPoints(self.cleanedWikiText.split('Examples[edit]')[1].split('Tips & Tricks')[0].strip())
        except: self.examplePoints = []
        # analyse these versions to find the number of points and then reuse the summaryPoints method

# fetch wiki
botcWiki = MediaWiki(url='https://wiki.bloodontheclocktower.com/api.php',
                     user_agent='clocktowerAlmanacizationator/0.0 (discord @ Panfex)')
# temp list of character names
characterNames = ["Washerwoman", "Butler", "Scarlet Woman", "Imp", "Scapegoat", "Deus ex Fiasco", "Big Wig"]

# match wiki page name formatting
for name in characterNames:
    name = name.replace(" ", "_")

# step 2: for each character, pull their wiki page

characterToSearch = "Noble"
p = botcWiki.page(characterToSearch)
soup = BeautifulSoup(p.html, "html.parser")
# soupedText = soup.get_text(separator=" ", strip=True)
# print(soup)
testCharacter = clocktowerCharacter(characterToSearch, soup)
testCharacter.parseWikiText()
testCharacter.infodump()

# step 3: extract relevant info from wiki page and format into LaTeX



# step 4: assemble full LaTeX output (as .txt file?)


